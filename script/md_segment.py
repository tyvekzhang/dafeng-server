import markdown
from bs4 import BeautifulSoup
import re

def read_markdown_file(file_path):
    """读取Markdown文件并返回其内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def markdown_to_html(markdown_text):
    """将Markdown文本转换为HTML"""
    return markdown.markdown(markdown_text)

def segment_markdown(html_content):
    """将HTML内容分段"""
    soup = BeautifulSoup(html_content, 'html.parser')
    segments = []
    current_segment = ""

    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
        if element.name.startswith('h'):
            if current_segment:
                segments.append(current_segment.strip())
            current_segment = element.text + "\n"
        else:
            current_segment += element.text + "\n"

    if current_segment:
        segments.append(current_segment.strip())

    return segments

def clean_segment(segment):
    """清理段落，移除多余的空白字符"""
    return re.sub(r'\s+', ' ', segment).strip()

def main(file_path):
    # 读取Markdown文件
    markdown_content = read_markdown_file(file_path)

    # 将Markdown转换为HTML
    html_content = markdown_to_html(markdown_content)

    # 分段
    segments = segment_markdown(html_content)

    # 清理并打印段落
    for i, segment in enumerate(segments, 1):
        cleaned_segment = clean_segment(segment)
        print(f"Segment {i}:")
        print(cleaned_segment)
        print("-" * 40)

if __name__ == "__main__":
    file_path = r"D:\Container\Files\2024-12\trial\environmental_protection_20241129_093004.md"
    main(file_path)