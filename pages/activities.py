"""Page de gestion des activités (ShotCaller)."""

import streamlit as st
from datetime import datetime, timedelta
from auth.session import require_role, get_user_id
from database.models import UserRole
from database.queries import ActivityQueries, CompositionQueries, RegistrationQueries, AssignmentQueries, WeaponQueries
from components.activity_card import render_activity_card
from utils.albion_constants import ACTIVITY_STATUS_LABELS


def render_activities_page():
    """Page de gestion des activités."""
    require_role(UserRole.SHOTCALLER)
    
    st.title("📅 Gestion des Activités")
    
    user_id = get_user_id()
    
    # Tabs
    tab_list, tab_create, tab_manage = st.tabs(["📋 Mes Activités", "➕ Créer", "⚙️ Gérer"])
    
    with tab_list:
        render_activities_list(user_id)
    
    with tab_create:
        render_create_activity(user_id)
    
    with tab_manage:
        render_manage_activities(user_id)


def render_activities_list(user_id: str):
    """Afficher la liste des activités."""
    st.subheader("Mes Activités")
    
    try:
        activities = ActivityQueries.get_all_activities(created_by=user_id)
        
        if not activities:
            st.info("Vous n'avez pas encore créé d'activité. Utilisez l'onglet 'Créer' !")
            return
        
        # Filtres
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            status_filter = st.selectbox(
                "Filtrer par statut",
                options=["Tous"] + list(ACTIVITY_STATUS_LABELS.keys())
            )
        
        with col_filter2:
            sort_by = st.selectbox(
                "Trier par",
                options=["Date (croissant)", "Date (décroissant)", "Nom"]
            )
        
        # Appliquer les filtres
        filtered_activities = activities
        if status_filter != "Tous":
            filtered_activities = [a for a in activities if a.get('status') == status_filter]
        
        # Trier
        if sort_by == "Date (croissant)":
            filtered_activities = sorted(filtered_activities, key=lambda x: x.get('scheduled_at', ''))
        elif sort_by == "Date (décroissant)":
            filtered_activities = sorted(filtered_activities, key=lambda x: x.get('scheduled_at', ''), reverse=True)
        else:
            filtered_activities = sorted(filtered_activities, key=lambda x: x.get('name', ''))
        
        st.markdown(f"**{len(filtered_activities)} activité(s)**")
        
        for activity in filtered_activities:
            registrations = RegistrationQueries.get_registrations_by_activity(activity['id'])
            assignments = AssignmentQueries.get_assignments_by_activity(activity['id'])
            
            render_activity_card(
                activity,
                registrations_count=len(registrations),
                assignments_count=len(assignments),
                show_actions=True,
                on_view=lambda a: view_activity_details(a),
                on_delete=lambda a: delete_activity(a)
            )
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des activités : {str(e)}")


