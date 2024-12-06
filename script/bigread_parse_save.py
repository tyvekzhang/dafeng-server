from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Session, SQLModel, create_engine, JSON
import json

# Define the data model
class Article(SQLModel, table=True):
    id: int = Field(primary_key=True)
    brain_id: str = Field(default="")
    title: str
    lexile: str
    lexile_num: int
    grade: str
    hash_id: str
    topic_id: int
    uid: int
    chat_id: str = Field(default="")
    content: str
    quiz: int
    img: str
    tts_info: Optional[str] = Field(default=None)
    v_info: Optional[str] = Field(default=None)
    mark_complete: int
    help_me_info: str = Field(default="")
    page_content: Optional[str] = Field(default=None)
    word_parsing: Optional[str] = Field(default=None)
    subject: str
    wordcount: int
    make_type: str
    sources: Optional[str] = Field(default=None)
    related: Optional[str] = Field(default=None)
    images: Optional[str] = Field(default=None)
    step_lock: str
    free_id: str
    created_at: datetime
    updated_at: datetime

# Create the database engine
engine = create_engine("sqlite:///articles.db")

# Create the tables
SQLModel.metadata.create_all(engine)

# Parse the JSON response
response_json = '''
{
    "code": 200,
    "data": [
        {
            "id": 39040,
            "brain_id": "",
            "title": "Malala Yousafzai's Address to the United Nations, July 2013",
            "lexile": "860L",
            "lexile_num": 860,
            "grade": "8th Grade",
            "hash_id": "c03b0b9cf4974838a62307015f03cc90",
            "topic_id": 0,
            "uid": 0,
            "chat_id": "",
            "content": "In the name of God, The Most Beneficen",
            "quiz": 0,
            "img": "files/png/7237700444053590016.png",
            "tts_info": null,
            "v_info": null,
            "mark_complete": 0,
            "help_me_info": "",
            "page_content": null,
            "word_parsing": null,
            "subject": "Speech",
            "wordcount": 1526,
            "make_type": "THIRD",
            "sources": null,
            "related": null,
            "images": null,
            "step_lock": "{\"quiz\": 1, \"vocabulary\": 1}",
            "free_id": "7255562960578772992",
            "created_at": "2024-09-06T05:57:38+08:00",
            "updated_at": "2024-10-25T20:56:52+08:00"
        }
    ]
}
'''

response_data = json.loads(response_json)

# Save the data to the database
with Session(engine) as session:
    for item in response_data['data']:
        article = Article(
            id=item['id'],
            brain_id=item['brain_id'],
            title=item['title'],
            lexile=item['lexile'],
            lexile_num=item['lexile_num'],
            grade=item['grade'],
            hash_id=item['hash_id'],
            topic_id=item['topic_id'],
            uid=item['uid'],
            chat_id=item['chat_id'],
            content=item['content'],
            quiz=item['quiz'],
            img=item['img'],
            tts_info=item['tts_info'],
            v_info=item['v_info'],
            mark_complete=item['mark_complete'],
            help_me_info=item['help_me_info'],
            page_content=item['page_content'],
            word_parsing=item['word_parsing'],
            subject=item['subject'],
            wordcount=item['wordcount'],
            make_type=item['make_type'],
            sources=item['sources'],
            related=item['related'],
            images=item['images'],
            step_lock=item['step_lock'],
            free_id=item['free_id'],
            created_at=datetime.fromisoformat(item['created_at']),
            updated_at=datetime.fromisoformat(item['updated_at'])
        )
        session.add(article)
    session.commit()

print("Data has been successfully saved to the database.")

# Verify the data was saved
with Session(engine) as session:
    articles = session.query(Article).all()
    for article in articles:
        print(f"Article ID: {article.id}, Title: {article.title}")