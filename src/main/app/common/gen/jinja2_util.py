import json
from datetime import datetime

from src.main.app.common.enums.enum import ConstantCode
from src.main.app.common.gen.gen_constants import GenConstants
from src.main.app.schema.gen_table_schema import TableGen


class Jinja2Utils:
    PROJECT_PATH = "main/java"
    MYBATIS_PATH = "main/resources/mapper"
    DEFAULT_PARENT_MENU_ID = "3"

    @staticmethod
    def prepare_context(table_gen: TableGen):
        """
        设置模板变量信息
        """
        gen_table = table_gen.gen_table

        package_name = gen_table.package_name
        import_list = Jinja2Utils.get_import_list(table_gen)
        function_name = gen_table.function_name
        table_name = gen_table.table_name
        author = gen_table.function_author
        date_time = datetime.now().strftime("%Y-%m-%d")
        class_name = Jinja2Utils.capitalize(gen_table.class_name)
        lowercase_class_name = Jinja2Utils.uncapitalize(class_name)
        primary_key = table_gen.pk_field
        router_name = Jinja2Utils.to_kebab_case(class_name)
        kebab_case_class_name = router_name
        fields = table_gen.fields
        module_name = gen_table.module_name
        business_name = gen_table.business_name

        tpl_category = gen_table.tpl_category


        context = {
            "package_name": package_name,
            "import_list": import_list,
            "function_name": function_name,
            "table_name": table_name,
            "author": author,
            "datetime": date_time,
            "class_name": class_name,
            "lowercase_class_name": lowercase_class_name,
            "primary_key": primary_key,
            "router_name": router_name,
            "kebab_case_class_name": kebab_case_class_name,
            "fields": fields,
            # "tpl_category": tpl_category,
            # "module_name": module_name,
            # "business_name": Jinja2Utils.capitalize(business_name),
            # "base_package": Jinja2Utils.get_package_prefix(package_name),
            # "permission_prefix": Jinja2Utils.get_permission_prefix(module_name, business_name),
            # "table": gen_table,
            # "dicts": Jinja2Utils.get_dicts(gen_table),
        }

        # Jinja2Utils.set_menu_context(context, gen_table)
        #
        # if tpl_category == "tree":
        #     Jinja2Utils.set_tree_context(context, gen_table)
        # elif tpl_category == "sub":
        #     Jinja2Utils.set_sub_context(context, gen_table)

        return context

    @staticmethod
    def set_menu_context(context, gen_table):
        options = gen_table.get("options", "{}")
        params_obj = json.loads(options)
        parent_menu_id = Jinja2Utils.get_parent_menu_id(params_obj)
        context["parentMenuId"] = parent_menu_id

    @staticmethod
    def set_tree_context(context, gen_table):
        options = gen_table.get("options", "{}")
        params_obj = json.loads(options)
        tree_code = params_obj.get("treeCode")
        tree_parent_code = params_obj.get("treeParentCode")
        tree_name = params_obj.get("treeName")

        context.update({
            "treeCode": tree_code,
            "treeParentCode": tree_parent_code,
            "treeName": tree_name,
            "expandColumn": Jinja2Utils.get_expand_column(gen_table),
            "tree_parent_code": params_obj.get("treeParentCode"),
            "tree_name": params_obj.get("treeName"),
        })

    @staticmethod
    def set_sub_context(context, gen_table):
        sub_table = gen_table.get("subTable", {})
        sub_table_name = gen_table.get("subTableName")
        sub_table_fk_name = gen_table.get("subTableFkName")

        sub_class_name = sub_table.get("className")
        sub_table_fk_class_name = Jinja2Utils.convert_to_camel_case(sub_table_fk_name)

        context.update({
            "subTable": sub_table,
            "subTableName": sub_table_name,
            "subTableFkName": sub_table_fk_name,
            "subTableFkClassName": sub_table_fk_class_name,
            "subTableFkclassName": Jinja2Utils.uncapitalize(sub_table_fk_class_name),
            "subClassName": sub_class_name,
            "subclassName": Jinja2Utils.uncapitalize(sub_class_name),
            "subImportList": Jinja2Utils.get_import_list(sub_table),
        })

    @staticmethod
    def get_template_list(backend: str, tpl_backend_type: str, tpl_category: str, tpl_web_type: str):
        """
        获取模板信息
        :param backend: 后端语言, java, python, go, rust...
        :param tpl_backend_type: 后端语言使用的模板类型, mybatis, mybatis-plus...
        :param tpl_category: 模板类别 (如 CRUD、TREE、SUB 等)
        :param tpl_web_type: 前端类型 (如 react 或 element-plus)
        :return: 模板列表
        """
        index_tpl = "jinja2/react/index.tsx.j2"
        index_create_tpl = "jinja2/react/components/indexCreate.tsx.j2"
        if tpl_web_type == "element-plus":
            use_web_type = "vm/react/v3"
        entity_tpl = "jinja2/java/mybatis_plus/entity.java.j2"
        mapper_tpl = "jinja2/java/mybatis_plus/mapper.java.j2"
        service_tpl = "jinja2/java/mybatis_plus/service.java.j2"
        serviceimpl_tpl = "jinja2/java/mybatis_plus/serviceImpl.java.j2"
        controller_tpl = "jinja2/java/mybatis_plus/controller.java.j2"
        create_tpl = "jinja2/java/command/create.java.j2"
        modify_tpl = "jinja2/java/command/modify.java.j2"
        batch_modify_tpl = "jinja2/java/command/batchModify.java.j2"
        query_tpl = "jinja2/java/command/query.java.j2"
        detail_tpl = "jinja2/java/vo/detail.java.j2"
        page_tpl = "jinja2/java/vo/page.java.j2"
        converter_tpl = "jinja2/java/converter/converter.java.j2"
        api_tpl = "jinja2/js/api.js.j2"
        type_tpl = "jinja2/js/type.js.j2"
        if backend == GenConstants.JAVA:
            if tpl_backend_type == GenConstants.MYBATIS:
                entity_tpl = "jinja2/java/mybatis/entity.java.j2"
        templates = [
            index_create_tpl,
            entity_tpl,
            mapper_tpl,
            service_tpl,
            serviceimpl_tpl,
            controller_tpl,
            create_tpl,
            modify_tpl,
            query_tpl,
            detail_tpl,
            page_tpl,
            converter_tpl,
            api_tpl,
            type_tpl,
            index_tpl,
            batch_modify_tpl,
        ]

        # if tpl_category == "crud":
        #     templates.append(f"{use_web_type}/index.react.vm")
        # elif tpl_category == "tree":
        #     templates.append(f"{use_web_type}/index-tree.react.vm")
        # elif tpl_category == "sub":
        #     templates.append(f"{use_web_type}/index.react.vm")
        #     templates.append("vm/java/sub-entity.java.j2")

        return templates


    @staticmethod
    def get_file_name(template, table_gen):
        """
        获取文件名
        """
        gen_table = table_gen.gen_table
        file_name = ""
        package_name = gen_table.package_name
        module_name = gen_table.module_name
        class_name = gen_table.class_name
        business_name = gen_table.business_name

        java_path = f"{Jinja2Utils.PROJECT_PATH}/{package_name.replace('.', '/')}"
        mybatis_path = f"{Jinja2Utils.MYBATIS_PATH}/{module_name}"
        client_path = "src"
        kebab_case_class_name= Jinja2Utils.to_kebab_case(business_name)

        if "entity.java.j2" in template:
            file_name = f"{java_path}/entity/{class_name}DO.java"
        elif "sub-entity.java.j2" in template and gen_table.get("tplCategory") == "sub":
            sub_class_name = gen_table.get("subTable").get("className")
            file_name = f"{java_path}/domain/{sub_class_name}.java"
        elif "mapper.java.j2" in template:
            file_name = f"{java_path}/mapper/{class_name}Mapper.java"
        elif "service.java.j2" in template:
            file_name = f"{java_path}/service/I{class_name}Service.java"
        elif "serviceImpl.java.j2" in template:
            file_name = f"{java_path}/service/impl/{class_name}ServiceImpl.java"
        elif "controller.java.j2" in template:
            file_name = f"{java_path}/controller/{class_name}Controller.java"
        elif "converter.java.j2" in template:
            file_name = f"{java_path}/converter/{class_name}Converter.java"
        elif "create.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Create.java"
        elif "modify.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Modify.java"
        elif "batchModify.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}BatchModify.java"
        elif "query.java.j2" in template:
            file_name = f"{java_path}/command/{class_name}Query.java"
        elif "detail.java.j2" in template:
            file_name = f"{java_path}/vo/{class_name}Detail.java"
        elif "page.java.j2" in template:
            file_name = f"{java_path}/vo/{class_name}Page.java"
        elif "mapper.xml.vm" in template:
            file_name = f"{mybatis_path}/{class_name}Mapper.xml"
        elif "sql.vm" in template:
            file_name = f"{business_name}Menu.sql"
        elif "api.js.j2" in template:
            file_name = f"{client_path}/service/{kebab_case_class_name}.ts"
        elif "type.js.j2" in template:
            file_name = f"{client_path}/types/{kebab_case_class_name}.ts"

        return file_name

    @staticmethod
    def get_package_prefix(package_name):
        """
        获取包前缀
        """
        last_index = package_name.rfind(".")
        return package_name[:last_index] if last_index != -1 else package_name

    @staticmethod
    def get_import_list(gen_table):
        """
        根据列类型获取导入包
        """
        fields = gen_table.fields

        sub_gen_table = gen_table.sub_table
        import_list = set()

        if sub_gen_table:
            import_list.add("java.util.List")

        for field in fields:
            if field.gen_field.field_type == "Date":
                import_list.add("java.util.Date")
            elif field.gen_field.field_type == "BigDecimal":
                import_list.add("java.math.BigDecimal")
            elif field.gen_field.field_type == "LocalDateTime":
                import_list.add("java.time.LocalDateTime")

        return list(import_list)

    @staticmethod
    def get_dicts(gen_table):
        """
        根据列类型获取字典组
        """
        columns = gen_table.get("columns", [])
        dicts = set()
        Jinja2Utils.add_dicts(dicts, columns)

        sub_table = gen_table.get("subTable")
        if sub_table:
            sub_columns = sub_table.get("columns", [])
            Jinja2Utils.add_dicts(dicts, sub_columns)

        return ", ".join(dicts)

    @staticmethod
    def add_dicts(dicts, columns):
        """
        添加字典列表
        """
        for column in columns:
            if (
                not column.get("isSuperColumn")
                and column.get("dictType")
                and column.get("htmlType") in {"select", "radio", "checkbox"}
            ):
                dicts.add(f"'{column.get('dictType')}'")

    @staticmethod
    def get_permission_prefix(module_name, business_name):
        """
        获取权限前缀
        """
        return f"{module_name}:{business_name}"

    @staticmethod
    def get_parent_menu_id(params_obj):
        """
        获取上级菜单 ID 字段
        """
        if params_obj and "parentMenuId" in params_obj:
            return params_obj.get("parentMenuId")
        return Jinja2Utils.DEFAULT_PARENT_MENU_ID

    @staticmethod
    def get_tree_code(params_obj):
        """
        获取 TreeCode 字段
        """
        return params_obj.get("treeCode", "")

    @staticmethod
    def get_tree_parent_code(params_obj):
        """
        获取 TreeParentCode 字段
        """
        return params_obj.get("treeParentCode", "")

    @staticmethod
    def get_tree_name(params_obj):
        """
        获取 TreeName 字段
        """
        return params_obj.get("treeName", "")

    @staticmethod
    def get_expand_column(gen_table):
        """
        获取树表的展开列
        """
        columns = gen_table.get("columns", [])
        for index, column in enumerate(columns):
            if column.get("isList") and column.get("isSuperColumn") is False:
                return index
        return 0

    @staticmethod
    def convert_to_camel_case(name):
        """
        将字符串转换为驼峰命名
        """
        words = name.split("_")
        return words[0] + ''.join(word.capitalize() for word in words[1:])

    @staticmethod
    def uncapitalize(name):
        """
        将字符串的首字母小写
        """
        if not name:
            return ""
        return name[0].lower() + name[1:]

    @staticmethod
    def capitalize(name):
        """
        将字符串的首字母大写
        """
        if not name:
            return ""
        return name[0].upper() + name[1:]

    @staticmethod
    def to_kebab_case(name):
        if not name:
            return name
        result = []
        for i, c in enumerate(name):
            if c.isupper():
                if i != 0:
                    result.append('-')
                result.append(c.lower())
            else:
                result.append(c)
        return ''.join(result)