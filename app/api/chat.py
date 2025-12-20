from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from vector_store.vector_store import search
from app.rag.generator import generate_answer

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    search_results = search(req.message, top_k=5)
    # Extract text from search results
    contexts = [result["text"] for result in search_results]
    answer = generate_answer(req.message, contexts)
    return ChatResponse(answer=answer)
