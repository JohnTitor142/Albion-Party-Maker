# Guide de Déploiement - Albion Zerg Manager

Ce guide vous accompagne pas à pas pour déployer l'application sur Streamlit Cloud avec Supabase comme backend.

## 🎯 Vue d'Ensemble

L'application sera déployée sur deux plateformes :
- **Frontend** : Streamlit Cloud (gratuit)
- **Backend/BDD** : Supabase (gratuit)

## 📋 Prérequis

- Compte GitHub (gratuit)
- Compte Supabase (gratuit) : https://supabase.com
- Compte Streamlit Cloud (gratuit) : https://streamlit.io/cloud

---

## Étape 1 : Configuration de Supabase

### 1.1 Créer un Projet Supabase

1. Allez sur https://supabase.com et connectez-vous
2. Cliquez sur "New Project"
3. Remplissez les informations :
   - **Name** : `albion-zerg-manager` (ou autre nom)
   - **Database Password** : Créez un mot de passe fort et **sauvegardez-le**
   - **Region** : Choisissez la région la plus proche (ex: Europe West pour la France)
   - **Pricing Plan** : Free
4. Cliquez sur "Create new project"
5. Attendez quelques minutes que le projet soit créé

### 1.2 Exécuter le Script SQL

1. Dans votre projet Supabase, allez dans l'onglet **SQL Editor** (icône `</>` dans le menu gauche)
2. Cliquez sur "New query"
3. Copiez **tout** le contenu du fichier `database/schema.sql` de votre projet
4. Collez-le dans l'éditeur SQL
5. Cliquez sur **"Run"** (ou appuyez sur Ctrl+Enter)
6. Vérifiez qu'il n'y a pas d'erreur (vous devriez voir "Success. No rows returned")

### 1.3 Récupérer les Clés API

1. Allez dans **Settings** > **API** (icône engrenage dans le menu gauche)
2. Notez les valeurs suivantes (vous en aurez besoin) :
   - **Project URL** : `https://xxxxx.supabase.co`
   - **anon public** key : `eyJhbGc...` (longue chaîne)
   - **service_role** key : `eyJhbGc...` (longue chaîne, **à garder secrète**)

### 1.4 Créer votre Premier Utilisateur Admin

1. Allez dans **Authentication** > **Users**
2. Cliquez sur "Add user" > "Create new user"
3. Remplissez :
   - **Email** : Votre email
   - **Password** : Votre mot de passe
   - **Auto Confirm User** : ✅ (cochez la case)
4. Cliquez sur "Create user"
5. **Important** : Notez l'**User UID** (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 1.5 Configurer le Premier Admin

1. Retournez dans **SQL Editor**
2. Exécutez cette requête (remplacez `VOTRE_USER_ID` et `VOTRE_EMAIL`) :

```sql
-- Créer le profil admin
INSERT INTO users_profiles (id, email, username, role, is_active)
VALUES (
    'VOTRE_USER_ID',  -- Remplacez par l'UID de l'étape 1.4
    'votre@email.com',  -- Remplacez par votre email
    'Admin',  -- Remplacez par le nom d'utilisateur souhaité
    'admin',
    true
);
```

3. Cliquez sur "Run"
4. Votre premier compte admin est créé ! 🎉

---

## Étape 2 : Pousser le Code sur GitHub

### 2.1 Initialiser Git (si pas déjà fait)

Ouvrez un terminal dans le dossier du projet :

```bash
git init
git add .
git commit -m "Initial commit - Albion Zerg Manager"
```

### 2.2 Créer un Repository GitHub

1. Allez sur https://github.com
2. Cliquez sur le bouton **"+"** en haut à droite > **"New repository"**
3. Remplissez :
   - **Repository name** : `albion-zerg-manager`
   - **Visibility** : Public ou Private (au choix)
4. Cliquez sur "Create repository"
5. Suivez les instructions pour pousser votre code :

```bash
git remote add origin https://github.com/VOTRE_USERNAME/albion-zerg-manager.git
git branch -M main
git push -u origin main
```

---

## Étape 3 : Déployer sur Streamlit Cloud

### 3.1 Connecter Streamlit à GitHub

1. Allez sur https://streamlit.io/cloud
2. Connectez-vous avec votre compte GitHub
3. Autorisez Streamlit à accéder à vos repositories

### 3.2 Créer une Nouvelle App

1. Cliquez sur "New app"
2. Remplissez :
   - **Repository** : Sélectionnez `VOTRE_USERNAME/albion-zerg-manager`
   - **Branch** : `main`
   - **Main file path** : `app.py`
3. Cliquez sur "Advanced settings..."

### 3.3 Configurer les Secrets

Dans la section **Secrets**, collez ce contenu (remplacez par vos vraies valeurs) :

