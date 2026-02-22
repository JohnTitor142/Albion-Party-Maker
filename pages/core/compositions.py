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
    
    # Récupérer les armes
    try:
        weapons = WeaponQueries.get_all_weapons()
    except:
        weapons = []
    
    # Initialiser l'état de session pour les slots
    if 'composition_slots' not in st.session_state:
        st.session_state.composition_slots = {1: []}  # Groupe 1 par défaut avec liste vide de slots
    
    with st.form("create_composition"):
        name = st.text_input("Nom de la composition", placeholder="Ex: Zerg PvP Standard")
        description = st.text_area("Description", placeholder="Décrivez cette composition...")
        
        st.markdown("---")
        st.subheader("Définir les Groupes")
        
        # Sélecteur du nombre de groupes
        num_groups = st.number_input(
            "Nombre de groupes (1 groupe = max 20 joueurs)", 
            min_value=1, 
            max_value=5, 
            value=len(st.session_state.composition_slots),
            help="Un zerg Albion est constitué de groupes de 20 joueurs maximum"
        )
        
        # S'assurer que composition_slots a le bon nombre de groupes
        current_groups = list(st.session_state.composition_slots.keys())
        for g in range(1, int(num_groups) + 1):
            if g not in st.session_state.composition_slots:
                st.session_state.composition_slots[g] = []
        
        # Supprimer les groupes en trop
        for g in current_groups:
            if g > int(num_groups):
                del st.session_state.composition_slots[g]
        
        # Afficher les groupes avec tabs
        if int(num_groups) > 1:
            group_tabs = st.tabs([f"Groupe {i}" for i in range(1, int(num_groups) + 1)])
        else:
            group_tabs = [st.container()]
        
        all_slots_data = []
        
        for group_idx, tab in enumerate(group_tabs, start=1):
            with tab:
                st.markdown(f"### Groupe {group_idx}")
                
                # Nombre de slots pour ce groupe
                num_slots = st.number_input(
                    f"Nombre de types d'armes différents pour le groupe {group_idx}", 
                    min_value=1, 
                    max_value=20, 
                    value=max(1, len(st.session_state.composition_slots.get(group_idx, []))),
                    key=f"num_slots_g{group_idx}"
                )
                
                group_total = 0
                
                for slot_idx in range(int(num_slots)):
                    st.markdown(f"**Slot #{slot_idx + 1}**")
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        category = st.selectbox(
                            "Catégorie",
                            options=WEAPON_CATEGORIES,
                            key=f"slot_cat_g{group_idx}_s{slot_idx}"
                        )
                    
                    with col2:
                        # Afficher TOUTES les armes de cette catégorie
                        category_weapons = [w for w in weapons if w.get('category') == category]
                        
                        weapon_options = ["Any (toute arme de cette catégorie)"] + [
                            f"{w.get('name')}" for w in category_weapons
                        ]
                        
                        selected_weapon = st.selectbox(
                            "Arme spécifique",
                            options=weapon_options,
                            key=f"slot_weapon_g{group_idx}_s{slot_idx}"
                        )
                        
                        weapon_id = None
                        if selected_weapon != "Any (toute arme de cette catégorie)":
                            weapon_id = next(
                                (w['id'] for w in category_weapons if w.get('name') == selected_weapon), 
                                None
                            )
                    
                    with col3:
                        quantity = st.number_input(
                            "Quantité",
                            min_value=1,
                            max_value=20,
                            value=1,
                            key=f"slot_qty_g{group_idx}_s{slot_idx}"
                        )
                        group_total += quantity
                    
                    all_slots_data.append({
                        'category': category,
                        'weapon_id': weapon_id,
                        'quantity': quantity,
                        'group_number': group_idx
                    })
                
                # Afficher le total pour ce groupe
                if group_total > 20:
                    st.warning(f"⚠️ Total groupe {group_idx}: {group_total} joueurs (recommandé: max 20)")
                else:
                    st.info(f"Total groupe {group_idx}: {group_total} joueurs")
        
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
                    is_template=True,
                    total_groups=int(num_groups)
                )
                
                if composition:
                    # Créer tous les slots
                    for slot in all_slots_data:
                        CompositionQueries.create_slot(
                            composition_id=composition['id'],
                            weapon_id=slot['weapon_id'],
                            category=slot['category'],
                            quantity=slot['quantity'],
                            group_number=slot['group_number']
                        )
                    
                    st.success(f"✅ Composition '{name}' créée avec succès !")
                    st.balloons()
                    
                    # Réinitialiser l'état
                    st.session_state.composition_slots = {1: []}
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
