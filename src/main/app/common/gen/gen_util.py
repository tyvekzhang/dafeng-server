import re
from typing import List

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.gen.gen_constants import GenConstants
from src.main.app.common.util.string_util import StringUtils
from src.main.app.model.gen_table_model import GenTableDO

config = load_config()
gen_config = config.gen

class GenUtils:
    @staticmethod
    def init_table(gen_table: GenTableDO):
        gen_table.class_name = GenUtils.convert_class_name(gen_table.name)
        gen_table.package_name = gen_config.package_name
        gen_table.module_name = GenUtils.get_module_name(gen_config.package_name)
        gen_table.business_name = GenUtils.get_business_name(gen_table.name)
        gen_table.function_name = GenUtils.replace_text(gen_table.comment)
        gen_table.function_author = gen_config.author

    @staticmethod
    def init_column_field(column, table):
        """
        Initialize column attribute fields
        """
        data_type = GenUtils.get_db_type(column.column_type)
        column_name = column.column_name
        column.table_id = table.table_id
        column.create_by = table.create_by

        # Set Java field name
        column.java_field = StringUtils.to_camel_case(column_name)
        # Set default type
        column.java_type = GenConstants.TYPE_STRING
        column.query_type = GenConstants.QUERY_EQ

        if GenUtils.arrays_contains(GenConstants.COLUMNTYPE_STR, data_type) or GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TEXT, data_type):
            # Set text area for string length over 500
            column_length = GenUtils.get_column_length(column.column_type)
            html_type = GenConstants.HTML_TEXTAREA if column_length >= 500 or GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TEXT, data_type) else GenConstants.HTML_INPUT
            column.html_type = html_type
        elif GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TIME, data_type):
            column.java_type = GenConstants.TYPE_DATE
            column.html_type = GenConstants.HTML_DATETIME
        elif GenUtils.arrays_contains(GenConstants.COLUMNTYPE_NUMBER, data_type):
            column.html_type = GenConstants.HTML_INPUT

            # Use BigDecimal for floating point types
            str_values = StringUtils.split(StringUtils.substring_between(column.column_type, "(", ")"), ",")
            if str_values and len(str_values) == 2 and int(str_values[1]) > 0:
                column.java_type = GenConstants.TYPE_BIGDECIMAL
            # Use Integer for small integer types
            elif str_values and len(str_values) == 1 and int(str_values[0]) <= 10:
                column.java_type = GenConstants.TYPE_INTEGER
            # Use Long for large integer types
            else:
                column.java_type = GenConstants.TYPE_LONG

        # Insert field (default all fields need to be inserted)
        column.is_insert = GenConstants.REQUIRE

        # Edit field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_EDIT, column_name) and not column.is_pk():
            column.is_edit = GenConstants.REQUIRE

        # List field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_LIST, column_name) and not column.is_pk():
            column.is_list = GenConstants.REQUIRE

        # Query field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_QUERY, column_name) and not column.is_pk():
            column.is_query = GenConstants.REQUIRE

        # Query field type
        if StringUtils.ends_with_ignore_case(column_name, "name"):
            column.query_type = GenConstants.QUERY_LIKE

        # Set radio button for status fields
        if StringUtils.ends_with_ignore_case(column_name, "status"):
            column.html_type = GenConstants.HTML_RADIO
        # Set dropdown for type and sex fields
        elif StringUtils.ends_with_ignore_case(column_name, "type") or StringUtils.ends_with_ignore_case(column_name, "sex"):
            column.html_type = GenConstants.HTML_SELECT
        # Set image upload control for image fields
        elif StringUtils.ends_with_ignore_case(column_name, "image"):
            column.html_type = GenConstants.HTML_IMAGE_UPLOAD
        # Set file upload control for file fields
        elif StringUtils.ends_with_ignore_case(column_name, "file"):
            column.html_type = GenConstants.HTML_FILE_UPLOAD
        # Set rich text control for content fields
        elif StringUtils.ends_with_ignore_case(column_name, "content"):
            column.html_type = GenConstants.HTML_EDITOR

    @staticmethod
    def arrays_contains(arr, target_value) -> bool:
        return target_value in arr

    @staticmethod
    def get_module_name(package_name: str) -> str:
        return package_name.split(".")[-1]

    @staticmethod
    def get_business_name(table_name) -> str:
        return table_name.split("_")[-1]

    @staticmethod
    def convert_class_name(table_name: str) -> str:
        auto_remove_pre = gen_config.auto_remove_pre
        table_prefix = gen_config.table_prefix
        if auto_remove_pre and StringUtils.is_not_empty(table_prefix):
            search_list = StringUtils.split(table_prefix, ",")
            table_name = GenUtils.replace_first(table_name, search_list)
        return StringUtils.to_camel_case(table_name)

    @staticmethod
    def replace_first(replacement: str, search_list: List[str]) -> str:
        for search_string in search_list:
            if replacement.startswith(search_string):
                return replacement.replace(search_string, "", 1)
        return replacement

    @staticmethod
    def replace_text(text):
        return re.sub(r"表", "", text)

    @staticmethod
    def get_db_type(column_type):
        return column_type.split("(")[0] if "(" in column_type else column_type

    @staticmethod
    def get_column_length(column_type):
        if "(" in column_type:
            length = column_type.split("(")[1].split(")")[0]
            return int(length)
        else:
            return 0