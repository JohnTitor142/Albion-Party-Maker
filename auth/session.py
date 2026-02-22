"""Gestion des sessions utilisateur avec Streamlit."""

import streamlit as st
from typing import Optional, Dict, Any
from database.models import UserRole


def init_session_state():
    """Initialiser l'état de session Streamlit."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    
    if "username" not in st.session_state:
        st.session_state.username = None
    
    if "email" not in st.session_state:
        st.session_state.email = None


def set_user_session(user_data: Dict[str, Any], profile_data: Dict[str, Any]):
    """
    Définir les données utilisateur dans la session.
    
    Args:
        user_data: Données de auth.users
        profile_data: Données de users_profiles
    """
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.user_id = user_data.get("id")
    st.session_state.email = user_data.get("email")
    
    if profile_data:
        st.session_state.user_role = profile_data.get("role")
        st.session_state.username = profile_data.get("username")
    else:
        st.session_state.user_role = None
        st.session_state.username = None


def clear_session():
    """Effacer toutes les données de session."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.user_id = None
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.email = None


def is_authenticated() -> bool:
    """Vérifier si l'utilisateur est authentifié."""
    return st.session_state.get("authenticated", False)


def get_user_id() -> Optional[str]:
    """Récupérer l'ID de l'utilisateur connecté."""
    return st.session_state.get("user_id")


def get_user_role() -> Optional[str]:
    """Récupérer le rôle de l'utilisateur connecté."""
    return st.session_state.get("user_role")


def get_username() -> Optional[str]:
    """Récupérer le nom d'utilisateur connecté."""
    return st.session_state.get("username")


def get_email() -> Optional[str]:
    """Récupérer l'email de l'utilisateur connecté."""
    return st.session_state.get("email")


def is_admin() -> bool:
    """Vérifier si l'utilisateur est admin."""
    return get_user_role() == UserRole.ADMIN.value


def is_shotcaller() -> bool:
    """Vérifier si l'utilisateur est shotcaller."""
    role = get_user_role()
    return role in [UserRole.SHOTCALLER.value, UserRole.ADMIN.value]


def is_user() -> bool:
    """Vérifier si l'utilisateur a au moins le rôle user."""
    return get_user_role() is not None


def require_auth():
    """Forcer l'authentification ou rediriger."""
    if not is_authenticated():
        st.warning("⚠️ Vous devez être connecté pour accéder à cette page.")
        st.stop()


def require_role(required_role: UserRole):
    """
    Forcer un rôle minimum ou bloquer l'accès.
    
    Args:
        required_role: Rôle requis (UserRole enum)
    """
    require_auth()
    
    current_role = get_user_role()
    
    role_hierarchy = {
        UserRole.USER.value: 1,
        UserRole.SHOTCALLER.value: 2,
        UserRole.ADMIN.value: 3
    }
    
    current_level = role_hierarchy.get(current_role, 0)
    required_level = role_hierarchy.get(required_role.value, 999)
    
    if current_level < required_level:
        st.error(f"❌ Accès refusé. Rôle requis : {required_role.value}")
        st.stop()
