import ollama
from db import get_non_enriched_ids_by_product_type
from enrichment import local_enrichment
from notifier import run_notifier
from datetime import datetime, timezone
from threading import Lock, Event
from uuid import uuid4

_cancel_event = Event()
_job_lock = Lock()
_job_status = {
    "run_id": None,
    "status": "idle",
    "started_at": None,
    "finished_at": None,
    "error": None
}

def run_local_enrichment():
    try:
        non_enriched_dict = get_non_enriched_ids_by_product_type()
        was_canceled = local_enrichment(non_enriched_dict, _cancel_event)

        if was_canceled or _cancel_event.is_set():
            _job_status["status"] = "canceled"
        else:
            run_notifier(non_enriched_dict)
            _job_status["status"] = "completed"

    except Exception as e:
        _job_status["status"] = "failed"
        _job_status["error"] = str(e)
    finally:
        _job_status["finished_at"] = datetime.now(timezone.utc).isoformat()
        _job_lock.release()
    

def get_enrichment_status():
    return _job_status.copy()

def try_start_enrichment() -> str | None:
    if not _job_lock.acquire(blocking=False):
        return None

    _cancel_event.clear()

    run_id = f"enrichment_{uuid4().hex[:8]}"
    _job_status.update(
        {
            "run_id": run_id,
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "finished_at": None,
            "error": None
        }
    )
    return run_id

def is_ollama_available() -> bool:
    try:
        ollama.list()
        return True
    except Exception:
        return False

def cancel_enrichment(run_id: str) -> bool:
    if _job_status["run_id"] != run_id:
        return False

    if _job_status["status"] != "running":
        return False

    _cancel_event.set()
    return True

