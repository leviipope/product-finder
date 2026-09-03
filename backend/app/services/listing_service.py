from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.listing import Listing, EnrichedLaptopListing
from app.schemas.listing import ListingFilterParams, EnrichedLaptopFilterParams

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

# Number comparison for RAM, storage size, screen size, and refresh rate is done lexicographically since they are stored as strings. 
# This may not yield accurate results for numerical comparisons. 
# Consider storing these attributes as integers or floats for proper range filtering.
def get_enriched_laptop_listings(db: Session, params: EnrichedLaptopFilterParams) -> list[EnrichedLaptopListing]:
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
    if params.min_ram:
        stmt = stmt.where(EnrichedLaptopListing.ram >= params.min_ram)
    if params.max_ram:
        stmt = stmt.where(EnrichedLaptopListing.ram <= params.max_ram)
    if params.min_storage_size:
        stmt = stmt.where(EnrichedLaptopListing.storage_size >= params.min_storage_size)
    if params.max_storage_size:
        stmt = stmt.where(EnrichedLaptopListing.storage_size <= params.max_storage_size)
    if params.storage_type:
        stmt = stmt.where(EnrichedLaptopListing.storage_type == params.storage_type)
    if params.resolution:
        stmt = stmt.where(EnrichedLaptopListing.resolution == params.resolution)
    if params.min_screen_size:
        stmt = stmt.where(EnrichedLaptopListing.screen_size >= params.min_screen_size)
    if params.max_screen_size:
        stmt = stmt.where(EnrichedLaptopListing.screen_size <= params.max_screen_size)
    if params.panel_type:
        stmt = stmt.where(EnrichedLaptopListing.panel_type == params.panel_type)
    if params.min_refresh_rate:
        stmt = stmt.where(EnrichedLaptopListing.refresh_rate >= params.min_refresh_rate)
    if params.max_refresh_rate:
        stmt = stmt.where(EnrichedLaptopListing.refresh_rate <= params.max_refresh_rate)
    if params.location:
        stmt = stmt.where(EnrichedLaptopListing.location.ilike(f"%{params.location}%"))

    stmt = stmt.offset(params.skip).limit(params.limit)

    return list(db.scalars(stmt).all())
