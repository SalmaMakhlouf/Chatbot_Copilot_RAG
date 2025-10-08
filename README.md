# Chatbot_Copilot_RAG
Chatbot intelligent basé sur LLM et RAG (LangChain, Azure) pour automatiser l’accès aux dashboards R&amp;D.
# Chatbot Copilot RAG

## 🎯 Objectif
Développer un chatbot intelligent basé sur LLM et RAG (LangChain, FAISS, Azure) pour automatiser l’accès aux dashboards R&D et faciliter la prise de décision.

## 🛠️ Technologies utilisées
- Python 3.10+
- LangChain
- Azure Cognitive Services / OpenAI
- Streamlit (interface utilisateur)

## ⚙️ Architecture
1. **Chargement des données** (CSV, JSON, SQL)
2. **Vectorisation** avec embeddings (Azure OpenAI / Sentence Transformers)
3. **Recherche** via FAISS
4. **LLM** (GPT-3.5/4) pour générer des réponses
5. **Interface** avec Streamlit

![Architecture du projet](https://via.placeholder.com/800x400.png?text=Schema+Chatbot+RAG)

## 🚀 Installation
Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/SalmaMakhlouf/Chatbot_Copilot_RAG.git
cd Chatbot_Copilot_RAG
pip install -r requirements.txt
