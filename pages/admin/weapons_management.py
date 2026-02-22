"""Page de gestion des armes (Admin)."""

import streamlit as st
from auth.session import require_role
from database.models import UserRole
from database.queries import WeaponQueries
from utils.albion_constants import WEAPON_CATEGORIES, CATEGORY_ICONS


def render_weapons_management_page():
    """Page de gestion des armes (Admin uniquement)."""
    require_role(UserRole.ADMIN)
    
    st.title("⚔️ Gestion des Armes")
    
    # Tabs
    tab_list, tab_create = st.tabs(["📋 Toutes les Armes", "➕ Ajouter"])
    
    with tab_list:
        render_weapons_list()
    
    with tab_create:
        render_create_weapon()


def render_weapons_list():
    """Afficher la liste des armes."""
    st.subheader("Liste des Armes")
    
    try:
        # Récupérer toutes les armes (actives et inactives)
        weapons = WeaponQueries.get_all_weapons(is_active=None)
        
        if not weapons:
            st.info("Aucune arme trouvée. Utilisez l'onglet 'Ajouter' pour en créer.")
            return
        
        # Filtres
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            category_filter = st.selectbox(
                "Filtrer par catégorie",
                options=["Toutes"] + WEAPON_CATEGORIES
            )
        
        with col_filter2:
            status_filter = st.selectbox(
                "Filtrer par statut",
                options=["Tous", "Actif", "Inactif"]
            )
        
        with col_filter3:
            sort_by = st.selectbox(
                "Trier par",
                options=["Nom", "Catégorie"]
            )
        
        # Appliquer les filtres
        filtered_weapons = weapons
        
        if category_filter != "Toutes":
            filtered_weapons = [w for w in filtered_weapons if w.get('category') == category_filter]
        
        if status_filter == "Actif":
            filtered_weapons = [w for w in filtered_weapons if w.get('is_active') == True]
        elif status_filter == "Inactif":
            filtered_weapons = [w for w in filtered_weapons if w.get('is_active') == False]
        
        # Trier
        if sort_by == "Nom":
            filtered_weapons = sorted(filtered_weapons, key=lambda x: x.get('name', ''))
        elif sort_by == "Catégorie":
            filtered_weapons = sorted(filtered_weapons, key=lambda x: (x.get('category', ''), x.get('name', '')))
        
        st.markdown(f"**{len(filtered_weapons)} arme(s)**")
        st.markdown("---")
        
        # Afficher les armes
        from utils.helpers import group_by_category
        
        grouped = group_by_category(filtered_weapons)
        
        for category in sorted(grouped.keys()):
            icon = CATEGORY_ICONS.get(category, "⚔️")
            
            with st.expander(f"{icon} **{category}** ({len(grouped[category])})", expanded=True):
                for weapon in sorted(grouped[category], key=lambda x: x.get('name', '')):
                    render_weapon_card(weapon)
    
    except Exception as e:
        st.error(f"❌ Erreur : {str(e)}")


def render_weapon_card(weapon: dict):
    """Afficher une carte d'arme."""
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"**{weapon.get('name')}**")
        if weapon.get('tier'):
            st.caption(f"Tier {weapon.get('tier')}")
    
    with col2:
        is_active = weapon.get('is_active', False)
        if is_active:
            st.success("✅ Actif")
        else:
            st.error("❌ Inactif")
    
    with col3:
        if st.button("✏️", key=f"edit_{weapon['id']}", help="Éditer"):
            show_edit_weapon_form(weapon)
    
    with col4:
        current_status = weapon.get('is_active', False)
        action_label = "❌" if current_status else "✅"
        
        if st.button(action_label, key=f"toggle_{weapon['id']}", help="Changer statut"):
            try:
                WeaponQueries.update_weapon(weapon['id'], {'is_active': not current_status})
                st.success(f"✅ Statut mis à jour pour {weapon.get('name')}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
    
    st.markdown("---")


def render_create_weapon():
    """Formulaire de création d'arme."""
    st.subheader("Ajouter une Nouvelle Arme")
    
    with st.form("create_weapon"):
        name = st.text_input("Nom de l'arme", placeholder="Ex: Great Axe")
        
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Catégorie", options=WEAPON_CATEGORIES)
        
        with col2:
            tier = st.selectbox("Tier (optionnel)", options=["---", "4", "5", "6", "7", "8"])
            tier_value = None if tier == "---" else int(tier)
        
        icon_url = st.text_input("URL de l'icône (optionnel)", placeholder="https://...")
        
        submit = st.form_submit_button("✅ Ajouter l'Arme", use_container_width=True)
        
        if submit:
            if not name or not category:
                st.error("❌ Le nom et la catégorie sont obligatoires.")
                return
            
            try:
                weapon = WeaponQueries.create_weapon(
                    name=name,
                    category=category,
                    tier=tier_value
                )
                
                if weapon:
                    st.success(f"✅ Arme '{name}' ajoutée avec succès !")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'ajout de l'arme.")
            
            except Exception as e:
                if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                    st.error(f"❌ Une arme nommée '{name}' existe déjà.")
                else:
                    st.error(f"❌ Erreur : {str(e)}")


def show_edit_weapon_form(weapon: dict):
    """Formulaire d'édition d'arme."""
    with st.form(f"edit_weapon_form_{weapon['id']}"):
        st.subheader(f"Modifier : {weapon.get('name')}")
        
        new_name = st.text_input("Nom", value=weapon.get('name', ''))
        new_category = st.selectbox(
            "Catégorie",
            options=WEAPON_CATEGORIES,
            index=WEAPON_CATEGORIES.index(weapon.get('category')) if weapon.get('category') in WEAPON_CATEGORIES else 0
        )
        
        current_tier = weapon.get('tier')
        tier_options = ["---", "4", "5", "6", "7", "8"]
        tier_index = 0 if not current_tier else tier_options.index(str(current_tier))
        
        new_tier = st.selectbox("Tier", options=tier_options, index=tier_index)
        new_tier_value = None if new_tier == "---" else int(new_tier)
        
        submit = st.form_submit_button("💾 Enregistrer", use_container_width=True)
        
        if submit:
            try:
                updates = {
                    'name': new_name,
                    'category': new_category,
                    'tier': new_tier_value
                }
                
                WeaponQueries.update_weapon(weapon['id'], updates)
                st.success(f"✅ Arme '{new_name}' mise à jour !")
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
