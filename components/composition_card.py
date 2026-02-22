"""Composant pour afficher une carte de composition."""

import streamlit as st
from typing import Dict, Any, List
from utils.albion_constants import CATEGORY_ICONS, CATEGORY_COLORS


def render_composition_card(composition: Dict[str, Any], slots: List[Dict[str, Any]], 
                           show_actions: bool = False, on_edit=None, on_delete=None):
    """
    Afficher une carte de composition.
    
    Args:
        composition: Données de la composition
        slots: Liste des slots de la composition
        show_actions: Afficher les boutons d'action
        on_edit: Callback pour édition
        on_delete: Callback pour suppression
    """
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader(f"🧩 {composition.get('name', 'Sans nom')}")
            if composition.get('description'):
                st.caption(composition['description'])
        
        with col2:
            if show_actions:
                if on_edit and st.button("✏️", key=f"edit_{composition['id']}", help="Éditer"):
                    on_edit(composition)
                if on_delete and st.button("🗑️", key=f"del_{composition['id']}", help="Supprimer"):
                    on_delete(composition)
        
        # Grouper les slots par catégorie
        slots_by_category = {}
        total_slots = 0
        
        for slot in slots:
            category = slot.get('category', 'Autre')
            weapon_name = slot.get('weapons', {}).get('name') if isinstance(slot.get('weapons'), dict) else slot.get('weapon_name', 'Any')
            quantity = slot.get('quantity', 0)
            total_slots += quantity
            
            if category not in slots_by_category:
                slots_by_category[category] = []
            
            slots_by_category[category].append({
                'weapon': weapon_name or f"Any {category}",
                'quantity': quantity
            })
        
        # Afficher les slots
        if slots_by_category:
            cols = st.columns(len(slots_by_category))
            
            for idx, (category, category_slots) in enumerate(sorted(slots_by_category.items())):
                with cols[idx]:
                    icon = CATEGORY_ICONS.get(category, "⚔️")
                    color = CATEGORY_COLORS.get(category, "#95A5A6")
                    
                    category_total = sum(s['quantity'] for s in category_slots)
                    
                    st.markdown(
                        f"<div style='background-color: {color}22; padding: 10px; border-radius: 5px; border-left: 3px solid {color};'>"
                        f"<b>{icon} {category}</b><br>"
                        f"<small>Total: {category_total}</small><br><br>",
                        unsafe_allow_html=True
                    )
                    
                    for slot in category_slots:
                        st.markdown(f"• {slot['quantity']}x {slot['weapon']}")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Aucun slot défini pour cette composition.")
        
        st.markdown(f"**Total zerg : {total_slots} joueurs**")
        st.markdown("---")


def render_composition_summary(composition: Dict[str, Any], slots: List[Dict[str, Any]]) -> str:
    """
    Générer un résumé textuel d'une composition.
    
    Args:
        composition: Données de la composition
        slots: Liste des slots
        
    Returns:
        String résumé
    """
    lines = [f"**{composition.get('name')}**"]
    
    if composition.get('description'):
        lines.append(composition['description'])
    
    slots_by_category = {}
    for slot in slots:
        category = slot.get('category', 'Autre')
        if category not in slots_by_category:
            slots_by_category[category] = 0
        slots_by_category[category] += slot.get('quantity', 0)
    
    for category, total in sorted(slots_by_category.items()):
        icon = CATEGORY_ICONS.get(category, "⚔️")
        lines.append(f"{icon} {category}: {total}")
    
    return "\n".join(lines)
