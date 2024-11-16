from typing import Optional

from pydantic import BaseModel, constr

from src.main.app.schema.common_schema import PageBase

# SQL templates for different databases
DB_CREATE_TEMPLATES = {
    "mysql": """
        CREATE DATABASE IF NOT EXISTS {database_name}
        CHARACTER SET {character_set}
        COLLATE {collation};
    """,
    "postgresql": """
        CREATE DATABASE {database_name}
        WITH ENCODING '{character_set}'
        LC_COLLATE 'en_US.UTF-8'
        LC_CTYPE 'en_US.UTF-8';
    """,
    "sqlite": "-- SQLite does not need CREATE DATABASE",
}


# Database creation request model
class DatabaseAdd(BaseModel):
    connection_id: int
    database_name: constr(min_length=1, max_length=63)
    character_set: Optional[str] = None
    collation: Optional[str] = None


class DatabaseQuery(PageBase):
    connection_id: int


class DatabaseExport(BaseModel):
    pass


class DatabaseQueryForm(BaseModel):
    pass


class DatabaseModify(BaseModel):
    pass


class MySQLSchema(BaseModel):
    schema_name: str
    default_character_set_name: str
    default_collation_name: str
