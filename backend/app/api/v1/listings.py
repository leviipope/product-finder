from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.listing import ListingFilterParams, ListingResponse, EnrichedLaptopFilterParams, EnrichedLaptopListingResponse
from app.services import listing_service

router = APIRouter(prefix="/listings", tags=["Listings"])

@router.get("/non_enriched", response_model=list[ListingResponse])
def read_listings(
    filters: ListingFilterParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated listings based on user search parameters.

    - **city**: Filter by location string (ILIKE)
    - **min_price / max_price**: Range filtering in HUF
    - **skip / limit**: Offset pagination controls
    """
    return listing_service.get_listings(db, filters)

@router.get("/", response_model=list[EnrichedLaptopListingResponse])
def read_enriched_laptop_listings(
    filters: EnrichedLaptopFilterParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated enriched laptop listings based on user search parameters.

    - **site**: Filter by site
    - **brand**: Filter by enriched brand
    - **model**: Filter by enriched model
    - **title**: Filter by title (ILIKE)
    - **min_price / max_price**: Range filtering in HUF
    - **iced_status**: Filter by iced status
    - **cpu_brand**: Filter by CPU brand
    - **cpu_model**: Filter by CPU model
    - **gpu_brand**: Filter by GPU brand
    - **gpu_model**: Filter by GPU model
    - **gpu_type**: Filter by GPU type
    - **min_ram / max_ram**: Range filtering for RAM size
    - **min_storage_size / max_storage_size**: Range filtering for storage size
    - **storage_type**: Filter by storage type
    - **resolution**: Filter by resolution
    - **min_screen_size / max_screen_size**: Range filtering for screen size
    - **panel_type**: Filter by panel type
    - **min_refresh_rate / max_refresh_rate**: Range filtering for refresh rate
    - **location**: Filter by location (ILIKE)
    - **skip / limit**: Offset pagination controls
    """
    return listing_service.get_enriched_laptop_listings(db, filters)