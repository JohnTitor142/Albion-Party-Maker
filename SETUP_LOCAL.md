# 🚀 Guide de Démarrage Rapide - Configuration Locale

## ✅ Problème Résolu

L'erreur d'import a été corrigée ! Maintenant il faut juste configurer Supabase.

---

## 📋 Étapes à Suivre (5 minutes)

### Étape 1 : Créer un Projet Supabase

1. **Allez sur https://supabase.com**
2. Cliquez sur **"Start your project"** (ou "Sign in" si vous avez déjà un compte)
3. Connectez-vous avec GitHub
4. Cliquez sur **"New Project"**
5. Remplissez :
   - **Name** : `albion-zerg-test`
   - **Database Password** : Créez un mot de passe fort (ex: `MonMotDePasse123!`)
   - **Region** : Europe West (Frankfurt ou London)
   - **Pricing Plan** : Free
6. Cliquez sur **"Create new project"**
7. ⏳ **Attendez 2-3 minutes** que le projet soit créé

---

### Étape 2 : Récupérer vos Clés API

Une fois le projet créé :

1. Dans le menu de gauche, cliquez sur **Settings** (icône ⚙️)
2. Cliquez sur **API**
3. Vous verrez :

**Project URL** (en haut de la page)
```
https://xxxxxxxxxxxxx.supabase.co
```

**API Keys** (plus bas)

**Publishable** (clé publique, anciennement "anon")
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFz...
```

**Secret** (clé secrète, anciennement "service_role")
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFz...
⚠️ This key has the ability to bypass Row Level Security
```

4. **Copiez ces 3 valeurs** (vous allez les coller dans `.env`)

💡 **Note** : Si vous voyez "anon public" et "service_role" au lieu de "Publishable" et "Secret", c'est l'ancienne interface - les clés sont exactement les mêmes !

📖 **Guide détaillé avec captures** : [SUPABASE_KEYS_GUIDE.md](SUPABASE_KEYS_GUIDE.md)

---

### Étape 3 : Remplir le Fichier `.env`

1. Ouvrez le fichier : `C:\code perso\python\albion-zerg\.env`
2. Remplacez les lignes vides par vos vraies valeurs :

**AVANT :**
```bash
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_KEY=
```

**APRÈS (avec vos vraies valeurs de Supabase):**
```bash
# Project URL (Settings > API, en haut)
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co

# Publishable key (Settings > API > API Keys section)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFz...

# Secret key (Settings > API > API Keys section) 
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFz...
```

3. **Sauvegardez** le fichier

---

### Étape 4 : Exécuter le Script SQL

Maintenant il faut créer les tables dans Supabase :

1. Dans Supabase, cliquez sur **SQL Editor** (icône `</>` dans le menu de gauche)
2. Cliquez sur **"New query"**
3. Ouvrez le fichier : `C:\code perso\python\albion-zerg\database\schema.sql`
4. **Sélectionnez TOUT le contenu** (Ctrl+A) et copiez (Ctrl+C)
5. Retournez dans Supabase et **collez** dans l'éditeur SQL (Ctrl+V)
6. Cliquez sur **"Run"** (ou appuyez sur Ctrl+Enter)
7. Vous devriez voir : ✅ **"Success. No rows returned"**

---

### Étape 4.5 : Activer l'Authentification ⚠️ IMPORTANT

**Cette étape est OBLIGATOIRE** sinon vous aurez une erreur 404 lors de l'inscription !

1. Dans le menu Supabase, allez dans **Authentication** (🔐)
2. Cliquez sur **Providers**
3. Activez **Email** :
   - Cliquez sur "Email"
   - ✅ Cochez **"Enable Email provider"**
   - ✅ Cochez **"Enable Email Signup"**
   - ⚪ **Décochez** "Confirm email" (pour le test local)
4. Cliquez sur **Save**

5. Configurez les URLs :
   - Allez dans **Authentication** > **URL Configuration**
   - **Site URL** : `http://localhost:8501`
   - **Redirect URLs** : `http://localhost:8501/**`
   - Cliquez sur **Save**

📖 **En cas d'erreur** : Consultez [FIX_AUTH_ERROR.md](FIX_AUTH_ERROR.md)

---

### Étape 5 : Créer votre Premier Utilisateur Admin

Maintenant, créez votre compte admin :

1. Dans Supabase, allez dans **Authentication** > **Users** (menu de gauche)
2. Cliquez sur **"Add user"** > **"Create new user"**
3. Remplissez :
   - **Email** : Votre email (ex: `admin@exemple.com`)
   - **Password** : Votre mot de passe (ex: `Admin123!`)
   - ✅ **Cochez** : "Auto Confirm User"
4. Cliquez sur **"Create user"**
5. **IMPORTANT** : Notez l'**User UID** (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

Maintenant, donnez-lui le rôle Admin :

6. Retournez dans **SQL Editor**
7. Créez une nouvelle requête et collez ceci (remplacez les valeurs) :

```sql
-- Créer le profil admin
INSERT INTO users_profiles (id, email, username, role, is_active)
VALUES (
    'COLLEZ_ICI_LE_USER_UID',  -- L'UID de l'étape 5
    'admin@exemple.com',        -- Votre email
    'Admin',                    -- Votre pseudo
    'admin',
    true
);
```

8. Cliquez sur **"Run"**
9. Vous devriez voir : ✅ **"Success. 1 rows affected"**

---

### Étape 6 : Lancer l'Application ! 🚀

Maintenant tout est prêt !

```bash
# Dans le terminal, dans le dossier albion-zerg
streamlit run app.py
```

L'application va s'ouvrir dans votre navigateur sur : **http://localhost:8501**

---

## 🎉 Connexion

Connectez-vous avec :
- **Email** : L'email que vous avez utilisé à l'étape 5
- **Password** : Le mot de passe que vous avez utilisé à l'étape 5

Vous devriez voir le dashboard avec le rôle **Admin** 👑 !

---

## ❓ Problèmes Fréquents

### "SUPABASE_URL not found"
➡️ Vérifiez que le fichier `.env` contient bien vos clés (pas de lignes vides)

### "Connection refused" 
➡️ Vérifiez que :
- Votre projet Supabase est bien actif (pas en pause)
- Les clés dans `.env` sont correctes (pas d'espaces en trop)

### "Table does not exist"
➡️ Vous n'avez pas exécuté le script SQL (étape 4)

### "User not found"
➡️ Vous n'avez pas créé le profil admin (étape 5)

---

## 📞 Besoin d'Aide ?

Si ça ne fonctionne toujours pas :

1. Vérifiez que toutes les étapes sont complètes
2. Redémarrez l'application : `streamlit run app.py`
3. Vérifiez les logs dans le terminal

---

## ✅ Checklist Rapide

- [ ] Compte Supabase créé
- [ ] Projet Supabase créé (2-3 min d'attente)
- [ ] Clés API copiées dans `.env`
- [ ] Script SQL exécuté (Success)
- [ ] Utilisateur admin créé (avec UID)
- [ ] Profil admin créé dans SQL (1 row affected)
- [ ] Application lancée : `streamlit run app.py`
- [ ] Connexion réussie !

---

Bon test ! 🎮
