from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.quiz_service import add_question, get_subjects, get_categories

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/add_quest", response_class=HTMLResponse)
async def add_quest_get(request: Request):
    sujets = get_subjects()
    categories = get_categories()
    return templates.TemplateResponse("add_quest.html", {"request": request, "sujets": sujets, "categories": categories})

@router.post("/add_quest")
async def add_quest_post(request: Request):
    form = await request.form()
    # Récupérer sujets, types, question, réponses et correctes
    # Validation et appel à add_question()
    return {"status": "ok"}