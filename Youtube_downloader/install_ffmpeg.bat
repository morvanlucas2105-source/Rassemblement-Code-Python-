@echo off
echo Installation de FFmpeg pour Windows...
echo.

:: Vérifier si PowerShell est disponible
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo Erreur: PowerShell n'est pas disponible.
    pause
    exit /b 1
)

:: Télécharger FFmpeg
echo Téléchargement de FFmpeg...
powershell -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'"

:: Vérifier si le téléchargement a réussi
if not exist ffmpeg.zip (
    echo Erreur: Le téléchargement a échoué.
    pause
    exit /b 1
)

:: Extraire FFmpeg
echo Extraction de FFmpeg...
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force"

:: Trouver le dossier d'extraction
for /d %%i in (ffmpeg-*) do set "ffmpeg_dir=%%i"

if not defined ffmpeg_dir (
    echo Erreur: Impossible de trouver le dossier FFmpeg.
    pause
    exit /b 1
)

:: Copier les fichiers binaires
echo Installation de FFmpeg...
mkdir "C:\ffmpeg" 2>nul
xcopy "%ffmpeg_dir%\bin\*" "C:\ffmpeg\" /Y /E /I

:: Ajouter au PATH système
echo Ajout de FFmpeg au PATH...
setx PATH "%PATH%;C:\ffmpeg" /M

:: Nettoyer
echo Nettoyage...
del ffmpeg.zip
rmdir /s /q "%ffmpeg_dir%"

echo.
echo FFmpeg a été installé avec succès!
echo Redémarrez votre terminal pour que les changements prennent effet.
echo.
pause
