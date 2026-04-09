from llama_index.core import Document
from app.chunking import semantic_chunk_documents
from app.vector_db import upload_documents


def ingest_documents(file_contents,file_names):
    documents=[]
    for content , name in zip(file_contents,file_names):
        documents.append(Document(text=content,metadata={"doc_name":name}))
    chunks= semantic_chunk_documents(documents)
    chunk_docs=[Document(text=chunk) for chunk in chunks]
    upload_documents(chunk_docs)
    # upload_documents(chunk_docs,namespace=hr)