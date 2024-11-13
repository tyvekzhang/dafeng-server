from pydantic import BaseModel, constr

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
    connection_id: int = None
    database_name: constr(min_length=1, max_length=63)
    character_set: str = "utf8mb4"
    collation: str = "utf8mb4_unicode_ci"


class DatabaseQuery(BaseModel):
    pass


class DatabaseExport(BaseModel):
    pass


class DatabaseQueryForm(BaseModel):
    pass


class DatabaseModify(BaseModel):
    pass
