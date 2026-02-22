# 🚀 DÉPLOIEMENT RAPIDE - 3 Étapes

## Étape 1 : GitHub (5 min)

### A. Initialiser Git

**Option 1 : Script automatique** (Windows)
```bash
# Double-cliquez sur ce fichier
setup_git.bat
```

**Option 2 : Commandes manuelles**
```bash
git init
git add .
git commit -m "Initial commit - Albion Zerg Manager"
```

### B. Créer Repository GitHub

1. https://github.com/new
2. Nom : `albion-zerg-manager`
3. Public (ou Private)
4. **Create repository**

### C. Pousser le Code

```bash
# Remplacez VOTRE_USERNAME par votre username GitHub
git remote add origin https://github.com/VOTRE_USERNAME/albion-zerg-manager.git
git branch -M main
git push -u origin main
```

---

## Étape 2 : Streamlit Cloud (3 min)

### A. Se Connecter
1. https://streamlit.io/cloud
2. **Sign in with GitHub**

### B. Créer l'App
1. **New app**
2. Repository : `VOTRE_USERNAME/albion-zerg-manager`
3. Branch : `main`
4. Main file : `app.py`

### C. Configurer les Secrets ⚠️ IMPORTANT

Cliquez sur **"Advanced settings..."** > **Secrets**

Collez ceci (avec VOS vraies valeurs) :

```toml
SUPABASE_URL = "https://xydupnaraygknoriibqz.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGc...votre-clé"
SUPABASE_SERVICE_KEY = "eyJhbGc...votre-clé"
```

### D. Déployer
**Deploy!** → Attendez 2-3 minutes

---

## Étape 3 : Configuration Supabase (1 min)

Dans Supabase **Authentication** > **URL Configuration** :

**Site URL :**
```
https://votre-app-name.streamlit.app
```

**Redirect URLs :**
```
https://votre-app-name.streamlit.app
https://votre-app-name.streamlit.app/**
```

**Save**

---

## ✅ Terminé !

Votre app est en ligne : `https://votre-app-name.streamlit.app` 🎉

---

## 📖 Guides Détaillés

- **Guide complet** : [DEPLOY_STREAMLIT.md](DEPLOY_STREAMLIT.md)
- **Dépannage** : Voir les logs dans Streamlit > Manage app

---

## ⚡ Commandes Utiles

```bash
# Mettre à jour l'app après modifications
git add .
git commit -m "Update: description du changement"
git push

# L'app Streamlit se redéploiera automatiquement !
```

---

**Bon déploiement !** 🚀
