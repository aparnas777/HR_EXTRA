from app.vector_db import get_query_engine,load_index
# from app.reranker import rerank_with_metadata
from app.llm import generate_answer

def query_with_rerank(query):
    # retriever = get_retriever(namespace="hr")
    # retriever = get_retriever()
    # docs = retriever.retrieve(query)
    # if not docs:
    #     return "No relevant information found."
    # docs_list=[{"metadata": {"text":d.text}} for d in docs]
    # top_docs = rerank_with_metadata(query,docs_list)
    # context="\n\n".join(top_docs)
    # return generate_answer(query,context)
    query_engine=get_query_engine(index)
    response=query_engine.query(query)
    return str(response)
