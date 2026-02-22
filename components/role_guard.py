"""Guard de vérification des permissions."""

import streamlit as st
from functools import wraps
from database.models import UserRole
from auth.session import require_auth, require_role


def require_authentication(func):
    """
    Décorateur pour forcer l'authentification.
    
    Usage:
        @require_authentication
        def my_page():
            ...
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        require_auth()
        return func(*args, **kwargs)
    return wrapper


def require_role_decorator(role: UserRole):
    """
    Décorateur pour forcer un rôle minimum.
    
    Usage:
        @require_role_decorator(UserRole.SHOTCALLER)
        def shotcaller_page():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            require_role(role)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def show_permission_error(message: str = "Vous n'avez pas les permissions nécessaires."):
    """
    Afficher un message d'erreur de permission.
    
    Args:
        message: Message personnalisé
    """
    st.error(f"❌ {message}")
    st.stop()


def check_ownership(user_id: str, resource_owner_id: str, resource_name: str = "ressource") -> bool:
    """
    Vérifier si l'utilisateur est propriétaire d'une ressource.
    
    Args:
        user_id: ID de l'utilisateur connecté
        resource_owner_id: ID du propriétaire de la ressource
        resource_name: Nom de la ressource (pour le message d'erreur)
        
    Returns:
        True si propriétaire
    """
    from auth.session import is_admin
    
    if is_admin():
        return True
    
    if user_id != resource_owner_id:
        show_permission_error(f"Vous n'êtes pas autorisé à modifier cette {resource_name}.")
        return False
    
    return True
