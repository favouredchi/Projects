# Create a Personal Blogging Website with the following endpoints: 
# #return a list of articles, Return a single article, Create a new article, 
# Updatea  single article, Delete a single article, Update a single article, Delete a single article

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Create a SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

# Create a table for articles
class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)


# Create the table
Base.metadata.create_all(bind=engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Return a list of articles
@app.get("/articles/")
def get_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

# Return a single article
@app.get("/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# Create a new article
@app.post("/articles/")
def create_article(title: str, content: str, db: Session = Depends(get_db)):
    article = Article(title=title, content=content)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

# Update a single article
@app.put("/articles/{article_id}")
def update_article(article_id: int, title: str, content: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    article.title = title
    article.content = content
    db.commit()
    db.refresh(article)
    return article

# Delete a single article
@app.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return




