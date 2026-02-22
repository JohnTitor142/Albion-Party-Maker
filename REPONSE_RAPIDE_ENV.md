# ✅ RÉPONSE RAPIDE : Configuration .env

## 🎯 Les 3 Valeurs à Copier depuis Supabase

Dans Supabase, allez dans **Settings** ⚙️ > **API**

### 1️⃣ Project URL (en haut de la page)

**Ce que vous voyez dans Supabase :**
```
Project URL
────────────────────────────────
https://abcdefghijklmnop.supabase.co
```

**Dans votre `.env` :**
```bash
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
```

---

### 2️⃣ Publishable Key (clé publique)

**Nouvelle interface - Ce que vous voyez :**
```
Publishable
────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**OU ancienne interface :**
```
anon public
────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Dans votre `.env` :**
```bash
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 3️⃣ Secret Key (clé secrète)

**Nouvelle interface - Ce que vous voyez :**
```
Secret
────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
⚠️ This key has the ability to bypass Row Level Security
```

**OU ancienne interface :**
```
service_role
────────────────────────────────
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Dans votre `.env` :**
```bash
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📝 Votre Fichier `.env` Final

Ouvrez `C:\code perso\python\albion-zerg\.env` et remplissez :

```bash
# Configuration locale
SUPABASE_URL=https://votre-id-projet.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZvdHJlLWlkLXByb2pldCIsInJvbGUiOiJhbm9uIiwiaWF0IjoxNjAwMDAwMDAwLCJleHAiOjE5MTU1NTU1NTV9.votre-signature-complete-ici
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZvdHJlLWlkLXByb2pldCIsInJvbGUiOiJzZXJ2aWNlX3JvbGUiLCJpYXQiOjE2MDAwMDAwMDAsImV4cCI6MTkxNTU1NTU1NX0.votre-signature-complete-ici
```

**SANS espaces, SANS guillemets !**

---

## ✅ Équivalences des Noms

| Dans Supabase (nouveau) | Dans Supabase (ancien) | Dans .env |
|-------------------------|------------------------|-----------|
| **Publishable** | anon public | `SUPABASE_ANON_KEY` |
| **Secret** | service_role | `SUPABASE_SERVICE_KEY` |

**C'est la même chose !** Supabase a juste renommé pour plus de clarté.

---

## 🔍 Comment Savoir si c'est Bon ?

### Les clés doivent :
- ✅ Commencer par `eyJ`
- ✅ Être très longues (~250 caractères)
- ✅ Contenir des points `.` (3 parties séparées)
- ❌ PAS d'espaces avant ou après
- ❌ PAS de guillemets `"` autour

### Test rapide :
```bash
python check_config.py
```

Si OK, vous verrez :
```
✅ Le fichier .env existe
✅ Toutes les clés sont présentes
✅ Connexion Supabase réussie !
```

---

## 🚀 Une fois configuré

Lancez l'application :
```bash
streamlit run app.py
```

Ça devrait fonctionner ! 🎉

---

**Besoin d'aide ?** Consultez [SUPABASE_KEYS_GUIDE.md](SUPABASE_KEYS_GUIDE.md) pour un guide détaillé avec visuels.
