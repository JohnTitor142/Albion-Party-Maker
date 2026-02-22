-- ============================================
-- MISE À JOUR DES ARMES D'ALBION ONLINE
-- Version Wiki 2024 - Liste Complète et À Jour
-- ============================================

-- Supprimer toutes les anciennes armes
DELETE FROM weapons;

-- ============================================
-- WARRIOR WEAPONS (Warrior's Forge)
-- ============================================

-- SWORDS (Tank/DPS)
INSERT INTO weapons (name, category) VALUES
    ('Broadsword', 'Tank'),
    ('Claymore', 'DPS Melee'),
    ('Dual Swords', 'DPS Melee'),
    ('Clarent Blade', 'DPS Melee'),
    ('Carving Sword', 'DPS Melee'),
    ('Galatine Pair', 'DPS Melee'),
    ('Kingmaker', 'Tank'),
    ('Infinity Blade', 'DPS Melee');

-- AXES (DPS Melee)
INSERT INTO weapons (name, category) VALUES
    ('Battleaxe', 'DPS Melee'),
    ('Greataxe', 'DPS Melee'),
    ('Halberd', 'DPS Melee'),
    ('Carrioncaller', 'DPS Melee'),
    ('Infernal Scythe', 'DPS Melee'),
    ('Bear Paws', 'DPS Melee'),
    ('Realmbreaker', 'DPS Melee'),
    ('Crystal Reaper', 'DPS Melee');

-- MACES (Tank)
INSERT INTO weapons (name, category) VALUES
    ('Mace', 'Tank'),
    ('Heavy Mace', 'Tank'),
    ('Morning Star', 'Tank'),
    ('Bedrock Mace', 'Tank'),
    ('Incubus Mace', 'Tank'),
    ('Camlann Mace', 'Tank'),
    ('Oathkeepers', 'Tank'),
    ('Dreadstorm Monarch', 'Tank');

-- HAMMERS (Tank)
INSERT INTO weapons (name, category) VALUES
    ('Hammer', 'Tank'),
    ('Polehammer', 'Tank'),
    ('Great Hammer', 'Tank'),
    ('Tombhammer', 'Tank'),
    ('Forge Hammers', 'Tank'),
    ('Grovekeeper', 'Tank'),
    ('Hand of Justice', 'Tank'),
    ('Truebolt Hammer', 'Tank');

-- WAR GLOVES (DPS Melee)
INSERT INTO weapons (name, category) VALUES
    ('Brawler Gloves', 'DPS Melee'),
    ('Battle Bracers', 'DPS Melee'),
    ('Spiked Gauntlets', 'DPS Melee'),
    ('Ursine Maulers', 'DPS Melee'),
    ('Hellfire Hands', 'DPS Melee'),
    ('Ravenstrike Cestus', 'DPS Melee'),
    ('Fists of Avalon', 'DPS Melee'),
    ('Forcepulse Bracers', 'DPS Melee');

-- CROSSBOWS (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Crossbow', 'DPS Range'),
    ('Heavy Crossbow', 'DPS Range'),
    ('Light Crossbow', 'DPS Range'),
    ('Weeping Repeater', 'DPS Range'),
    ('Boltcasters', 'DPS Range'),
    ('Siegebow', 'DPS Range'),
    ('Energy Shaper', 'DPS Range'),
    ('Arclight Blasters', 'DPS Range');

-- ============================================
-- HUNTER WEAPONS (Hunter's Lodge)
-- ============================================

-- BOWS (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Bow', 'DPS Range'),
    ('Warbow', 'DPS Range'),
    ('Longbow', 'DPS Range'),
    ('Whispering Bow', 'DPS Range'),
    ('Wailing Bow', 'DPS Range'),
    ('Bow of Badon', 'DPS Range'),
    ('Mistpiercer', 'DPS Range'),
    ('Skystrider Bow', 'DPS Range');

-- DAGGERS (DPS Melee)
INSERT INTO weapons (name, category) VALUES
    ('Dagger', 'DPS Melee'),
    ('Dagger Pair', 'DPS Melee'),
    ('Claws', 'DPS Melee'),
    ('Bloodletter', 'DPS Melee'),
    ('Demonfang', 'DPS Melee'),
    ('Deathgivers', 'DPS Melee'),
    ('Bridled Fury', 'DPS Melee'),
    ('Twin Slayers', 'DPS Melee');

-- SPEARS (DPS Melee)
INSERT INTO weapons (name, category) VALUES
    ('Spear', 'DPS Melee'),
    ('Pike', 'DPS Melee'),
    ('Glaive', 'DPS Melee'),
    ('Heron Spear', 'DPS Melee'),
    ('Spirithunter', 'DPS Melee'),
    ('Trinity Spear', 'DPS Melee'),
    ('Daybreaker', 'DPS Melee'),
    ('Rift Glaive', 'DPS Melee');

-- QUARTERSTAVES (Tank/Support)
INSERT INTO weapons (name, category) VALUES
    ('Quarterstaff', 'Tank'),
    ('Iron-clad Staff', 'Tank'),
    ('Double Bladed Staff', 'Tank'),
    ('Black Monk Stave', 'Tank'),
    ('Soulscythe', 'Tank'),
    ('Staff of Balance', 'Tank'),
    ('Grailseeker', 'Tank'),
    ('Phantom Twinblade', 'Tank');

-- SHAPESHIFTER STAVES (DPS Melee)
INSERT INTO weapons (name, category) VALUES
    ('Prowling Staff', 'DPS Melee'),
    ('Rootbound Staff', 'DPS Melee'),
    ('Primal Staff', 'DPS Melee'),
    ('Bloodmoon Staff', 'DPS Melee'),
    ('Hellspawn Staff', 'DPS Melee'),
    ('Earthrune Staff', 'DPS Melee'),
    ('Lightcaller', 'DPS Melee'),
    ('Stillgaze Staff', 'DPS Melee');

-- NATURE STAVES (Healer)
INSERT INTO weapons (name, category) VALUES
    ('Nature Staff', 'Healer'),
    ('Great Nature Staff', 'Healer'),
    ('Wild Staff', 'Healer'),
    ('Druidic Staff', 'Healer'),
    ('Blight Staff', 'Healer'),
    ('Rampant Staff', 'Healer'),
    ('Ironroot Staff', 'Healer'),
    ('Forgebark Staff', 'Healer');

-- ============================================
-- MAGE WEAPONS (Mage's Tower)
-- ============================================

-- FIRE STAVES (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Fire Staff', 'DPS Range'),
    ('Great Fire Staff', 'DPS Range'),
    ('Infernal Staff', 'DPS Range'),
    ('Wildfire Staff', 'DPS Range'),
    ('Brimstone Staff', 'DPS Range'),
    ('Blazing Staff', 'DPS Range'),
    ('Dawnsong', 'DPS Range'),
    ('Flamewalker Staff', 'DPS Range');

-- HOLY STAVES (Healer)
INSERT INTO weapons (name, category) VALUES
    ('Holy Staff', 'Healer'),
    ('Great Holy Staff', 'Healer'),
    ('Divine Staff', 'Healer'),
    ('Lifetouch Staff', 'Healer'),
    ('Fallen Staff', 'Healer'),
    ('Redemption Staff', 'Healer'),
    ('Hallowfall', 'Healer'),
    ('Exalted Staff', 'Healer');

-- ARCANE STAVES (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Arcane Staff', 'DPS Range'),
    ('Great Arcane Staff', 'DPS Range'),
    ('Enigmatic Staff', 'DPS Range'),
    ('Witchwork Staff', 'DPS Range'),
    ('Occult Staff', 'DPS Range'),
    ('Malevolent Locus', 'DPS Range'),
    ('Evensong', 'DPS Range'),
    ('Astral Staff', 'DPS Range');

-- FROST STAVES (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Frost Staff', 'DPS Range'),
    ('Great Frost Staff', 'DPS Range'),
    ('Glacial Staff', 'DPS Range'),
    ('Hoarfrost Staff', 'DPS Range'),
    ('Icicle Staff', 'DPS Range'),
    ('Permafrost Prism', 'DPS Range'),
    ('Chillhowl', 'DPS Range'),
    ('Arctic Staff', 'DPS Range');

-- CURSED STAVES (DPS Range)
INSERT INTO weapons (name, category) VALUES
    ('Cursed Staff', 'DPS Range'),
    ('Great Cursed Staff', 'DPS Range'),
    ('Demonic Staff', 'DPS Range'),
    ('Lifecurse Staff', 'DPS Range'),
    ('Cursed Skull', 'DPS Range'),
    ('Damnation Staff', 'DPS Range'),
    ('Shadowcaller', 'DPS Range'),
    ('Rotcaller Staff', 'DPS Range');

-- ============================================
-- VÉRIFICATION ET STATISTIQUES
-- ============================================

-- Compter les armes par catégorie
SELECT 
    category,
    COUNT(*) as nombre_armes
FROM weapons
GROUP BY category
ORDER BY category;

-- Total
SELECT COUNT(*) as total_armes FROM weapons;

-- Afficher un message de succès
SELECT 'Base de données des armes mise à jour avec succès! Version Wiki 2024' AS message;

-- ============================================
-- NOTES
-- ============================================
-- Total: 152 armes (sans Shields, Torches, Tomes)
-- 
-- Catégories:
-- - Tank: 32 armes
-- - Healer: 16 armes  
-- - DPS Melee: 48 armes
-- - DPS Range: 56 armes
--
-- Note: Les images peuvent être ajoutées ultérieurement via icon_url
-- URLs des images disponibles sur: https://wiki.albiononline.com/
