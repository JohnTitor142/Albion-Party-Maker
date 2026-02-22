"""
Albion Zerg Manager - Application principale
Application Streamlit pour la gestion des compositions de zerg dans Albion Online

Page d'accueil : Authentification (Login/Signup)
Les utilisateurs connectés sont automatiquement redirigés vers le Dashboard
"""

import streamlit as st
from auth.session import init_session_state, is_authenticated
from auth.login import show_login
from auth.signup import show_signup


# Configuration de la page
st.set_page_config(
    page_title="Connexion - Albion Zerg Manager",
    page_icon="🗡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour la page de login
st.markdown("""
<style>
    /* Masquer la sidebar sur la page de login */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 600px;
    }
    
    /* Boutons */
    .stButton button {
        border-radius: 5px;
        width: 100%;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding-left: 24px;
        padding-right: 24px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Fonction principale de l'application."""
    
    # Initialiser la session
    init_session_state()
    
    # Si l'utilisateur est déjà connecté, le rediriger vers le Dashboard
    if is_authenticated():
        st.switch_page("pages/1_📊_Dashboard.py")
    else:
        render_login_page()


def render_login_page():
    """Afficher la page de connexion/inscription."""
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://via.placeholder.com/150x150.png?text=🗡️", width=150)
    
    st.title("🗡️ Albion Zerg Manager")
    st.markdown("### Gérez vos compositions et activités de zerg")
    st.markdown("---")
    
    # Tabs pour login/signup
    tab1, tab2 = st.tabs(["🔑 Connexion", "📝 Inscription"])
    
    with tab1:
        st.markdown("#### Connectez-vous à votre compte")
        show_login()
    
    with tab2:
        st.markdown("#### Créer un nouveau compte")
        show_signup()
    
    # Footer
    st.markdown("---")
    st.caption("💡 Besoin d'aide ? Contactez un administrateur.")


if __name__ == "__main__":
    main()
