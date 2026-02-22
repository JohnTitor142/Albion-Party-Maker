# Guide : Ajout du Support des Groupes

## Contexte

Ce guide explique comment appliquer la mise à jour de la base de données pour ajouter le support des groupes dans les compositions.

## Étape 1 : Exécuter le Script SQL

1. Connectez-vous à votre projet Supabase : https://supabase.com/dashboard
2. Allez dans **SQL Editor** (dans le menu de gauche)
3. Cliquez sur **New query**
4. Copiez le contenu du fichier `database/add_groups_support.sql`
5. Collez-le dans l'éditeur SQL
6. Cliquez sur **Run** (ou Ctrl+Entrée)

## Étape 2 : Vérifier l'Application

Le script ajoute :
- Un champ `total_groups` à la table `compositions` (nombre de groupes dans une composition)
- Un champ `group_number` à la table `composition_slots` (numéro du groupe pour chaque slot)
- Mise à jour des données existantes avec les valeurs par défaut (groupe 1)
- Un index pour optimiser les performances

## Étape 3 : Vérification

Exécutez cette requête pour vérifier que les colonnes ont été ajoutées :

```sql
-- Vérifier la structure de compositions
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'compositions' AND column_name = 'total_groups';

-- Vérifier la structure de composition_slots
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'composition_slots' AND column_name = 'group_number';

-- Vérifier les données existantes
SELECT id, name, total_groups FROM compositions;
SELECT id, composition_id, group_number FROM composition_slots LIMIT 10;
```

## Étape 4 : Redémarrer l'Application

Une fois le script exécuté avec succès, redémarrez votre application Streamlit :

```bash
streamlit run app.py
```

## En cas de problème

Si le script échoue, vérifiez :
- Que vous avez les permissions nécessaires (propriétaire du projet)
- Qu'aucune contrainte n'empêche la modification
- Les messages d'erreur dans la console Supabase

Pour annuler les changements (rollback) :

```sql
-- Supprimer les colonnes ajoutées
ALTER TABLE compositions DROP COLUMN IF EXISTS total_groups;
ALTER TABLE composition_slots DROP COLUMN IF EXISTS group_number;

-- Supprimer l'index
DROP INDEX IF EXISTS idx_composition_slots_group;
```
