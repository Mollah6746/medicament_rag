import pandas as pd
import faiss
import numpy as np
from config import Config, embedding_model
from utils import io_file
from tqdm import tqdm

def run_indexing():
    print(f"Lecture de {Config.EXCEL_SOURCE}...")
    df = pd.read_excel(Config.EXCEL_SOURCE)
    
    docs = []
    print("Extraction des données...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        
        nom = str(row.get("denominat", "Inconnu"))  
        indic = str(row.get("indications", "N/A"))  
        poso = str(row.get("posologie", "N/A"))     
        contre_inc = str(row.get("contre_indications", "N/A"))
        effets = str(row.get("effets_indesirables", "N/A"))    
        prescr = str(row.get("conditions_prescription", "N/A")) 
        
        # Construction du texte complet pour l'index vectoriel
        texte_complet = (
            f"Médicament: {nom}. \n"
            f"Indications: {indic}. \n"
            f"Contre-indications: {contre_inc}. \n"
            f"Posologie: {poso}. \n"
            f"Effets indésirables: {effets}. \n"
            f"Conditions de prescription: {prescr}."
        )
        docs.append({"contenu": texte_complet, "nom": nom})

    print("Création de l'index vectoriel...")
    embeddings = embedding_model.encode([d["contenu"] for d in docs])
    embeddings = np.array(embeddings).astype('float32')

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Sauvegarde indempotente
    faiss.write_index(index, Config.FAISS_INDEX)
    io_file(Config.META_DATA, mode='w', data=docs)
    print("Indexation terminée avec succès.")

if __name__ == "__main__":
    run_indexing()