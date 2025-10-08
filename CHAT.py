# CHAT.py — version publique (Azure Cognitive Search + Azure OpenAI)
import os
import json
import datetime
from typing import Dict, Any, List

from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

from langchain_openai import AzureOpenAI, AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.agents import tool
from langchain.docstore.document import Document
from langchain_community.vectorstores.azuresearch import AzureSearch

# Charge les variables d'environnement (.env si présent)
load_dotenv()

# -------------------- Config Azure OpenAI --------------------
API_TYPE = os.getenv("OPENAI_API_TYPE", "azure")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AOAI_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")  # à adapter à ton déploiement
EMBED_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")  # idem

# -------------------- Config Azure Search --------------------
AZ_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  # ex: https://xxx.search.windows.net
AZ_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")            # clé admin ou query
AZ_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")        # ex: resources-manag
AZ_SEARCH_CONTENT_KEY = os.getenv("AZURE_SEARCH_CONTENT_KEY", "content")  # champ texte principal

# -------------------- Initialisation LLM & embeddings --------------------
llm = AzureOpenAI(
    azure_deployment=DEPLOYMENT,
    openai_api_key=AOAI_KEY,
    openai_api_type=API_TYPE,
    openai_api_version=AOAI_VERSION,
    azure_endpoint=AOAI_ENDPOINT,
    temperature=0.2,
)

embed_model = AzureOpenAIEmbeddings(
    azure_deployment=EMBED_DEPLOYMENT,
    openai_api_key=AOAI_KEY,
    openai_api_type=API_TYPE,
    openai_api_version=AOAI_VERSION,
    azure_endpoint=AOAI_ENDPOINT,
)

# -------------------- Initialisation du VectorStore Azure Search --------------------
# NB: on n'écrit plus d'endpoint/clé en dur.
vector_store_rm = AzureSearch(
    azure_search_endpoint=AZ_SEARCH_ENDPOINT,
    azure_search_key=AZ_SEARCH_KEY,
    index_name=AZ_SEARCH_INDEX,
    embedding_function=embed_model.embed_query,
)

def RAG_rm(query: str, k: int = 10, max_context_length: int = 4096) -> str:
    """
    Hybrid search sur Azure Search + filtrage par similarité cosine pour ne garder que le plus pertinent.
    Retourne un contexte concaténé en texte.
    """
    try:
        docs: List[Document] = vector_store_rm.hybrid_search(query, k=k)
    except Exception as e:
        # En prod tu peux logger; ici on retourne un msg clair.
        return "No relevant documents found."

    if not docs:
        return "No relevant documents found."

    context_parts: List[str] = []
    total_length = 0

    # Embedding de la requête pour filtrage (optionnel mais utile)
    query_embedding = embed_model.embed_query(query)

    for doc in docs:
        content = (doc.page_content or "").strip()
        if not content:
            continue

        # Similarité query-doc
        doc_embedding = embed_model.embed_query(content)
        similarity = float(cosine_similarity([query_embedding], [doc_embedding])[0][0])

        if similarity < 0.7:   # seuil à ajuster si besoin
            continue

        if total_length + len(content) > max_context_length:
            break

        context_parts.append(content)
        total_length += len(content)

    context = "\n\n".join(context_parts)
    return context if context else "No relevant documents found."

# -------------------- Tool de préprocessing --------------------
@tool
def preproc1(query: str) -> Dict[str, str]:
    """Produit l'input dict pour le prompt: {'query': ..., 'context': ...}"""
    context = RAG_rm(query)
    return {"query": query, "context": context}

# -------------------- Prompt --------------------
templateFR = """
Assume I am a Resource Manager at Schneider Electric. I have data about the projects my teams work on,
the human resources involved, and the organizations to which these resources belong. Can you help me find and use those informations to answer natural questions
and retrieve the most relevant details ? If the information is not available, please state that clearly and do not provide incorrect information.

Consider synonyms and related terms for better understanding. For example, "managing" can also mean "manager of", "leading", "overseeing", or "supervising".
Consider synonyms and related terms for better understanding. For example, "capacity" refers to "Current Availability of resources".
Consider synonyms and related terms for better understanding. For example, "internal resources" refers to "resources with Contract Type as internal".

Query:
{query}
Context:
{context}

Answer:
"""

prompt = PromptTemplate(
    template=templateFR,
    input_variables=["query", "context"],
)

# Chaîne équivalente à: preproc -> prompt -> llm
def _build_prompt(input_data: Dict[str, Any]) -> str:
    q = (input_data.get("query") or "").strip()
    ctx = RAG_rm(q)
    return prompt.format(query=q, context=ctx)

def execute_chain_json(input_data: Dict[str, Any]) -> str:
    """
    API stable pour app.py
    """
    final_prompt = _build_prompt(input_data)
    return llm.invoke(final_prompt)
