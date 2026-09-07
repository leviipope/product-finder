from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.services import enrichment_service

router = APIRouter(prefix="/enrichment", tags=["Enrichment"])

@router.post("/local", status_code=status.HTTP_202_ACCEPTED)
def start_local_enrichment(background_tasks: BackgroundTasks):
    if not enrichment_service.is_ollama_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama is not available. Start Ollama and try again."
        )

    run_id = enrichment_service.try_start_enrichment()

    if run_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An enrichment job is already running."
        )

    background_tasks.add_task(enrichment_service.run_local_enrichment)

    return {
        "run_id": run_id,
        "status": "started",
    }

@router.get("/local/status")
def get_local_enrichment_status():
    return enrichment_service.get_enrichment_status()