import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def init_jinja2():
    # 定义模板所在的目录
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    # 创建一个加载器，Jinja2将从这个目录中查找模板
    loader = FileSystemLoader(template_dir)

    # 创建Jinja2环境
    # 'select_autoescape' 用于自动转义，防止XSS攻击
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(['html', 'xml']),
        # 这里可以设置其他参数如缓存大小等
    )

    # 可以在这里设置全局变量或过滤器等
    # env.globals['some_static_var'] = "value"

    # 返回环境对象，这个对象可以用来渲染模板
    return env

# 使用示例
if __name__ == "__main__":
    try:
        jinja_env = init_jinja2()
        # 现在你可以使用jinja_env来加载和渲染模板了
        template = jinja_env.get_template('example.html')
        print(template.render(name='World'))
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Jinja2: {e}")