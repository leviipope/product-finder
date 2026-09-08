from app.models.listing import EnrichedGPUListing, EnrichedLaptopListing, Listing
from app.schemas.listing import (
    EnrichedGPUListingFilterParams,
    EnrichedLaptopFilterParams,
    ListingFilterParams,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_listings(db: Session, params: ListingFilterParams) -> list[Listing]:
    stmt = select(Listing)

    if params.city:
        stmt = stmt.where(Listing.location.ilike(f"%{params.city}%"))
    if params.product_type:
        stmt = stmt.where(Listing.product_type == params.product_type)
    if params.min_price is not None:
        stmt = stmt.where(Listing.price >= params.min_price)
    if params.max_price is not None:
        stmt = stmt.where(Listing.price <= params.max_price)

    stmt = stmt.offset(params.skip).limit(params.limit)

    return list(db.scalars(stmt).all())


def get_enriched_laptop_listing(
    db: Session, site: str, listing_id: int
) -> EnrichedLaptopListing | None:
    stmt = select(EnrichedLaptopListing).where(
        EnrichedLaptopListing.site == site,
        EnrichedLaptopListing.listing_id == listing_id,
    )

    return db.scalars(stmt).first()


def get_enriched_laptop_listings(
    db: Session, params: EnrichedLaptopFilterParams
) -> list[EnrichedLaptopListing]:
    stmt = select(EnrichedLaptopListing)

    if params.site:
        stmt = stmt.where(EnrichedLaptopListing.site == params.site)
    if params.brand:
        stmt = stmt.where(EnrichedLaptopListing.brand == params.brand)
    if params.model:
        stmt = stmt.where(EnrichedLaptopListing.model == params.model)
    if params.title:
        stmt = stmt.where(EnrichedLaptopListing.title.ilike(f"%{params.title}%"))
    if params.min_price is not None:
        stmt = stmt.where(EnrichedLaptopListing.price >= params.min_price)
    if params.max_price is not None:
        stmt = stmt.where(EnrichedLaptopListing.price <= params.max_price)
    if params.iced_status is not None:
        stmt = stmt.where(EnrichedLaptopListing.iced_status == params.iced_status)
    if params.cpu_brand:
        stmt = stmt.where(EnrichedLaptopListing.cpu_brand == params.cpu_brand)
    if params.cpu_model:
        stmt = stmt.where(EnrichedLaptopListing.cpu_model == params.cpu_model)
    if params.gpu_brand:
        stmt = stmt.where(EnrichedLaptopListing.gpu_brand == params.gpu_brand)
    if params.gpu_model:
        stmt = stmt.where(EnrichedLaptopListing.gpu_model == params.gpu_model)
    if params.gpu_type:
        stmt = stmt.where(EnrichedLaptopListing.gpu_type == params.gpu_type)
    if params.min_ram_gb:
        stmt = stmt.where(EnrichedLaptopListing.ram_gb >= params.min_ram_gb)
    if params.max_ram_gb:
        stmt = stmt.where(EnrichedLaptopListing.ram_gb <= params.max_ram_gb)
    if params.min_storage_size_gb:
        stmt = stmt.where(
            EnrichedLaptopListing.storage_size_gb >= params.min_storage_size_gb
        )
    if params.max_storage_size_gb:
        stmt = stmt.where(
            EnrichedLaptopListing.storage_size_gb <= params.max_storage_size_gb
        )
    if params.storage_type:
        stmt = stmt.where(EnrichedLaptopListing.storage_type == params.storage_type)
    if params.resolution:
        stmt = stmt.where(EnrichedLaptopListing.resolution == params.resolution)
    if params.min_screen_size_inch:
        stmt = stmt.where(
            EnrichedLaptopListing.screen_size_inch >= params.min_screen_size_inch
        )
    if params.max_screen_size_inch:
        stmt = stmt.where(
            EnrichedLaptopListing.screen_size_inch <= params.max_screen_size_inch
        )
    if params.panel_type:
        stmt = stmt.where(EnrichedLaptopListing.panel_type == params.panel_type)
    if params.min_refresh_rate_hz:
        stmt = stmt.where(
            EnrichedLaptopListing.refresh_rate_hz >= params.min_refresh_rate_hz
        )
    if params.max_refresh_rate_hz:
        stmt = stmt.where(
            EnrichedLaptopListing.refresh_rate_hz <= params.max_refresh_rate_hz
        )
    if params.location:
        stmt = stmt.where(EnrichedLaptopListing.location.ilike(f"%{params.location}%"))

    stmt = stmt.offset(params.skip).limit(params.limit)

    return list(db.scalars(stmt).all())


def get_enriched_gpu_listing(
    db: Session, site: str, listing_id: int
) -> EnrichedGPUListing | None:
    stmt = select(EnrichedGPUListing).where(
        EnrichedGPUListing.site == site, EnrichedGPUListing.listing_id == listing_id
    )

    return db.scalars(stmt).first()


def get_enriched_gpu_listings(
    db: Session, params: EnrichedGPUListingFilterParams
) -> list[EnrichedGPUListing]:
    stmt = select(EnrichedGPUListing)

    if params.site:
        stmt = stmt.where(EnrichedGPUListing.site == params.site)
    if params.brand:
        stmt = stmt.where(EnrichedGPUListing.brand == params.brand)
    if params.model:
        stmt = stmt.where(EnrichedGPUListing.model.ilike(f"%{params.model}%"))
    if params.min_price is not None:
        stmt = stmt.where(EnrichedGPUListing.price >= params.min_price)
    if params.max_price is not None:
        stmt = stmt.where(EnrichedGPUListing.price <= params.max_price)
    if params.min_vram_gb is not None:
        stmt = stmt.where(EnrichedGPUListing.vram_gb >= params.min_vram_gb)
    if params.max_vram_gb is not None:
        stmt = stmt.where(EnrichedGPUListing.vram_gb <= params.max_vram_gb)
    if params.iced_status is not None:
        stmt = stmt.where(EnrichedGPUListing.iced_status == params.iced_status)

    stmt = stmt.offset(params.skip).limit(params.limit)

    return list(db.scalars(stmt).all())


def get_price_history(db: Session, site: str, listing_id: int) -> list[int] | None:
    stmt = select(Listing).where(Listing.site == site, Listing.id == listing_id)

    listing = db.scalars(stmt).first()

    if listing is None:
        return None

    if listing.price_history is None:
        return []

    return list(listing.price_history)
