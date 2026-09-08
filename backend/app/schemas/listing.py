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
    """
    Response model for enriched laptop listings with all fields.
    This model is used for detailed listing views on the frontend.
    """

    site: str
    listing_id: int
    brand: str | None
    model: str | None
    title: str
    price: int | None
    currency: str
    iced_status: bool
    iced_at: datetime | None
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
    img_url: str | None
    seller: str | None
    seller_rating: str | None
    seller_profile_url: str | None
    delivery_options: str | None
    description: str | None
    location: str
    listed_at: datetime | None
    scraped_at: datetime


class EnrichedLaptopListingBrowseResponse(BaseModel):
    """
    Response model for browsing enriched laptop listings with essential fields.
    These fields will be in the individual listing cards on the frontend.
    """

    site: str
    listing_id: int
    brand: str | None
    model: str | None
    title: str
    price: int | None
    currency: str
    iced_status: bool
    cpu_brand: str | None
    cpu_model: str | None
    gpu_brand: str | None
    gpu_model: str | None
    ram_gb: int | None
    storage_size_gb: int | None
    resolution: str | None
    refresh_rate_hz: int | None


class EnrichedGPUListingFilterParams(BaseModel):
    site: str | None = None
    brand: str | None = None
    model: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    min_vram_gb: int | None = None
    max_vram_gb: int | None = None
    iced_status: bool | None = None
    skip: int = 0
    limit: int = 20


class EnrichedGPUListingResponse(BaseModel):
    site: str
    listing_id: int
    brand: str | None
    model: str | None
    vram_gb: int | None
    price: int | None
    title: str
    currency: str
    iced_status: bool
    iced_at: datetime | None
    price_history: list[int | None] | None
    archived_at: datetime | None
    listing_url: str
    img_url: str | None
    seller: str | None
    seller_rating: str | None
    seller_profile_url: str | None
    delivery_options: str | None
    description: str | None
    location: str
    listed_at: datetime | None
    scraped_at: datetime


class EnrichedGPUListingBrowseResponse(BaseModel):
    site: str
    listing_id: int
    brand: str | None
    model: str | None
    vram_gb: int | None
    price: int | None
    currency: str
    iced_status: bool
