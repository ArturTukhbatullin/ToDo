from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# # Строка подключения для SQLite
# DATABASE_URL = "sqlite:///todo.db"

# # Создаём Engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Настраиваем фабрику сеансов
# SessionLocal = sessionmaker(bind=engine)

# --------------- Асинхронное подключение к PostgreSQL -------------------------

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# Строка подключения для Postgresql
DATABASE_URL = "postgresql+asyncpg://todo_user:todo_user@localhost:5432/todo_db"

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Определяем базовый класс для моделей
class Base(DeclarativeBase): 
    pass
