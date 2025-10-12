from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import RedirectResponse
from app.services.user_service import create_user, authenticate_user
from app.security import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)
    if not user:
        return {"error": "Identifiants invalides"}
    token = create_access_token({"sub": user['username']})
    response = RedirectResponse(url="/add_quest")
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return response