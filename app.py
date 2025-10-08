import os
import base64
import streamlit as st
from PIL import Image

# >>> importe la version publique sécurisée
from chat_public import execute_chain_json

# --- chemins images (mets des images neutres dans ton repo ou commente-les)
powerbi_dashboard_image_path = "Dash_PowerBi.png"
copilot_path = "coopilot.png"
chat_image_path = "Schneider-Electric-logo.png"

def get_base64_image(image_path: str) -> str | None:
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def load_image_safe(image_path: str) -> Image.Image | None:
    try:
        return Image.open(image_path)
    except Exception:
        return None

def clean_response(text: str) -> str:
    """Nettoyage doux: on supprime sections Query/Context/suggestions sans couper brutalement la réponse."""
    if not text:
        return ""
    # supprime les blocs "Query:" et "Context:" s'ils apparaissent
    markers = ["\nQuery:", "\nContext:", "\nQUERY:", "\nCONTEXT:"]
    for m in markers:
        if m in text:
            text = text.split(m)[0]
    # quelques expressions indésirables
    unwanted = ["I recommend", "You could try", "suggestions:"]
    for u in unwanted:
        if u in text:
            # au lieu de couper à zéro, on retire juste la phrase à partir de ce mot
            parts = text.split(u)
            # on garde le début + on termine proprement
            text = parts[0].rstrip()
    # espaces
    return text.strip()

def main():
    st.set_page_config(layout="wide", page_title="Resource Management Copilot")

    # petit style pour le bouton
    st.markdown("""
        <style>
        .stButton button {
            background-color: #4CAF50; color: white; border: none;
            padding: 10px 20px; border-radius: 8px; font-size: 16px;
        }
        .top-right-logo { position: absolute; top: 0; right: 0; margin: 10px; }
        </style>
    """, unsafe_allow_html=True)

    # logo en haut (silencieux si absent)
    chat_image_b64 = get_base64_image(chat_image_path)
    if chat_image_b64:
        st.markdown(
            f"<img src='data:image/png;base64,{chat_image_b64}' class='top-right-logo' width='250'>",
            unsafe_allow_html=True
        )

    st.markdown("<h1 style='margin-top: 0px;'>🔗 RM Copilot</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([3.5, 1.5])

    # --- Sidebar
    with st.sidebar:
        img = load_image_safe(copilot_path)
        if img: st.image(img, width=300)
        st.markdown("### Approche IA")
        # pour l’instant, on n’active que RAG (les autres cases sont placeholders)
        use_RAG = st.checkbox("AI Model using RAG", value=True)
        st.caption("Les options SelfQuery / SQL viendront plus tard.")

    # --- Colonne Dashboard
    with col1:
        st.write("### Resource Management Dashboard")
        dash_img = load_image_safe(powerbi_dashboard_image_path)
        if dash_img:
            st.image(dash_img, use_column_width=True)
        else:
            st.info("📊 Ajoute une image de dashboard (ex: `Dash_PowerBi.png`) pour l'illustration.")

    # --- Colonne Chat
    with col2:
        st.write("### How can I help you?")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "last_question" not in st.session_state:
            st.session_state.last_question = ""

        # historique
        for msg in st.session_state.chat_history:
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Copilot:** {msg['response']}")

        text = st.text_area("Enter your question:", height=100, key="user_input_area")

        if st.button("Send"):
            if not text.strip():
                st.warning("Please enter a question.")
            elif not use_RAG:
                st.info("Enable 'AI Model using RAG' to query the knowledge base.")
            else:
                # pas de doublon immédiat
                if text.strip() == st.session_state.last_question:
                    st.info("You already asked this question.")
                else:
                    st.session_state.last_question = text.strip()
                    with st.spinner("Thinking..."):
                        raw = execute_chain_json({"query": text.strip()})
                        cleaned = clean_response(raw)
                    st.session_state.chat_history.append({"user": text.strip(), "response": cleaned})
                    # vide la zone de texte
                    st.session_state["user_input_area"] = ""

if __name__ == "__main__":
    main()
