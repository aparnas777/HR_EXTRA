import os
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.pinecone import PineconeVectorStore
from app.embeddings import embed_model
from llama_index.core.postprocessor import SentenceTransformerRerank

# --- Environment Variables ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX", "rag-getting-started")




# --- Initialize Pinecone & Embedding ---
pc = Pinecone(api_key=PINECONE_API_KEY)
reranker = SentenceTransformerRerank(
    model="BAAI/bge-reranker-base",
    top_n=3
)

def get_vector_store(namespace="hr"):
    pinecone_index= pc.Index(INDEX_NAME)
    return PineconeVectorStore(pinecone_index,namespace=namespace)

def load_index(namespace="hr"):
    vector_Store = get_vector_store(namespace)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store,
            storage_context=storage_context,
            embed_model=embed_model)


# Upload function
def upload_documents(documents,namespace="hr"):
    # nodes = semantic_chunk_documents(documents)
    vector_store = get_vector_store(namespace)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model, show_progress=True
    )
    return index

def get_query_engine(index):
    return index.as_query_engine(
        similarity_top_k=10,
        node_postprocessors=[reranker]
    )


# # Retriever instance
# def get_retriever(namespace="hr",top_k=5):
#     # vector_store = get_vector_store(namespace)
#     # return vector_store.as_retriever(similarity_top_k=top_k)
#     return index.as_retriever(similarity_top_k=top_k)


# # --- Helper: Infer Policy Type from Filename ---
# def infer_policy_type(filename):
#     filename = filename.lower()
#     if "hr" in filename:
#         return "HR"
#     elif "travel" in filename:
#         return "Travel"
#     elif "it" in filename:
#         return "IT"
#     else:
#         return "General"


# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def infer_policy_type_from_text(text):
#     prompt = f"""
#     Classify the following document into a policy type (HR, Travel, IT, Finance, or General):
    
#     Document:
#     {text}
    
#     Respond with only the policy type.
#     """
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )
#     policy_type = response.choices[0].message.content.strip()
#     return policy_type


# # --- Retrieve Query ---
# def query_documents(index, query_text, policy_type=None, top_k=5):
#     filters = None
#     if policy_type:
#         from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
#         filters = MetadataFilters(
#             filters=[ExactMatchFilter(key="policy_type", value=policy_type)]
#         )

#     query_engine = index.as_query_engine(
#         similarity_top_k=top_k,
#         filters=filters
#     )

#     response = query_engine.query(query_text)
#     return response


# import os
# from llama_index.core import VectorStoreIndex
# from llama_index.vector_stores.faiss import FaissVectorStore
# from llama_index.embeddings.openai import OpenAIEmbedding
# import faiss

# dimension = 1536
# faiss_index=faiss.IndexFlatL2(dimension)

# embed_model=OpenAIEmbedding(model="text-embedding-3-large")

# index=None
# def upload_documents(documnets):
#     global index
#     vector_store=FaissVectorStore(faiss_index)
#     index=VectorStoreIndex.from_documents(documnets, vector_store=vector_store,embed_model=embed_model,show_progress=True)
# def get_retriever(top_k=5):
#     returnindex.as_query_engine(similarity_top_k=top_k)


