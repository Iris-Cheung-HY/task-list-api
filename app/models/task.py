from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True, default=None)

    def to_dict(self):
        task_as_dict={}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        if self.completed_at:
            task_as_dict["is_complete"] = True
        elif not self.completed_at or self.completed_at == None:
            task_as_dict["is_complete"] = False
        return task_as_dict
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"],
                    completed_at=None)
        
        return new_task