def render_create_activity(user_id: str):
    """Formulaire de création d'activité."""
    st.subheader("Créer une Nouvelle Activité")
    
    try:
        # Récupérer les compositions de l'utilisateur
        compositions = CompositionQueries.get_all_compositions(created_by=user_id)
        
        if not compositions:
            st.warning("⚠️ Vous devez d'abord créer une composition avant de créer une activité.")
            st.info("💡 Allez dans 'Compositions' pour en créer une.")
            return
        
        with st.form("create_activity"):
            name = st.text_input("Nom de l'activité", placeholder="Ex: ZvZ Samedi 20h")
            description = st.text_area("Description", placeholder="Informations sur l'activité...")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Sélectionner la composition
                comp_options = {f"{c.get('name')}": c.get('id') for c in compositions}
                selected_comp_name = st.selectbox("Composition", options=list(comp_options.keys()))
                composition_id = comp_options.get(selected_comp_name)
            
            with col2:
                max_participants = st.number_input("Nombre max de participants", min_value=1, max_value=100, value=40)
            
            # Date et heure
            col_date, col_time = st.columns(2)
            
            with col_date:
                date = st.date_input("Date", min_value=datetime.now().date())
            
            with col_time:
                time = st.time_input("Heure", value=datetime.now().replace(hour=20, minute=0).time())
            
            submit = st.form_submit_button("✅ Créer l'Activité", use_container_width=True)
            
            if submit:
                if not name or not composition_id:
                    st.error("❌ Le nom et la composition sont obligatoires.")
                    return
                
                try:
                    # Combiner date et heure
                    scheduled_at = datetime.combine(date, time)
                    
                    # Créer l'activité
                    activity = ActivityQueries.create_activity(
                        name=name,
                        description=description,
                        composition_id=composition_id,
                        scheduled_at=scheduled_at,
                        created_by=user_id,
                        max_participants=max_participants
                    )
                    
                    if activity:
                        st.success(f"✅ Activité '{name}' créée avec succès !")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création de l'activité.")
                
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_manage_activities(user_id: str):
    """Gérer les activités (assignations)."""
    st.subheader("Gérer les Assignations")
    
    try:
        # Récupérer les activités ouvertes ou verrouillées
        activities = ActivityQueries.get_all_activities(created_by=user_id)
        manageable_activities = [a for a in activities if a.get('status') in ['open', 'locked']]
        
        if not manageable_activities:
            st.info("Aucune activité à gérer pour le moment.")
            return
        
        # Sélectionner une activité
        activity_options = {f"{a.get('name')} - {a.get('scheduled_at', '')}": a for a in manageable_activities}
        selected_activity_name = st.selectbox("Sélectionner une activité", options=list(activity_options.keys()))
        
        if selected_activity_name:
            activity = activity_options[selected_activity_name]
            render_activity_management(activity, user_id)
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_activity_management(activity: dict, user_id: str):
    """Interface de gestion d'une activité spécifique."""
    st.markdown("---")
    st.subheader(f"Gestion : {activity.get('name')}")
    
    try:
        # Récupérer les données
        registrations = RegistrationQueries.get_registrations_by_activity(activity['id'])
        assignments = AssignmentQueries.get_assignments_by_activity(activity['id'])
        composition = CompositionQueries.get_composition_by_id(activity.get('composition_id'))
        slots = CompositionQueries.get_slots_by_composition(activity.get('composition_id')) if activity.get('composition_id') else []
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📝 Inscriptions", len(registrations))
        
        with col2:
            st.metric("✅ Assignés", len(assignments))
        
        with col3:
            max_part = activity.get('max_participants', 40)
            st.metric("🎯 Remplissage", f"{len(assignments)}/{max_part}")
        
        # Changer le statut
        current_status = activity.get('status', 'open')
        new_status = st.selectbox(
            "Statut de l'activité",
            options=['open', 'locked', 'completed', 'cancelled'],
            index=['open', 'locked', 'completed', 'cancelled'].index(current_status)
        )
        
        if new_status != current_status:
            if st.button("💾 Mettre à jour le statut"):
                try:
                    ActivityQueries.update_activity(activity['id'], {'status': new_status})
                    st.success(f"✅ Statut mis à jour : {ACTIVITY_STATUS_LABELS.get(new_status)}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
        
        st.markdown("---")
        
        # Tabs pour gérer
        tab_reg, tab_assign = st.tabs(["📝 Inscriptions", "✅ Assignations"])
        
        with tab_reg:
            st.subheader("Inscriptions reçues")
            
            if not registrations:
                st.info("Aucune inscription pour le moment.")
            else:
                # Grouper par arme
                from utils.helpers import group_by_category
                
                for registration in registrations:
                    weapon_data = registration.get('weapons', {})
                    weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                    weapon_category = weapon_data.get('category', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                    
                    user_data = registration.get('users_profiles', {})
                    username = user_data.get('username', 'N/A') if isinstance(user_data, dict) else 'N/A'
                    
                    col_user, col_weapon, col_priority, col_action = st.columns([2, 2, 1, 1])
                    
                    with col_user:
                        st.write(f"**{username}**")
                    
                    with col_weapon:
                        st.write(f"⚔️ {weapon_name}")
                        st.caption(weapon_category)
                    
                    with col_priority:
                        st.write(f"Priorité {registration.get('priority', 1)}")
                    
                    with col_action:
                        # Vérifier si déjà assigné
                        is_assigned = any(a.get('user_id') == registration.get('user_id') for a in assignments)
                        
                        if is_assigned:
                            st.success("✅ Assigné")
                        else:
                            if st.button("➕ Assigner", key=f"assign_{registration['id']}"):
                                try:
                                    AssignmentQueries.create_assignment(
                                        activity_id=activity['id'],
                                        user_id=registration.get('user_id'),
                                        weapon_id=registration.get('weapon_id'),
                                        assigned_by=user_id
                                    )
                                    st.success("✅ Assignation créée !")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Erreur : {str(e)}")
                    
                    st.markdown("---")
        
        with tab_assign:
            st.subheader("Assignations finales")
            
            if not assignments:
                st.info("Aucune assignation pour le moment. Assignez des joueurs depuis l'onglet 'Inscriptions'.")
            else:
                for assignment in assignments:
                    user_data = assignment.get('users_profiles_activity_assignments_user_id_fkey', {})
                    username = user_data.get('username', 'N/A') if isinstance(user_data, dict) else 'N/A'
                    
                    weapon_data = assignment.get('weapons', {})
                    weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                    
                    col_user, col_weapon, col_action = st.columns([2, 2, 1])
                    
                    with col_user:
                        st.write(f"**{username}**")
                    
                    with col_weapon:
                        st.write(f"⚔️ {weapon_name}")
                    
                    with col_action:
                        if st.button("🗑️", key=f"unassign_{assignment['id']}"):
                            try:
                                AssignmentQueries.delete_assignment(assignment['id'])
                                st.success("✅ Assignation supprimée !")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erreur : {str(e)}")
                    
                    st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def view_activity_details(activity: dict):
    """Voir les détails d'une activité (placeholder)."""
    st.info(f"🔍 Détails de '{activity.get('name')}' - Utilisez l'onglet 'Gérer' !")


def delete_activity(activity: dict):
    """Supprimer une activité."""
    if st.session_state.get(f"confirm_delete_activity_{activity['id']}", False):
        try:
            success = ActivityQueries.delete_activity(activity['id'])
            if success:
                st.success(f"✅ Activité '{activity.get('name')}' supprimée.")
                del st.session_state[f"confirm_delete_activity_{activity['id']}"]
                st.rerun()
            else:
                st.error("❌ Erreur lors de la suppression.")
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
    else:
        st.warning(f"⚠️ Êtes-vous sûr de vouloir supprimer '{activity.get('name')}' ?")
        if st.button("Confirmer la suppression", key=f"confirm_activity_{activity['id']}"):
            st.session_state[f"confirm_delete_activity_{activity['id']}"] = True
            st.rerun()
