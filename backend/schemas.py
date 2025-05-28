from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int|None = Field(None, readOnly=True)
    title: str
    completed: bool = False
