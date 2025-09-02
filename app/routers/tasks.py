from fastapi import APIRouter

from fastapi import Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from typing import Annotated

router = APIRouter(prefix='/tasks', tags=['tasks'])
templates = Jinja2Templates(directory="app/templates/")

class Task(BaseModel):
    id: Optional[int] = None  # Делаем id необязательным
    text: str

    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "text": "Simple message",
                    }
                ]
        }
    }

tasks_db=[Task(id=1,text='task1'),Task(id=2,text='task2')]

@router.get("/")
async def get_all_tasks(request:Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "tasks.html", {"tasks": tasks_db})



# @router.get('/')
# async def all_products(db: Annotated[AsyncSession, Depends(get_db)]):
#     products = await db.scalars(select(Product).where(Product.is_active == True, Product.stock > 0))
#     if not products:
#         return HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='There are no product'
#         )
#     return products.all()
