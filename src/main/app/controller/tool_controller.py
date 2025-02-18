import os
import uuid
from pdf2image import convert_from_path
from fastapi import File, UploadFile, Form, HTTPException, APIRouter
from fastapi.responses import StreamingResponse
import zipfile
from io import BytesIO

tool_router = APIRouter()

# 临时文件存储路径
TEMP_DIR = "../../temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# 尝试从环境变量获取 poppler 路径
POPPLER_PATH = r"D:\Container\ProgramFiles\Release-24.08.0-0\poppler-24.08.0\Library\bin"

@tool_router.post("/crop-pdf")
async def crop_pdf_to_image(
        file: UploadFile = File(...),  # 上传的 PDF 文件
        page_range: str = Form(...)    # 页码范围，例如 "1-3"
):
    # 验证文件类型
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # 解析页码范围
    try:
        start_page, end_page = map(int, page_range.split("-"))
        if start_page < 1 or end_page < start_page:
            raise ValueError("Invalid page range.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid page range format. Use 'start-end' (e.g., '1-3').")

    # 保存上传的文件到临时目录
    temp_input_path = os.path.join(TEMP_DIR, f"input_{uuid.uuid4().hex}.pdf")
    try:
        with open(temp_input_path, "wb") as buffer:
            buffer.write(await file.read())

        # 使用 pdf2image 将 PDF 转换为图片
        try:
            images = convert_from_path(temp_input_path, first_page=start_page, last_page=end_page, poppler_path=POPPLER_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error converting PDF to images: {str(e)}")

        # 将图片打包为 zip 文件
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for i, image in enumerate(images, start=start_page):
                img_filename = f"page_{i}.png"
                img_buffer = BytesIO()
                image.save(img_buffer, 'PNG')
                img_buffer.seek(0)
                zip_file.writestr(img_filename, img_buffer.getvalue())

        zip_buffer.seek(0)

        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=cropped_images.zip"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        # 确保临时 PDF 文件被删除
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)