from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.sql import func

from .database import Base


class Article(Base):
    __tablename__ = "article"

    url = Column(String, primary_key=True, index=True)

    title = Column(String, unique=False, index=True)
    authors = Column(String, unique=False, index=True)
    content = Column(String, unique=False, index=True)
    excerpt = Column(String, unique=False, index=False)
    content_length = Column(Integer, unique=False, index=False)
    published_date = Column(DateTime(timezone=True), unique=False, index=True, default=func.now())
    domain = Column(String, unique=False, index=True)
    language = Column(String, unique=False, index=True)
    media = Column(String, unique=False, index=False)
    meta_info = Column(JSON, unique=False, index=False)

    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())



