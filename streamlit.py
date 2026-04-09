import streamlit as st
from app.ingest import ingest_documents
from app.rag_pipeline import query_with_rerank

st.set_page_config(page_title="HR Chatbot", layout="wide")

st.title("HR Chatbot")

# --- Session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Upload Section ---
with st.sidebar:
    st.header("Upload Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload policy documents",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Upload"):
        contents=[]
        names=[]

        for f in uploaded_files:
            content = f.read().decode("utf-8", errors="ignore")
            contents.append(content)
            names.append(file.name)


        ingest_documents(contents,names)
        st.success("Documents uploaded!")

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat Input ---
query = st.text_input("Ask about policies...")

if st.button("Ask"):
    if query:
        response = query_with_rerank(query)
        st.write(response)
