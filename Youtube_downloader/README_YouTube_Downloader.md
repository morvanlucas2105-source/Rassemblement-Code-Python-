# YouTube Downloader GUI

Une interface graphique simple pour télécharger des vidéos YouTube en format MP4.

## Fonctionnalités

- Interface graphique conviviale avec tkinter
- Téléchargement de vidéos YouTube en format MP4 (vidéo complète)
- Barre de progression en temps réel
- Gestion des erreurs avec messages d'alerte
- Téléchargement automatique dans le dossier Téléchargements

## Prérequis

### 1. Installation de Python
Assurez-vous d'avoir Python 3.6+ installé sur votre système.

### 2. Installation des dépendances
```bash
pip install yt-dlp
```

## Utilisation

1. Lancez l'application :
```bash
python Youtube_Downloader_GUI.py
```

2. Collez l'URL de la vidéo YouTube dans le champ prévu

3. Cliquez sur le bouton "Télécharger"

4. La barre de progression montrera l'avancement du téléchargement

5. Les fichiers sont sauvegardés dans votre dossier Téléchargements :
   - Windows: `C:\Users\VotreNom\Downloads` ou `C:\Users\VotreNom\Téléchargements`
   - Linux: `~/Downloads` ou `~/Téléchargements`
   - macOS: `~/Downloads`

## Format des fichiers

- **MP4**: Les vidéos sont téléchargées dans la meilleure qualité disponible

## Dépannage

### Erreur de téléchargement
- Vérifiez que l'URL YouTube est valide
- Assurez-vous d'avoir une connexion internet stable
- Vérifiez que la vidéo n'est pas privée ou restreinte

### L'application ne se lance pas
Vérifiez que toutes les dépendances sont installées :
```bash
pip install yt-dlp
```

## Notes

- L'application utilise yt-dlp, une version améliorée de youtube-dl
- Les téléchargements sont effectués dans un thread séparé pour ne pas bloquer l'interface
- L'interface est responsive et s'adapte à différentes résolutions d'écran
