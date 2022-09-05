from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from newsfetch_core.newplease_adapter import NewsPleaseHtmlAdapter
from sqlalchemy.orm import Session

from newsfetch_core import api_schemas
from core import db_models, crud
from core.database import engine, SessionLocal

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    pass


@app.get("/health-check/", response_class=JSONResponse)
async def health_check() -> JSONResponse:
    return JSONResponse({"status": "OK"})


@app.post("/article", response_model=api_schemas.Article)
async def create_article(article: api_schemas.Article, db: Session = Depends(get_db)) -> api_schemas.Article:
    db_article = crud.get_article_by_url(db, url=article.url)
    if db_article:
        raise HTTPException(status_code=400, detail=f"article with url {article.url} already exists!")
    db_article = crud.create_article(db=db, article=article)
    return api_schemas.Article.from_orm(db_article)


@app.put("/article", response_model=api_schemas.Article)
async def update_article(article: api_schemas.Article, db: Session = Depends(get_db)) -> api_schemas.Article:
    db_article = crud.get_article_by_url(db, url=article.url)
    if not db_article:
        raise HTTPException(status_code=400, detail=f"article with url {article.url} does not exist!")
    return crud.update_article(db=db, article=article)


@app.get("/articles", response_model=list[api_schemas.Article])
async def get_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[api_schemas.Article]:
    if limit > config.MAX_LIMIT:
        limit = config.MAX_LIMIT
    db_articles = crud.get_articles(db, skip=skip, limit=limit)
    return db_articles


@app.get("/article", response_model=api_schemas.Article)
async def get_article_by_url(url: str, db: Session = Depends(get_db)) -> api_schemas.Article:
    db_article = crud.get_article_by_url(db, url=url)
    if db_article is None:
        raise HTTPException(status_code=404, detail=f"article with url {url} does not exist!")
    return db_article


@app.delete("/article", response_class=JSONResponse)
async def delete_article_by_url(url: str, db: Session = Depends(get_db)) -> JSONResponse:
    try:
        crud.delete_article_by_url(db, url=url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"error deleting article with url {url}: {e}")
    return JSONResponse({"status": "OK"})


@app.get("/articles/search", response_model=list[api_schemas.Article])
async def articles_search(start_date: datetime = None,
                          end_date: datetime = None,
                          q: str = None,
                          skip: int = 0,
                          limit: int = 10,
                          db: Session = Depends(get_db)) -> list[api_schemas.Article]:
    db_articles = crud.articles_search(db, start_date=start_date, end_date=end_date, q=q, skip=skip, limit=limit)
    return db_articles

@app.post("/article/parse", response_model=api_schemas.Article)
async def parse_article(parse_article_input: api_schemas.ParseArticleInput) -> api_schemas.Article:
    newsplease_adapter = NewsPleaseHtmlAdapter(html=parse_article_input.html, url=parse_article_input.url)
    return newsplease_adapter.get_article()

if __name__ == "__main__":
    uvicorn.run("fastapi_main:app", reload=True)
