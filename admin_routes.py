from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from pydantic import BaseModel
from app.ingest import ingest_documents
from faq_db import get_frequent_queries, add_faq, get_all_faqs

router = APIRouter()

@router.post("/upload-doc")
async def upload_document(files: List[UploadFile] = File(...)):
    contents = []
    names = []
    
    for file in files:
        content = await file.read()
        try:
            decoded_content = content.decode("utf-8", errors="ignore")
            contents.append(decoded_content)
            names.append(file.filename)
        except Exception as e:
             raise HTTPException(status_code=400, detail=f"Error reading file {file.filename}: {str(e)}")
            
    if contents:
        # Pass to the ingestion pipeline
        try:
            ingest_documents(contents, names)
            return {"message": f"Successfully uploaded {len(files)} documents."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")
    
    return {"message": "No valid files found."}

@router.get("/frequent-queries")
async def frequent_queries_endpoint():
    # Show queries asked 2 or more times
    queries = get_frequent_queries(min_frequency=2)
    return {"queries": queries}

class FAQRequest(BaseModel):
    question: str
    answer: str
    source: str = 'admin'

@router.post("/faq")
async def create_faq(req: FAQRequest):
    success = add_faq(req.question, req.answer, source=req.source)
    if success:
        return {"message": "FAQ added successfully"}
    else:
        raise HTTPException(status_code=400, detail="This FAQ already exists")