"""Composant sidebar avec navigation."""

import streamlit as st
from streamlit_option_menu import option_menu
from auth.session import (
    is_authenticated, get_username, get_user_role,
    is_admin, is_shotcaller, clear_session
)
from database.models import UserRole


def render_sidebar() -> str:
    """
    Afficher la sidebar avec navigation.
    
    Returns:
        Page sélectionnée
    """
    with st.sidebar:
        st.title("🗡️ Albion Zerg")
        
        if is_authenticated():
            # Infos utilisateur
            st.markdown(f"**{get_username()}**")
            role_emoji = {
                "admin": "👑",
                "shotcaller": "📣",
                "user": "⚔️"
            }
            role = get_user_role()
            st.caption(f"{role_emoji.get(role, '⚔️')} {role.title()}")
            st.markdown("---")
            
            # Menu de navigation
            menu_options = ["Dashboard"]
            menu_icons = ["house"]
            
            # Options selon le rôle
            if is_shotcaller():
                menu_options.extend(["Compositions", "Activités"])
                menu_icons.extend(["puzzle", "calendar"])
            
            # Options pour tous les users
            menu_options.extend(["Mes Inscriptions", "Rosters"])
            menu_icons.extend(["pencil", "people"])
            
            # Options admin
            if is_admin():
                menu_options.extend(["Admin - Users", "Admin - Armes"])
                menu_icons.extend(["person-gear", "tools"])
            
            selected = option_menu(
                menu_title="Navigation",
                options=menu_options,
                icons=menu_icons,
                default_index=0,
                styles={
                    "container": {"padding": "0!important"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"},
                }
            )
            
            st.markdown("---")
            
            # Bouton déconnexion
            if st.button("🚪 Déconnexion", use_container_width=True):
                clear_session()
                st.rerun()
            
            return selected
        
        else:
            st.info("👋 Bienvenue !")
            return "Login"


def get_page_config(page_name: str) -> dict:
    """
    Obtenir la configuration d'une page.
    
    Args:
        page_name: Nom de la page
        
    Returns:
        Dictionnaire de configuration
    """
    configs = {
        "Dashboard": {
            "title": "📊 Tableau de Bord",
            "icon": "📊"
        },
        "Compositions": {
            "title": "🧩 Gestion des Compositions",
            "icon": "🧩"
        },
        "Activités": {
            "title": "📅 Gestion des Activités",
            "icon": "📅"
        },
        "Mes Inscriptions": {
            "title": "📝 Mes Inscriptions",
            "icon": "📝"
        },
        "Rosters": {
            "title": "👥 Rosters",
            "icon": "👥"
        },
        "Admin - Users": {
            "title": "👥 Gestion des Utilisateurs",
            "icon": "👥"
        },
        "Admin - Armes": {
            "title": "⚔️ Gestion des Armes",
            "icon": "⚔️"
        }
    }
    
    return configs.get(page_name, {"title": page_name, "icon": "📄"})
