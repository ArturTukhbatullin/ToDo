from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор категории")
    name: str = Field(description="Название категории")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если есть")
    is_active: bool = Field(description="Активность категории")
    model_config = ConfigDict(from_attributes=True)

class Task(BaseModel):
    """
    Модель для ответа с данными задачи.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор задачи")
    name: str = Field(description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    priority: str= Field('Средний',description='Приорететность задачи') 
    category: str = Field(description='Категория задачи')
    category_id: int = Field(description="ID категории")
    is_active: bool = Field(description="Активность задачи")
    deadline:datetime = Field(description='Срок выполнения задачи')
    model_config = ConfigDict(from_attributes=True)