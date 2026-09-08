from app.models.search import Search
from app.schemas.search import SearchCreate, SearchFilterParams
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_searches(db: Session, params: SearchFilterParams) -> list[Search]:
    stmt = select(Search)

    stmt = stmt.offset(params.skip).limit(params.limit)

    return list(db.scalars(stmt).all())


def create_search(db: Session, search_data: SearchCreate) -> Search:
    new_search = Search(
        email=search_data.email,
        search_name=search_data.search_name,
        category=search_data.category,
        filters=search_data.filters,
        is_active=True,
    )
    db.add(new_search)
    db.commit()
    db.refresh(new_search)
    return new_search


def delete_search(db: Session, search_id: int) -> None:
    search = db.get(Search, search_id)
    if search:
        db.delete(search)
        db.commit()


def activate_search(db: Session, search_id: int) -> None:
    search = db.get(Search, search_id)
    if search:
        search.is_active = True
        db.commit()


def deactivate_search(db: Session, search_id: int) -> None:
    search = db.get(Search, search_id)
    if search:
        search.is_active = False
        db.commit()
