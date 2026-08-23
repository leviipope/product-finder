from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.listing import ListingFilterParams, ListingResponse
from app.services import listing_service

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.get("/", response_model=list[ListingResponse])
def read_listings(
    filters: ListingFilterParams = Depends(),
    db: Session = Depends(get_db)
):
    """
    Fetch paginated tech listings with optional price, city and product type filters.
    """
    return listing_service.get_listings(db, filters)
