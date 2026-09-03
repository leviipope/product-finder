from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text, JSON
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
    price_history: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)

    img: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    iced_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    listed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
