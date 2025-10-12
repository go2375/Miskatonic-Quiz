from fastapi import FastAPI
from app.routes import auth, quiz

app = FastAPI()
app.include_router(auth.router)
app.include_router(quiz.router)