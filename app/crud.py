from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import string
from . import models, schemas

def get_db_url_by_short_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def create_db_url(db: Session, url: schemas.URLCreate):
    if url.custom_code:
        short_code = url.custom_code
    else:
        short_code = generate_short_code()
    
    if url.expiry_days:
        expires_at = datetime.utcnow() + timedelta(days=url.expiry_days)
    else:
        expires_at = None
    
    db_url = models.URL(
        original_url=str(url.original_url),  # Явное преобразование в строку
        short_code=short_code,
        expires_at=expires_at
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def update_db_clicks(db: Session, db_url: models.URL):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url

def generate_short_code(length: int = 6):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))