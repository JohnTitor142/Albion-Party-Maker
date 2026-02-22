"""
Script de vérification de la configuration
Exécutez ce script pour tester votre configuration avant de lancer l'app
"""

import sys
import os

def check_env_file():
    """Vérifier que le fichier .env existe et contient les clés."""
    print("🔍 Vérification du fichier .env...")
    
    if not os.path.exists('.env'):
        print("❌ Le fichier .env n'existe pas !")
        print("   ➡️ Copiez .env.example vers .env")
        return False
    
    print("✅ Le fichier .env existe")
    
    # Vérifier le contenu
    with open('.env', 'r') as f:
        content = f.read()
    
    required_keys = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_KEY']
    missing_keys = []
    
    for key in required_keys:
        if f'{key}=' not in content or f'{key}=\n' in content or f'{key}= ' in content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Clés manquantes ou vides : {', '.join(missing_keys)}")
        print("   ➡️ Remplissez ces clés dans .env avec vos valeurs Supabase")
        return False
    
    print("✅ Toutes les clés sont présentes")
    return True


def check_dependencies():
    """Vérifier que les dépendances sont installées."""
    print("\n🔍 Vérification des dépendances...")
    
    required_modules = [
        'streamlit',
        'supabase',
        'dotenv',
        'pandas',
        'plotly',
        'pydantic',
        'streamlit_option_menu'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        module_name = 'python-dotenv' if module == 'dotenv' else module
        module_name = 'streamlit-option-menu' if module == 'streamlit_option_menu' else module_name
        
        try:
            if module == 'dotenv':
                import dotenv
            elif module == 'streamlit_option_menu':
                import streamlit_option_menu
            else:
                __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module_name)
            print(f"   ❌ {module_name}")
    
    if missing_modules:
        print(f"\n❌ Modules manquants : {', '.join(missing_modules)}")
        print("   ➡️ Installez-les avec : pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True


def check_supabase_connection():
    """Vérifier la connexion à Supabase."""
    print("\n🔍 Vérification de la connexion Supabase...")
    
    try:
        from config.supabase_config import get_supabase
        client = get_supabase()
        print("✅ Connexion Supabase réussie !")
        return True
    except ValueError as e:
        print(f"❌ Erreur de configuration : {str(e)}")
        print("   ➡️ Vérifiez vos clés dans .env")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion : {str(e)}")
        print("   ➡️ Vérifiez que votre projet Supabase est actif")
        return False


def check_database_tables():
    """Vérifier que les tables existent."""
    print("\n🔍 Vérification des tables de la base de données...")
    
    try:
        from config.supabase_config import get_supabase
        client = get_supabase()
        
        # Essayer de requêter une table simple
        response = client.table('weapons').select('id').limit(1).execute()
        
        print("✅ Les tables de la base de données existent")
        print(f"   ℹ️ Nombre d'armes trouvées : {len(response.data) if response.data else 0}")
        
        if not response.data:
            print("   ⚠️ Aucune arme trouvée - Le script SQL a-t-il été exécuté ?")
        
        return True
    except Exception as e:
        print(f"❌ Les tables n'existent pas ou sont inaccessibles")
        print(f"   Erreur : {str(e)}")
        print("   ➡️ Exécutez le script database/schema.sql dans Supabase SQL Editor")
        return False


def main():
    """Fonction principale."""
    print("=" * 60)
    print("🚀 VÉRIFICATION DE LA CONFIGURATION - Albion Zerg Manager")
    print("=" * 60)
    
    checks = [
        ("Fichier .env", check_env_file),
        ("Dépendances Python", check_dependencies),
        ("Connexion Supabase", check_supabase_connection),
        ("Tables de la base", check_database_tables)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erreur inattendue lors de '{name}' : {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    all_ok = True
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    print("=" * 60)
    
    if all_ok:
        print("\n🎉 TOUT EST PRÊT !")
        print("   Lancez l'application avec : streamlit run app.py")
        return 0
    else:
        print("\n⚠️ CONFIGURATION INCOMPLÈTE")
        print("   Corrigez les erreurs ci-dessus avant de lancer l'app")
        print("\n📖 Consultez SETUP_LOCAL.md pour un guide détaillé")
        return 1


if __name__ == "__main__":
    sys.exit(main())
