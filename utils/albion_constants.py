"""Constantes Albion Online."""

# Catégories d'armes
WEAPON_CATEGORIES = [
    "Tank",
    "Healer",
    "DPS Melee",
    "DPS Range",
    "Support"
]

# Couleurs par catégorie (pour l'UI)
CATEGORY_COLORS = {
    "Tank": "#4A90E2",        # Bleu
    "Healer": "#50C878",      # Vert
    "DPS Melee": "#E74C3C",   # Rouge
    "DPS Range": "#9B59B6",   # Violet
    "Support": "#F39C12"      # Orange
}

# Icônes par catégorie (émojis)
CATEGORY_ICONS = {
    "Tank": "🛡️",
    "Healer": "💚",
    "DPS Melee": "⚔️",
    "DPS Range": "🏹",
    "Support": "✨"
}

# Tiers d'armes Albion
WEAPON_TIERS = [4, 5, 6, 7, 8]

# Statuts d'activité
ACTIVITY_STATUS_LABELS = {
    "open": "🟢 Ouvert",
    "locked": "🔒 Verrouillé",
    "completed": "✅ Terminé",
    "cancelled": "❌ Annulé"
}

# Couleurs des statuts
ACTIVITY_STATUS_COLORS = {
    "open": "#50C878",
    "locked": "#F39C12",
    "completed": "#4A90E2",
    "cancelled": "#E74C3C"
}
