# 🔑 Guide : Où Trouver les Clés Supabase (Interface 2025)

## 📍 Étape par Étape

### 1. Accéder à votre Projet Supabase

1. Allez sur https://supabase.com
2. Connectez-vous
3. Sélectionnez votre projet

---

### 2. Aller dans Settings > API

1. Dans le menu de gauche, cliquez sur **⚙️ Settings** (tout en bas)
2. Dans le sous-menu, cliquez sur **API**

Vous arrivez sur la page de configuration API.

---

### 3. Récupérer les 3 Valeurs

Sur cette page, vous verrez **3 sections importantes** :

#### 📌 Section 1 : Project URL (en haut)

```
Project URL
────────────────────────────────────────
https://abcdefghijklmnop.supabase.co
```

➡️ **Copiez cette URL complète** → c'est votre `SUPABASE_URL`

---

#### 📌 Section 2 : API Keys

Vous verrez maintenant **2 clés** :

##### 🟢 Publishable (anciennement "anon public")

```
Publishable
────────────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJz...
[Bouton: Copy]
```

➡️ **Copiez cette clé** → c'est votre `SUPABASE_ANON_KEY`

**Note** : Cette clé est publique, elle peut être utilisée côté client.

---

##### 🔴 Secret (anciennement "service_role")

```
Secret
────────────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJz...
[Bouton: Copy]

⚠️ This key has the ability to bypass Row Level Security.
   Never share it publicly.
```

➡️ **Copiez cette clé** → c'est votre `SUPABASE_SERVICE_KEY`

**⚠️ ATTENTION** : Cette clé est **secrète** et donne tous les droits ! Ne la partagez jamais.

---

### 4. Ancienne Interface (Legacy)

Si vous voyez encore l'ancienne interface avec :
- `anon public` 
- `service_role`

**C'est exactement pareil !** Utilisez-les de la même manière :
- `anon public` = `Publishable` → `SUPABASE_ANON_KEY`
- `service_role` = `Secret` → `SUPABASE_SERVICE_KEY`

---

## 📝 Remplir le Fichier `.env`

Une fois que vous avez copié les 3 valeurs, ouvrez votre fichier `.env` et remplissez :

```bash
# 1. Project URL
SUPABASE_URL=https://abcdefghijklmnop.supabase.co

# 2. Publishable key (anon)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxMjM0NTY3OCwiZXhwIjoxOTI3OTIxNjc4fQ.abcdefg123456...

# 3. Secret key (service_role)
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjEyMzQ1Njc4LCJleHAiOjE5Mjc5MjE2Nzh9.xyz789...
```

---

## ✅ Vérification

### Les clés sont-elles correctes ?

**URL** :
- ✅ Commence par `https://`
- ✅ Se termine par `.supabase.co`
- ✅ Contient votre identifiant de projet au milieu

**Clés (Publishable et Secret)** :
- ✅ Commencent toutes les deux par `eyJ`
- ✅ Sont très longues (~250 caractères)
- ✅ Contiennent des points `.` qui séparent 3 parties
- ✅ Pas d'espaces au début ou à la fin

---

## 🧪 Test Rapide

Pour vérifier que vos clés fonctionnent :

```bash
python check_config.py
```

Si tout est OK, vous verrez :
```
✅ Le fichier .env existe
✅ Toutes les clés sont présentes
✅ Connexion Supabase réussie !
```

---

## ❓ Problèmes Fréquents

### "SUPABASE_URL not found"
➡️ Vous avez oublié de copier le Project URL (la première valeur)

### "Invalid API key"
➡️ Vous avez copié la mauvaise clé ou il y a des espaces en trop

### "Connection refused"
➡️ Vérifiez que votre projet Supabase est bien actif (pas en pause)

### Je ne trouve pas l'onglet API
➡️ Settings (en bas du menu de gauche) > API

---

## 🎯 Récapitulatif Rapide

| Où dans Supabase | Nom Actuel | Nom Ancien | Variable .env |
|------------------|------------|------------|---------------|
| En haut de la page API | Project URL | Project URL | `SUPABASE_URL` |
| API Keys section | Publishable | anon public | `SUPABASE_ANON_KEY` |
| API Keys section | Secret | service_role | `SUPABASE_SERVICE_KEY` |

---

Vous êtes prêt ! 🚀
