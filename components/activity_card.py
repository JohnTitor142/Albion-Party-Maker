"""Composant pour afficher une carte d'activité."""

import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime
from utils.helpers import format_datetime, time_until
from utils.albion_constants import ACTIVITY_STATUS_LABELS, ACTIVITY_STATUS_COLORS


def render_activity_card(activity: Dict[str, Any], 
                         registrations_count: int = 0,
                         assignments_count: int = 0,
                         show_actions: bool = False,
                         on_view=None,
                         on_edit=None,
                         on_delete=None):
    """
    Afficher une carte d'activité.
    
    Args:
        activity: Données de l'activité
        registrations_count: Nombre d'inscriptions
        assignments_count: Nombre d'assignations
        show_actions: Afficher les boutons d'action
        on_view: Callback pour voir les détails
        on_edit: Callback pour édition
        on_delete: Callback pour suppression
    """
    status = activity.get('status', 'open')
    status_color = ACTIVITY_STATUS_COLORS.get(status, "#95A5A6")
    status_label = ACTIVITY_STATUS_LABELS.get(status, status)
    
    scheduled_at = activity.get('scheduled_at')
    if isinstance(scheduled_at, str):
        scheduled_at = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
    
    max_participants = activity.get('max_participants', 40)
    fill_percentage = (assignments_count / max_participants * 100) if max_participants > 0 else 0
    
    with st.container():
        # En-tête avec statut
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"📅 {activity.get('name', 'Sans nom')}")
        
        with col2:
            st.markdown(
                f"<div style='text-align: right; color: {status_color}; font-weight: bold;'>{status_label}</div>",
                unsafe_allow_html=True
            )
        
        # Infos principales
        col_date, col_comp = st.columns(2)
        
        with col_date:
            st.markdown(f"**📆 Date:** {format_datetime(scheduled_at)}")
            st.caption(time_until(scheduled_at))
        
        with col_comp:
            comp_name = "N/A"
            if activity.get('compositions'):
                comp_name = activity['compositions'].get('name', 'N/A')
            elif activity.get('composition_name'):
                comp_name = activity['composition_name']
            st.markdown(f"**🧩 Composition:** {comp_name}")
        
        # Description
        if activity.get('description'):
            with st.expander("📝 Description"):
                st.write(activity['description'])
        
        # Statistiques
        col_reg, col_assign, col_total = st.columns(3)
        
        with col_reg:
            st.metric("Inscriptions", registrations_count)
        
        with col_assign:
            st.metric("Assignés", f"{assignments_count}/{max_participants}")
        
        with col_total:
            st.metric("Remplissage", f"{fill_percentage:.0f}%")
        
        # Barre de progression
        st.progress(min(fill_percentage / 100, 1.0))
        
        # Actions
        if show_actions:
            action_cols = st.columns(3)
            
            with action_cols[0]:
                if on_view and st.button("👁️ Voir détails", key=f"view_{activity['id']}", use_container_width=True):
                    on_view(activity)
            
            with action_cols[1]:
                if on_edit and st.button("✏️ Éditer", key=f"edit_{activity['id']}", use_container_width=True):
                    on_edit(activity)
            
            with action_cols[2]:
                if on_delete and st.button("🗑️ Supprimer", key=f"del_{activity['id']}", use_container_width=True):
                    on_delete(activity)
        
        st.markdown("---")


def render_activity_status_badge(status: str) -> str:
    """
    Générer un badge HTML pour le statut.
    
    Args:
        status: Statut de l'activité
        
    Returns:
        HTML du badge
    """
    color = ACTIVITY_STATUS_COLORS.get(status, "#95A5A6")
    label = ACTIVITY_STATUS_LABELS.get(status, status)
    
    return f"<span style='background-color: {color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;'>{label}</span>"
