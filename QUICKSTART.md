# Guide de Démarrage Rapide

## Installation Locale (Développement)

### 1. Cloner le projet
```bash
cd albion-zerg
```

### 2. Créer un environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer Supabase
1. Créez un compte sur https://supabase.com
2. Créez un nouveau projet
3. Exécutez le script `database/schema.sql` dans l'éditeur SQL de Supabase
4. Récupérez vos clés API (Settings > API)

### 5. Configurer les variables d'environnement
```bash
# Copier le template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Éditez .env avec vos vraies valeurs Supabase
```

### 6. Créer votre premier admin
Dans Supabase SQL Editor :
```sql
-- 1. Créez un utilisateur dans Authentication > Users
-- 2. Puis exécutez (remplacez les valeurs) :
INSERT INTO users_profiles (id, email, username, role, is_active)
VALUES ('USER_UID_FROM_AUTH', 'votre@email.com', 'Admin', 'admin', true);
```

### 7. Lancer l'application
```bash
streamlit run app.py
```

L'application sera accessible sur http://localhost:8501

## Structure du Projet

```
albion-zerg/
├── app.py                 # Point d'entrée principal
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement (local)
├── .env.example          # Template des variables
├── README.md             # Documentation principale
├── DEPLOYMENT.md         # Guide de déploiement
├── QUICKSTART.md         # Ce fichier
│
├── .streamlit/
│   └── config.toml       # Configuration Streamlit (thème)
│
├── auth/                 # Module d'authentification
│   ├── login.py         # Page de connexion
│   ├── signup.py        # Page d'inscription
│   └── session.py       # Gestion des sessions
│
├── config/              # Configuration
│   └── supabase_config.py
│
├── database/            # Base de données
│   ├── schema.sql      # Schéma SQL complet
│   ├── models.py       # Modèles Pydantic
│   └── queries.py      # Requêtes SQL
│
├── components/          # Composants réutilisables
│   ├── sidebar.py      # Navigation
│   ├── role_guard.py   # Vérification permissions
│   ├── composition_card.py
│   ├── activity_card.py
│   └── weapon_selector.py
│
├── pages/              # Pages de l'application
│   ├── dashboard.py
│   ├── compositions.py
│   ├── activities.py
│   ├── my_activities.py
│   ├── roster.py
│   └── admin/
│       ├── user_management.py
│       └── weapons_management.py
│
└── utils/              # Utilitaires
    ├── permissions.py
    ├── albion_constants.py
    └── helpers.py
```

## Workflow Typique

### En tant qu'Admin
1. Créer des ShotCallers (Admin - Users)
2. Gérer les armes disponibles (Admin - Armes)
3. Superviser les activités

### En tant que ShotCaller
1. Créer des compositions de zerg (Compositions)
   - Ex: "5 Tanks, 10 Healers, 25 DPS"
2. Créer des activités basées sur ces compositions (Activités)
   - Ex: "ZvZ Samedi 20h"
3. Gérer les inscriptions et assigner les joueurs (Activités > Gérer)
4. Verrouiller le roster final

### En tant que User (Joueur)
1. S'inscrire aux activités ouvertes (Mes Inscriptions)
2. Sélectionner 1-3 armes par ordre de préférence
3. Consulter son assignation finale (Mes Assignations)
4. Voir le roster complet (Rosters)

## Commandes Utiles

### Lancer l'app en mode développement
```bash
streamlit run app.py
```

### Mettre à jour les dépendances
```bash
pip install -r requirements.txt --upgrade
```

### Générer requirements.txt (si vous ajoutez des packages)
```bash
pip freeze > requirements.txt
```

### Vérifier la connexion Supabase
Testez dans un terminal Python :
```python
from config.supabase_config import get_supabase
client = get_supabase()
print("Connexion OK!")
```

## Dépannage Rapide

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur "SUPABASE_URL not found"
Vérifiez que le fichier `.env` existe et contient vos clés.

### Erreur "Connection refused"
1. Vérifiez que Supabase est accessible
2. Vérifiez vos clés API dans `.env`
3. Vérifiez que le projet Supabase est actif

### L'app ne démarre pas
```bash
# Redémarrez avec le mode verbose
streamlit run app.py --logger.level=debug
```

## Prochaines Étapes

1. ✅ Installation locale terminée
2. 📖 Lisez le [README.md](README.md) pour plus de détails
3. 🚀 Consultez [DEPLOYMENT.md](DEPLOYMENT.md) pour déployer en production
4. 🎮 Commencez à organiser vos zergs !

## Support

Des questions ? Créez une issue sur GitHub ou consultez :
- [Documentation Supabase](https://supabase.com/docs)
- [Documentation Streamlit](https://docs.streamlit.io)

Bon jeu ! 🗡️
