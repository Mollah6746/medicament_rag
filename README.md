Système RAG Médical Multi-Agents

Projet Mastère Data & IA - HETIC

Ce projet implémente une architecture de Retrieval-Augmented Generation (RAG) permettant d'interroger une base de données de 15 649 médicaments. Le système utilise deux agents spécialisés pour fournir des conseils pharmacologiques sécurisés basés sur les notices officielles de l'ANSM.

Choix Techniques & Architecture
L'architecture a été pensée pour être modulaire et indempotente :

Logiciel de base : Python avec une approche "Clean Code" pour séparer la logique de la configuration.

Moteur RAG : Utilisation de FAISS (Facebook AI Similarity Search) pour une recherche sémantique ultra-rapide dans l'index vectoriel.

Modèle d'Embedding : all-MiniLM-L6-v2 pour transformer les notices textuelles en vecteurs de 384 dimensions.

LLM : Llama-3.1-8b via l'API Groq, choisi pour sa vitesse et ses performances en raisonnement médical.

Multi-Agents :

Agent A : Interface patient pour la récolte des symptômes.

Agent B : Expert pharmacologue analysant les notices (posologie, contre-indications, effets secondaires).

Structure du Projet
rag.py : Orchestrateur principal et interface de conversation continue.

indexation.py : Script gérant l'extraction de l'Excel (62 Mo) et la génération de l'index vectoriel.

config.py : Centralisation de la connexion unique au provider et des paramètres globaux.

contexte.txt : Stockage externe des prompts système pour faciliter la maintenance sans toucher au code.

.env : Gestion sécurisée des clés API (exclu du commit via .gitignore).

Installation et Lancement
1. Prérequis
Assurez-vous d'avoir Python installé, puis installez les dépendances :

Bash
pip install -r requirements.txt
2. Configuration
Créez un fichier .env à la racine du projet :

Plaintext
GROQ_API_KEY=votre_cle_api_ici
Note : Le fichier Excel CIS_RCP_export.xlsx doit être présent à la racine.

3. Lancement
Il suffit de lancer le script principal :

Bash
python rag.py
Fonctionnement automatique : Si l'index vectoriel est absent, le système lance automatiquement indexation.py pour traiter les 15 649 lignes de l'Excel avant de démarrer la conversation.

Utilisation
Posez vos questions sur des symptômes ou des médicaments précis (ex: "Quels sont les effets secondaires de l'Abacavir ?").

L'Agent B structurera sa réponse avec : Dénomination, Posologie, Effets secondaires et Conditions de prescription.

Tapez 'quitter' pour fermer la session.

Pourquoi ce projet est robuste ?
Sécurité : Les clés API et les données volumineuses sont protégées par le .gitignore.

Persistance : Une fois l'index généré, le chargement est instantané au prochain démarrage.

Extensibilité : Modifier les instructions des agents se fait simplement dans le fichier contexte.txt