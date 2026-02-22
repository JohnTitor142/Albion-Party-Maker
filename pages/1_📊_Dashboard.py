"""Page Dashboard - Tableau de bord."""

import streamlit as st
from auth.session import require_auth, init_session_state, is_authenticated
from pages.core.dashboard import render_dashboard

# Configuration de la page
st.set_page_config(
    page_title="Dashboard - Albion Zerg",
    page_icon="📊",
    layout="wide"
)

# CSS pour masquer la page "app" de la sidebar
st.markdown("""
<style>
    /* Masquer la page d'accueil "app" dans la sidebar */
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

# Afficher le dashboard
render_dashboard()
