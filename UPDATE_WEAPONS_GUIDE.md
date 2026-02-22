# 🗡️ Mise à Jour des Armes - Albion Online 2024

## ✅ Ce Qui a Été Fait

J'ai créé un script SQL complet avec **toutes les armes actuelles** d'Albion Online (version Wiki 2024) :

### 📊 Statistiques

- **152 armes** au total (sans Shields, Torches, Tomes)
- **4 catégories** :
  - 🛡️ **Tank** : 32 armes
  - 💚 **Healer** : 16 armes  
  - ⚔️ **DPS Melee** : 48 armes
  - 🏹 **DPS Range** : 56 armes

### 🆕 Nouvelles Armes Incluses

**Armes Crystal (Saison de Guilde) :**
- Infinity Blade (Sword)
- Crystal Reaper (Axe)
- Astral Staff (Arcane)
- Rift Glaive (Spear)

**Toutes les armes Artifact :**
- Rune, Soul, Relic, Avalon, Crystal variants
- Toutes les armes standard de chaque arbre

---

## 🚀 Comment Appliquer la Mise à Jour

### Option 1 : En Production (Supabase)

1. **Ouvrez Supabase** > **SQL Editor**
2. **New query**
3. Ouvrez le fichier : `database/update_weapons_2024.sql`
4. **Copiez TOUT** (Ctrl+A, Ctrl+C)
5. **Collez** dans Supabase (Ctrl+V)
6. **Run** (Ctrl+Enter)

Vous verrez :
```
✅ Success
message: "Base de données des armes mise à jour avec succès! Version Wiki 2024"
```

Et un tableau avec le nombre d'armes par catégorie.

---

### Option 2 : En Local (Test)

Si vous voulez tester en local d'abord :

1. **Sauvegardez les anciennes données** (optionnel) :
```sql
-- Créer une copie de sauvegarde
CREATE TABLE weapons_backup AS SELECT * FROM weapons;
```

2. **Exécutez le script** comme ci-dessus

3. **Testez l'app** :
```bash
streamlit run app.py
```

4. **Si problème, restaurez** :
```sql
-- Restaurer l'ancienne version
DELETE FROM weapons;
INSERT INTO weapons SELECT * FROM weapons_backup;
```

---

## 📸 Ajout des Images (Optionnel)

Le script ne contient pas encore les URLs des images. Si vous voulez les ajouter :

### URLs des Images Wiki

Les images sont disponibles sur : https://wiki.albiononline.com/

Format d'URL typique :
```
https://wiki.albiononline.com/wiki/Special:Redirect/file/Broadsword.png
```

### Script pour Ajouter les Images (Exemple)

```sql
-- Exemple pour quelques armes
UPDATE weapons SET icon_url = 'https://wiki.albiononline.com/wiki/Special:Redirect/file/Broadsword.png' 
WHERE name = 'Broadsword';

UPDATE weapons SET icon_url = 'https://wiki.albiononline.com/wiki/Special:Redirect/file/Greataxe.png' 
WHERE name = 'Greataxe';

-- etc...
```

**Note** : Il y a 152 armes, donc ajouter toutes les images manuellement serait long. On peut le faire plus tard si nécessaire.

---

## ⚠️ Points d'Attention

### 1. Impact sur les Compositions Existantes

Si vous avez déjà des compositions créées avec les anciennes armes :

```sql
-- Vérifier les compositions affectées
SELECT DISTINCT w.name 
FROM composition_slots cs
LEFT JOIN weapons w ON cs.weapon_id = w.id
WHERE w.id IS NULL;
```

Si des compositions utilisent des armes qui n'existent plus, elles pointeront vers des IDs invalides.

**Solution** : Après la mise à jour, vérifiez et mettez à jour les compositions manuellement via l'interface Admin.

---

### 2. Nouvelles Catégories

Les anciennes armes utilisaient peut-être des catégories différentes. Le nouveau script utilise :
- `Tank`
- `Healer`
- `DPS Melee`
- `DPS Range`

---

## 🧪 Vérifications Après Mise à Jour

### 1. Compter les Armes

```sql
SELECT COUNT(*) as total_armes FROM weapons;
-- Devrait retourner: 152
```

### 2. Voir les Armes par Catégorie

```sql
SELECT category, COUNT(*) as nombre
FROM weapons
GROUP BY category
ORDER BY category;
```

Résultat attendu :
```
DPS Melee  | 48
DPS Range  | 56
Healer     | 16
Tank       | 32
```

### 3. Tester dans l'App

1. Allez dans **Admin - Armes**
2. Vérifiez que toutes les armes apparaissent
3. Testez la création d'une composition avec les nouvelles armes

---

## 📚 Sources

- **Wiki Albion Online** : https://wiki.albiononline.com/wiki/Weapon
- **Dernière mise à jour** : Janvier 2024 (Crystal Raiders Update)
- **Armes exclues** : Shields, Torches, Tomes (pas des armes principales)

---

## 🔄 Futures Mises à Jour

Quand Albion ajoute de nouvelles armes :

1. Consultez le wiki : https://wiki.albiononline.com/wiki/Weapon
2. Ajoutez les nouvelles armes via l'interface **Admin - Armes**
3. Ou mettez à jour le script SQL et ré-exécutez

---

## ✅ Checklist

- [ ] Backup des anciennes armes (optionnel)
- [ ] Script SQL exécuté dans Supabase
- [ ] Vérification : 152 armes présentes
- [ ] Vérification : 4 catégories correctes
- [ ] Test dans l'app : Admin - Armes
- [ ] Test : Création d'une composition

---

**Tout est prêt ! Exécutez le script et vos armes seront à jour !** 🎮
