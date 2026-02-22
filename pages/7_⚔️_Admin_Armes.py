"""Page Admin - Gestion des armes (Admin uniquement)."""

import streamlit as st
from auth.session import require_role, init_session_state, is_authenticated, is_admin
from database.models import UserRole
from pages.admin.weapons_management import render_weapons_management_page

# Configuration de la page
st.set_page_config(
    page_title="Admin - Armes - Albion Zerg",
    page_icon="⚔️",
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

# Vérifier le rôle
if not is_admin():
    st.error("❌ Accès refusé. Cette page est réservée aux Administrateurs.")
    st.info("👉 Contactez un administrateur si vous pensez que c'est une erreur.")
    st.stop()

# Afficher la page
render_weapons_management_page()
