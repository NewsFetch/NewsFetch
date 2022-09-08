from datetime import datetime
from typing import Optional, List, Any

from pydantic import Field
from pydantic.main import BaseModel


class Article(BaseModel):
    url: str
    title: str
    authors: List[str]
    content: str
    excerpt: Optional[str] = None
    content_length: int
    published_date: datetime
    language: str
    domain: str
    media: Optional[str] = None
    meta_info: Optional[dict[str, Any]] = None

    class Config:
        orm_mode = True

    def get_authors_str(self):
        return ",".join(self.authors)

    @classmethod
    def from_orm(cls, obj: Any) -> 'Article':
        # `obj` is the orm model instance
        if hasattr(obj, 'authors'):
            obj.authors = obj.authors.split(',')
        return super().from_orm(obj)

class ArticleSearchParams(BaseModel):
    start_date: Optional[datetime]
    end_date: Optional[datetime]

class ParseArticleInput(BaseModel):
    url: str
    html: str