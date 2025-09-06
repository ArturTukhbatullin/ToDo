from fastapi import APIRouter

from fastapi import Depends, status, HTTPException,Form
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse,RedirectResponse
from urllib.parse import quote

from sqlalchemy.ext.asyncio import AsyncSession
from app.db_depends import get_async_db

from app.schemas import Category as Category_schemes
from app.models.categories import Category as Category_models

from sqlalchemy import select,insert,desc

router = APIRouter(prefix='/categories', tags=['categories'])
templates = Jinja2Templates(directory="app/templates/")

# Форма для создания категории: get
@router.get("/create_category")
async def create_category(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request,"create_category.html", {"category": []})


# todo
# Форма для создания категории: post
@router.post("/create_category", status_code=status.HTTP_201_CREATED)
async def create_category(request: Request,\
                          name : str =Form(...),\
                    db: AsyncSession = Depends(get_async_db))  :#-> HTMLResponse:
    
    #категории
    if name=="":
        name='main'
    category_id_last = await db.scalars(select(Category_models).where(Category_models.name==name).order_by(desc(Category_models.id)))
    category_id_all = await db.scalars(select(Category_models).order_by(desc(Category_models.id)))
    category_id_last=category_id_last.first()
    category_id_all=category_id_all.first()

    if category_id_last is None:
        id = category_id_all.id + 1
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category allready exist")


    new_category = Category_schemes(id=id,\
                                    name=name,
                                    is_active=True)
    
    await db.execute(insert(Category_models).values(
                        id = new_category.id,\
                        name = new_category.name,\
                        is_active = new_category.is_active
                    )
    )

    await db.commit()
    
    # Перенаправляем с сообщением об успехе
    message = "Категория успешно создана!"
    return RedirectResponse(
        url=f"/categories/create_category/?message={quote(message)}&type=success", 
        status_code=303
    )