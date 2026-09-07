from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.listing import EnrichedGPUListingFilterParams, EnrichedGPUListingBrowseResponse, EnrichedGPUListingResponse, EnrichedLaptopListingBrowseResponse, ListingFilterParams, ListingResponse, EnrichedLaptopFilterParams, EnrichedLaptopListingResponse
from app.services import listing_service

router = APIRouter(prefix="/listings", tags=["Listings"])

@router.get("/non_enriched", response_model=list[ListingResponse])
def read_listings(
    filters: ListingFilterParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated non-enriched laptop listings based on user search parameters.

    - **city**: Filter by location string (ILIKE)
    - **min_price / max_price**: Range filtering in HUF
    - **skip / limit**: Offset pagination controls
    """
    return listing_service.get_listings(db, filters)

@router.get("/laptops/{site}/{listing_id}", response_model=EnrichedLaptopListingResponse)
def read_enriched_laptop_listing(
    site: str,
    listing_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch a single enriched laptop listing by site and listing ID.

    - **site**: The site identifier for the listing
    - **listing_id**: The unique ID of the listing
    """
    listing = listing_service.get_enriched_laptop_listing(db, site, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/laptops", response_model=list[EnrichedLaptopListingBrowseResponse])
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

@router.get("/gpus/{site}/{listing_id}", response_model=EnrichedGPUListingResponse)
def read_enriched_gpu_listing(
    site: str,
    listing_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch a single enriched GPU listing by site and listing ID.

    - **site**: The site identifier for the listing
    - **listing_id**: The unique ID of the listing
    """
    listing = listing_service.get_enriched_gpu_listing(db, site, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

@router.get("/gpus", response_model=list[EnrichedGPUListingBrowseResponse])
def read_enriched_gpu_listings(
    filters: EnrichedGPUListingFilterParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated enriched GPU listings based on user search parameters.

    - **site**: Filter by site
    - **brand**: Filter by enriched brand
    - **model**: Filter by enriched model
    - **min_price / max_price**: Range filtering in HUF
    - **min_vram / max_vram**: Range filtering for VRAM size
    - **iced_status**: Filter by iced status
    - **skip / limit**: Offset pagination controls
    """
    return listing_service.get_enriched_gpu_listings(db, filters)

@router.get("{site}/{listing_id}/price_history", response_model=list[int])
def read_price_history(
    site: str,
    listing_id: int,
    db: Session = Depends(get_db)
):
    """
    Fetch the price history of a specific listing.

    - **site**: The site identifier for the listing
    - **listing_id**: The unique ID of the listing
    """
    price_history = listing_service.get_price_history(db, site, listing_id)
    if price_history is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return price_history