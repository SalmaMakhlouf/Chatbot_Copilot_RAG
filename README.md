# 🤖 Resource Management Copilot (POC)

## 🎯 Objectif
Ce projet est un **Proof of Concept (POC)** développé pour démontrer l’utilisation de l’IA générative et de la recherche augmentée (RAG) afin de **faciliter l’accès aux données de gestion de ressources**.  
L’idée principale : proposer un **Copilot** capable de répondre aux questions des managers en langage naturel, en s’appuyant sur les données stockées dans les systèmes existants.

## 🛠️ Technologies utilisées
- **LangChain** : orchestration des appels LLM et pipeline RAG  
- **Azure OpenAI (GPT-4o)** : génération de réponses  
- **Azure Cognitive Search** : recherche sémantique et hybride sur les données  
- **Streamlit** : interface utilisateur simple et interactive  
- **Python** (3.10+)  
- **Autres** : Scikit-learn (cosine similarity), Pillow, dotenv  

## ⚙️ Architecture du POC
1. **Préparation des données** : fichiers (CSV, JSON, SQL) indexés dans Azure Cognitive Search.  
2. **Recherche augmentée (RAG)** :  
   - embeddings générés via Azure OpenAI  
   - requêtes utilisateur envoyées au moteur Azure Search  
   - post-traitement des résultats (filtrage par similarité cosine).  
3. **LLM (Azure OpenAI GPT-4o)** : génère une réponse contextualisée à partir du prompt et du contexte.  
4. **Interface (Streamlit)** :  
   - affichage d’un dashboard Power BI (statique dans le POC)  
   - zone de chat interactive avec mémoire de conversation.  

![Architecture du projet](https://via.placeholder.com/900x400.png?text=Architecture+Copilot+RAG)


## 🚀 Installation
Clonez ce dépôt et installez les dépendances :

```bash
git clone https://github.com/<ton-username>/Chatbot_Copilot_RAG.git
cd Chatbot_Copilot_RAG
pip install -r requirements.txt
```
## 📊 Résultats attendus
- Réduction du temps de recherche d’information (~30 %).
- Simplification de l’accès aux données pour les managers non techniques.
- Base pour un futur Copilot intégré dans les dashboards R&D.

## 📌 Limitations
- Données utilisées ici = **factices** (les données réelles internes ne sont pas publiées).
- Le POC n’intègre que la recherche RAG ; les autres approches (SQL direct, SelfQuery) sont prévues en extension.
- Interface Streamlit volontairement simple.

## 👩‍💻 Auteur
- **Salma Makhlouf**  
  Data Scientist & Engineer spécialisée en NLP et IA générative  
  [LinkedIn](https://www.linkedin.com/in/salma-makhlouf)

## 📸 Aperçu du POC
![Copilot Screenshot](POC_vision.jpg)

