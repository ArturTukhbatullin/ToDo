from fastapi import FastAPI
from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.routers import tasks,welcome,categories
app = FastAPI(description="The ToDo application",version='0.0.1')

# Монтируем статические файлы
templates = Jinja2Templates(directory="app/templates/")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# welcome for '/'
@app.get("/")
async def welcome_local_root(request:Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "main.html", {"message": 'welcome_local_root'})

# welcome for 'welcome/'
app.include_router(welcome.router)
app.include_router(tasks.router)
app.include_router(categories.router)