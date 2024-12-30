import os
import re
from typing import List

from src.main.app.common.config.config_manager import load_config
from src.main.app.common.gen.gen_constants import GenConstants
from src.main.app.common.util.string_util import StringUtils, is_empty
from src.main.app.model.db_field_model import FieldDO
from src.main.app.model.gen_field_model import GenFieldDO
from src.main.app.model.gen_table_model import GenTableDO

config = load_config()
gen_config = config.gen

class GenUtils:
    @staticmethod
    def init_table(gen_table: GenTableDO):
        gen_table.class_name = GenUtils.convert_class_name(gen_table.class_name)
        gen_table.package_name = gen_config.package_name
        gen_table.module_name = GenUtils.get_module_name(gen_config.package_name)
        gen_table.business_name = GenUtils.get_business_name(gen_table.class_name)
        gen_table.function_name = GenUtils.replace_text(gen_table.function_name)
        gen_table.function_author = gen_config.author

    @staticmethod
    def init_field(gen_field: GenFieldDO, field_record: FieldDO):
        """
        Initialize column attribute fields
        """
        data_type = field_record.type
        field_name = field_record.name

        gen_field.field_name = StringUtils.to_camel_case(field_name)
        # Set default type
        gen_field.field_type = GenConstants.TYPE_STRING
        gen_field.js_type = GenConstants.TYPE_JS_STRING
        gen_field.query_type = GenConstants.QUERY_EQ
        gen_field.primary_key = field_record.primary_key
        gen_field.comment = field_record.comment

        if GenUtils.arrays_contains(GenConstants.COLUMNTYPE_STR, data_type) or GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TEXT, data_type):
            field_length = field_record.length
            html_type = GenConstants.HTML_TEXTAREA if GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TEXT, data_type) or field_length >= 500 else GenConstants.HTML_INPUT
            gen_field.html_type = html_type
        elif GenUtils.arrays_contains(GenConstants.COLUMNTYPE_TIME, data_type):
            gen_field.field_type = GenConstants.TYPE_LOCALDATETIME
            gen_field.html_type = GenConstants.HTML_DATETIME
        elif GenUtils.arrays_contains(GenConstants.COLUMNTYPE_NUMBER, data_type):
            gen_field.html_type = GenConstants.HTML_INPUT
            gen_field.js_type = GenConstants.TYPE_JS_NUMBER
            scale = field_record.scale
            length = field_record.length
            if scale is not None:
                gen_field.field_type = GenConstants.TYPE_BIGDECIMAL
            elif data_type == "int4" or data_type == "int2" or (length is not None and length <= 10):
                gen_field.field_type = GenConstants.TYPE_INTEGER
            else:
                gen_field.field_type = GenConstants.TYPE_LONG

        # Insert field (default all fields need to be inserted)
        gen_field.creatable = GenConstants.REQUIRE

        # Edit field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_EDIT, field_name) and not field_record.primary_key:
            gen_field.modifiable = GenConstants.REQUIRE

        # Page field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_LIST, field_name) and not field_record.primary_key:
            gen_field.pageable = GenConstants.REQUIRE

        # Detail field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_LIST, field_name) and not field_record.primary_key:
            gen_field.detailable = GenConstants.REQUIRE

        # Query field
        if not GenUtils.arrays_contains(GenConstants.COLUMNNAME_NOT_QUERY, field_name) and not field_record.primary_key:
            gen_field.queryable = GenConstants.REQUIRE

        # Query field type
        if StringUtils.ends_with_ignore_case(field_name, "name"):
            gen_field.query_type = GenConstants.QUERY_LIKE

        # Set radio button for status fields
        if StringUtils.ends_with_ignore_case(field_name, "status"):
            gen_field.html_type = GenConstants.HTML_RADIO
        # Set dropdown for type and sex fields
        elif StringUtils.ends_with_ignore_case(field_name, "type") or StringUtils.ends_with_ignore_case(field_name, "sex"):
            gen_field.html_type = GenConstants.HTML_SELECT
        # Set image upload control for image fields
        elif StringUtils.ends_with_ignore_case(field_name, "image"):
            gen_field.html_type = GenConstants.HTML_IMAGE_UPLOAD
        # Set file upload control for file fields
        elif StringUtils.ends_with_ignore_case(field_name, "file"):
            gen_field.html_type = GenConstants.HTML_FILE_UPLOAD
        # Set rich text control for content fields
        elif StringUtils.ends_with_ignore_case(field_name, "content"):
            gen_field.html_type = GenConstants.HTML_EDITOR

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
    def get_db_type(field_type):
        return field_type.split("(")[0] if "(" in field_type else field_type

    @staticmethod
    def get_field_length(field_type):
        if "(" in field_type:
            length = field_type.split("(")[1].split(")")[0]
            return int(length)
        else:
            return 0

    @staticmethod
    def trim_jinja2_name(name: str) -> str:
        if is_empty(name):
            return ""
            # Get the base name of the file (without directory)
        base_name = os.path.basename(name)

        # Split the base name and extension
        name_without_extension, _ = os.path.splitext(base_name)

        # Split again to remove the .j2 extension if present
        name_without_j2, _ = os.path.splitext(name_without_extension)

        return name_without_j2