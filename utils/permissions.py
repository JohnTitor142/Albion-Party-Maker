"""Fonctions utilitaires pour les permissions."""

from typing import Callable
from database.models import UserRole
from auth.session import get_user_role


def has_permission(required_role: UserRole) -> bool:
    """
    Vérifier si l'utilisateur a le rôle requis.
    
    Args:
        required_role: Rôle minimum requis
        
    Returns:
        True si l'utilisateur a les permissions
    """
    current_role = get_user_role()
    
    if not current_role:
        return False
    
    role_hierarchy = {
        UserRole.USER.value: 1,
        UserRole.SHOTCALLER.value: 2,
        UserRole.ADMIN.value: 3
    }
    
    current_level = role_hierarchy.get(current_role, 0)
    required_level = role_hierarchy.get(required_role.value, 999)
    
    return current_level >= required_level


def can_manage_composition(composition_created_by: str) -> bool:
    """
    Vérifier si l'utilisateur peut gérer une composition.
    
    Args:
        composition_created_by: ID du créateur de la composition
        
    Returns:
        True si l'utilisateur peut gérer la composition
    """
    from auth.session import get_user_id, is_admin
    
    if is_admin():
        return True
    
    return get_user_id() == composition_created_by


def can_manage_activity(activity_created_by: str) -> bool:
    """
    Vérifier si l'utilisateur peut gérer une activité.
    
    Args:
        activity_created_by: ID du créateur de l'activité
        
    Returns:
        True si l'utilisateur peut gérer l'activité
    """
    from auth.session import get_user_id, is_admin
    
    if is_admin():
        return True
    
    return get_user_id() == activity_created_by


def can_register_to_activity(activity_status: str) -> bool:
    """
    Vérifier si un utilisateur peut s'inscrire à une activité.
    
    Args:
        activity_status: Statut de l'activité
        
    Returns:
        True si l'inscription est possible
    """
    return activity_status == "open"


def can_assign_players(activity_created_by: str) -> bool:
    """
    Vérifier si l'utilisateur peut assigner des joueurs.
    
    Args:
        activity_created_by: ID du créateur de l'activité
        
    Returns:
        True si l'utilisateur peut assigner
    """
    return can_manage_activity(activity_created_by)
