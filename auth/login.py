"""Page de connexion."""

import streamlit as st
from config.supabase_config import get_supabase
from database.queries import UserQueries
from auth.session import set_user_session, init_session_state


def show_login():
    """Afficher le formulaire de connexion."""
    init_session_state()
    
    st.title("🗡️ Albion Zerg Manager")
    st.subheader("Connexion")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="votre-email@exemple.com")
        password = st.text_input("Password", type="password", placeholder="Votre mot de passe")
        
        submit = st.form_submit_button("Se connecter", use_container_width=True)
        
        if submit:
            if not email or not password:
                st.error("❌ Veuillez remplir tous les champs.")
                return
            
            try:
                supabase = get_supabase()
                
                # Authentification avec Supabase
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if auth_response.user:
                    # Récupérer le profil utilisateur
                    profile = UserQueries.get_profile_by_id(auth_response.user.id)
                    
                    if not profile:
                        st.error("❌ Profil utilisateur introuvable. Contactez un administrateur.")
                        return
                    
                    if not profile.get("is_active"):
                        st.error("❌ Votre compte est désactivé. Contactez un administrateur.")
                        return
                    
                    # Définir la session
                    set_user_session(auth_response.user.model_dump(), profile)
                    
                    st.success(f"✅ Bienvenue, {profile.get('username')} !")
                    st.rerun()
                else:
                    st.error("❌ Identifiants incorrects.")
                    
            except Exception as e:
                st.error(f"❌ Erreur de connexion : {str(e)}")
    
    st.markdown("---")
    st.info("💡 Pas encore de compte ? Inscrivez-vous ci-dessous.")


def render_login_page():
    """Rendre la page de connexion complète."""
    show_login()
