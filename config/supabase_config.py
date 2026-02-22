"""Configuration Supabase pour Albion Zerg Manager."""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class SupabaseConfig:
    """Classe de configuration Supabase."""
    
    _client: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """
        Obtenir le client Supabase (singleton).
        
        Returns:
            Client Supabase configuré
            
        Raises:
            ValueError: Si les variables d'environnement ne sont pas définies
        """
        if cls._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_ANON_KEY")
            
            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL et SUPABASE_ANON_KEY doivent être définis. "
                    "Vérifiez votre fichier .env"
                )
            
            cls._client = create_client(url, key)
        
        return cls._client
    
    @classmethod
    def get_service_client(cls) -> Client:
        """
        Obtenir un client Supabase avec service key (pour opérations admin).
        
        Returns:
            Client Supabase avec service key
            
        Raises:
            ValueError: Si la service key n'est pas définie
        """
        url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not service_key:
            raise ValueError(
                "SUPABASE_URL et SUPABASE_SERVICE_KEY doivent être définis "
                "pour les opérations admin"
            )
        
        return create_client(url, service_key)


# Instance globale du client
def get_supabase() -> Client:
    """
    Fonction helper pour obtenir le client Supabase.
    
    Returns:
        Client Supabase configuré
    """
    return SupabaseConfig.get_client()
