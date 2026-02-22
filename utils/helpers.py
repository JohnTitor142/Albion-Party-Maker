"""Fonctions helper utilitaires."""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd


def format_datetime(dt: datetime, format: str = "%d/%m/%Y %H:%M") -> str:
    """
    Formater une datetime.
    
    Args:
        dt: Datetime à formater
        format: Format de sortie
        
    Returns:
        String formatée
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    return dt.strftime(format)


def time_until(dt: datetime) -> str:
    """
    Calculer le temps restant jusqu'à une date.
    
    Args:
        dt: Datetime cible
        
    Returns:
        String lisible (ex: "Dans 2 jours")
    """
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
    
    now = datetime.now(dt.tzinfo)
    delta = dt - now
    
    if delta.total_seconds() < 0:
        return "Passé"
    
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    
    if days > 0:
        return f"Dans {days} jour{'s' if days > 1 else ''}"
    elif hours > 0:
        return f"Dans {hours}h{minutes:02d}"
    else:
        return f"Dans {minutes} min"


def group_by_category(items: List[Dict[str, Any]], category_field: str = "category") -> Dict[str, List[Dict[str, Any]]]:
    """
    Grouper des items par catégorie.
    
    Args:
        items: Liste d'items à grouper
        category_field: Nom du champ catégorie
        
    Returns:
        Dictionnaire {catégorie: [items]}
    """
    grouped = {}
    for item in items:
        category = item.get(category_field, "Autre")
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(item)
    return grouped


def calculate_fill_rate(assigned: int, total: int) -> float:
    """
    Calculer le taux de remplissage en pourcentage.
    
    Args:
        assigned: Nombre d'assignations
        total: Nombre total de places
        
    Returns:
        Pourcentage (0-100)
    """
    if total == 0:
        return 0.0
    return (assigned / total) * 100


def export_roster_to_text(roster: List[Dict[str, Any]]) -> str:
    """
    Exporter un roster en format texte (pour Discord).
    
    Args:
        roster: Liste des assignations
        
    Returns:
        String formatée pour Discord
    """
    if not roster:
        return "Aucune assignation pour le moment."
    
    # Grouper par catégorie d'arme
    by_category = group_by_category(roster, "category")
    
    lines = ["**🗡️ ROSTER ALBION ZERG 🗡️**\n"]
    
    for category, assignments in sorted(by_category.items()):
        lines.append(f"\n**{category}** ({len(assignments)})")
        for assignment in assignments:
            weapon = assignment.get("weapon_name", "N/A")
            username = assignment.get("username", "N/A")
            lines.append(f"  • {weapon} - {username}")
    
    lines.append(f"\n**Total: {len(roster)} joueurs**")
    
    return "\n".join(lines)


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Récupérer une valeur de manière sécurisée dans un dict.
    
    Args:
        data: Dictionnaire source
        key: Clé à récupérer
        default: Valeur par défaut
        
    Returns:
        Valeur ou default
    """
    return data.get(key, default) if data else default
