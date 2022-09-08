from datetime import datetime

from newsfetch_core import api_schemas
from sqlalchemy.orm import Session

from . import db_models


def get_article_by_url(db: Session, url: str):
    return db.query(db_models.Article).filter(db_models.Article.url == url).first()


def delete_article_by_url(db: Session, url: str):
    db_article = db.query(db_models.Article).filter(db_models.Article.url == url).first()
    db.delete(db_article)
    db.commit()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: api_schemas.Article):
    db_article = db_models.Article(url=article.url,
                                   title=article.title,
                                   authors=article.get_authors_str(),
                                   content=article.content,
                                   excerpt=article.excerpt,
                                   content_length=article.content_length,
                                   published_date=article.published_date,
                                   language=article.language,
                                   domain=article.domain,
                                   media=article.media,
                                   meta_info=article.meta_info,
                                   )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article: api_schemas.Article):
    db_article = db.query(db_models.Article) \
        .filter(db_models.Article.url == article.url) \
        .first()

    db_article.title = article.title
    db_article.authors = article.get_authors_str()
    db_article.content = article.content
    db_article.excerpt = article.excerpt
    db_article.content_length = article.content_length
    db_article.published_date = article.published_date
    db_article.language = article.language
    db_article.domain = article.domain
    db_article.media = article.media
    db_article.meta_info = article.meta_info

    db.commit()
    db.refresh(db_article)
    return db_article


def articles_search(db: Session,
                    start_date: datetime,
                    end_date: datetime,
                    q: str,
                    skip: int = 0,
                    limit: int = 100):
    query = db.query(db_models.Article)
    if start_date:
        query = query.filter(db_models.Article.published_date >= start_date)
    if end_date:
        query = query.filter(db_models.Article.published_date <= end_date)
    if q:
        query = query.filter(db_models.Article.title.contains(q))
    return query \
        .offset(skip) \
        .limit(limit) \
        .all()
