"""Template operation util"""

import os
from typing import Any
from jinja2 import Template
from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import SystemException

base_dir: str = os.path.dirname(os.path.abspath(__file__))
resource_dir: str = os.path.abspath(
    os.path.join(base_dir, os.pardir, os.pardir, os.pardir, "resource")
)
home_template_dir: str = os.path.join(resource_dir, "template")


def load_template_file(
    template_name: str, module: str = "default", sub_module: str = ""
) -> Template:
    """
    Load template.

    Args:
        template_name: Name of the template file.
        module: Module directory name.
        sub_module: Sub-module directory name.

    Returns:
        Jinja2 Template object.

    Raises:
        SystemException: If template not found.
    """
    module_template_dir: str = os.path.join(home_template_dir, module)
    sub_module_template_dir: str = (
        module_template_dir
        if not sub_module
        else os.path.join(module_template_dir, sub_module)
    )
    template_path: str = os.path.join(sub_module_template_dir, template_name)
    if not os.path.exists(template_path):
        raise SystemException(
            ResponseCode.TEMPLATE_NOT_FOUND_ERROR.code,
            f"{ResponseCode.TEMPLATE_NOT_FOUND_ERROR.msg}: {template_path}",
        )
    with open(template_path, "r", encoding="UTF-8") as f:
        return Template(f.read())


def render_template(template: Template, **context: Any) -> str:
    """
    Render template.

    Args:
        template: Template to render.
        **context: Template variables.

    Returns:
        Rendered template string.
    """
    return template.render(**context)


def load_and_render_template(
    template_name: str, module: str = "default", sub_module: str = "", **context: Any
) -> str:
    """
    Load and render template.

    Args:
        template_name: Name of the template file.
        module: Module directory name.
        sub_module: Sub-module directory name.
        **context: Template variables for rendering.

    Returns:
        Rendered template string.

    Raises:
        SystemException: If template not found or rendering fails.
    """
    return render_template(
        load_template_file(template_name, module, sub_module), **context
    )
