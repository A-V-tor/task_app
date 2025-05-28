from fastapi import APIRouter
from schemas import Task
from database import Task as TaskModel


router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get("/tasks", response_model=list[Task])
def fetch_tasks():
    """Получить список всех задач."""

    data = TaskModel.fetch_all_tasks()

    return data


@router.post("/tasks")
def create_task(task: Task):
    """Создать новую задачу."""
    TaskModel.create_task(task.title)
    data = {"message": f"Новая задача {task.title} создана"}

    return data