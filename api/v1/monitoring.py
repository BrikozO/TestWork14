from celery.result import AsyncResult
from fastapi import APIRouter

router = APIRouter(prefix="/monitoring")

@router.get("/{task_id}")
async def get_task(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.ready():  # If the task is done
        return {"task_id": task_id, "status": "completed", "result": task_result.result}
    elif task_result.failed():  # If the task failed
        return {"task_id": task_id, "status": "failed"}
    else:  # If the task is still in progress
        return {"task_id": task_id, "status": "in progress"}