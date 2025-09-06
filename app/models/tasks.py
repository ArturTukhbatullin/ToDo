from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column, relationship
from datetime import datetime,timedelta,date
from sqlalchemy import ForeignKey

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(50), nullable=False)
    description : Mapped[str] = mapped_column(String(500), default="")
    # category : Mapped[str] = mapped_column(String(20),default="main")
    priority : Mapped[str] = mapped_column(String(20),default="Средний")
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)
    deadline : Mapped[DateTime] = mapped_column(DateTime,default=date.today()+timedelta(days=365))
    created_at : Mapped[DateTime] = mapped_column(DateTime, default=date.today())

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="tasks")