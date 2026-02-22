# ⚠️ Erreur : Authentification Non Activée dans Supabase

## Problème

Vous voyez cette erreur lors de l'inscription :
```
❌ Erreur d'inscription : {'message': 'JSON could not be generated', 'code': 404...
```

**Cause** : L'authentification n'est pas activée dans votre projet Supabase.

---

## ✅ Solution : Activer l'Authentification

### Étape 1 : Aller dans Authentication

1. Ouvrez votre projet Supabase
2. Dans le menu de gauche, cliquez sur **🔐 Authentication**
3. Cliquez sur **Providers** (ou **Settings**)

---

### Étape 2 : Activer Email Authentication

1. Dans la liste des providers, cherchez **Email**
2. Cliquez sur **Email** (ou activez le toggle)
3. Assurez-vous que ces options sont activées :
   - ✅ **Enable Email provider**
   - ✅ **Enable Email Signup**
   - ✅ **Confirm email** (peut être désactivé pour le test local)

4. Cliquez sur **Save** (en bas)

---

### Étape 3 : Configurer l'URL du Site (Optionnel mais Recommandé)

1. Toujours dans **Authentication** > **URL Configuration**
2. Ajoutez votre URL locale :

```
Site URL: http://localhost:8501
Redirect URLs: http://localhost:8501/**
```

3. Cliquez sur **Save**

---

### Étape 4 : Désactiver la Confirmation d'Email (Pour le Test Local)

Pour tester plus facilement en local :

1. Dans **Authentication** > **Providers** > **Email**
2. Trouvez **Confirm email**
3. **Désactivez** cette option pour le développement local
4. Cliquez sur **Save**

⚠️ **Note** : Réactivez-la en production !

---

### Étape 5 : Vérifier dans Authentication > Users

1. Allez dans **Authentication** > **Users**
2. Vous devriez voir une page vide (ou vos users existants)
3. Si vous voyez "Auth schema not found", c'est que le script SQL n'a pas bien tourné

---

## 🔍 Vérification : Le Script SQL a-t-il Créé les Triggers Auth ?

Le script SQL doit avoir créé un système automatique pour créer les profils.

### Vérifier dans SQL Editor :

Exécutez cette requête :
```sql
-- Vérifier que la table users_profiles existe
SELECT * FROM users_profiles LIMIT 1;
```

Si ça marche, c'est bon ✅

Si erreur "table does not exist", réexécutez le script SQL complet.

---

## 🧪 Test Après Configuration

1. **Redémarrez votre application Streamlit** :
   ```bash
   # Arrêtez avec Ctrl+C
   streamlit run app.py
   ```

2. **Essayez de vous inscrire** :
   - Allez sur l'onglet "Inscription"
   - Remplissez le formulaire
   - Cliquez sur "S'inscrire"

3. **Si ça marche**, vous verrez :
   ```
   ✅ Compte créé avec succès ! Bienvenue, [username] !
   ```

---

## ❓ Toujours une Erreur ?

### Erreur "User already registered"
➡️ Cet email existe déjà. Essayez un autre email ou connectez-vous.

### Erreur "Invalid email"
➡️ Utilisez un format d'email valide : `test@exemple.com`

### Erreur "Email not confirmed"
➡️ Désactivez la confirmation d'email (voir Étape 4)

### Erreur "Auth schema not found"
➡️ Le script SQL n'a pas été exécuté complètement. Réexécutez-le :
1. Ouvrez `database/schema.sql`
2. Copiez TOUT le contenu (Ctrl+A, Ctrl+C)
3. Dans Supabase > SQL Editor > New query
4. Collez et Run

---

## 📸 Capture d'Écran Attendue

Dans **Authentication** > **Providers**, vous devriez voir :

```
┌─────────────────────────────────────────┐
│ Providers                                │
├─────────────────────────────────────────┤
│                                          │
│ Email                                    │
│ ✅ Enabled                               │
│                                          │
│ Google (optionnel)                       │
│ ○ Disabled                               │
│                                          │
│ ... autres providers                     │
│                                          │
└─────────────────────────────────────────┘
```

---

## ✅ Checklist Rapide

- [ ] Authentication > Providers > Email est activé
- [ ] Enable Email Signup est coché
- [ ] Confirm email est désactivé (pour test local)
- [ ] Site URL configurée (http://localhost:8501)
- [ ] Application Streamlit redémarrée
- [ ] Test d'inscription avec un nouvel email

---

Essayez maintenant et dites-moi si ça fonctionne ! 🚀
