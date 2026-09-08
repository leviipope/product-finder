from typing import Annotated

from app.database import get_db
from app.schemas.search import SearchCreate, SearchFilterParams, SearchResponse
from app.services import search_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/searches", tags=["Searches"])


@router.get("/", response_model=list[SearchResponse])
def read_searches(
    filters: Annotated[SearchFilterParams, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    """
    Fetch paginated searches based on user search parameters.

    - **skip / limit**: Offset pagination controls
    """
    return search_service.get_searches(db, filters)


@router.post("/", response_model=SearchResponse)
def create_search(search_data: SearchCreate, db: Annotated[Session, Depends(get_db)]):
    """
    Create a new search entry.

    - **email**: User's email address
    - **search_name**: Name of the search
    - **category**: Category of the search
    - **filters**: Dictionary of filters for the search
    """
    return search_service.create_search(db, search_data)


@router.delete("/{search_id}", status_code=204)
def delete_search(search_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Delete a search entry by its ID.

    - **search_id**: The ID of the search to delete
    """
    search_service.delete_search(db, search_id)


@router.patch("/{search_id}/activate", status_code=204)
def activate_search(search_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Activate a search entry by its ID.

    - **search_id**: The ID of the search to activate
    """
    search_service.activate_search(db, search_id)


@router.patch("/{search_id}/deactivate", status_code=204)
def deactivate_search(search_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Deactivate a search entry by its ID.

    - **search_id**: The ID of the search to deactivate
    """
    search_service.deactivate_search(db, search_id)
