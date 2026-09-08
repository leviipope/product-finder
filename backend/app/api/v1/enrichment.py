from app.services import enrichment_service
from fastapi import APIRouter, BackgroundTasks, HTTPException, status

router = APIRouter(prefix="/enrichment", tags=["Enrichment"])


@router.post("/local", status_code=status.HTTP_202_ACCEPTED)
def start_local_enrichment(background_tasks: BackgroundTasks):
    if not enrichment_service.is_ollama_available():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Ollama is not available. Start Ollama and try again.",
        )

    run_id = enrichment_service.try_start_enrichment()

    if run_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An enrichment job is already running.",
        )

    background_tasks.add_task(enrichment_service.run_local_enrichment)

    job_status = enrichment_service.get_enrichment_status()

    return {
        "run_id": run_id,
        "status": "started",
        "estimated_runtime": job_status["estimated_runtime"],
    }


@router.get("/local/status")
def get_local_enrichment_status():
    return enrichment_service.get_enrichment_status()


@router.post("/local/cancel", status_code=status.HTTP_202_ACCEPTED)
def cancel_local_enrichment(run_id: str):
    if enrichment_service.get_enrichment_status()["status"] != "running":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No enrichment job is currently running.",
        )

    enriched_counts = enrichment_service.cancel_enrichment(run_id)

    if enriched_counts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unknown enrichment run_id."
        )

    return {
        "run_id": run_id,
        "status": "cancellation_requested",
        "enriched_counts": enriched_counts,
    }
