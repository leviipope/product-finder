from pydantic import BaseModel, EmailStr, Field
from typing import Any

class SearchFilterParams(BaseModel):
    skip: int = 0
    limit: int = 20

class SearchCreate(BaseModel):
    email: EmailStr
    search_name: str
    category: str
    filters: dict[str, Any] = Field(default_factory=dict)

class SearchResponse(BaseModel):
    search_id: int
    email: EmailStr
    search_name: str
    category: str
    filters: dict[str, Any]
    is_active: bool