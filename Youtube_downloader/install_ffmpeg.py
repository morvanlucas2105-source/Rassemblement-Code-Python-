import os
import zipfile
import requests
import subprocess
import sys
from pathlib import Path

def download_ffmpeg():
    print("Téléchargement de FFmpeg...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    local_filename = "ffmpeg.zip"
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Téléchargement terminé.")
        return local_filename
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return None

def extract_ffmpeg(zip_path):
    print("Extraction de FFmpeg...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("Extraction terminée.")
        
        # Trouver le dossier d'extraction
        for item in Path('.').iterdir():
            if item.is_dir() and 'ffmpeg' in item.name.lower():
                return item
        return None
    except Exception as e:
        print(f"Erreur lors de l'extraction: {e}")
        return None

def install_ffmpeg(ffmpeg_dir):
    print("Installation de FFmpeg...")
    try:
        # Créer le dossier d'installation
        install_path = Path("C:/ffmpeg")
        install_path.mkdir(exist_ok=True)
        
        # Copier les fichiers binaires
        bin_path = ffmpeg_dir / "bin"
        for file in bin_path.glob("*"):
            if file.is_file():
                target = install_path / file.name
                with open(file, 'rb') as src, open(target, 'wb') as dst:
                    dst.write(src.read())
        
        # Ajouter au PATH utilisateur
        add_to_user_path(str(install_path))
        
        print(f"FFmpeg installé dans: {install_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'installation: {e}")
        return False

def add_to_user_path(ffmpeg_path):
    """Ajouter FFmpeg au PATH de l'utilisateur"""
    try:
        import winreg
        
        # Ouvrir la clé Environment de l'utilisateur
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            "Environment", 
                            0, 
                            winreg.KEY_READ | winreg.KEY_WRITE)
        
        # Lire la valeur actuelle du PATH
        try:
            current_path, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current_path = ""
        
        # Ajouter FFmpeg au PATH s'il n'y est pas déjà
        if ffmpeg_path not in current_path:
            new_path = f"{current_path};{ffmpeg_path}" if current_path else ffmpeg_path
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
            print("FFmpeg ajouté au PATH utilisateur.")
        else:
            print("FFmpeg est déjà dans le PATH.")
            
        winreg.CloseKey(key)
        
    except Exception as e:
        print(f"Impossible de modifier le PATH: {e}")

def main():
    print("=== Installation de FFmpeg ===")
    
    # Vérifier si FFmpeg est déjà installé
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("FFmpeg est déjà installé!")
            return
    except:
        pass
    
    # Télécharger FFmpeg
    zip_file = download_ffmpeg()
    if not zip_file:
        return
    
    # Extraire FFmpeg
    ffmpeg_dir = extract_ffmpeg(zip_file)
    if not ffmpeg_dir:
        return
    
    # Installer FFmpeg
    if install_ffmpeg(ffmpeg_dir):
        print("\n✅ FFmpeg a été installé avec succès!")
        print("Redémarrez votre terminal pour que les changements prennent effet.")
    else:
        print("\n❌ L'installation de FFmpeg a échoué.")
    
    # Nettoyer
    try:
        os.remove(zip_file)
        import shutil
        shutil.rmtree(ffmpeg_dir)
    except:
        pass

if __name__ == "__main__":
    main()
