-- ============================================
-- Albion Zerg Manager - Supabase SQL Schema
-- ============================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TYPES
-- ============================================

-- Type pour les rôles utilisateurs
CREATE TYPE user_role AS ENUM ('admin', 'shotcaller', 'user');

-- Type pour le statut des activités
CREATE TYPE activity_status AS ENUM ('open', 'locked', 'completed', 'cancelled');

-- Type pour le statut des inscriptions
CREATE TYPE registration_status AS ENUM ('pending', 'approved', 'declined');

-- ============================================
-- TABLES
-- ============================================

-- Table des profils utilisateurs
CREATE TABLE users_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    role user_role DEFAULT 'user' NOT NULL,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Table des armes d'Albion Online
CREATE TABLE weapons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    tier INTEGER,
    icon_url TEXT,
    is_active BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Table des compositions de zerg
CREATE TABLE compositions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users_profiles(id) ON DELETE CASCADE NOT NULL,
    is_template BOOLEAN DEFAULT true NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Table des slots d'armes dans une composition
CREATE TABLE composition_slots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    composition_id UUID REFERENCES compositions(id) ON DELETE CASCADE NOT NULL,
    weapon_id UUID REFERENCES weapons(id) ON DELETE SET NULL,
    category TEXT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Table des activités/events
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    composition_id UUID REFERENCES compositions(id) ON DELETE SET NULL,
    scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
    status activity_status DEFAULT 'open' NOT NULL,
    created_by UUID REFERENCES users_profiles(id) ON DELETE CASCADE NOT NULL,
    max_participants INTEGER DEFAULT 40 NOT NULL CHECK (max_participants > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Table des inscriptions aux activités
CREATE TABLE activity_registrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES users_profiles(id) ON DELETE CASCADE NOT NULL,
    weapon_id UUID REFERENCES weapons(id) ON DELETE CASCADE NOT NULL,
    priority INTEGER NOT NULL CHECK (priority > 0),
    notes TEXT,
    status registration_status DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    UNIQUE(activity_id, user_id, weapon_id)
);

-- Table des assignations finales
CREATE TABLE activity_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    activity_id UUID REFERENCES activities(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES users_profiles(id) ON DELETE CASCADE NOT NULL,
    weapon_id UUID REFERENCES weapons(id) ON DELETE CASCADE NOT NULL,
    assigned_by UUID REFERENCES users_profiles(id) ON DELETE SET NULL NOT NULL,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    notes TEXT,
    UNIQUE(activity_id, user_id)
);

-- ============================================
-- INDEX
-- ============================================

CREATE INDEX idx_users_profiles_role ON users_profiles(role);
CREATE INDEX idx_users_profiles_username ON users_profiles(username);
CREATE INDEX idx_weapons_category ON weapons(category);
CREATE INDEX idx_weapons_active ON weapons(is_active);
CREATE INDEX idx_compositions_created_by ON compositions(created_by);
CREATE INDEX idx_composition_slots_composition ON composition_slots(composition_id);
CREATE INDEX idx_composition_slots_weapon ON composition_slots(weapon_id);
CREATE INDEX idx_activities_created_by ON activities(created_by);
CREATE INDEX idx_activities_status ON activities(status);
CREATE INDEX idx_activities_scheduled ON activities(scheduled_at);
CREATE INDEX idx_registrations_activity ON activity_registrations(activity_id);
CREATE INDEX idx_registrations_user ON activity_registrations(user_id);
CREATE INDEX idx_registrations_weapon ON activity_registrations(weapon_id);
CREATE INDEX idx_assignments_activity ON activity_assignments(activity_id);
CREATE INDEX idx_assignments_user ON activity_assignments(user_id);

-- ============================================
-- FUNCTIONS
-- ============================================

-- Fonction pour mettre à jour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour users_profiles
CREATE TRIGGER update_users_profiles_updated_at
    BEFORE UPDATE ON users_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour compositions
CREATE TRIGGER update_compositions_updated_at
    BEFORE UPDATE ON compositions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger pour activities
CREATE TRIGGER update_activities_updated_at
    BEFORE UPDATE ON activities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================

-- Activer RLS sur toutes les tables
ALTER TABLE users_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE weapons ENABLE ROW LEVEL SECURITY;
ALTER TABLE compositions ENABLE ROW LEVEL SECURITY;
ALTER TABLE composition_slots ENABLE ROW LEVEL SECURITY;
ALTER TABLE activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_assignments ENABLE ROW LEVEL SECURITY;

-- ============================================
-- RLS POLICIES - users_profiles
-- ============================================

-- Lecture : Tous les utilisateurs authentifiés peuvent voir les profils actifs
CREATE POLICY "Users can view active profiles"
    ON users_profiles FOR SELECT
    USING (auth.uid() IS NOT NULL AND is_active = true);

-- Mise à jour : Utilisateur peut modifier son propre profil (sauf role)
CREATE POLICY "Users can update own profile"
    ON users_profiles FOR UPDATE
    USING (auth.uid() = id)
    WITH CHECK (auth.uid() = id AND role = (SELECT role FROM users_profiles WHERE id = auth.uid()));

