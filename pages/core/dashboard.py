"""Page dashboard principale."""

import streamlit as st
from datetime import datetime, timedelta
from auth.session import require_auth, get_user_role, get_user_id, is_admin, is_shotcaller
from database.queries import ActivityQueries, CompositionQueries, UserQueries, RegistrationQueries
from components.activity_card import render_activity_card
from utils.helpers import time_until, format_datetime


def render_dashboard():
    """Afficher le dashboard principal."""
    require_auth()
    
    st.title("📊 Tableau de Bord")
    
    user_role = get_user_role()
    user_id = get_user_id()
    
    # Dashboard selon le rôle
    if is_admin():
        render_admin_dashboard()
    elif is_shotcaller():
        render_shotcaller_dashboard(user_id)
    else:
        render_user_dashboard(user_id)


def render_admin_dashboard():
    """Dashboard pour les admins."""
    st.subheader("👑 Vue Administrateur")
    
    try:
        # Statistiques globales
        col1, col2, col3, col4 = st.columns(4)
        
        users = UserQueries.get_all_users(is_active=True)
        activities = ActivityQueries.get_all_activities()
        compositions = CompositionQueries.get_all_compositions()
        
        with col1:
            st.metric("👥 Utilisateurs actifs", len(users))
        
        with col2:
            open_activities = [a for a in activities if a.get('status') == 'open']
            st.metric("📅 Activités ouvertes", len(open_activities))
        
        with col3:
            st.metric("🧩 Compositions", len(compositions))
        
        with col4:
            upcoming = [a for a in activities if a.get('status') in ['open', 'locked']]
            st.metric("📆 Activités à venir", len(upcoming))
        
        st.markdown("---")
        
        # Prochaines activités
        st.subheader("📅 Prochaines Activités")
        
        upcoming_activities = sorted(
            [a for a in activities if a.get('status') in ['open', 'locked']],
            key=lambda x: x.get('scheduled_at', '')
        )[:5]
        
        if upcoming_activities:
            for activity in upcoming_activities:
                render_activity_card(activity, show_actions=False)
        else:
            st.info("Aucune activité à venir.")
        
        # Répartition des rôles
        st.markdown("---")
        st.subheader("📊 Répartition des Rôles")
        
        role_counts = {}
        for user in users:
            role = user.get('role', 'user')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        col_roles = st.columns(len(role_counts))
        for idx, (role, count) in enumerate(sorted(role_counts.items())):
            with col_roles[idx]:
                role_emoji = {"admin": "👑", "shotcaller": "📣", "user": "⚔️"}
                st.metric(f"{role_emoji.get(role, '⚔️')} {role.title()}", count)
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du dashboard : {str(e)}")


def render_shotcaller_dashboard(user_id: str):
    """Dashboard pour les shotcallers."""
    st.subheader("📣 Vue ShotCaller")
    
    try:
        # Mes statistiques
        col1, col2, col3 = st.columns(3)
        
        my_compositions = CompositionQueries.get_all_compositions(created_by=user_id)
        my_activities = ActivityQueries.get_all_activities(created_by=user_id)
        
        open_activities = [a for a in my_activities if a.get('status') == 'open']
        
        with col1:
            st.metric("🧩 Mes Compositions", len(my_compositions))
        
        with col2:
            st.metric("📅 Mes Activités", len(my_activities))
        
        with col3:
            st.metric("📝 Activités ouvertes", len(open_activities))
        
        st.markdown("---")
        
        # Mes prochaines activités
        st.subheader("📅 Mes Prochaines Activités")
        
        upcoming = sorted(
            [a for a in my_activities if a.get('status') in ['open', 'locked']],
            key=lambda x: x.get('scheduled_at', '')
        )[:5]
        
        if upcoming:
            for activity in upcoming:
                # Compter les inscriptions
                registrations = RegistrationQueries.get_registrations_by_activity(activity['id'])
                render_activity_card(
                    activity, 
                    registrations_count=len(registrations),
                    show_actions=False
                )
        else:
            st.info("Aucune activité à venir. Créez-en une dans 'Activités' !")
        
        # Actions rapides
        st.markdown("---")
        st.subheader("⚡ Actions Rapides")
        
        col_act1, col_act2 = st.columns(2)
        
        with col_act1:
            if st.button("➕ Créer une Composition", use_container_width=True):
                st.info("Allez dans 'Compositions' pour créer une nouvelle composition.")
        
        with col_act2:
            if st.button("➕ Créer une Activité", use_container_width=True):
                st.info("Allez dans 'Activités' pour créer une nouvelle activité.")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du dashboard : {str(e)}")


def render_user_dashboard(user_id: str):
    """Dashboard pour les users."""
    st.subheader("⚔️ Vue Joueur")
    
    try:
        # Mes inscriptions
        my_registrations = RegistrationQueries.get_registrations_by_user(user_id)
        
        # Activités disponibles
        all_activities = ActivityQueries.get_all_activities(status='open')
        
        # Statistiques
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("📝 Mes Inscriptions", len(my_registrations))
        
        with col2:
            st.metric("📅 Activités disponibles", len(all_activities))
        
        st.markdown("---")
        
        # Mes inscriptions actives
        st.subheader("📝 Mes Inscriptions")
        
        if my_registrations:
            for registration in my_registrations[:5]:
                activity_data = registration.get('activities', {})
                if not activity_data:
                    continue
                
                weapon_data = registration.get('weapons', {})
                weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                
                with st.container():
                    col_act, col_weapon, col_priority = st.columns([3, 2, 1])
                    
                    with col_act:
                        st.markdown(f"**📅 {activity_data.get('name')}**")
                        scheduled = activity_data.get('scheduled_at')
                        if scheduled:
                            st.caption(format_datetime(scheduled))
                    
                    with col_weapon:
                        st.markdown(f"⚔️ {weapon_name}")
                    
                    with col_priority:
                        priority = registration.get('priority', 1)
                        st.markdown(f"**Priorité {priority}**")
                    
                    st.markdown("---")
        else:
            st.info("Aucune inscription. Allez dans 'Mes Inscriptions' pour vous inscrire à une activité !")
        
        # Activités ouvertes
        st.subheader("📅 Activités Ouvertes")
        
        if all_activities:
            st.info(f"🎯 {len(all_activities)} activité(s) disponible(s) pour inscription !")
            
            for activity in all_activities[:3]:
                with st.container():
                    col_name, col_date = st.columns([3, 2])
                    
                    with col_name:
                        st.markdown(f"**📅 {activity.get('name')}**")
                    
                    with col_date:
                        scheduled = activity.get('scheduled_at')
                        if scheduled:
                            if isinstance(scheduled, str):
                                scheduled = datetime.fromisoformat(scheduled.replace('Z', '+00:00'))
                            st.caption(time_until(scheduled))
                    
                    st.markdown("---")
            
            st.info("💡 Allez dans 'Mes Inscriptions' pour vous inscrire !")
        else:
            st.info("Aucune activité ouverte pour le moment.")
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du dashboard : {str(e)}")
