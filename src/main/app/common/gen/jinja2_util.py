import json
from datetime import datetime

class Jinja2Utils:
    PROJECT_PATH = "main/java"
    MYBATIS_PATH = "main/resources/mapper"
    DEFAULT_PARENT_MENU_ID = "3"

    @staticmethod
    def prepare_context(gen_table):
        """
        设置模板变量信息
        """
        module_name = gen_table.get("moduleName")
        business_name = gen_table.get("businessName")
        package_name = gen_table.get("packageName")
        tpl_category = gen_table.get("tplCategory")
        function_name = gen_table.get("functionName", "【请填写功能名称】")

        context = {
            "tplCategory": tpl_category,
            "tableName": gen_table.get("tableName"),
            "functionName": function_name,
            "ClassName": gen_table.get("className"),
            "className": Jinja2Utils.uncapitalize(gen_table.get("className")),
            "moduleName": module_name,
            "BusinessName": Jinja2Utils.capitalize(business_name),
            "businessName": business_name,
            "basePackage": Jinja2Utils.get_package_prefix(package_name),
            "packageName": package_name,
            "author": gen_table.get("functionAuthor"),
            "datetime": datetime.now().strftime("%Y-%m-%d"),
            "pkColumn": gen_table.get("pkColumn"),
            "importList": Jinja2Utils.get_import_list(gen_table),
            "permissionPrefix": Jinja2Utils.get_permission_prefix(module_name, business_name),
            "columns": gen_table.get("columns"),
            "table": gen_table,
            "dicts": Jinja2Utils.get_dicts(gen_table),
        }

        Jinja2Utils.set_menu_context(context, gen_table)

        if tpl_category == "tree":
            Jinja2Utils.set_tree_context(context, gen_table)
        elif tpl_category == "sub":
            Jinja2Utils.set_sub_context(context, gen_table)

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
    def get_template_list(tpl_category, tpl_web_type):
        """
        获取模板信息
        :param tpl_category: 模板类别 (如 CRUD、TREE、SUB 等)
        :param tpl_web_type: 前端类型 (如 vue 或 element-plus)
        :return: 模板列表
        """
        use_web_type = "vm/vue"
        if tpl_web_type == "element-plus":
            use_web_type = "vm/vue/v3"

        templates = [
            "vm/java/domain.java.vm",
            "vm/java/mapper.java.j2",
            "vm/java/service.java.j2",
            "vm/java/serviceImpl.java.j2",
            "vm/java/controller.java.j2",
            "vm/xml/mapper.xml.vm",
            "vm/sql/sql.vm",
            "vm/js/api.js.vm",
        ]

        if tpl_category == "crud":
            templates.append(f"{use_web_type}/index.vue.vm")
        elif tpl_category == "tree":
            templates.append(f"{use_web_type}/index-tree.vue.vm")
        elif tpl_category == "sub":
            templates.append(f"{use_web_type}/index.vue.vm")
            templates.append("vm/java/sub-domain.java.j2")

        return templates


    @staticmethod
    def get_file_name(template, gen_table):
        """
        获取文件名
        """
        file_name = ""
        package_name = gen_table.get("packageName")
        module_name = gen_table.get("moduleName")
        class_name = gen_table.get("className")
        business_name = gen_table.get("businessName")

        java_path = f"{Jinja2Utils.PROJECT_PATH}/{package_name.replace('.', '/')}"
        mybatis_path = f"{Jinja2Utils.MYBATIS_PATH}/{module_name}"
        vue_path = "vue"

        if "domain.java.vm" in template:
            file_name = f"{java_path}/domain/{class_name}.java"
        elif "sub-domain.java.j2" in template and gen_table.get("tplCategory") == "sub":
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
        elif "mapper.xml.vm" in template:
            file_name = f"{mybatis_path}/{class_name}Mapper.xml"
        elif "sql.vm" in template:
            file_name = f"{business_name}Menu.sql"
        elif "api.js.vm" in template:
            file_name = f"{vue_path}/api/{module_name}/{business_name}.js"
        elif "index.vue.vm" in template or "index-tree.vue.vm" in template:
            file_name = f"{vue_path}/views/{module_name}/{business_name}/index.vue"

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
        columns = gen_table.get("columns", [])
        sub_gen_table = gen_table.get("subTable")
        import_list = set()

        if sub_gen_table:
            import_list.add("java.util.List")

        for column in columns:
            if not column.get("isSuperColumn") and column.get("javaType") == "Date":
                import_list.add("java.util.Date")
                import_list.add("com.fasterxml.jackson.annotation.JsonFormat")
            elif not column.get("isSuperColumn") and column.get("javaType") == "BigDecimal":
                import_list.add("java.math.BigDecimal")

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