-- Admin peut tout faire
CREATE POLICY "Admins have full access to users_profiles"
    ON users_profiles FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ============================================
-- RLS POLICIES - weapons
-- ============================================

-- Lecture : Tous peuvent voir les armes actives
CREATE POLICY "Anyone can view active weapons"
    ON weapons FOR SELECT
    USING (auth.uid() IS NOT NULL AND is_active = true);

-- Modification : Admins seulement
CREATE POLICY "Only admins can manage weapons"
    ON weapons FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ============================================
-- RLS POLICIES - compositions
-- ============================================

-- Lecture : Tous les utilisateurs authentifiés
CREATE POLICY "Users can view compositions"
    ON compositions FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Création : ShotCallers et Admins
CREATE POLICY "ShotCallers can create compositions"
    ON compositions FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role IN ('shotcaller', 'admin')
        )
    );

-- Modification/Suppression : Créateur ou Admin
CREATE POLICY "Users can update own compositions"
    ON compositions FOR UPDATE
    USING (
        created_by = auth.uid() OR
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Users can delete own compositions"
    ON compositions FOR DELETE
    USING (
        created_by = auth.uid() OR
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ============================================
-- RLS POLICIES - composition_slots
-- ============================================

-- Lecture : Tous
CREATE POLICY "Users can view composition slots"
    ON composition_slots FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Modification : Créateur de la composition ou Admin
CREATE POLICY "Composition owners can manage slots"
    ON composition_slots FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM compositions c
            WHERE c.id = composition_slots.composition_id
            AND (c.created_by = auth.uid() OR
                 EXISTS (SELECT 1 FROM users_profiles WHERE id = auth.uid() AND role = 'admin'))
        )
    );

-- ============================================
-- RLS POLICIES - activities
-- ============================================

-- Lecture : Tous
CREATE POLICY "Users can view activities"
    ON activities FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Création : ShotCallers et Admins
CREATE POLICY "ShotCallers can create activities"
    ON activities FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role IN ('shotcaller', 'admin')
        )
    );

-- Modification : Créateur ou Admin
CREATE POLICY "Activity creators can update"
    ON activities FOR UPDATE
    USING (
        created_by = auth.uid() OR
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

CREATE POLICY "Activity creators can delete"
    ON activities FOR DELETE
    USING (
        created_by = auth.uid() OR
        EXISTS (
            SELECT 1 FROM users_profiles
            WHERE id = auth.uid() AND role = 'admin'
        )
    );

-- ============================================
-- RLS POLICIES - activity_registrations
-- ============================================

-- Lecture : User voit ses inscriptions + Créateur de l'activité voit toutes les inscriptions
CREATE POLICY "Users can view own registrations"
    ON activity_registrations FOR SELECT
    USING (
        user_id = auth.uid() OR
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_registrations.activity_id
            AND (a.created_by = auth.uid() OR
                 EXISTS (SELECT 1 FROM users_profiles WHERE id = auth.uid() AND role = 'admin'))
        )
    );

-- Création : Users peuvent s'inscrire si activité ouverte
CREATE POLICY "Users can register to open activities"
    ON activity_registrations FOR INSERT
    WITH CHECK (
        user_id = auth.uid() AND
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_id AND a.status = 'open'
        )
    );

-- Modification : User peut modifier ses inscriptions si activité ouverte
CREATE POLICY "Users can update own registrations"
    ON activity_registrations FOR UPDATE
    USING (
        user_id = auth.uid() AND
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_registrations.activity_id AND a.status = 'open'
        )
    );

-- Suppression : User peut se désinscrire si activité ouverte
CREATE POLICY "Users can delete own registrations"
    ON activity_registrations FOR DELETE
    USING (
        user_id = auth.uid() AND
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_registrations.activity_id AND a.status = 'open'
        )
    );

-- ============================================
-- RLS POLICIES - activity_assignments
-- ============================================

-- Lecture : Participants de l'activité + Créateur
CREATE POLICY "Users can view assignments"
    ON activity_assignments FOR SELECT
    USING (
        user_id = auth.uid() OR
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_assignments.activity_id
            AND (a.created_by = auth.uid() OR
                 EXISTS (SELECT 1 FROM users_profiles WHERE id = auth.uid() AND role = 'admin'))
        ) OR
        EXISTS (
            SELECT 1 FROM activity_registrations ar
            WHERE ar.activity_id = activity_assignments.activity_id
            AND ar.user_id = auth.uid()
        )
    );

-- Création/Modification/Suppression : Créateur de l'activité ou Admin
CREATE POLICY "Activity creators can manage assignments"
    ON activity_assignments FOR ALL
    USING (
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_assignments.activity_id
            AND (a.created_by = auth.uid() OR
                 EXISTS (SELECT 1 FROM users_profiles WHERE id = auth.uid() AND role = 'admin'))
        )
    );

-- ============================================
-- DONNÉES INITIALES - Armes d'Albion Online
-- ============================================

