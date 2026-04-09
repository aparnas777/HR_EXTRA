from llama_index.core.node_parser import SemanticSplitterNodeParser
from app.embeddings import embed_model

def semantic_chunk_documents(documents):
    splitter = SemanticSplitterNodeParser(
        buffer_size=3, 
        breakpoint_percentile_threshold=95, 
        embed_model=embed_model
    )
    nodes = splitter.get_nodes_from_documents(documents)
    # chunks = [node.text for node in nodes]
    chunk_docs=[]
    for node in nodes:
        chunk_docs.append({
            "text": node.text,"metadata":node.metadata
        })
    return chunk_docs