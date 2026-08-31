import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import os
import threading

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Téléchargeur Vidéo YouTube")
        self.root.geometry("500x200")
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
        
        # Bouton de téléchargement
        self.download_button = ttk.Button(main_frame, text="Télécharger", command=self.start_download)
        self.download_button.grid(row=2, column=0, pady=10)
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Label de statut
        self.status_label = ttk.Label(main_frame, text="Prêt à télécharger")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Configuration des poids de la grille
        main_frame.columnconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
    def download_video(self, url):
        try:
            # Chemin de téléchargement dans le dossier D: avec nom de fichier basé sur le titre de la vidéo
            downloads_path = os.path.join("D:", "Video_Download", "%(title)s.%(ext)s")
            
            # Créer le dossier de destination s'il n'existe pas
            os.makedirs(os.path.join("D:", "Video_Download"), exist_ok=True)
            
            # Options pour garantir l'intégration audio-vidéo
            ydl_opts = {
                'format': 'best',
                'outtmpl': downloads_path,
                'merge_output_format': 'mp4',
                'ignoreerrors': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.root.after(0, self.download_complete)
            
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
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
        messagebox.showinfo("Succès", "La vidéo a été téléchargée avec succès dans D:\\Video_Download\\")
    
    def download_error(self, error_message):
        self.progress.stop()
        self.download_button.config(state='normal')
        self.status_label.config(text="Erreur lors du téléchargement")
        messagebox.showerror("Erreur", f"Une erreur s'est produite:\n{error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()
