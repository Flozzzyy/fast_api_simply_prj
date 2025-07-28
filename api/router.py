from typing import Annotated

from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import STaskAdd, STask, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("")
async def add_task(
        name: str,
        description: str | None = None,
) -> STaskId:
    task = STaskAdd(name=name, description=description)
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks


@router.delete("/{task_id}")
async def delete_task(task_id: int) -> dict:
    success = await TaskRepository.delete_one(task_id)
    if success:
        return {"ok": True, "message": f"Задача {task_id} удалена"}
    else:
        return {"ok": False, "message": f"Задача {task_id} не найдена"}
