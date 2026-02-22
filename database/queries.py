"""Requêtes SQL réutilisables pour Albion Zerg Manager."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from config.supabase_config import get_supabase
from database.models import (
    UserProfile, Weapon, Composition, CompositionSlot,
    Activity, ActivityRegistration, ActivityAssignment,
    UserRole, ActivityStatus
)


class UserQueries:
    """Requêtes pour les utilisateurs."""
    
    @staticmethod
    def get_profile_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer le profil d'un utilisateur par ID."""
        supabase = get_supabase()
        response = supabase.table("users_profiles").select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_profile_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Récupérer le profil d'un utilisateur par email."""
        supabase = get_supabase()
        response = supabase.table("users_profiles").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_profile(user_id: str, email: str, username: str, role: str = "user") -> Dict[str, Any]:
        """Créer un nouveau profil utilisateur."""
        supabase = get_supabase()
        data = {
            "id": user_id,
            "email": email,
            "username": username,
            "role": role,
            "is_active": True
        }
        response = supabase.table("users_profiles").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour un profil utilisateur."""
        supabase = get_supabase()
        response = supabase.table("users_profiles").update(updates).eq("id", user_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def get_all_users(is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Récupérer tous les utilisateurs."""
        supabase = get_supabase()
        query = supabase.table("users_profiles").select("*")
        if is_active is not None:
            query = query.eq("is_active", is_active)
        response = query.execute()
        return response.data


