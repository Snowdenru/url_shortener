from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional
from datetime import datetime

class URLBase(BaseModel):
    original_url: str  # Изменили HttpUrl на str

    @field_validator('original_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")
        return v

class URLCreate(URLBase):
    custom_code: Optional[str] = None
    expiry_days: Optional[int] = None

    @field_validator('custom_code')
    def validate_custom_code(cls, v):
        if v is not None and not v.isalnum():
            raise ValueError("Custom code must be alphanumeric")
        return v

class URLInfo(URLBase):
    short_code: str
    clicks: int
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True