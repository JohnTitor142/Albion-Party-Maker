"""Page d'inscription."""

import streamlit as st
from config.supabase_config import get_supabase
from database.queries import UserQueries
from auth.session import set_user_session, init_session_state


def show_signup():
    """Afficher le formulaire d'inscription."""
    init_session_state()
    
    st.title("🗡️ Albion Zerg Manager")
    st.subheader("Inscription")
    
    with st.form("signup_form"):
        username = st.text_input("Nom d'utilisateur", placeholder="VotreNomDeJoueur")
        email = st.text_input("Email", placeholder="votre-email@exemple.com")
        password = st.text_input("Mot de passe", type="password", placeholder="Minimum 6 caractères")
        password_confirm = st.text_input("Confirmer le mot de passe", type="password")
        
        st.info("ℹ️ Après inscription, vous aurez le rôle 'User' par défaut.")
        
        submit = st.form_submit_button("S'inscrire", use_container_width=True)
        
        if submit:
            # Validations
            if not username or not email or not password or not password_confirm:
                st.error("❌ Veuillez remplir tous les champs.")
                return
            
            if len(username) < 3:
                st.error("❌ Le nom d'utilisateur doit contenir au moins 3 caractères.")
                return
            
            if len(password) < 6:
                st.error("❌ Le mot de passe doit contenir au moins 6 caractères.")
                return
            
            if password != password_confirm:
                st.error("❌ Les mots de passe ne correspondent pas.")
                return
            
            try:
                supabase = get_supabase()
                
                # Vérifier si le username existe déjà
                existing_profile = supabase.table("users_profiles").select("username").eq("username", username).execute()
                if existing_profile.data:
                    st.error(f"❌ Le nom d'utilisateur '{username}' est déjà pris.")
                    return
                
                # Créer le compte Supabase Auth
                auth_response = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    # Créer le profil utilisateur
                    profile = UserQueries.create_profile(
                        user_id=auth_response.user.id,
                        email=email,
                        username=username,
                        role="user"
                    )
                    
                    if profile:
                        st.success(f"✅ Compte créé avec succès ! Bienvenue, {username} !")
                        
                        # Connecter automatiquement l'utilisateur
                        set_user_session(auth_response.user.model_dump(), profile)
                        st.rerun()
                    else:
                        st.error("❌ Erreur lors de la création du profil.")
                else:
                    st.error("❌ Erreur lors de la création du compte.")
                    
            except Exception as e:
                error_msg = str(e)
                if "already registered" in error_msg.lower():
                    st.error("❌ Cet email est déjà utilisé.")
                elif "invalid email" in error_msg.lower():
                    st.error("❌ Email invalide.")
                else:
                    st.error(f"❌ Erreur d'inscription : {error_msg}")
    
    st.markdown("---")
    st.info("💡 Vous avez déjà un compte ? Connectez-vous ci-dessus.")


def render_signup_page():
    """Rendre la page d'inscription complète."""
    show_signup()
