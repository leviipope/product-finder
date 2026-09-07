from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Listing(Base):
    __tablename__ = "listings"

    site: Mapped[str] = mapped_column(String, primary_key=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String, index=True)
    product_type: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Integer, index=True)
    currency: Mapped[str] = mapped_column(String, default="HUF")
    listing_url: Mapped[str] = mapped_column(String)

    seller: Mapped[str] = mapped_column(String)
    seller_rating: Mapped[str] = mapped_column(String)
    seller_profile_url: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String, index=True)

    iced_status: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str] = mapped_column(Text)
    scraped_at: Mapped[datetime] = mapped_column(DateTime)

    category: Mapped[str] = mapped_column(JSON)
    delivery_options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price_history: Mapped[Optional[list[int]]] = mapped_column(JSON, nullable=True)

    img: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    iced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    listed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class EnrichedLaptopListing(Base):
    __tablename__ = "laptop_view"

    site: Mapped[str] = mapped_column(String, primary_key=True)
    listing_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    brand: Mapped[Optional[str]] = mapped_column(String)
    model: Mapped[Optional[str]] = mapped_column(String)
    title: Mapped[str] = mapped_column(String, index=True)
    price: Mapped[float] = mapped_column(Integer, index=True)
    currency: Mapped[str] = mapped_column(String, default="HUF")
    iced_status: Mapped[bool] = mapped_column(Boolean, default=False)
    iced_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    cpu_brand: Mapped[Optional[str]] = mapped_column(String)
    cpu_model: Mapped[Optional[str]] = mapped_column(String)
    gpu_brand: Mapped[Optional[str]] = mapped_column(String)
    gpu_model: Mapped[Optional[str]] = mapped_column(String)
    gpu_type: Mapped[Optional[str]] = mapped_column(String)
    ram_gb: Mapped[Optional[int]] = mapped_column(Integer)
    storage_size_gb: Mapped[Optional[int]] = mapped_column(Integer)
    storage_type: Mapped[Optional[str]] = mapped_column(String)
    resolution: Mapped[Optional[str]] = mapped_column(String)
    screen_size_inch: Mapped[Optional[float]] = mapped_column(Float)
    panel_type: Mapped[Optional[str]] = mapped_column(String)
    refresh_rate_hz: Mapped[Optional[int]] = mapped_column(Integer)
    img_url: Mapped[Optional[str]] = mapped_column(String)
    seller: Mapped[Optional[str]] = mapped_column(String)
    seller_rating: Mapped[Optional[str]] = mapped_column(String)
    seller_profile_url: Mapped[Optional[str]] = mapped_column(String)
    delivery_options: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    listing_url: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String, index=True)
    listed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scraped_at: Mapped[datetime] = mapped_column(DateTime)

class EnrichedGPUListing(Base):
    __tablename__ = "gpu_view"

    site: Mapped[str] = mapped_column(String, primary_key=True)
    listing_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    brand: Mapped[Optional[str]] = mapped_column(String, index=True)
    model: Mapped[Optional[str]] = mapped_column(String, index=True)
    vram_gb: Mapped[Optional[int]] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)
    currency: Mapped[str] = mapped_column(String, default="HUF")
    iced_status: Mapped[bool] = mapped_column(Boolean, default=False)
    iced_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    price_history: Mapped[Optional[int]] = mapped_column(JSON, nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    listing_url: Mapped[str] = mapped_column(String)
    img_url: Mapped[Optional[str]] = mapped_column(String)
    seller: Mapped[Optional[str]] = mapped_column(String)
    seller_rating: Mapped[Optional[str]] = mapped_column(String)
    seller_profile_url: Mapped[Optional[str]] = mapped_column(String)
    delivery_options: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String)
    listed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scraped_at: Mapped[datetime] = mapped_column(DateTime)