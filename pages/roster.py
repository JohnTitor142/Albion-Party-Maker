"""Page de visualisation des rosters."""

import streamlit as st
from auth.session import require_auth
from database.queries import ActivityQueries, AssignmentQueries, CompositionQueries
from utils.helpers import export_roster_to_text, format_datetime, group_by_category
from utils.albion_constants import CATEGORY_ICONS


def render_roster_page():
    """Page de visualisation des rosters."""
    require_auth()
    
    st.title("👥 Rosters des Activités")
    
    try:
        # Récupérer toutes les activités
        activities = ActivityQueries.get_all_activities()
        
        if not activities:
            st.info("Aucune activité créée pour le moment.")
            return
        
        # Filtrer par statut
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            status_filter = st.selectbox(
                "Filtrer par statut",
                options=["Tous", "open", "locked", "completed"]
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
        st.markdown("---")
        
        # Sélectionner une activité
        if filtered_activities:
            activity_options = {
                f"{a.get('name')} - {format_datetime(a.get('scheduled_at', ''))}": a 
                for a in filtered_activities
            }
            
            selected_activity_name = st.selectbox(
                "Sélectionner une activité",
                options=list(activity_options.keys())
            )
            
            if selected_activity_name:
                activity = activity_options[selected_activity_name]
                render_roster_details(activity)
        else:
            st.info("Aucune activité ne correspond aux filtres.")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_roster_details(activity: dict):
    """Afficher les détails du roster d'une activité."""
    st.markdown("---")
    st.subheader(f"Roster : {activity.get('name')}")
    
    try:
        # Récupérer les assignations
        assignments = AssignmentQueries.get_assignments_by_activity(activity['id'])
        
        # Récupérer la composition
        composition = None
        slots = []
        if activity.get('composition_id'):
            composition = CompositionQueries.get_composition_by_id(activity['composition_id'])
            slots = CompositionQueries.get_slots_by_composition(activity['composition_id'])
        
        # Infos activité
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📅 Date", format_datetime(activity.get('scheduled_at', '')))
        
        with col2:
            max_part = activity.get('max_participants', 40)
            st.metric("👥 Assignés", f"{len(assignments)}/{max_part}")
        
        with col3:
            fill_rate = (len(assignments) / max_part * 100) if max_part > 0 else 0
            st.metric("📊 Remplissage", f"{fill_rate:.0f}%")
        
        st.progress(min(fill_rate / 100, 1.0))
        
        if activity.get('description'):
            with st.expander("📝 Description"):
                st.write(activity['description'])
        
        st.markdown("---")
        
        # Afficher la composition demandée
        if composition and slots:
            st.subheader("🧩 Composition Demandée")
            
            # Grouper par catégorie
            slots_by_cat = {}
            for slot in slots:
                cat = slot.get('category', 'Autre')
                if cat not in slots_by_cat:
                    slots_by_cat[cat] = []
                slots_by_cat[cat].append(slot)
            
            cols = st.columns(len(slots_by_cat))
            
            for idx, (category, cat_slots) in enumerate(sorted(slots_by_cat.items())):
                with cols[idx]:
                    icon = CATEGORY_ICONS.get(category, "⚔️")
                    total = sum(s.get('quantity', 0) for s in cat_slots)
                    st.markdown(f"**{icon} {category}**")
                    st.caption(f"Total: {total}")
            
            st.markdown("---")
        
        # Roster actuel
        st.subheader("👥 Roster Actuel")
        
        if not assignments:
            st.info("Aucune assignation pour le moment.")
        else:
            # Enrichir les données
            enriched_assignments = []
            for assignment in assignments:
                user_data = assignment.get('users_profiles_activity_assignments_user_id_fkey', {})
                username = user_data.get('username', 'N/A') if isinstance(user_data, dict) else 'N/A'
                
                weapon_data = assignment.get('weapons', {})
                weapon_name = weapon_data.get('name', 'N/A') if isinstance(weapon_data, dict) else 'N/A'
                weapon_category = weapon_data.get('category', 'Autre') if isinstance(weapon_data, dict) else 'Autre'
                
                enriched_assignments.append({
                    'username': username,
                    'weapon_name': weapon_name,
                    'category': weapon_category,
                    'notes': assignment.get('notes')
                })
            
            # Grouper par catégorie
            by_category = group_by_category(enriched_assignments, 'category')
            
            # Afficher par catégorie
            for category in sorted(by_category.keys()):
                icon = CATEGORY_ICONS.get(category, "⚔️")
                st.markdown(f"### {icon} {category} ({len(by_category[category])})")
                
                for player in sorted(by_category[category], key=lambda x: x['username']):
                    col_name, col_weapon = st.columns([2, 2])
                    
                    with col_name:
                        st.write(f"**{player['username']}**")
                    
                    with col_weapon:
                        st.write(f"⚔️ {player['weapon_name']}")
                    
                    if player.get('notes'):
                        st.caption(f"📝 {player['notes']}")
                
                st.markdown("---")
        
        # Export
        if assignments:
            st.subheader("📤 Exporter")
            
            export_text = export_roster_to_text(enriched_assignments)
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                st.download_button(
                    label="📄 Télécharger (TXT)",
                    data=export_text,
                    file_name=f"roster_{activity.get('name', 'activity').replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col_export2:
                if st.button("📋 Copier pour Discord", use_container_width=True):
                    st.code(export_text, language="markdown")
                    st.info("💡 Copiez le texte ci-dessus et collez-le dans Discord !")
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")
