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


@router.delete("/tasks/{id}")
def delete_task(id: int):
    """Удалить задачу по идентификатору."""
    try:
        TaskModel.delete_note_by_id(id)
        data = {"message": f"Задача с идентификатором {id} удалена"}
    except Exception as e:
        data = {"error": str(e)}

    return data
