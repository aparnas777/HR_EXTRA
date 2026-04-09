from dotenv import load_dotenv


from llama_index.embeddings.openai import OpenAIEmbedding
embed_model=OpenAIEmbedding(model="text-embedding-3-large")


# # Load API keys from .env
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=OPENAI_API_KEY)

# def embed_query(text, retries=3):
#     if not text:
#         return []
#     for i in range(retries):
#         try:
#             response = client.embeddings.create(
#             model="text-embedding-3-large",
#             input=[text]
#         )
#             return response.data[0].embedding  

#         except Exception:
#             print(f"Embedding attempt {i + 1} failed: {e}")
#             time.sleep(2)
#     raise Exception("Embedding failed after multiple retries")