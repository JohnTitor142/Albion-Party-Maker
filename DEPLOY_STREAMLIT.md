# 🚀 Guide de Déploiement sur Streamlit Cloud

## Étape 1 : Pousser sur GitHub

### 1.1 Initialiser Git (si pas déjà fait)

```bash
# Dans le dossier albion-zerg
cd "C:\code perso\python\albion-zerg"

# Initialiser git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Albion Zerg Manager"
```

---

### 1.2 Créer un Repository GitHub

1. Allez sur https://github.com
2. Connectez-vous
3. Cliquez sur le **"+"** en haut à droite > **"New repository"**
4. Remplissez :
   - **Repository name** : `albion-zerg-manager`
   - **Visibility** : Public (ou Private, au choix)
   - **NE COCHEZ PAS** "Initialize with README" (vous avez déjà un README)
5. Cliquez sur **"Create repository"**

---

### 1.3 Pousser le Code

GitHub vous donnera des commandes. Utilisez celles-ci :

```bash
# Connecter votre repo local à GitHub
git remote add origin https://github.com/VOTRE_USERNAME/albion-zerg-manager.git

# Renommer la branche en main
git branch -M main

# Pousser le code
git push -u origin main
```

**Note** : Si GitHub demande l'authentification, utilisez un **Personal Access Token** :
- GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
- Generate new token > Cochez "repo" > Generate
- Utilisez ce token comme mot de passe

---

## Étape 2 : Déployer sur Streamlit Cloud

### 2.1 Se Connecter

1. Allez sur https://streamlit.io/cloud
2. Cliquez sur **"Sign in with GitHub"**
3. Autorisez Streamlit à accéder à vos repos

---

### 2.2 Créer une Nouvelle App

1. Cliquez sur **"New app"**
2. Remplissez :
   - **Repository** : Sélectionnez `VOTRE_USERNAME/albion-zerg-manager`
   - **Branch** : `main`
   - **Main file path** : `app.py`
   - **App URL** : Choisissez un nom unique (ex: `albion-zerg-manager`)

---

### 2.3 Configurer les Secrets ⚠️ IMPORTANT

**Avant de déployer**, cliquez sur **"Advanced settings..."**

Dans la section **Secrets**, collez ceci (avec VOS vraies valeurs Supabase) :

```toml
SUPABASE_URL = "https://xydupnaraygknoriibqz.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGc...votre-anon-key-complète"
SUPABASE_SERVICE_KEY = "eyJhbGc...votre-service-key-complète"
```

**Format TOML important :**
- Utilisez des guillemets `"` autour des valeurs
- Pas de `=` supplémentaire
- Une ligne par secret

---

### 2.4 Déployer

1. Cliquez sur **"Deploy!"**
2. Attendez 2-3 minutes pendant le build
3. L'app sera accessible à : `https://votre-app-name.streamlit.app`

---

## Étape 3 : Vérifier que Tout Fonctionne

### 3.1 Tester l'App

1. Ouvrez l'URL de votre app
2. Testez l'inscription avec un nouvel email
3. Testez la connexion

---

### 3.2 Logs en Temps Réel

En cas d'erreur, consultez les logs :
- En bas à droite de l'app : **"Manage app"**
- Cliquez sur **"Logs"**
- Vous verrez les erreurs en temps réel

---

## 🔧 Problèmes Fréquents

### Erreur "Module not found"
➡️ Le fichier `requirements.txt` n'a pas été poussé sur GitHub
```bash
git add requirements.txt
git commit -m "Add requirements"
git push
```

### Erreur "SUPABASE_URL not found"
➡️ Les secrets ne sont pas configurés correctement dans Streamlit
1. Allez dans **Manage app** > **Settings** > **Secrets**
2. Vérifiez le format TOML

### Erreur 403/401 Supabase
➡️ Vérifiez que vos clés sont correctes dans les secrets

### L'app se met en veille
➡️ Normal avec le plan gratuit après 7 jours d'inactivité
- Elle redémarre automatiquement au premier accès

---

## 🎯 Configuration Supabase pour Production

### Mettre à Jour les URLs

Dans Supabase **Authentication** > **URL Configuration**, ajoutez :

**Site URL :**
```
https://votre-app-name.streamlit.app
```

**Redirect URLs :**
```
https://votre-app-name.streamlit.app
https://votre-app-name.streamlit.app/**
https://votre-app-name.streamlit.app/auth/callback
```

Cliquez sur **Save**

---

## ✅ Checklist Complète

- [ ] Code poussé sur GitHub
- [ ] Repository créé sur GitHub
- [ ] Compte Streamlit Cloud créé
- [ ] App créée sur Streamlit
- [ ] Secrets configurés (SUPABASE_URL, ANON_KEY, SERVICE_KEY)
- [ ] App déployée avec succès
- [ ] URLs mises à jour dans Supabase Authentication
- [ ] Test d'inscription réussi
- [ ] Test de connexion réussi

---

## 🌐 URLs Finales

Après déploiement, vous aurez :

- **App publique** : `https://votre-app-name.streamlit.app`
- **Dashboard Streamlit** : https://share.streamlit.io/
- **Manage app** : Pour voir les logs et paramètres

---

## 📊 Limites du Plan Gratuit

### Streamlit Cloud Free
- ✅ 1 app publique
- ✅ 1 GB RAM
- ⚠️ Mise en veille après 7 jours d'inactivité
- ✅ Pas de limite de visiteurs

### Pour Plus d'Apps
- **Streamlit Team** : $20/mois pour 3 apps privées

---

## 🆘 Support

En cas de problème :
1. Vérifiez les **logs** dans Streamlit
2. Vérifiez que le script SQL RLS a été exécuté
3. Vérifiez les **secrets** (format TOML)
4. Testez en local d'abord

---

## 🎉 C'est Terminé !

Votre application est maintenant en ligne et accessible à tous ! 🚀

Partagez simplement l'URL : `https://votre-app-name.streamlit.app`

---

**Bon déploiement !** 🎮
