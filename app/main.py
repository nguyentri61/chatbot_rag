from fastapi import FastAPI
from app.api.chat import router

app = FastAPI(title="Badminton RAG Chatbot")
app.include_router(router, prefix="/api")
