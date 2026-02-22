-- ============================================
-- Script de migration : Ajout du support des groupes
-- ============================================
-- Ce script ajoute les champs nécessaires pour gérer
-- les groupes dans les compositions (1 à 5 groupes de 20 joueurs max)

-- Ajouter le champ total_groups à la table compositions
ALTER TABLE compositions 
ADD COLUMN total_groups INTEGER DEFAULT 1 CHECK (total_groups BETWEEN 1 AND 5);

-- Ajouter le champ group_number à la table composition_slots
ALTER TABLE composition_slots 
ADD COLUMN group_number INTEGER DEFAULT 1 CHECK (group_number BETWEEN 1 AND 5);

-- Mettre à jour toutes les compositions existantes avec total_groups = 1
UPDATE compositions 
SET total_groups = 1 
WHERE total_groups IS NULL;

-- Mettre à jour tous les slots existants avec group_number = 1
UPDATE composition_slots 
SET group_number = 1 
WHERE group_number IS NULL;

-- Créer un index pour améliorer les performances des requêtes groupées
CREATE INDEX idx_composition_slots_group ON composition_slots(composition_id, group_number);

-- Commentaires sur les colonnes
COMMENT ON COLUMN compositions.total_groups IS 'Nombre total de groupes dans la composition (1-5), chaque groupe contient max 20 joueurs';
COMMENT ON COLUMN composition_slots.group_number IS 'Numéro du groupe auquel appartient ce slot (1-5)';
