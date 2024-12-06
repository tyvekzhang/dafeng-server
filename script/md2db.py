import os
import re
from markdown import markdown
from bs4 import BeautifulSoup

from typing import Optional
from sqlmodel import Field, Column, String, SQLModel, BigInteger, Integer, Text, Session, create_engine
from src.main.app.model.model_base import ModelBase


class ReadArticleBase(SQLModel):
    topic_id: Optional[int] = Field(default= 1, sa_column=Column(BigInteger))
    title: Optional[str] = Field(sa_column=Column(String(200)))
    content: Optional[str] = Field(sa_column=Column(Text))
    pic_url: Optional[str] = Field(default= '', sa_column=Column(String(200)))
    word_count: Optional[int] = Field(sa_column=Column(Integer))
    age_begin: Optional[int] = Field(sa_column=Column(Integer))
    age_end: Optional[int] = Field(sa_column=Column(Integer))
    lexile_begin: Optional[int] = Field(sa_column=Column(Integer))
    lexile_end: Optional[int] = Field(sa_column=Column(Integer))
    status: Optional[int] = Field(default=0, sa_column=Column(Integer))

class ReadArticleDO(ReadArticleBase, ModelBase, table=True):
    __tablename__ = "read_article"
    __table_args__ = ({"comment": "阅读文章表"},)


db_url = f"postgresql://root:My_dev-123@172.21.14.53:5432/singularity_read"
engine = create_engine(db_url, echo=True)

def markdown_to_text_via_html(markdown_text):
    # 将 Markdown 转换为 HTML
    html = markdown(markdown_text)

    # 使用 BeautifulSoup 解析 HTML 并提取纯文本
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def extract_content(text):
    # Extract metadata
    metadata = {}
    metadata_match = re.search(r'---\n(.*?)\n---', text, re.DOTALL)
    if metadata_match:
        metadata_text = metadata_match.group(1)
        for line in metadata_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

    # Extract title
    title = metadata.get('title', '')

    # Extract Lexile level
    lexile_level = metadata.get('lexile_level', '')
    lexile_match = re.match(r'(\d+)L-(\d+)L', lexile_level)
    lexile_level_start = lexile_match.group(1) if lexile_match else ''
    lexile_level_end = lexile_match.group(2) if lexile_match else ''

    # Extract age level
    age = metadata.get('age_group', '')
    age_match = re.match(r'(\d+)-(\d+)', age)
    age_start = age_match.group(1) if age_match else ''
    age_end = age_match.group(2) if age_match else ''

    # Extract word count
    word_count = metadata.get('word_count', '')

    # Extract content (everything after the metadata block)
    content = re.sub(r'---\n.*?---\n', '', text, flags=re.DOTALL).strip()
    content = markdown_to_text_via_html(content).strip()
    content = re.sub(r'\n+', '\n\n', content)
    content = content.replace('\n\n', '\\n\\n').replace('\n', ' ')
    sentences = re.split(r'(?<=[.!?]) +|(\\n\\n)', content)
    sentences = [s for s in sentences if s]  # 过滤掉空字符串
    result_sen = []
    for sentence in sentences:
        if sentence == '\\n\\n':
            result_sen[-1] += '\n\n'
        else:
            result_sen.append(sentence)
    return {
        'title': title,
        'age_begin': int(age_start) if age_start != '' else 0,
        'age_end': int(age_end) if age_end != '' else 0,
        'lexile_begin': int(lexile_level_start) if lexile_level_start != '' else 0,
        'lexile_end': int(lexile_level_end) if lexile_level_end != '' else 0,
        'word_count': int(word_count) if word_count != '' else 0,
        'content': content
    }


def read_md_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


def process_md_files(directory: str):
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                file_path = os.path.join(directory, filename)
                text = read_md_file(file_path)
                if text:
                    try:
                        result = extract_content(text)
                        record = ReadArticleDO(**result)
                        session.add(record)
                    except:
                        print(file_path)

        try:
            session.commit()
            print("All files processed and committed successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error committing to database: {e}")

def main():
    directory = r"D:\Container\Files\2024-12\trial_test"  # Replace with the actual path to your markdown files
    process_md_files(directory)

if __name__ == "__main__":
    main()