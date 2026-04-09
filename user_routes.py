from fastapi import APIRouter
from pydantic import BaseModel
from app.rag_pipeline import query_with_rerank
from faq_db import log_user_query, get_all_faqs

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    query = req.query
    # 1. Log query for FAQ analysis
    log_user_query(query)
    
    # 2. Get RAG Response
    try:
        response_text = query_with_rerank(query)
    except Exception as e:
        response_text = f"Sorry, I encountered an error: {str(e)}"
    
    return {"response": response_text}

@router.get("/faqs")
async def faqs_endpoint():
    faqs = get_all_faqs()
    return {"faqs": faqs}