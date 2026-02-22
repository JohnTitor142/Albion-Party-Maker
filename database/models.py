"""Modèles de données pour Albion Zerg Manager."""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """Rôles utilisateurs."""
    ADMIN = "admin"
    SHOTCALLER = "shotcaller"
    USER = "user"


class ActivityStatus(str, Enum):
    """Statut des activités."""
    OPEN = "open"
    LOCKED = "locked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RegistrationStatus(str, Enum):
    """Statut des inscriptions."""
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class UserProfile(BaseModel):
    """Modèle pour le profil utilisateur."""
    id: str
    email: str
    username: str
    role: UserRole
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class Weapon(BaseModel):
    """Modèle pour une arme d'Albion Online."""
    id: str
    name: str
    category: str
    tier: Optional[int] = None
    icon_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime


class Composition(BaseModel):
    """Modèle pour une composition de zerg."""
    id: str
    name: str
    description: Optional[str] = None
    created_by: str
    is_template: bool = True
    created_at: datetime
    updated_at: datetime


class CompositionSlot(BaseModel):
    """Modèle pour un slot d'arme dans une composition."""
    id: str
    composition_id: str
    weapon_id: Optional[str] = None
    category: Optional[str] = None
    quantity: int = Field(gt=0)
    created_at: datetime
    
    # Données enrichies (non en DB)
    weapon_name: Optional[str] = None


class Activity(BaseModel):
    """Modèle pour une activité/event."""
    id: str
    name: str
    description: Optional[str] = None
    composition_id: Optional[str] = None
    scheduled_at: datetime
    status: ActivityStatus = ActivityStatus.OPEN
    created_by: str
    max_participants: int = Field(default=40, gt=0)
    created_at: datetime
    updated_at: datetime
    
    # Données enrichies (non en DB)
    creator_name: Optional[str] = None
    composition_name: Optional[str] = None
    registrations_count: Optional[int] = 0
    assignments_count: Optional[int] = 0


class ActivityRegistration(BaseModel):
    """Modèle pour une inscription à une activité."""
    id: str
    activity_id: str
    user_id: str
    weapon_id: str
    priority: int = Field(gt=0)
    notes: Optional[str] = None
    status: RegistrationStatus = RegistrationStatus.PENDING
    created_at: datetime
    
    # Données enrichies (non en DB)
    username: Optional[str] = None
    weapon_name: Optional[str] = None
    activity_name: Optional[str] = None


class ActivityAssignment(BaseModel):
    """Modèle pour une assignation finale."""
    id: str
    activity_id: str
    user_id: str
    weapon_id: str
    assigned_by: str
    assigned_at: datetime
    notes: Optional[str] = None
    
    # Données enrichies (non en DB)
    username: Optional[str] = None
    weapon_name: Optional[str] = None
    assigned_by_name: Optional[str] = None


class CompositionWithSlots(BaseModel):
    """Modèle enrichi d'une composition avec ses slots."""
    composition: Composition
    slots: List[CompositionSlot] = []
    total_slots: int = 0


class ActivityWithDetails(BaseModel):
    """Modèle enrichi d'une activité avec tous les détails."""
    activity: Activity
    composition: Optional[Composition] = None
    slots: List[CompositionSlot] = []
    registrations: List[ActivityRegistration] = []
    assignments: List[ActivityAssignment] = []
    
    @property
    def is_full(self) -> bool:
        """Vérifie si l'activité est complète."""
        return len(self.assignments) >= self.activity.max_participants
    
    @property
    def fill_percentage(self) -> float:
        """Calcule le pourcentage de remplissage."""
        if self.activity.max_participants == 0:
            return 0.0
        return (len(self.assignments) / self.activity.max_participants) * 100
