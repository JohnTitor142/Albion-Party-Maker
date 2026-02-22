"""Composant sélecteur d'armes."""

import streamlit as st
from typing import List, Dict, Any, Optional
from utils.albion_constants import WEAPON_CATEGORIES, CATEGORY_ICONS


def render_weapon_selector(weapons: List[Dict[str, Any]], 
                          key: str = "weapon_selector",
                          filter_by_category: Optional[str] = None,
                          label: str = "Sélectionner une arme") -> Optional[str]:
    """
    Afficher un sélecteur d'armes avec filtrage par catégorie.
    
    Args:
        weapons: Liste des armes disponibles
        key: Clé unique pour le widget
        filter_by_category: Filtrer par catégorie (None = toutes)
        label: Label du sélecteur
        
    Returns:
        ID de l'arme sélectionnée ou None
    """
    if filter_by_category:
        weapons = [w for w in weapons if w.get('category') == filter_by_category]
    
    if not weapons:
        st.warning("Aucune arme disponible.")
        return None
    
    # Créer les options avec icônes
    weapon_options = {}
    for weapon in weapons:
        category = weapon.get('category', 'Autre')
        icon = CATEGORY_ICONS.get(category, "⚔️")
        display_name = f"{icon} {weapon.get('name')} ({category})"
        weapon_options[display_name] = weapon.get('id')
    
    selected_display = st.selectbox(
        label,
        options=list(weapon_options.keys()),
        key=key
    )
    
    return weapon_options.get(selected_display) if selected_display else None


def render_multi_weapon_selector(weapons: List[Dict[str, Any]], 
                                 max_selections: int = 3,
                                 key_prefix: str = "multi_weapon") -> List[Dict[str, Any]]:
    """
    Afficher un sélecteur multi-armes avec priorités.
    
    Args:
        weapons: Liste des armes disponibles
        max_selections: Nombre maximum d'armes sélectionnables
        key_prefix: Préfixe pour les clés des widgets
        
    Returns:
        Liste de dicts avec weapon_id et priority
    """
    st.write(f"**Sélectionnez jusqu'à {max_selections} armes par ordre de préférence**")
    
    selections = []
    used_weapons = set()
    
    for i in range(max_selections):
        priority = i + 1
        
        # Filtrer les armes déjà sélectionnées
        available_weapons = [w for w in weapons if w.get('id') not in used_weapons]
        
        if not available_weapons:
            break
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            weapon_id = render_weapon_selector(
                available_weapons,
                key=f"{key_prefix}_{priority}",
                label=f"Choix #{priority}"
            )
        
        with col2:
            st.markdown(f"<div style='margin-top: 35px;'>Priorité: {priority}</div>", unsafe_allow_html=True)
        
        if weapon_id:
            selections.append({
                'weapon_id': weapon_id,
                'priority': priority
            })
            used_weapons.add(weapon_id)
        else:
            break
    
    return selections


def render_weapon_list(weapons: List[Dict[str, Any]], 
                       group_by_category: bool = True,
                       show_icons: bool = True):
    """
    Afficher une liste d'armes.
    
    Args:
        weapons: Liste des armes
        group_by_category: Grouper par catégorie
        show_icons: Afficher les icônes
    """
    if not weapons:
        st.info("Aucune arme à afficher.")
        return
    
    if group_by_category:
        from utils.helpers import group_by_category as group_func
        grouped = group_func(weapons, 'category')
        
        for category in sorted(grouped.keys()):
            icon = CATEGORY_ICONS.get(category, "⚔️") if show_icons else ""
            st.subheader(f"{icon} {category}")
            
            for weapon in sorted(grouped[category], key=lambda w: w.get('name', '')):
                st.markdown(f"- {weapon.get('name')}")
    else:
        for weapon in sorted(weapons, key=lambda w: w.get('name', '')):
            category = weapon.get('category', 'Autre')
            icon = CATEGORY_ICONS.get(category, "⚔️") if show_icons else ""
            st.markdown(f"{icon} **{weapon.get('name')}** - {category}")