class WeaponQueries:
    """Requêtes pour les armes."""
    
    @staticmethod
    def get_all_weapons(is_active: bool = True) -> List[Dict[str, Any]]:
        """Récupérer toutes les armes."""
        supabase = get_supabase()
        query = supabase.table("weapons").select("*").order("category", desc=False).order("name", desc=False)
        if is_active is not None:
            query = query.eq("is_active", is_active)
        response = query.execute()
        return response.data
    
    @staticmethod
    def get_weapons_by_category(category: str, is_active: bool = True) -> List[Dict[str, Any]]:
        """Récupérer les armes par catégorie."""
        supabase = get_supabase()
        query = supabase.table("weapons").select("*").eq("category", category).order("name", desc=False)
        if is_active is not None:
            query = query.eq("is_active", is_active)
        response = query.execute()
        return response.data
    
    @staticmethod
    def get_weapon_by_id(weapon_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une arme par ID."""
        supabase = get_supabase()
        response = supabase.table("weapons").select("*").eq("id", weapon_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_weapon(name: str, category: str, tier: Optional[int] = None) -> Dict[str, Any]:
        """Créer une nouvelle arme."""
        supabase = get_supabase()
        data = {
            "name": name,
            "category": category,
            "tier": tier,
            "is_active": True
        }
        response = supabase.table("weapons").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_weapon(weapon_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour une arme."""
        supabase = get_supabase()
        response = supabase.table("weapons").update(updates).eq("id", weapon_id).execute()
        return response.data[0] if response.data else None


class CompositionQueries:
    """Requêtes pour les compositions."""
    
    @staticmethod
    def get_all_compositions(created_by: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupérer toutes les compositions."""
        supabase = get_supabase()
        query = supabase.table("compositions").select("*, users_profiles(username)").order("created_at", desc=True)
        if created_by:
            query = query.eq("created_by", created_by)
        response = query.execute()
        return response.data
    
    @staticmethod
    def get_composition_by_id(composition_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une composition par ID."""
        supabase = get_supabase()
        response = supabase.table("compositions").select("*, users_profiles(username)").eq("id", composition_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_composition(name: str, description: str, created_by: str, is_template: bool = True) -> Dict[str, Any]:
        """Créer une nouvelle composition."""
        supabase = get_supabase()
        data = {
            "name": name,
            "description": description,
            "created_by": created_by,
            "is_template": is_template
        }
        response = supabase.table("compositions").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_composition(composition_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour une composition."""
        supabase = get_supabase()
        response = supabase.table("compositions").update(updates).eq("id", composition_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_composition(composition_id: str) -> bool:
        """Supprimer une composition."""
        supabase = get_supabase()
        response = supabase.table("compositions").delete().eq("id", composition_id).execute()
        return len(response.data) > 0
    
    @staticmethod
    def get_slots_by_composition(composition_id: str) -> List[Dict[str, Any]]:
        """Récupérer les slots d'une composition."""
        supabase = get_supabase()
        response = supabase.table("composition_slots").select("*, weapons(name)").eq("composition_id", composition_id).execute()
        return response.data
    
    @staticmethod
    def create_slot(composition_id: str, weapon_id: Optional[str], category: Optional[str], quantity: int) -> Dict[str, Any]:
        """Créer un slot dans une composition."""
        supabase = get_supabase()
        data = {
            "composition_id": composition_id,
            "weapon_id": weapon_id,
            "category": category,
            "quantity": quantity
        }
        response = supabase.table("composition_slots").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_slot(slot_id: str) -> bool:
        """Supprimer un slot."""
        supabase = get_supabase()
        response = supabase.table("composition_slots").delete().eq("id", slot_id).execute()
        return len(response.data) > 0


class ActivityQueries:
    """Requêtes pour les activités."""
    
    @staticmethod
    def get_all_activities(status: Optional[str] = None, created_by: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupérer toutes les activités."""
        supabase = get_supabase()
        query = supabase.table("activities").select(
            "*, users_profiles(username), compositions(name)"
        ).order("scheduled_at", desc=False)
        
        if status:
            query = query.eq("status", status)
        if created_by:
            query = query.eq("created_by", created_by)
        
        response = query.execute()
        return response.data
    
    @staticmethod
    def get_activity_by_id(activity_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une activité par ID."""
        supabase = get_supabase()
        response = supabase.table("activities").select(
            "*, users_profiles(username), compositions(name)"
        ).eq("id", activity_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_activity(name: str, description: str, composition_id: str, 
                       scheduled_at: datetime, created_by: str, max_participants: int = 40) -> Dict[str, Any]:
        """Créer une nouvelle activité."""
        supabase = get_supabase()
        data = {
            "name": name,
            "description": description,
            "composition_id": composition_id,
            "scheduled_at": scheduled_at.isoformat(),
            "created_by": created_by,
            "max_participants": max_participants,
            "status": "open"
        }
        response = supabase.table("activities").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_activity(activity_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour une activité."""
        supabase = get_supabase()
        response = supabase.table("activities").update(updates).eq("id", activity_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_activity(activity_id: str) -> bool:
        """Supprimer une activité."""
        supabase = get_supabase()
        response = supabase.table("activities").delete().eq("id", activity_id).execute()
        return len(response.data) > 0


class RegistrationQueries:
    """Requêtes pour les inscriptions."""
    
    @staticmethod
    def get_registrations_by_activity(activity_id: str) -> List[Dict[str, Any]]:
        """Récupérer les inscriptions d'une activité."""
        supabase = get_supabase()
        response = supabase.table("activity_registrations").select(
            "*, users_profiles(username), weapons(name, category)"
        ).eq("activity_id", activity_id).order("priority", desc=False).execute()
        return response.data
    
    @staticmethod
    def get_registrations_by_user(user_id: str) -> List[Dict[str, Any]]:
        """Récupérer les inscriptions d'un utilisateur."""
        supabase = get_supabase()
        response = supabase.table("activity_registrations").select(
            "*, activities(name, scheduled_at, status), weapons(name, category)"
        ).eq("user_id", user_id).execute()
        return response.data
    
    @staticmethod
    def create_registration(activity_id: str, user_id: str, weapon_id: str, 
                          priority: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """Créer une inscription."""
        supabase = get_supabase()
        data = {
            "activity_id": activity_id,
            "user_id": user_id,
            "weapon_id": weapon_id,
            "priority": priority,
            "notes": notes,
            "status": "pending"
        }
        response = supabase.table("activity_registrations").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_registration(registration_id: str) -> bool:
        """Supprimer une inscription."""
        supabase = get_supabase()
        response = supabase.table("activity_registrations").delete().eq("id", registration_id).execute()
        return len(response.data) > 0


class AssignmentQueries:
    """Requêtes pour les assignations."""
    
    @staticmethod
    def get_assignments_by_activity(activity_id: str) -> List[Dict[str, Any]]:
        """Récupérer les assignations d'une activité."""
        supabase = get_supabase()
        response = supabase.table("activity_assignments").select(
            "*, users_profiles!activity_assignments_user_id_fkey(username), weapons(name, category)"
        ).eq("activity_id", activity_id).execute()
        return response.data
    
    @staticmethod
    def get_assignment_by_user_activity(user_id: str, activity_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer l'assignation d'un utilisateur pour une activité."""
        supabase = get_supabase()
        response = supabase.table("activity_assignments").select(
            "*, weapons(name, category)"
        ).eq("user_id", user_id).eq("activity_id", activity_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def create_assignment(activity_id: str, user_id: str, weapon_id: str, 
                         assigned_by: str, notes: Optional[str] = None) -> Dict[str, Any]:
        """Créer une assignation."""
        supabase = get_supabase()
        data = {
            "activity_id": activity_id,
            "user_id": user_id,
            "weapon_id": weapon_id,
            "assigned_by": assigned_by,
            "notes": notes
        }
        response = supabase.table("activity_assignments").insert(data).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def update_assignment(assignment_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour une assignation."""
        supabase = get_supabase()
        response = supabase.table("activity_assignments").update(updates).eq("id", assignment_id).execute()
        return response.data[0] if response.data else None
    
    @staticmethod
    def delete_assignment(assignment_id: str) -> bool:
        """Supprimer une assignation."""
        supabase = get_supabase()
        response = supabase.table("activity_assignments").delete().eq("id", assignment_id).execute()
        return len(response.data) > 0
