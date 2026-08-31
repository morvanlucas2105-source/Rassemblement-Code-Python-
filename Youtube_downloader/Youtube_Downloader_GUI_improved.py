import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import os
import threading
import subprocess
import requests
import zipfile
import shutil
from pathlib import Path

class YoutubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - Fusion Audio/Video")
        self.root.geometry("500x250")
        self.root.resizable(False, False)
        
        # Configuration du style
        self.style = ttk.Style()
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TEntry', font=('Arial', 10))
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Label et champ pour l'URL
        ttk.Label(main_frame, text="URL de la vidéo YouTube:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Information sur le format
        ttk.Label(main_frame, text="Format: MP4 avec audio intégré").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # Bouton de téléchargement
        self.download_button = ttk.Button(main_frame, text="Télécharger", command=self.start_download)
        self.download_button.grid(row=3, column=0, pady=10)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Label de statut
        self.status_label = ttk.Label(main_frame, text="Prêt à télécharger")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Configuration des poids de la grille
        main_frame.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
    
    def find_ffmpeg(self):
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

    def download_ffmpeg_auto(self):
        """Télécharge et installe FFmpeg automatiquement"""
        try:
            self.status_label.config(text="Téléchargement de FFmpeg...")
            
            # Télécharger FFmpeg
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            zip_path = os.path.join(os.getcwd(), "ffmpeg.zip")
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Extraire FFmpeg
            self.status_label.config(text="Extraction de FFmpeg...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # Trouver le dossier d'extraction
            ffmpeg_dir = None
            for item in Path('.').iterdir():
                if item.is_dir() and 'ffmpeg' in item.name.lower():
                    ffmpeg_dir = item
                    break
            
            if ffmpeg_dir:
                # Créer le dossier ffmpeg local
                local_ffmpeg = Path("ffmpeg")
                local_ffmpeg.mkdir(exist_ok=True)
                
                # Copier les fichiers binaires
                bin_path = ffmpeg_dir / "bin"
                for file in bin_path.glob("*"):
                    if file.is_file():
                        shutil.copy2(file, local_ffmpeg)
                
                # Nettoyer
                os.remove(zip_path)
                shutil.rmtree(ffmpeg_dir)
                
                return str(local_ffmpeg / "ffmpeg.exe")
            
        except Exception as e:
            self.root.after(0, lambda: self.download_error(f"Erreur installation FFmpeg: {str(e)}"))
            return None
        
        return None

    def download_video(self, url):
        try:
            # Chemin de téléchargement dans le dossier Téléchargements de l'utilisateur
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads_path):
                downloads_path = os.path.join(os.path.expanduser("~"), "Téléchargements")
            
            # Trouver ou installer FFmpeg
            ffmpeg_path = self.find_ffmpeg()
            if not ffmpeg_path:
                if messagebox.askyesno("FFmpeg non trouvé", 
                                      "FFmpeg n'est pas installé. Voulez-vous le télécharger automatiquement ?"):
                    ffmpeg_path = self.download_ffmpeg_auto()
                    if not ffmpeg_path:
                        self.root.after(0, lambda: self.download_error("Impossible d'installer FFmpeg"))
                        return
                else:
                    self.root.after(0, lambda: self.download_error("FFmpeg est requis pour fusionner audio et vidéo"))
                    return
            
            output_template = os.path.join(downloads_path, "%(title)s.%(ext)s")
            
            # Options optimisées pour garantir la fusion audio-vidéo en MP4
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
                'outtmpl': output_template,
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
                'ffmpeg_location': os.path.dirname(ffmpeg_path),
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'ignoreerrors': True,
                'no_warnings': True,
                'verbose': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.root.after(0, lambda: self.status_label.config(
                    text=f"Téléchargement: {info.get('title', 'Vidéo')}"
                ))
                ydl.download([url])
            
            self.root.after(0, self.download_complete)
            
        except yt_dlp.DownloadError as e:
            # Si le format spécifié n'est pas disponible, essayer avec format par défaut
            if "Requested format is not available" in str(e):
                try:
                    # Essayer avec une configuration encore plus simple
                    ydl_opts_simple = {
                        'format': 'best',
                        'outtmpl': output_template,
                        'progress_hooks': [self.progress_hook],
                        'noplaylist': True,
                        'ffmpeg_location': os.path.dirname(ffmpeg_path),
                        'ignoreerrors': True,
                    }
                    
                    with yt_dlp.YoutubeDL(ydl_opts_simple) as ydl:
                        ydl.download([url])
                    
                    self.root.after(0, self.download_complete)
                except Exception as e2:
                    self.root.after(0, lambda: self.download_error(str(e2)))
            else:
                self.root.after(0, lambda: self.download_error(str(e)))
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.root.after(0, lambda: self.status_label.config(text=f"Téléchargement: {d.get('_percent_str', '0%')}"))
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.status_label.config(text="Fusion audio-vidéo..."))
    
    def start_download(self):
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL YouTube valide")
            return
        
        # Désactiver le bouton pendant le téléchargement
        self.download_button.config(state='disabled')
        self.progress.start(10)
        self.status_label.config(text="Démarrage du téléchargement...")
        
        # Lancer le téléchargement dans un thread séparé
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()
    
    def download_complete(self):
        self.progress.stop()
        self.download_button.config(state='normal')
        self.status_label.config(text="Téléchargement terminé avec succès!")
        messagebox.showinfo("Succès", "La vidéo avec audio intégré a été téléchargée avec succès!")
    
    def download_error(self, error_message):
        self.progress.stop()
        self.download_button.config(state='normal')
        self.status_label.config(text="Erreur lors du téléchargement")
        messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloaderGUI(root)
    root.mainloop()
