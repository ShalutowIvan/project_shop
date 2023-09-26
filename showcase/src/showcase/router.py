from fastapi import APIRouter, Depends, HTTPException, Request, Response

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import insert, select

from database import db

from .models import *


router = APIRouter(
    prefix="/home",
    tags=["Showcase"]
)


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):    
    org = db.query(organization).all()[0]#список возвращается по умолчанию 
    
    print(f"Название {org.name_org}")


    context = {
    "request": request,
    "a_id": 777,

    }
    return templates.TemplateResponse("showcase/test2.html", context)



# async

