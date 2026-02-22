"""Page de gestion des compositions (ShotCaller)."""

import streamlit as st
from auth.session import require_role, get_user_id
from database.models import UserRole
from database.queries import CompositionQueries, WeaponQueries
from components.composition_card import render_composition_card
from components.weapon_selector import render_weapon_selector
from utils.albion_constants import WEAPON_CATEGORIES


def render_compositions_page():
    """Page de gestion des compositions."""
    require_role(UserRole.SHOTCALLER)
    
    st.title("🧩 Gestion des Compositions")
    
    user_id = get_user_id()
    
    # Tabs
    tab_list, tab_create = st.tabs(["📋 Mes Compositions", "➕ Créer"])
    
    with tab_list:
        render_compositions_list(user_id)
    
    with tab_create:
        render_create_composition(user_id)


def render_compositions_list(user_id: str):
    """Afficher la liste des compositions."""
    st.subheader("Mes Compositions")
    
    try:
        compositions = CompositionQueries.get_all_compositions(created_by=user_id)
        
        if not compositions:
            st.info("Vous n'avez pas encore créé de composition. Utilisez l'onglet 'Créer' !")
            return
        
        for composition in compositions:
            slots = CompositionQueries.get_slots_by_composition(composition['id'])
            
            render_composition_card(
                composition, 
                slots,
                show_actions=True,
                on_edit=lambda c: edit_composition(c),
                on_delete=lambda c: delete_composition(c)
            )
    
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des compositions : {str(e)}")


def render_create_composition(user_id: str):
    """Formulaire de création de composition."""
    st.subheader("Créer une Nouvelle Composition")
    
    with st.form("create_composition"):
        name = st.text_input("Nom de la composition", placeholder="Ex: Zerg PvP Standard")
        description = st.text_area("Description", placeholder="Décrivez cette composition...")
        
        st.markdown("---")
        st.subheader("Définir les Slots")
        
        # Récupérer les armes
        try:
            weapons = WeaponQueries.get_all_weapons()
        except:
            weapons = []
        
        # Nombre de slots à créer
        num_slots = st.number_input("Nombre de slots différents", min_value=1, max_value=10, value=3)
        
        slots_data = []
        
        for i in range(int(num_slots)):
            st.markdown(f"**Slot #{i+1}**")
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                category = st.selectbox(
                    "Catégorie",
                    options=WEAPON_CATEGORIES,
                    key=f"slot_cat_{i}"
                )
            
            with col2:
                # Filtrer les armes par catégorie
                category_weapons = [w for w in weapons if w.get('category') == category]
                
                weapon_options = ["Any (toute arme de cette catégorie)"] + [w.get('name') for w in category_weapons]
                selected_weapon = st.selectbox(
                    "Arme spécifique",
                    options=weapon_options,
                    key=f"slot_weapon_{i}"
                )
                
                weapon_id = None
                if selected_weapon != "Any (toute arme de cette catégorie)":
                    weapon_id = next((w['id'] for w in category_weapons if w.get('name') == selected_weapon), None)
            
            with col3:
                quantity = st.number_input(
                    "Quantité",
                    min_value=1,
                    max_value=40,
                    value=5,
                    key=f"slot_qty_{i}"
                )
            
            slots_data.append({
                'category': category,
                'weapon_id': weapon_id,
                'quantity': quantity
            })
        
        submit = st.form_submit_button("✅ Créer la Composition", use_container_width=True)
        
        if submit:
            if not name:
                st.error("❌ Le nom est obligatoire.")
                return
            
            try:
                # Créer la composition
                composition = CompositionQueries.create_composition(
                    name=name,
                    description=description,
                    created_by=user_id,
                    is_template=True
                )
                
                if composition:
                    # Créer les slots
                    for slot in slots_data:
                        CompositionQueries.create_slot(
                            composition_id=composition['id'],
                            weapon_id=slot['weapon_id'],
                            category=slot['category'],
                            quantity=slot['quantity']
                        )
                    
                    st.success(f"✅ Composition '{name}' créée avec succès !")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de la création de la composition.")
            
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")


def edit_composition(composition: dict):
    """Éditer une composition (placeholder)."""
    st.info(f"🚧 Édition de '{composition.get('name')}' - Fonctionnalité à venir !")


def delete_composition(composition: dict):
    """Supprimer une composition."""
    if st.session_state.get(f"confirm_delete_{composition['id']}", False):
        try:
            success = CompositionQueries.delete_composition(composition['id'])
            if success:
                st.success(f"✅ Composition '{composition.get('name')}' supprimée.")
                del st.session_state[f"confirm_delete_{composition['id']}"]
                st.rerun()
            else:
                st.error("❌ Erreur lors de la suppression.")
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
    else:
        st.warning(f"⚠️ Êtes-vous sûr de vouloir supprimer '{composition.get('name')}' ?")
        if st.button("Confirmer la suppression", key=f"confirm_{composition['id']}"):
            st.session_state[f"confirm_delete_{composition['id']}"] = True
            st.rerun()
