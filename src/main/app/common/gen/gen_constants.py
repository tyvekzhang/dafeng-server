class GenConstants:
    """Constants for code generation."""

    # Template types
    TPL_CRUD = "crud"
    TPL_TREE = "tree"
    TPL_SUB = "sub"

    # Tree-related fields
    TREE_CODE = "treeCode"
    TREE_PARENT_CODE = "treeParentCode"
    TREE_NAME = "treeName"

    # Menu-related fields
    PARENT_MENU_ID = "parentMenuId"
    PARENT_MENU_NAME = "parentMenuName"

    # Database column types
    COLUMNTYPE_STR = ["char", "varchar", "nvarchar", "varchar2"]
    COLUMNTYPE_TEXT = ["tinytext", "text", "mediumtext", "longtext"]
    COLUMNTYPE_TIME = ["datetime", "time", "date", "timestamp"]
    COLUMNTYPE_NUMBER = ["tinyint", "smallint", "mediumint", "int", "number", "integer",
                         "bit", "bigint", "float", "double", "decimal"]

    # Page settings for fields
    COLUMNNAME_NOT_EDIT = ["id", "create_by", "create_time", "del_flag"]
    COLUMNNAME_NOT_LIST = ["id", "create_by", "create_time", "del_flag", "update_by", "update_time"]
    COLUMNNAME_NOT_QUERY = ["id", "create_by", "create_time", "del_flag", "update_by", "update_time", "remark"]

    # Base entity fields
    BASE_ENTITY = ["createBy", "createTime", "updateBy", "updateTime", "remark"]
    TREE_ENTITY = ["parentName", "parentId", "orderNum", "ancestors"]

    # HTML input types
    HTML_INPUT = "input"
    HTML_TEXTAREA = "textarea"
    HTML_SELECT = "select"
    HTML_RADIO = "radio"
    HTML_CHECKBOX = "checkbox"
    HTML_DATETIME = "datetime"
    HTML_IMAGE_UPLOAD = "imageUpload"
    HTML_FILE_UPLOAD = "fileUpload"
    HTML_EDITOR = "editor"

    # Data types
    TYPE_STRING = "String"
    TYPE_INTEGER = "Integer"
    TYPE_LONG = "Long"
    TYPE_DOUBLE = "Double"
    TYPE_BIGDECIMAL = "BigDecimal"
    TYPE_DATE = "Date"

    # Query types
    QUERY_LIKE = "LIKE"
    QUERY_EQ = "EQ"

    # Requirement flag
    REQUIRE = "1"