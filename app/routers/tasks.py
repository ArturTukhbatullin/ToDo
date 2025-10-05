from fastapi import APIRouter

from fastapi import Depends, status, HTTPException,Form
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse,RedirectResponse
from urllib.parse import quote

from app.models.tasks import Task as Task_models
from app.schemas import Task as Task_schemes
from app.models.categories import Category as Category_models

from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db

from sqlalchemy import select,insert,desc,func



router = APIRouter(prefix='/tasks', tags=['tasks'])
templates = Jinja2Templates(directory="app/templates/")

from datetime import datetime,date,timedelta

@router.get("/")
async def get_all_tasks(request:Request,db: AsyncSession = Depends(get_async_db))-> HTMLResponse:
    tasks_db = await db.scalars(select(Task_models).where(Task_models.is_active==True))
    tasks_db = tasks_db.all()
    categories_db = await db.scalars(select(Category_models))
    categories_db = categories_db.all()
    return templates.TemplateResponse(request, "tasks.html", {"tasks": tasks_db,'categories':categories_db})

# Форма для создания задачи: get
@router.get("/create_task")
async def create_task(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request,"create_task.html", {"tasks": []})

# Форма для создания задачи: post
@router.post("/create_task", status_code=status.HTTP_201_CREATED)
async def create_task(request: Request,\
                    name:str=Form(...),\
                    description:str=Form(...),\
                    priority:str=Form(...),\
                    category:str=Form(...),\
                    is_active:bool=True,\
                    deadline:datetime=Form(...),
                    db: AsyncSession = Depends(get_async_db)
                    )  -> HTMLResponse:
    
    #задачи
    tasks_db = await db.scalars(select(Task_models))
    tasks_db = tasks_db.all()
    id=len(tasks_db)+1

    #категории
    if category=="":
        category='main'
    category_id_last = await db.scalars(select(Category_models).where(Category_models.name==category).order_by(desc(Category_models.id)))
    category_id_all = await db.scalars(select(Category_models).order_by(desc(Category_models.id)))
    category_id_last=category_id_last.first()
    if category_id_last is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        # category_id = category_id_all.id + 1 # создаю новую категорию
    else:
        category_id = category_id_last.id

    new_task=Task_schemes(id=id,\
                        name=name,\
                        category=category,\
                        description=description,\
                        is_active=is_active,\
                        priority=priority,\
                        category_id=category_id,\
                        deadline=deadline
                        )

    await db.execute(insert(Task_models).values(id=new_task.id,\
                        name=new_task.name,\
                        description=new_task.description,\
                        priority=new_task.priority,\
                        is_active=new_task.is_active,\
                        deadline=new_task.deadline,\
                        category_id=new_task.category_id,\
                        created_at=date.today()
                    )
                    )
    
    await db.commit()

    # Перенаправляем с сообщением об успехе
    message = "Задача успешно создана!"
    return RedirectResponse(
        url=f"/tasks/create_task/?message={quote(message)}&type=success", 
        status_code=303
    )


# пока неправильно работает
@router.get("/{id}")
async def get_tasks_info(id:int,db: AsyncSession = Depends(get_async_db)):
    tasks_db = await db.scalar(select(Task_models).where(Task_models.id==id))
    category_db = await db.scalar(select(Category_models).where(Category_models.id==tasks_db.category_id))
    # tasks_db = tasks_db.all()
    # return tasks_db
    return {
        "id": tasks_db.id,
        "name": tasks_db.name,
        "description": tasks_db.description,
        "category_id": tasks_db.category_id,
        "priority": tasks_db.priority,
        "is_active": tasks_db.is_active,
        "category":category_db.name,
        "deadline": tasks_db.deadline.isoformat() if tasks_db.deadline else None
    }

@router.delete("/delete/{id}")
async def delete_task(request:Request,id:int,db: AsyncSession = Depends(get_async_db)):
    tasks_db = await db.scalar(select(Task_models).where(Task_models.id==id))
    tasks_db.is_active=False
    await db.commit()

    message = "Задача успешно создана!"
    return RedirectResponse(
        url=f"/tasks/", 
        status_code=303
    )


@router.put("/edit/{id}")
async def edit_task(request:Request,id:int,update_task: Task_schemes,db: AsyncSession = Depends(get_async_db)):
    tasks_db = await db.scalar(select(Task_models).where(Task_models.id==id))

    # # Обновляем поля
    # if 'name' in update_task:
    #     tasks_db.name = update_task['name']
    # if 'description' in update_task:
    #     tasks_db.description = update_task['description']
    # if 'category_id' in update_task:
    #     tasks_db.category_id = update_task['category_id']
    # if 'priority' in update_task:
    #     tasks_db.priority = update_task['priority']

    # print(update_task)
    tasks_db.name=update_task.name
    tasks_db.description=update_task.description
    tasks_db.priority=update_task.priority

    await db.commit()

    return {"status":"done"}