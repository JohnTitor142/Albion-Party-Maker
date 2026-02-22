"""Page d'inscriptions aux activités (User)."""

import streamlit as st
from datetime import datetime
from auth.session import require_auth, get_user_id
from database.queries import ActivityQueries, RegistrationQueries, WeaponQueries, AssignmentQueries
from components.activity_card import render_activity_card
from utils.helpers import format_datetime, time_until


def render_my_activities_page():
    """Page de mes inscriptions."""
    require_auth()
    
    st.title("📝 Mes Inscriptions aux Activités")
    
    user_id = get_user_id()
    
    # Tabs
    tab_available, tab_my_reg, tab_my_assign = st.tabs([
        "📅 Activités Disponibles", 
        "📝 Mes Inscriptions",
        "✅ Mes Assignations"
    ])
    
    with tab_available:
        render_available_activities(user_id)
    
    with tab_my_reg:
        render_my_registrations(user_id)
    
    with tab_my_assign:
        render_my_assignments(user_id)


def render_available_activities(user_id: str):
    """Afficher les activités ouvertes."""
    st.subheader("Activités Ouvertes pour Inscription")
    
    try:
        # Récupérer les activités ouvertes
        activities = ActivityQueries.get_all_activities(status='open')
        
        if not activities:
            st.info("Aucune activité ouverte pour le moment. Revenez plus tard !")
            return
        
        st.success(f"🎯 {len(activities)} activité(s) disponible(s)")
        
        for activity in activities:
            # Vérifier si déjà inscrit
            my_registrations = RegistrationQueries.get_registrations_by_activity(activity['id'])
            is_registered = any(r.get('user_id') == user_id for r in my_registrations)
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"📅 {activity.get('name')}")
                    
                    col_date, col_desc = st.columns(2)
                    
                    with col_date:
                        scheduled = activity.get('scheduled_at')
                        if scheduled:
                            if isinstance(scheduled, str):
                                scheduled = datetime.fromisoformat(scheduled.replace('Z', '+00:00'))
                            st.write(f"**📆 Date:** {format_datetime(scheduled)}")
                            st.caption(time_until(scheduled))
                    
                    with col_desc:
                        if activity.get('description'):
                            with st.expander("📝 Description"):
                                st.write(activity['description'])
                
                with col2:
                    if is_registered:
                        st.success("✅ Inscrit")
                    else:
                        if st.button("➕ S'inscrire", key=f"register_{activity['id']}", use_container_width=True):
                            show_registration_form(activity, user_id)
                
                st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def show_registration_form(activity: dict, user_id: str):
    """Afficher le formulaire d'inscription."""
    st.subheader(f"S'inscrire à : {activity.get('name')}")
    
    try:
        # Récupérer les armes
        weapons = WeaponQueries.get_all_weapons()
        
        if not weapons:
            st.error("❌ Aucune arme disponible.")
            return
        
        with st.form(f"register_form_{activity['id']}"):
            st.info("💡 Sélectionnez jusqu'à 3 armes par ordre de préférence")
            
            # Sélectionner jusqu'à 3 armes
            selections = []
            
            for i in range(3):
                priority = i + 1
                
                col_weapon, col_notes = st.columns([2, 1])
                
                with col_weapon:
                    weapon_options = {f"{w.get('name')} ({w.get('category')})": w.get('id') for w in weapons}
                    weapon_options = {"---": None, **weapon_options}
                    
                    selected = st.selectbox(
                        f"Choix #{priority}",
                        options=list(weapon_options.keys()),
                        key=f"weapon_{priority}_{activity['id']}"
                    )
                    
                    weapon_id = weapon_options.get(selected)
                    
                    if weapon_id:
                        selections.append({
                            'weapon_id': weapon_id,
                            'priority': priority
                        })
            
            notes = st.text_area("Notes (optionnel)", placeholder="Commentaires...")
            
            submit = st.form_submit_button("✅ Confirmer l'inscription", use_container_width=True)
            
            if submit:
                if not selections:
                    st.error("❌ Veuillez sélectionner au moins une arme.")
                    return
                
                try:
                    # Créer les inscriptions
                    for selection in selections:
                        RegistrationQueries.create_registration(
                            activity_id=activity['id'],
                            user_id=user_id,
                            weapon_id=selection['weapon_id'],
                            priority=selection['priority'],
                            notes=notes if selection['priority'] == 1 else None
                        )
                    
                    st.success(f"✅ Inscription confirmée pour '{activity.get('name')}' !")
                    st.balloons()
                    st.rerun()
                
                except Exception as e:
                    if "duplicate" in str(e).lower():
                        st.error("❌ Vous êtes déjà inscrit avec cette arme.")
                    else:
                        st.error(f"❌ Erreur : {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_my_registrations(user_id: str):
    """Afficher mes inscriptions."""
    st.subheader("Mes Inscriptions Actives")
    
    try:
        registrations = RegistrationQueries.get_registrations_by_user(user_id)
        
        if not registrations:
            st.info("Vous n'êtes inscrit à aucune activité. Allez dans 'Activités Disponibles' !")
            return
        
        # Grouper par activité
        by_activity = {}
        for reg in registrations:
            activity_id = reg.get('activity_id')
            if activity_id not in by_activity:
                by_activity[activity_id] = []
            by_activity[activity_id].append(reg)
        
        for activity_id, activity_regs in by_activity.items():
            # Récupérer les infos de l'activité
            activity_data = activity_regs[0].get('activities', {}) if activity_regs else {}
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"📅 {activity_data.get('name', 'N/A')}")
                    
                    scheduled = activity_data.get('scheduled_at')
                    if scheduled:
                        if isinstance(scheduled, str):
                            scheduled = datetime.fromisoformat(scheduled.replace('Z', '+00:00'))
                        st.write(f"**📆 Date:** {format_datetime(scheduled)}")
                        st.caption(time_until(scheduled))
                
                with col2:
                    status = activity_data.get('status', 'open')
                    if status == 'open':
                        st.success("🟢 Ouvert")
                    elif status == 'locked':
                        st.warning("🔒 Verrouillé")
                    else:
                        st.info(status.title())
                
                # Afficher les armes inscrites
                st.write("**Vos armes :**")
                for reg in sorted(activity_regs, key=lambda x: x.get('priority', 999)):
                    weapon_data = reg.get('weapons', {})
                    weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                    priority = reg.get('priority', 1)
                    
                    col_weapon, col_action = st.columns([3, 1])
                    
                    with col_weapon:
                        st.write(f"• Priorité {priority}: ⚔️ {weapon_name}")
                    
                    with col_action:
                        if status == 'open':
                            if st.button("🗑️", key=f"delete_reg_{reg['id']}", help="Se désinscrire"):
                                try:
                                    RegistrationQueries.delete_registration(reg['id'])
                                    st.success("✅ Inscription supprimée !")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur : {str(e)}")
                
                st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_my_assignments(user_id: str):
    """Afficher mes assignations."""
    st.subheader("Mes Assignations Confirmées")
    
    try:
        # Récupérer toutes les activités
        all_activities = ActivityQueries.get_all_activities()
        
        my_assignments = []
        
        for activity in all_activities:
            assignment = AssignmentQueries.get_assignment_by_user_activity(user_id, activity['id'])
            if assignment:
                assignment['activity_data'] = activity
                my_assignments.append(assignment)
        
        if not my_assignments:
            st.info("Vous n'avez pas encore d'assignation confirmée.")
            return
        
        st.success(f"✅ {len(my_assignments)} assignation(s) confirmée(s)")
        
        for assignment in my_assignments:
            activity_data = assignment.get('activity_data', {})
            weapon_data = assignment.get('weapons', {})
            weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(f"📅 {activity_data.get('name', 'N/A')}")
                    
                    scheduled = activity_data.get('scheduled_at')
                    if scheduled:
                        if isinstance(scheduled, str):
                            scheduled = datetime.fromisoformat(scheduled.replace('Z', '+00:00'))
                        st.write(f"**📆 Date:** {format_datetime(scheduled)}")
                        st.caption(time_until(scheduled))
                    
                    st.write(f"**⚔️ Votre arme:** {weapon_name}")
                    
                    if assignment.get('notes'):
                        st.caption(f"📝 Note : {assignment['notes']}")
                
                with col2:
                    status = activity_data.get('status', 'open')
                    if status == 'locked':
                        st.warning("🔒 Verrouillé")
                    elif status == 'completed':
                        st.success("✅ Terminé")
                    else:
                        st.info(status.title())
                
                st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
