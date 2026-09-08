from app.api.v1.enrichment import router as enrichment_router
from app.api.v1.listings import router as listings_router
from app.api.v1.searches import router as searches_router
from fastapi import APIRouter

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(listings_router)
api_v1_router.include_router(searches_router)
api_v1_router.include_router(enrichment_router)
