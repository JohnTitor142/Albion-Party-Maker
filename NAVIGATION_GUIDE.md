# 🚀 Navigation - Pages Streamlit Natives - Guide Complet

## ✅ Changements Effectués

L'application utilise maintenant **complètement** le système de pages natives de Streamlit avec une page de login dédiée.

---

## 📁 Nouvelle Structure de Fichiers

```
app.py                           # Page de LOGIN/SIGNUP (point d'entrée)
pages/
  1_📊_Dashboard.py              # Dashboard (wrapper)
  2_📝_Mes_Inscriptions.py       # Inscriptions (wrapper)
  3_👥_Rosters.py                # Rosters (wrapper)
  4_🧩_Compositions.py           # Compositions (wrapper - ShotCaller+)
  5_📅_Activités.py              # Activités (wrapper - ShotCaller+)
  6_👑_Admin_Users.py            # Admin Users (wrapper - Admin)
  7_⚔️_Admin_Armes.py            # Admin Armes (wrapper - Admin)
  
  core/                          # Logique métier (invisible à Streamlit)
    dashboard.py                 # Fonctions render_*
    compositions.py              
    activities.py
    my_activities.py
    roster.py
```

---

## 🎯 Comment Ça Fonctionne

### 1. Page de Login (`app.py`)

- **Sidebar masquée** : Les utilisateurs non connectés ne voient pas les autres pages
- **Redirection automatique** : Si vous êtes déjà connecté, vous êtes envoyé au Dashboard
- **Layout centré** : Interface épurée focalisée sur la connexion

### 2. Pages Streamlit Natives

Les fichiers `1_*.py`, `2_*.py`, etc. sont des **wrappers légers** qui :
- Configurent la page
- Vérifient l'authentification (sinon → message d'erreur)
- Vérifient les permissions (pour les pages admin/shotcaller)
- Appellent les fonctions de rendu dans `pages/core/`

**Exemple** (`pages/1_📊_Dashboard.py`) :
```python
import streamlit as st
from auth.session import init_session_state, is_authenticated
from pages.core.dashboard import render_dashboard

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
init_session_state()

if not is_authenticated():
    st.warning("⚠️ Vous devez être connecté.")
    st.stop()

render_dashboard()
```

### 3. Dossier `pages/core/`

**Pourquoi ?**
- Streamlit détecte automatiquement **tous** les `.py` dans `pages/`
- Les fichiers dans `pages/core/` sont **ignorés** par Streamlit (sous-dossier)
- Cela permet de garder la logique métier sans polluer la navigation

**Contenu** : Les anciennes pages avec les fonctions `render_*()` qui contiennent toute la logique.

---

## 🔐 Sécurité et Contrôle d'Accès

### Pages Publiques
- `app.py` : Accessible à tous (login/signup)

### Pages Authentifiées
Tous les utilisateurs connectés :
- `1_📊_Dashboard.py`
- `2_📝_Mes_Inscriptions.py`
- `3_👥_Rosters.py`

### Pages ShotCaller+
ShotCallers et Admins :
- `4_🧩_Compositions.py`
- `5_📅_Activités.py`

**Contrôle** : `if not is_shotcaller(): st.error() + st.stop()`

### Pages Admin
Administrateurs uniquement :
- `6_👑_Admin_Users.py`
- `7_⚔️_Admin_Armes.py`

**Contrôle** : `if not is_admin(): st.error() + st.stop()`

---

## 🎨 Avantages de Cette Approche

### ✅ Sidebar Propre
- Les utilisateurs voient **uniquement** les pages avec emojis
- Pas de fichiers techniques (`dashboard.py`, `compositions.py`, etc.)

### ✅ Page de Login Dédiée
- **Sidebar invisible** sur la page de login
- **Layout centré** pour une meilleure UX
- **Redirection automatique** si déjà connecté

### ✅ Navigation Intuitive
- Les pages sont **numérotées** (ordre d'affichage)
- Les **emojis** rendent la navigation visuelle
- Streamlit gère la **sélection active**

### ✅ Sécurité Robuste
- Chaque page vérifie **elle-même** l'authentification
- Messages d'erreur clairs si accès non autorisé
- Pas de contournement possible via URL

---

## 🚀 Utilisation

### Lancer l'Application

```bash
streamlit run app.py
```

### Workflow Utilisateur

1. **Non connecté** :
   - Arrive sur `app.py` (login/signup)
   - Sidebar masquée, ne voit aucune autre page
   
2. **Login réussi** :
   - Redirection automatique vers `1_📊_Dashboard.py`
   - Sidebar apparaît avec les pages accessibles selon le rôle
   
3. **Navigation** :
   - Clic sur une page dans la sidebar
   - Si permissions OK → page s'affiche
   - Si permissions KO → message d'erreur clair

---

## 🛠️ Personnalisation

### Changer l'Ordre des Pages

Renommer les fichiers avec de nouveaux préfixes numériques :

```
1_📊_Dashboard.py  →  10_📊_Dashboard.py  (déplacer à la fin)
2_📝_Mes_Inscriptions.py  →  1_📝_Mes_Inscriptions.py  (déplacer au début)
```

### Changer les Icônes

Modifier les emojis dans les noms de fichiers :

```
1_📊_Dashboard.py  →  1_📈_Dashboard.py
```

### Ajouter une Nouvelle Page

1. Créer le fichier dans `pages/` avec le bon préfixe :
   ```python
   # pages/8_🔧_Nouvelle_Page.py
   import streamlit as st
   from auth.session import init_session_state, is_authenticated
   from pages.core.nouvelle_page import render_nouvelle_page
   
   st.set_page_config(page_title="Nouvelle Page", page_icon="🔧", layout="wide")
   init_session_state()
   
   if not is_authenticated():
       st.warning("⚠️ Connexion requise")
       st.stop()
   
   render_nouvelle_page()
   ```

2. Créer la logique dans `pages/core/nouvelle_page.py`
   ```python
   import streamlit as st
   
   def render_nouvelle_page():
       st.title("Ma Nouvelle Page")
       # ... votre code ...
   ```

---

## 📝 Notes Importantes

1. **Ne supprimez PAS `pages/core/`** : Ces fichiers contiennent la logique métier
2. **Les wrappers sont légers** : Ils font juste la vérification et appellent la logique
3. **Sidebar automatique** : Streamlit détecte les pages, pas besoin de `components/sidebar.py`
4. **Déconnexion** : Un bouton est disponible dans la sidebar Streamlit (en bas)

---

## 🐛 Dépannage

### "Page non trouvée" après connexion
- Vérifiez que `pages/1_📊_Dashboard.py` existe
- Vérifiez que les imports pointent vers `pages.core.*`

### "Import Error" dans une page
- Vérifiez que `pages/core/` contient bien tous les fichiers
- Vérifiez les imports : `from pages.core.dashboard import ...`

### Page visible mais bloquée
- C'est normal si vous n'avez pas les permissions
- Vérifiez votre rôle avec un admin

---

Votre navigation est maintenant **propre, sécurisée et intuitive** ! 🎉
