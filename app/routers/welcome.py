
from fastapi import APIRouter

from fastapi import Depends, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

router = APIRouter(prefix='/welcome', tags=['welcome'])
templates = Jinja2Templates(directory="app/templates/")

@router.get("/")
async def welcome(request:Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "main.html", {"message": 'welcome'})
