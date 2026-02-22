@echo off
echo ========================================
echo   Git Setup - Albion Zerg Manager
echo ========================================
echo.

REM Vérifier si git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git n'est pas installé !
    echo.
    echo Téléchargez Git depuis : https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git est installé
echo.

REM Vérifier si déjà un repo git
if exist .git (
    echo [INFO] Repository Git déjà initialisé
    echo.
    git status
    pause
    exit /b 0
)

echo [ETAPE 1] Initialisation du repository Git...
git init
if errorlevel 1 (
    echo [ERROR] Échec de l'initialisation Git
    pause
    exit /b 1
)
echo [OK] Repository initialisé
echo.

echo [ETAPE 2] Ajout de tous les fichiers...
git add .
if errorlevel 1 (
    echo [ERROR] Échec de l'ajout des fichiers
    pause
    exit /b 1
)
echo [OK] Fichiers ajoutés
echo.

echo [ETAPE 3] Premier commit...
git commit -m "Initial commit - Albion Zerg Manager"
if errorlevel 1 (
    echo [WARNING] Aucun changement à commiter ou erreur de commit
    echo.
)
echo [OK] Commit créé
echo.

echo ========================================
echo   Configuration terminée !
echo ========================================
echo.
echo Prochaines étapes :
echo.
echo 1. Créez un repository sur GitHub :
echo    https://github.com/new
echo.
echo 2. Connectez votre repo local :
echo    git remote add origin https://github.com/VOTRE_USERNAME/albion-zerg-manager.git
echo.
echo 3. Poussez le code :
echo    git branch -M main
echo    git push -u origin main
echo.
echo Guide complet : DEPLOY_STREAMLIT.md
echo.
pause
