# chat_public.py — version safe (démo locale)
import os, json
from dotenv import load_dotenv
from typing import Dict, Any, List
from langchain.prompts import PromptTemplate
from langchain_openai import AzureOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

load_dotenv()

# --- Config via env (aucun secret en dur) ---
API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AOAI_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
EMBED_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")

# --- LLM & Embeddings (Azure OpenAI) ---
llm = AzureOpenAI(
    azure_deployment=DEPLOYMENT,
    openai_api_key=AOAI_KEY,
    openai_api_type=API_TYPE,
    openai_api_version=AOAI_VERSION,
    azure_endpoint=AOAI_ENDPOINT,
    temperature=0.2,
)

emb = AzureOpenAIEmbeddings(
    azure_deployment=EMBED_DEPLOYMENT,
    openai_api_key=AOAI_KEY,
    openai_api_type=API_TYPE,
    openai_api_version=AOAI_VERSION,
    azure_endpoint=AOAI_ENDPOINT,
)

# --- Petit corpus factice pour la démo publique ---
sample_rows = [
    {"type":"resource","manager":"Thierry","contract_type":"Internal","count":72},
    {"type":"resource","manager":"Chitra Sukumar","contract_type":"Internal","count":225},
    {"type":"project","name":"POC Copilot RAG","status":"Active","risk":"Low"},
]
docs: List[Document] = [
    Document(page_content=json.dumps(r, ensure_ascii=False), metadata={"source":"data/sample.json"})
    for r in sample_rows
]
vstore = FAISS.from_documents(docs, emb)

def rag_search(query: str, k: int = 5) -> str:
    """Recherche sémantique locale FAISS (démo)."""
    matches = vstore.similarity_search(query, k=k)
    return "\n".join([m.page_content for m in matches]) if matches else "No relevant documents found."

templateFR = """Assume I am a Resource Manager at Schneider Electric...
If the information is not available, say it clearly.

Query:
{query}
Context:
{context}

Answer:"""

prompt = PromptTemplate(template=templateFR, input_variables=["query","context"])

def execute_chain_json(input_data: Dict[str, Any]) -> str:
    q = input_data.get("query","").strip()
    context = rag_search(q)
    p = prompt.format(query=q, context=context)
    return llm.invoke(p)