```toml
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGc..."
SUPABASE_SERVICE_KEY = "eyJhbGc..."
```

**⚠️ Important :**
- Utilisez les valeurs récupérées à l'Étape 1.3
- Ne partagez JAMAIS votre `SUPABASE_SERVICE_KEY` publiquement

### 3.4 Déployer

1. Cliquez sur "Deploy!"
2. Attendez quelques minutes que l'application démarre
3. Votre app sera accessible à : `https://votre-app.streamlit.app`

---

## Étape 4 : Premier Lancement

### 4.1 Tester la Connexion

1. Ouvrez l'URL de votre application
2. Connectez-vous avec l'email et le mot de passe que vous avez créés à l'Étape 1.4
3. Vous devriez voir le dashboard avec le rôle "Admin" 👑

### 4.2 Vérifier les Armes

1. Allez dans **Admin - Armes** dans le menu
2. Vous devriez voir toutes les armes d'Albion Online pré-remplies
3. Si ce n'est pas le cas, vérifiez que le script SQL s'est bien exécuté

---

## 🔧 Dépannage

### Problème : "Module not found"

**Solution** : Vérifiez que le fichier `requirements.txt` est bien poussé sur GitHub et contient toutes les dépendances.

### Problème : "Connection refused" ou erreur Supabase

**Solutions** :
1. Vérifiez que vos clés API sont correctes dans les secrets Streamlit
2. Vérifiez que votre projet Supabase est bien actif
3. Vérifiez que les policies RLS sont bien activées (dans le script SQL)

### Problème : "Unauthorized" ou "Permission denied"

**Solutions** :
1. Vérifiez que votre utilisateur a bien le rôle `admin` dans la table `users_profiles`
2. Exécutez cette requête SQL dans Supabase pour vérifier :

```sql
SELECT * FROM users_profiles WHERE email = 'votre@email.com';
```

### Problème : L'application ne démarre pas

**Solutions** :
1. Vérifiez les logs dans Streamlit Cloud (bouton "Manage app" > "Logs")
2. Vérifiez que tous les fichiers sont bien présents sur GitHub
3. Redémarrez l'application (bouton "Reboot app")

---

## 🎉 C'est Terminé !

Votre application Albion Zerg Manager est maintenant en ligne et accessible !

### Prochaines Étapes

1. **Inviter des utilisateurs** : Partagez le lien de l'application
2. **Créer des ShotCallers** : Allez dans Admin - Users pour promouvoir des utilisateurs
3. **Créer des compositions** : Les ShotCallers peuvent créer des templates de zerg
4. **Organiser des activités** : Créez votre premier ZvZ !

### Partager l'Application

Partagez simplement l'URL : `https://votre-app.streamlit.app`

Les nouveaux utilisateurs peuvent s'inscrire directement via l'onglet "Inscription".

---

## 📊 Limites du Plan Gratuit

### Supabase Free Tier :
- ✅ 500 MB de base de données (largement suffisant pour ~100 utilisateurs)
- ✅ 2 GB de bande passante/mois
- ✅ 50,000 utilisateurs auth
- ✅ Pas de limite de durée

### Streamlit Cloud Free :
- ✅ 1 app publique
- ✅ 1 GB de RAM
- ⚠️ L'app se met en veille après 7 jours d'inactivité (redémarre au premier accès)
- ✅ Pas de limite de visiteurs

**Pour 40 utilisateurs : Les plans gratuits sont parfaits ! 🎯**

---

## 🔐 Sécurité

### Bonnes Pratiques

1. **Ne jamais** commit le fichier `.env` dans Git (il est dans `.gitignore`)
2. **Ne jamais** partager votre `SUPABASE_SERVICE_KEY` publiquement
3. Activez la vérification d'email dans Supabase si besoin (Settings > Auth)
4. Changez régulièrement votre mot de passe admin
5. Surveillez les utilisateurs créés dans Supabase Dashboard

### Backup

Supabase fait des backups automatiques, mais vous pouvez aussi :
1. Aller dans **Database** > **Backups**
2. Télécharger un backup manuel si besoin

---

## 🚀 Upgrades Payants (Optionnel)

Si vous dépassez 40-50 utilisateurs actifs :

### Supabase Pro ($25/mois)
- 8 GB de DB
- 100 GB de bande passante
- Support prioritaire

### Streamlit Cloud Team ($20/mois)
- 3 apps privées
- Ressources accrues
- Support

**Total : ~$45/mois pour 100+ utilisateurs**

---

## 🆘 Support

- **Documentation Supabase** : https://supabase.com/docs
- **Documentation Streamlit** : https://docs.streamlit.io
- **Issues GitHub** : Créez une issue sur votre repository

Bon jeu sur Albion Online ! 🗡️⚔️🏹
