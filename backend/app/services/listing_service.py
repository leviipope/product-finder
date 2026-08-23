from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.listing import Listing
from app.schemas.listing import ListingFilterParams

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


