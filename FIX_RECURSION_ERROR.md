# 🔧 CORRECTIF : Erreur de Récursion Infinie RLS

## ❌ Erreur Rencontrée

```
infinite recursion detected in policy for relation "users_profiles"
```

## ✅ Solution

Cette erreur vient des policies RLS qui créent une boucle infinie. J'ai créé un script correctif.

---

## 📋 Étapes pour Corriger

### 1. Ouvrir Supabase SQL Editor

1. Allez dans votre projet Supabase
2. Cliquez sur **SQL Editor** (icône `</>`)
3. Cliquez sur **New query**

---

### 2. Exécuter le Script de Correction

1. Ouvrez le fichier : `database/fix_rls_policies.sql`
2. **Copiez TOUT le contenu** (Ctrl+A, Ctrl+C)
3. **Collez** dans l'éditeur SQL de Supabase (Ctrl+V)
4. Cliquez sur **Run** (ou Ctrl+Enter)

Vous devriez voir :
```
✅ Success
message: "Policies RLS corrigées avec succès!"
```

---

### 3. Tester l'Application

1. **Redémarrez** votre application Streamlit :
   ```bash
   # Arrêtez avec Ctrl+C
   streamlit run app.py
   ```

2. **Essayez de vous inscrire** :
   - Allez sur l'onglet "Inscription"
   - Remplissez le formulaire
   - Cliquez sur "S'inscrire"

3. **Ça devrait fonctionner !** 🎉

---

## 🔍 Qu'est-ce qui a été corrigé ?

### Problème
Les policies RLS faisaient des requêtes comme :
```sql
EXISTS (SELECT 1 FROM users_profiles WHERE id = auth.uid() AND role = 'admin')
```

Quand on essayait de lire `users_profiles`, la policy faisait un SELECT sur `users_profiles`, qui déclenchait la policy, qui faisait un SELECT... → **Récursion infinie !**

### Solution
Création d'une fonction helper `auth.user_role()` qui :
- Utilise `SECURITY DEFINER` pour bypasser les policies
- Est marquée `STABLE` pour le cache
- Retourne directement le rôle sans récursion

Maintenant les policies utilisent :
```sql
auth.user_role() = 'admin'
```

Au lieu de faire une sous-requête récursive.

---

## ✅ Vérifications Après Correction

### Test 1 : Inscription
```
✅ Compte créé avec succès !
```

### Test 2 : Connexion
```
✅ Bienvenue, [username] !
```

### Test 3 : Dashboard
```
✅ Affichage du dashboard selon votre rôle
```

---

## 🎯 Si l'Erreur Persiste

### Option A : Réinitialiser Complètement

Si le problème persiste, réinitialisez tout :

1. **SQL Editor** > **New query**
2. Exécutez :
```sql
-- Désactiver RLS temporairement
ALTER TABLE users_profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE weapons DISABLE ROW LEVEL SECURITY;
ALTER TABLE compositions DISABLE ROW LEVEL SECURITY;
ALTER TABLE composition_slots DISABLE ROW LEVEL SECURITY;
ALTER TABLE activities DISABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations DISABLE ROW LEVEL SECURITY;
ALTER TABLE activity_assignments DISABLE ROW LEVEL SECURITY;
```

3. Testez votre app (RLS désactivé = tout fonctionne)
4. Si ça marche, réexécutez `fix_rls_policies.sql`

---

### Option B : Recréer Complètement la Base

Si vraiment rien ne fonctionne :

1. **SQL Editor** > **New query**
2. Exécutez :
```sql
-- ATTENTION : CECI SUPPRIME TOUTES LES DONNÉES !
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
```

3. Réexécutez le script principal `database/schema.sql`
4. Puis exécutez `database/fix_rls_policies.sql`

---

## 📚 Pour en Savoir Plus

- [Supabase RLS Documentation](https://supabase.com/docs/guides/auth/row-level-security)
- [PostgreSQL Policies](https://www.postgresql.org/docs/current/sql-createpolicy.html)

---

**Exécutez le script `fix_rls_policies.sql` et ça devrait marcher !** 🚀
