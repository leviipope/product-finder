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
    Fetch paginated listings based on user search parameters.

    - **city**: Filter by location string (ILIKE)
    - **min_price / max_price**: Range filtering in HUF
    - **skip / limit**: Offset pagination controls
    """
    return listing_service.get_listings(db, filters)
