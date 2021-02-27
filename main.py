from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic.main import BaseModel

app = FastAPI()


@app.get('/')
def get_index_page():
    return {'data': 'articles list'}


@app.get('/articles/unpublished')
def get_unpublished():
    return {'data': 'unpublished articles'}


@app.get('/articles/{id}')
def get_articles_by_id(id: int):
    return {'data': id}


@app.get('/articles')
def get_articles(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    result = {'limit': limit, 'published': published}
    if sort:
        result.update({'sort': sort})
    return result


@app.get('/articles/{id}/comments')
def get_comments_by_article(id: int, limit = 10):
    return {'article_id': id}


class Article(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/articles')
def create_articles(article: Article):
    published = '' if article.published else '(unpublished)'
    return {'article': f'{article.title} {published}: {article.body}'}

