# 🔧 Exemple de Configuration `.env`

## Voici à quoi doit ressembler votre fichier `.env` une fois rempli :

```bash
# Configuration locale - NE PAS COMMIT CE FICHIER
# Copiez .env.example vers .env et remplissez vos vraies valeurs

# Supabase Configuration
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxMjM0NTY3OCwiZXhwIjoxOTI3OTIxNjc4fQ.abcdefghijklmnopqrstuvwxyz1234567890
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjEyMzQ1Njc4LCJleHAiOjE5Mjc5MjE2Nzh9.abcdefghijklmnopqrstuvwxyz0987654321
```

---

## 📝 Où Trouver Ces Valeurs ?

### Dans Supabase (Nouvelle Interface 2025) :

1. **Settings** (⚙️) > **API**
2. Vous verrez 3 informations :

#### Project URL
```
https://abcdefghijklmnop.supabase.co
```
↪️ C'est votre **SUPABASE_URL**

#### Publishable (clé publique)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOi...
```
↪️ C'est votre **SUPABASE_ANON_KEY**

#### Secret (clé secrète)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOi...
⚠️ This key has the ability to bypass Row Level Security
```
↪️ C'est votre **SUPABASE_SERVICE_KEY**

---

### Ancienne Interface (Legacy)

Si vous voyez encore :
- `anon public` au lieu de `Publishable`
- `service_role` au lieu de `Secret`

**C'est normal !** C'est exactement la même chose :
- `anon public` = `Publishable` → utilisez pour `SUPABASE_ANON_KEY`
- `service_role` = `Secret` → utilisez pour `SUPABASE_SERVICE_KEY`

📖 **Guide complet avec explications** : [SUPABASE_KEYS_GUIDE.md](SUPABASE_KEYS_GUIDE.md)

---

## ⚠️ Points Importants

1. **Pas d'espaces** autour du `=`
   - ✅ Bon : `SUPABASE_URL=https://...`
   - ❌ Mauvais : `SUPABASE_URL = https://...`

2. **Pas de guillemets** autour des valeurs
   - ✅ Bon : `SUPABASE_URL=https://...`
   - ❌ Mauvais : `SUPABASE_URL="https://..."`

3. **Les clés sont TRÈS longues** (normal !)
   - anon_key : ~250 caractères
   - service_key : ~250 caractères

4. **Ne commitez JAMAIS ce fichier** sur Git !
   - Le `.gitignore` l'empêche déjà
   - La `service_key` est sensible !

---

## ✅ Vérification Rapide

Après avoir rempli `.env`, vérifiez :

```bash
# Windows PowerShell
Get-Content .env
```

Vous devriez voir vos 3 lignes remplies (pas de lignes vides après le `=`).

---

## 🧪 Test de Connexion

Pour tester si vos clés sont correctes avant de lancer l'app :

```bash
python
```

Puis dans le shell Python :

```python
from config.supabase_config import get_supabase
client = get_supabase()
print("✅ Connexion Supabase OK !")
```

Si aucune erreur, c'est bon ! ✅

Si erreur "SUPABASE_URL not found" : vérifiez le fichier `.env`

---

## 🔄 Si Vous Changez de Projet Supabase

1. Allez dans le nouveau projet Supabase
2. Settings > API
3. Copiez les nouvelles clés
4. Remplacez dans `.env`
5. Redémarrez l'app : `streamlit run app.py`

---

Vous êtes prêt ! 🚀
