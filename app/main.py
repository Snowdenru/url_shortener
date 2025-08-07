from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas, crud
from .database import SessionLocal, engine
from config import settings

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/shorten", response_model=schemas.URLInfo)
def create_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    # Проверка URL на валидность
    if not (url.original_url.startswith('http://') or url.original_url.startswith('https://')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL must start with http:// or https://"
        )
    
    # Остальной код без изменений
    if url.custom_code:
        db_url = crud.get_db_url_by_short_code(db, url.custom_code)
        if db_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom code already exists"
            )
    
    db_url = crud.create_db_url(db, url)
    
    response = schemas.URLInfo(
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        clicks=db_url.clicks,
        created_at=db_url.created_at,
        expires_at=db_url.expires_at,
        is_active=db_url.is_active
    )
    
    return response

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    if not db_url.is_active:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL has expired"
        )
    
    if db_url.expires_at and db_url.expires_at < datetime.utcnow():
        db_url.is_active = False
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL has expired"
        )
    
    crud.update_db_clicks(db, db_url)
    return RedirectResponse(db_url.original_url)

@app.get("/stats/{short_code}", response_model=schemas.URLInfo)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_db_url_by_short_code(db, short_code)
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    return db_url

