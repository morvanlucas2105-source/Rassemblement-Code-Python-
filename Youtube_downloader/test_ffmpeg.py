import subprocess
import os
from pathlib import Path

def find_ffmpeg():
    """Trouve FFmpeg dans les emplacements communs"""
    # Emplacements communs pour FFmpeg
    common_paths = [
        "C:\\ffmpeg\\ffmpeg.exe",
        "C:\\Program Files\\ffmpeg\\ffmpeg.exe",
        "C:\\Program Files (x86)\\ffmpeg\\ffmpeg.exe",
        os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg.exe"),
    ]
    
    # Vérifier dans le PATH système
    try:
        result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    # Vérifier les emplacements communs
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

# Test de la détection FFmpeg
ffmpeg_path = find_ffmpeg()
if ffmpeg_path:
    print(f"FFmpeg trouvé à: {ffmpeg_path}")
    # Tester si FFmpeg fonctionne
    try:
        result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg fonctionne correctement!")
            print(result.stdout.split('\n')[0])  # Afficher la version
        else:
            print("FFmpeg trouvé mais ne fonctionne pas correctement")
    except Exception as e:
        print(f"Erreur lors du test FFmpeg: {e}")
else:
    print("FFmpeg non trouvé. Il faudra l'installer automatiquement.")
    print("Le téléchargeur proposera de télécharger FFmpeg automatiquement lors du premier lancement.")
