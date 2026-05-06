import os
import faiss
import numpy as np
from config import Config, client, embedding_model
from utils import io_file

def get_prompts():
    with open(Config.CONTEXT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    # Logique simple pour séparer les prompts
    agent_a = content.split("### AGENT_A_PROMPT ###")[1].split("### AGENT_B_PROMPT ###")[0].strip()
    agent_b = content.split("### AGENT_B_PROMPT ###")[1].strip()
    return agent_a, agent_b

def recherche_autonome(query, index, meta):
    v = np.array(embedding_model.encode([query])).astype('float32')
    _, indices = index.search(v, k=3)
    return "\n".join([meta[i]["contenu"] for i in indices[0] if i != -1])

def main():
    if not os.path.exists(Config.FAISS_INDEX):
        print("Index introuvable. Lancement de l'indexation...")
        from indexation import run_indexing
        run_indexing()

    index = faiss.read_index(Config.FAISS_INDEX)
    meta = io_file(Config.META_DATA, mode='r')
    prompt_a, prompt_b = get_prompts()

    print("Système RAG Médical prêt. (Tapez 'quitter' pour sortir)")

    while True:
        patient_query = input("\nPatient : ")

        # Condition de sortie
        if patient_query.lower() in ["quitter", "exit", "quit"]:
            print("Fin de la consultation. Au revoir !")
            break

        # Recherche autonome
        contexte_medical = recherche_autonome(patient_query, index, meta)
        
        # Historique simple pour la conversation
        messages = [
            {"role": "system", "content": prompt_b},
            {"role": "user", "content": f"Données officielles :\n{contexte_medical}\n\nQuestion patient : {patient_query}"}
        ]

        response = client.chat.completions.create(model=Config.MODEL_NAME, messages=messages)
        print("\nExpert (Agent B) :", response.choices[0].message.content)

if __name__ == "__main__":
    main()