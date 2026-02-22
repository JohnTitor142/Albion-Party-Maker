"""
Albion Zerg Manager - Application principale
Application Streamlit pour la gestion des compositions de zerg dans Albion Online
"""

import streamlit as st
from auth.session import init_session_state, is_authenticated
from auth.login import show_login
from auth.signup import show_signup
from components.sidebar import render_sidebar, get_page_config

# Pages
from pages.dashboard import render_dashboard
from pages.compositions import render_compositions_page
from pages.activities import render_activities_page
from pages.my_activities import render_my_activities_page
from pages.roster import render_roster_page
from pages.admin.user_management import render_user_management_page
from pages.admin.weapons_management import render_weapons_management_page


# Configuration de la page
st.set_page_config(
    page_title="Albion Zerg Manager",
    page_icon="🗡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Amélioration des cartes */
    .stContainer {
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Boutons */
    .stButton button {
        border-radius: 5px;
    }
    
    /* Metriques */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Fonction principale de l'application."""
    
    # Initialiser la session
    init_session_state()
    
    # Vérifier l'authentification
    if not is_authenticated():
        render_auth_page()
    else:
        render_authenticated_app()


def render_auth_page():
    """Afficher la page d'authentification."""
    
    # Tabs pour login/signup
    tab1, tab2 = st.tabs(["🔑 Connexion", "📝 Inscription"])
    
    with tab1:
        show_login()
    
    with tab2:
        show_signup()


def render_authenticated_app():
    """Afficher l'application authentifiée."""
    
    # Afficher la sidebar et récupérer la page sélectionnée
    selected_page = render_sidebar()
    
    # Router vers la bonne page
    page_config = get_page_config(selected_page)
    
    # Header de la page
    st.markdown(f"# {page_config['icon']} {page_config['title']}")
    st.markdown("---")
    
    # Afficher la page correspondante
    try:
        if selected_page == "Dashboard":
            render_dashboard()
        
        elif selected_page == "Compositions":
            render_compositions_page()
        
        elif selected_page == "Activités":
            render_activities_page()
        
        elif selected_page == "Mes Inscriptions":
            render_my_activities_page()
        
        elif selected_page == "Rosters":
            render_roster_page()
        
        elif selected_page == "Admin - Users":
            render_user_management_page()
        
        elif selected_page == "Admin - Armes":
            render_weapons_management_page()
        
        else:
            st.error(f"❌ Page inconnue : {selected_page}")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement de la page : {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
