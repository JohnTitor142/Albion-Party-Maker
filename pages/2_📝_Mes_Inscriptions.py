"""Page Mes Inscriptions - Gestion des inscriptions utilisateur."""

import streamlit as st
from auth.session import require_auth, init_session_state, is_authenticated, get_user_id
from pages.core.my_activities import render_my_activities_page

# Configuration de la page
st.set_page_config(
    page_title="Mes Inscriptions - Albion Zerg",
    page_icon="📝",
    layout="wide"
)

# CSS pour masquer la page "app" de la sidebar
st.markdown("""
<style>
    [data-testid="stSidebarNav"] li:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialiser la session
init_session_state()

# Vérifier l'authentification
if not is_authenticated():
    st.warning("⚠️ Vous devez être connecté pour accéder à cette page.")
    st.info("👉 Retournez à la page d'accueil pour vous connecter.")
    st.stop()

# Afficher la page
render_my_activities_page()
