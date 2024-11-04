import io
from datetime import datetime
from typing import List, Type

import pandas as pd
from loguru import logger
from pydantic import BaseModel
from starlette.responses import StreamingResponse


async def export_excel(
    schema: Type[BaseModel], file_name: str, records: List[BaseModel] = []
) -> StreamingResponse:
    """
    Export a template or data as an Excel file.
    """
    field_names = list(schema.model_fields.keys())
    user_export_df = pd.DataFrame(columns=field_names)
    if records:
        data_dicts = [item.model_dump() for item in records]
        user_export_df = pd.concat(
            [user_export_df, pd.DataFrame(data_dicts)], ignore_index=True
        )

    filename = f"{file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    stream = io.BytesIO()

    try:
        with pd.ExcelWriter(stream, engine="openpyxl") as writer:
            user_export_df.to_excel(writer, index=False, sheet_name=filename)
        stream.seek(0)
        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error(f"Failed to export Excel: {e}")
        raise
