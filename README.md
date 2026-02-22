# Albion Zerg Manager

Application web de gestion de compositions de zergs pour Albion Online, construite avec Streamlit et Supabase.

## Description

Albion Zerg Manager permet aux guildes d'Albion Online de gérer efficacement leurs compositions de groupe pour les activités ZvZ (Zerg vs Zerg). Les ShotCallers peuvent créer des compositions d'armes, organiser des activités, et assigner les joueurs aux rôles appropriés.

## Fonctionnalités

### Pour les ShotCallers
- Créer et gérer des compositions de zerg (templates d'armes)
- Organiser des activités/events avec dates et compositions
- Voir les inscriptions des joueurs
- Assigner les joueurs aux armes pour constituer le roster
- Verrouiller et publier les rosters finaux

### Pour les Users (Joueurs)
- S'inscrire aux activités avec leurs armes préférées (ordre de priorité)
- Voir leurs assignations confirmées
- Consulter les rosters des activités
- Gérer leurs préférences d'armes

### Pour les Admins
- Gérer les utilisateurs et leurs rôles
- Maintenir la liste des armes disponibles
- Accès complet à toutes les fonctionnalités

## Technologies

- **Frontend**: Streamlit
- **Backend**: Supabase (PostgreSQL)
- **Authentification**: Supabase Auth
- **Déploiement**: Streamlit Cloud (frontend) + Supabase Cloud (backend)

## Installation Locale

### 🚀 Guide Rapide (5 minutes)

**Consultez le guide détaillé : [SETUP_LOCAL.md](SETUP_LOCAL.md)**

### Résumé des Étapes

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Créer un projet Supabase** (gratuit)
   - Allez sur [supabase.com](https://supabase.com)
   - Créez un nouveau projet
   - Exécutez le script `database/schema.sql` dans SQL Editor
   - Récupérez vos clés API (Settings > API)

3. **Configurer `.env`**
```bash
# Copiez le template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Éditez .env avec vos clés Supabase
```
**Voir [ENV_EXAMPLE.md](ENV_EXAMPLE.md) pour un exemple détaillé**

4. **Créer votre premier admin**
   - Créez un utilisateur dans Supabase Authentication
   - Exécutez la requête SQL pour créer le profil admin
   - (Détails dans [SETUP_LOCAL.md](SETUP_LOCAL.md))

5. **Vérifier la configuration**
```bash
python check_config.py
```

6. **Lancer l'application**
```bash
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

### ⚠️ Problèmes Courants

- **"Module not found"** : `pip install -r requirements.txt`
- **"SUPABASE_URL not found"** : Vérifiez le fichier `.env`
- **"Connection refused"** : Vérifiez vos clés API Supabase
- **"Table does not exist"** : Exécutez le script SQL

📖 **Guide complet** : [SETUP_LOCAL.md](SETUP_LOCAL.md)

## Structure du Projet

```
albion-zerg/
├── app.py                          # Point d'entrée Streamlit
├── requirements.txt                # Dépendances Python
├── .env.example                    # Template variables d'environnement
├── README.md                       # Ce fichier
├── .streamlit/
│   └── config.toml                # Configuration Streamlit
├── config/
│   └── supabase_config.py         # Configuration Supabase
├── auth/
│   ├── login.py                   # Page de connexion
│   ├── signup.py                  # Page d'inscription
│   └── session.py                 # Gestion des sessions
├── database/
│   ├── schema.sql                 # Schéma SQL complet
│   ├── weapons_data.py            # Données armes Albion
│   ├── models.py                  # Modèles de données
│   └── queries.py                 # Requêtes SQL
├── components/
│   ├── sidebar.py                 # Navigation
│   ├── role_guard.py              # Vérification permissions
│   ├── composition_card.py        # Affichage composition
│   ├── activity_card.py           # Affichage activité
│   └── weapon_selector.py         # Sélecteur d'armes
├── pages/
│   ├── dashboard.py               # Tableau de bord
│   ├── compositions.py            # Gestion compositions
│   ├── activities.py              # Gestion activités
│   ├── my_activities.py           # Mes inscriptions
│   ├── roster.py                  # Vue roster
│   └── admin/
│       ├── user_management.py     # Gestion utilisateurs
│       └── weapons_management.py  # Gestion armes
└── utils/
    ├── permissions.py             # Logique permissions
    ├── albion_constants.py        # Constantes Albion
    └── helpers.py                 # Utilitaires
```

## Déploiement

### Supabase

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Exécuter le script `database/schema.sql` dans l'éditeur SQL
3. Configurer les RLS policies (incluses dans le script)
4. Récupérer les clés API

### Streamlit Cloud

1. Push le code sur GitHub
2. Se connecter sur [streamlit.io/cloud](https://streamlit.io/cloud)
3. Créer une nouvelle app liée à votre repository
4. Ajouter les secrets dans les paramètres:
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
5. Déployer

## Configuration

### Rôles Utilisateurs

- **admin**: Accès complet, gestion des utilisateurs et armes
- **shotcaller**: Création de compositions et activités, assignation des joueurs
- **user**: Inscription aux activités, consultation des rosters

### Permissions

Les permissions sont gérées via Row Level Security (RLS) dans Supabase. Voir `database/schema.sql` pour les policies détaillées.

## Support

Pour toute question ou problème, ouvrez une issue sur le repository GitHub.

## Licence

MIT

## Contributeurs

Projet créé pour la communauté Albion Online.