-- Tanks
INSERT INTO weapons (name, category) VALUES
    ('Sword', 'Tank'),
    ('Broadsword', 'Tank'),
    ('Clarent Blade', 'Tank'),
    ('Hammer', 'Tank'),
    ('Great Hammer', 'Tank'),
    ('Polehammer', 'Tank'),
    ('Mace', 'Tank'),
    ('Heavy Mace', 'Tank'),
    ('Incubus Mace', 'Tank'),
    ('Quarterstaff', 'Tank'),
    ('Iron-clad Staff', 'Tank'),
    ('Double Bladed Staff', 'Tank');

-- Healers
INSERT INTO weapons (name, category) VALUES
    ('Holy Staff', 'Healer'),
    ('Great Holy Staff', 'Healer'),
    ('Divine Staff', 'Healer'),
    ('Lifetouch Staff', 'Healer'),
    ('Redemption Staff', 'Healer'),
    ('Nature Staff', 'Healer'),
    ('Great Nature Staff', 'Healer'),
    ('Wild Staff', 'Healer'),
    ('Druidic Staff', 'Healer'),
    ('Blight Staff', 'Healer');

-- DPS Melee
INSERT INTO weapons (name, category) VALUES
    ('Axe', 'DPS Melee'),
    ('Greataxe', 'DPS Melee'),
    ('Halberd', 'DPS Melee'),
    ('Carrioncaller', 'DPS Melee'),
    ('Pike', 'DPS Melee'),
    ('Glaive', 'DPS Melee'),
    ('Dagger', 'DPS Melee'),
    ('Dagger Pair', 'DPS Melee'),
    ('Claws', 'DPS Melee'),
    ('Bloodletter', 'DPS Melee'),
    ('Black Hands', 'DPS Melee'),
    ('Spear', 'DPS Melee'),
    ('Trinity Spear', 'DPS Melee'),
    ('Spirithunter', 'DPS Melee');

-- DPS Range
INSERT INTO weapons (name, category) VALUES
    ('Bow', 'DPS Range'),
    ('Warbow', 'DPS Range'),
    ('Longbow', 'DPS Range'),
    ('Whispering Bow', 'DPS Range'),
    ('Crossbow', 'DPS Range'),
    ('Heavy Crossbow', 'DPS Range'),
    ('Light Crossbow', 'DPS Range'),
    ('Weeping Repeater', 'DPS Range'),
    ('Fire Staff', 'DPS Range'),
    ('Great Fire Staff', 'DPS Range'),
    ('Infernal Staff', 'DPS Range'),
    ('Wildfire Staff', 'DPS Range'),
    ('Frost Staff', 'DPS Range'),
    ('Glacial Staff', 'DPS Range'),
    ('Hoarfrost Staff', 'DPS Range'),
    ('Icicle Staff', 'DPS Range'),
    ('Arcane Staff', 'DPS Range'),
    ('Great Arcane Staff', 'DPS Range'),
    ('Enigmatic Staff', 'DPS Range'),
    ('Witchwork Staff', 'DPS Range'),
    ('Cursed Staff', 'DPS Range'),
    ('Great Cursed Staff', 'DPS Range'),
    ('Demonic Staff', 'DPS Range'),
    ('Shadowcaller', 'DPS Range');

-- Support/Utility
INSERT INTO weapons (name, category) VALUES
    ('Tome of Insight', 'Support'),
    ('Eye of Secrets', 'Support');

-- ============================================
-- VUES UTILES
-- ============================================

-- Vue : Statistiques des activités
CREATE OR REPLACE VIEW activity_stats AS
SELECT
    a.id AS activity_id,
    a.name AS activity_name,
    a.scheduled_at,
    a.status,
    COUNT(DISTINCT ar.user_id) AS registrations_count,
    COUNT(DISTINCT aa.user_id) AS assignments_count,
    a.max_participants
FROM activities a
LEFT JOIN activity_registrations ar ON a.id = ar.activity_id
LEFT JOIN activity_assignments aa ON a.id = aa.activity_id
GROUP BY a.id, a.name, a.scheduled_at, a.status, a.max_participants;

-- Vue : Composition avec détails des slots
CREATE OR REPLACE VIEW composition_details AS
SELECT
    c.id AS composition_id,
    c.name AS composition_name,
    c.description,
    c.created_by,
    up.username AS creator_name,
    cs.id AS slot_id,
    w.name AS weapon_name,
    cs.category,
    cs.quantity,
    c.created_at,
    c.updated_at
FROM compositions c
JOIN users_profiles up ON c.created_by = up.id
LEFT JOIN composition_slots cs ON c.id = cs.composition_id
LEFT JOIN weapons w ON cs.weapon_id = w.id;

-- ============================================
-- SCRIPT TERMINÉ
-- ============================================

-- Note: Après l'exécution de ce script, créez votre premier utilisateur admin
-- via Supabase Auth, puis mettez à jour son rôle manuellement :
--
-- UPDATE users_profiles SET role = 'admin' WHERE email = 'votre-email@example.com';
