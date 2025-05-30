from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

session_factory = sessionmaker(engine)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def __to_camel_case(s: str) -> str:
        words = s.split(' ')
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    @classmethod
    def fetch_all_tasks(cls):
        with session_factory() as session:
            tasks = session.execute(select(cls)).scalars().all()
            return [{
                "id": task.id,
                "title": cls.__to_camel_case(task.title),
                "completed": task.completed
            } for task in tasks]

    @classmethod
    def create_task(cls, title: str):
        with session_factory() as session:
            task = cls(title=title)
            session.add(task)
            session.commit()
            return task


    @classmethod
    def delete_note_by_id(cls, id: int):
        with session_factory() as session:
            task = session.get(cls, id)
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
