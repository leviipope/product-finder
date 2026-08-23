import json
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, field_validator

class ListingFilterParams(BaseModel):
    city: str | None = None
    product_type: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    skip: int = 0
    limit: int = 20

class ListingResponse(BaseModel):
    site: str
    id: int
    title: str
    category: list[str]
    product_type: str
    price: int | None
    price_history: list[int | None] | None
    currency: str
    img: str | None
    seller: str
    seller_rating: str
    seller_profile_url: str
    location: str
    delivery_options: str | None
    description: str
    listed_at: datetime | None
    scraped_at: datetime

    @field_validator("category", "price_history", mode="before")
    @classmethod
    def parse_json_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return value