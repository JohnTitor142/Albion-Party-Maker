"""Page de gestion des utilisateurs (Admin)."""

import streamlit as st
from auth.session import require_role, get_user_id
from database.models import UserRole
from database.queries import UserQueries
from utils.helpers import format_datetime


def render_user_management_page():
    """Page de gestion des utilisateurs (Admin uniquement)."""
    require_role(UserRole.ADMIN)
    
    st.title("👥 Gestion des Utilisateurs")
    
    try:
        # Récupérer tous les utilisateurs
        users = UserQueries.get_all_users()
        
        if not users:
            st.info("Aucun utilisateur trouvé.")
            return
        
        # Filtres
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            role_filter = st.selectbox(
                "Filtrer par rôle",
                options=["Tous", "admin", "shotcaller", "user"]
            )
        
        with col_filter2:
            status_filter = st.selectbox(
                "Filtrer par statut",
                options=["Tous", "Actif", "Inactif"]
            )
        
        with col_filter3:
            sort_by = st.selectbox(
                "Trier par",
                options=["Nom", "Date création", "Rôle"]
            )
        
        # Appliquer les filtres
        filtered_users = users
        
        if role_filter != "Tous":
            filtered_users = [u for u in filtered_users if u.get('role') == role_filter]
        
        if status_filter == "Actif":
            filtered_users = [u for u in filtered_users if u.get('is_active') == True]
        elif status_filter == "Inactif":
            filtered_users = [u for u in filtered_users if u.get('is_active') == False]
        
        # Trier
        if sort_by == "Nom":
            filtered_users = sorted(filtered_users, key=lambda x: x.get('username', ''))
        elif sort_by == "Date création":
            filtered_users = sorted(filtered_users, key=lambda x: x.get('created_at', ''), reverse=True)
        elif sort_by == "Rôle":
            filtered_users = sorted(filtered_users, key=lambda x: x.get('role', ''))
        
        st.markdown(f"**{len(filtered_users)} utilisateur(s)**")
        st.markdown("---")
        
        # Afficher les utilisateurs
        for user in filtered_users:
            render_user_card(user)
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_user_card(user: dict):
    """Afficher une carte utilisateur."""
    role_emoji = {
        "admin": "👑",
        "shotcaller": "📣",
        "user": "⚔️"
    }
    
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            emoji = role_emoji.get(user.get('role'), '⚔️')
            st.markdown(f"**{emoji} {user.get('username')}**")
            st.caption(user.get('email'))
        
        with col2:
            role = user.get('role', 'user')
            st.markdown(f"**Rôle:** {role.title()}")
        
        with col3:
            is_active = user.get('is_active', False)
            if is_active:
                st.success("✅ Actif")
            else:
                st.error("❌ Inactif")
        
        with col4:
            created = user.get('created_at')
            if created:
                st.caption(f"Créé le {format_datetime(created, '%d/%m/%Y')}")
        
        # Actions
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button("✏️ Modifier rôle", key=f"edit_role_{user['id']}", use_container_width=True):
                show_edit_role_form(user)
        
        with col_act2:
            current_status = user.get('is_active', False)
            action_label = "🔒 Désactiver" if current_status else "✅ Activer"
            
            if st.button(action_label, key=f"toggle_status_{user['id']}", use_container_width=True):
                try:
                    UserQueries.update_profile(user['id'], {'is_active': not current_status})
                    st.toast(f"✅ Statut mis à jour pour {user.get('username')}", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
        
        with col_act3:
            with st.expander("📊 Stats"):
                st.caption("Statistiques à venir...")
        
        st.markdown("---")


def show_edit_role_form(user: dict):
    """Formulaire de modification du rôle."""
    with st.form(f"edit_role_form_{user['id']}"):
        st.subheader(f"Modifier le rôle de {user.get('username')}")
        
        current_role = user.get('role', 'user')
        
        new_role = st.selectbox(
            "Nouveau rôle",
            options=["user", "shotcaller", "admin"],
            index=["user", "shotcaller", "admin"].index(current_role)
        )
        
        st.warning("⚠️ Attention : Modifier le rôle d'un utilisateur lui donne ou retire des permissions.")
        
        submit = st.form_submit_button("💾 Enregistrer", use_container_width=True)
        
        if submit:
            if new_role == current_role:
                st.info("Aucun changement à apporter.")
                return
            
            try:
                UserQueries.update_profile(user['id'], {'role': new_role})
                st.toast(f"✅ Rôle mis à jour: {new_role}", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
