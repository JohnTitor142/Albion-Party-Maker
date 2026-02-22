-- ============================================
-- CORRECTIF : Suppression et Recréation des Policies RLS
-- Exécutez ce script pour corriger l'erreur de récursion infinie
-- ============================================

-- ============================================
-- 1. SUPPRIMER TOUTES LES POLICIES EXISTANTES
-- ============================================

DROP POLICY IF EXISTS "Users can view active profiles" ON users_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON users_profiles;
DROP POLICY IF EXISTS "Admins have full access to users_profiles" ON users_profiles;
DROP POLICY IF EXISTS "Anyone can view active weapons" ON weapons;
DROP POLICY IF EXISTS "Only admins can manage weapons" ON weapons;
DROP POLICY IF EXISTS "Users can view compositions" ON compositions;
DROP POLICY IF EXISTS "ShotCallers can create compositions" ON compositions;
DROP POLICY IF EXISTS "Users can update own compositions" ON compositions;
DROP POLICY IF EXISTS "Users can delete own compositions" ON compositions;
DROP POLICY IF EXISTS "Users can view composition slots" ON composition_slots;
DROP POLICY IF EXISTS "Composition owners can manage slots" ON composition_slots;
DROP POLICY IF EXISTS "Users can view activities" ON activities;
DROP POLICY IF EXISTS "ShotCallers can create activities" ON activities;
DROP POLICY IF EXISTS "Activity creators can update" ON activities;
DROP POLICY IF EXISTS "Activity creators can delete" ON activities;
DROP POLICY IF EXISTS "Users can view own registrations" ON activity_registrations;
DROP POLICY IF EXISTS "Users can register to open activities" ON activity_registrations;
DROP POLICY IF EXISTS "Users can update own registrations" ON activity_registrations;
DROP POLICY IF EXISTS "Users can delete own registrations" ON activity_registrations;
DROP POLICY IF EXISTS "Users can view assignments" ON activity_assignments;
DROP POLICY IF EXISTS "Activity creators can manage assignments" ON activity_assignments;

-- ============================================
-- 2. CRÉER UNE FONCTION HELPER POUR ÉVITER LA RÉCURSION
-- ============================================

-- Fonction pour obtenir le rôle de l'utilisateur sans récursion
CREATE OR REPLACE FUNCTION auth.user_role()
RETURNS TEXT AS $$
BEGIN
  RETURN (
    SELECT role::TEXT 
    FROM public.users_profiles 
    WHERE id = auth.uid()
    LIMIT 1
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

-- ============================================
-- 3. NOUVELLES POLICIES - users_profiles
-- ============================================

-- Lecture : Tous les utilisateurs authentifiés peuvent voir les profils actifs
CREATE POLICY "Users can view active profiles"
    ON users_profiles FOR SELECT
    USING (auth.uid() IS NOT NULL AND is_active = true);

-- Insertion : Permettre l'insertion lors de l'inscription
CREATE POLICY "Users can insert own profile"
    ON users_profiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Mise à jour : Utilisateur peut modifier son propre profil
-- Admin peut tout modifier
CREATE POLICY "Users can update profiles"
    ON users_profiles FOR UPDATE
    USING (
        auth.uid() = id OR 
        auth.user_role() = 'admin'
    );

-- Suppression : Admins seulement
CREATE POLICY "Admins can delete profiles"
    ON users_profiles FOR DELETE
    USING (auth.user_role() = 'admin');

-- ============================================
-- 4. NOUVELLES POLICIES - weapons
-- ============================================

-- Lecture : Tous peuvent voir les armes actives
CREATE POLICY "Anyone can view active weapons"
    ON weapons FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Modification : Admins seulement
CREATE POLICY "Only admins can manage weapons"
    ON weapons FOR ALL
    USING (auth.user_role() = 'admin');

-- ============================================
-- 5. NOUVELLES POLICIES - compositions
-- ============================================

-- Lecture : Tous
CREATE POLICY "Users can view compositions"
    ON compositions FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Création : ShotCallers et Admins
CREATE POLICY "ShotCallers can create compositions"
    ON compositions FOR INSERT
    WITH CHECK (
        auth.user_role() IN ('shotcaller', 'admin')
    );

-- Modification : Créateur ou Admin
CREATE POLICY "Users can update own compositions"
    ON compositions FOR UPDATE
    USING (
        created_by = auth.uid() OR 
        auth.user_role() = 'admin'
    );

-- Suppression : Créateur ou Admin
CREATE POLICY "Users can delete own compositions"
    ON compositions FOR DELETE
    USING (
        created_by = auth.uid() OR 
        auth.user_role() = 'admin'
    );

-- ============================================
-- 6. NOUVELLES POLICIES - composition_slots
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
            AND (c.created_by = auth.uid() OR auth.user_role() = 'admin')
        )
    );

-- ============================================
-- 7. NOUVELLES POLICIES - activities
-- ============================================

-- Lecture : Tous
CREATE POLICY "Users can view activities"
    ON activities FOR SELECT
    USING (auth.uid() IS NOT NULL);

-- Création : ShotCallers et Admins
CREATE POLICY "ShotCallers can create activities"
    ON activities FOR INSERT
    WITH CHECK (
        auth.user_role() IN ('shotcaller', 'admin')
    );

-- Modification : Créateur ou Admin
CREATE POLICY "Activity creators can update"
    ON activities FOR UPDATE
    USING (
        created_by = auth.uid() OR 
        auth.user_role() = 'admin'
    );

-- Suppression : Créateur ou Admin
CREATE POLICY "Activity creators can delete"
    ON activities FOR DELETE
    USING (
        created_by = auth.uid() OR 
        auth.user_role() = 'admin'
    );

-- ============================================
-- 8. NOUVELLES POLICIES - activity_registrations
-- ============================================

-- Lecture : User voit ses inscriptions + Créateur de l'activité voit tout
CREATE POLICY "Users can view registrations"
    ON activity_registrations FOR SELECT
    USING (
        user_id = auth.uid() OR
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_registrations.activity_id
            AND (a.created_by = auth.uid() OR auth.user_role() = 'admin')
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
-- 9. NOUVELLES POLICIES - activity_assignments
-- ============================================

-- Lecture : Participants + Créateur
CREATE POLICY "Users can view assignments"
    ON activity_assignments FOR SELECT
    USING (
        user_id = auth.uid() OR
        EXISTS (
            SELECT 1 FROM activities a
            WHERE a.id = activity_assignments.activity_id
            AND (a.created_by = auth.uid() OR auth.user_role() = 'admin')
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
            AND (a.created_by = auth.uid() OR auth.user_role() = 'admin')
        )
    );

-- ============================================
-- FIN DU SCRIPT DE CORRECTION
-- ============================================

-- Vérifier que tout fonctionne
SELECT 'Policies RLS corrigées avec succès!' AS message;
