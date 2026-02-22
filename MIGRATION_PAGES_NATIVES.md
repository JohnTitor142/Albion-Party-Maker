# Migration vers Pages Streamlit Natives - Guide

## 🎯 Changements Effectués

L'application a été migrée vers le système de pages natives de Streamlit. Voici ce qui a changé :

### Avant
- Navigation manuelle via `components/sidebar.py`
- Toutes les pages chargées via `app.py` avec un router
- Navigation par option_menu custom

### Après
- **Navigation native Streamlit** : les pages apparaissent automatiquement dans la sidebar
- **app.py** : uniquement la page d'accueil (login/signup)
- **pages/** : toutes les pages authentifiées

## 📁 Nouvelle Structure

```
app.py                          # Page d'accueil (login/signup)
pages/
  1_📊_Dashboard.py             # Dashboard (tous les utilisateurs)
  2_📝_Mes_Inscriptions.py      # Inscriptions (tous les utilisateurs)
  3_👥_Rosters.py               # Rosters (tous les utilisateurs)
  4_🧩_Compositions.py          # Compositions (ShotCaller+)
  5_📅_Activités.py             # Activités (ShotCaller+)
  6_👑_Admin_Users.py           # Gestion users (Admin uniquement)
  7_⚔️_Admin_Armes.py           # Gestion armes (Admin uniquement)
  
  # Anciens fichiers (peuvent être supprimés)
  dashboard.py
  compositions.py
  activities.py
  my_activities.py
  roster.py
  admin/
    user_management.py
    weapons_management.py
```

## 🔐 Contrôle d'Accès

Chaque page native vérifie maintenant **elle-même** l'authentification et les permissions :

1. **Authentification** : toutes les pages vérifient `is_authenticated()`
2. **Rôles ShotCaller** : pages 4-5 vérifient `is_shotcaller()`
3. **Rôles Admin** : pages 6-7 vérifient `is_admin()`

Si un utilisateur tente d'accéder à une page sans les droits, il voit un message d'erreur clair.

## ✨ Avantages

1. **Simplicité** : Streamlit gère automatiquement la navigation
2. **URLs** : Chaque page a sa propre URL (ex: `?page=Dashboard`)
3. **Emojis** : Les icônes apparaissent directement dans la sidebar
4. **Ordre** : Les préfixes numériques contrôlent l'ordre d'affichage
5. **Performance** : Seule la page sélectionnée est chargée

## 🚀 Utilisation

Pour lancer l'application :

```bash
streamlit run app.py
```

La navigation se fait automatiquement via la sidebar Streamlit.

## 🗑️ Nettoyage (Optionnel)

Vous pouvez supprimer ces fichiers qui ne sont plus utilisés :

```
components/sidebar.py           # Remplacé par la sidebar native Streamlit
pages/dashboard.py              # Remplacé par pages/1_📊_Dashboard.py
pages/compositions.py           # Remplacé par pages/4_🧩_Compositions.py
pages/activities.py             # Remplacé par pages/5_📅_Activités.py
pages/my_activities.py          # Remplacé par pages/2_📝_Mes_Inscriptions.py
pages/roster.py                 # Remplacé par pages/3_👥_Rosters.py
```

**Note** : Les fichiers originaux sont toujours importés par les nouvelles pages, donc **ne les supprimez pas encore**. Ils contiennent la logique métier (fonctions `render_*`).

## 📝 Notes Importantes

1. **Les anciennes pages (dashboard.py, etc.) sont toujours nécessaires** car elles contiennent les fonctions `render_*` qui font le travail.
2. **Les nouvelles pages (1_📊_Dashboard.py, etc.)** sont juste des wrappers qui :
   - Configurent la page
   - Vérifient l'authentification/permissions
   - Appellent les fonctions `render_*` des anciennes pages
3. **components/sidebar.py peut être supprimé** car il n'est plus utilisé.

## 🎨 Personnalisation

Pour changer l'ordre ou les icônes des pages, modifiez les noms de fichiers :

- Le **préfixe numérique** (1_, 2_, etc.) contrôle l'ordre
- Le **texte** entre underscores devient le nom dans la sidebar
- Les **emojis** apparaissent dans la sidebar

Exemple :
```
1_📊_Dashboard.py  →  "📊 Dashboard" (1er dans la sidebar)
5_📅_Activités.py  →  "📅 Activités" (5ème dans la sidebar)
```
