import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

class Config:
    # Paramètres LLM
    MODEL_NAME = "llama-3.1-8b-instant"
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    
    # Fichiers
    EXCEL_SOURCE = "CIS_RCP_export.xlsx"
    CONTEXT_FILE = "contexte.txt"
    FAISS_INDEX = "medics_index.index"
    META_DATA = "medics_meta.json"

# Connexions uniques
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL_NAME)