from datetime import datetime
from pydantic import BaseModel

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

class EnrichedLaptopFilterParams(BaseModel):
    site: str | None = None
    brand: str | None = None
    model: str | None = None
    title: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    iced_status: bool | None = None
    cpu_brand: str | None = None
    cpu_model: str | None = None
    gpu_brand: str | None = None
    gpu_model: str | None = None
    gpu_type: str | None = None
    min_ram_gb: int | None = None
    max_ram_gb: int | None = None
    min_storage_size_gb: int | None = None
    max_storage_size_gb: int | None = None
    storage_type: str | None = None
    resolution: str | None = None
    min_screen_size_inch: float | None = None
    max_screen_size_inch: float | None = None
    panel_type: str | None = None
    min_refresh_rate_hz: int | None = None
    max_refresh_rate_hz: int | None = None
    location: str | None = None
    skip: int = 0
    limit: int = 20

class EnrichedLaptopListingResponse(BaseModel):
    site: str
    listing_id: int
    brand: str | None
    model: str | None
    title: str
    price: int | None
    currency: str
    iced_status: bool
    archived_at: datetime | None
    cpu_brand: str | None
    cpu_model: str | None
    gpu_brand: str | None
    gpu_model: str | None
    gpu_type: str | None
    ram_gb: int | None
    storage_size_gb: int | None
    storage_type: str | None
    resolution: str | None
    screen_size_inch: float | None
    panel_type: str | None
    refresh_rate_hz: int | None
    listing_url: str
    location: str
    listed_at: datetime | None
    scraped_at: datetime