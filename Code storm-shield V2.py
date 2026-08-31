from tkinter import *
import webbrowser
import time

champs1url1 = "https://"
champs1url2 = ":4343/admin/"

# Liste pour stocker les champs d'entrée
entries = []

def actionEvent(event, entry):
    """Ouvre le navigateur avec l'URL construite à partir de l'entrée"""
    ip = entry.get()
    if ip:
        champs1url = champs1url1 + ip + champs1url2
        webbrowser.open(champs1url)

def open_all_urls():
    """Ouvre toutes les URLs des champs remplis avec délai"""
    for entry in entries:
        ip = entry.get()
        if ip:
            champs1url = champs1url1 + ip + champs1url2
            webbrowser.open(champs1url)
            time.sleep(0.5)  # Délai de 0.5 seconde entre chaque ouverture

def open_individual_url(event, entry):
    """Ouvre l'URL du champ spécifique"""
    actionEvent(event, entry)

def add_new_field():
    """Ajoute un nouveau champ d'entrée avec son bouton associé"""
    # Créer un nouveau frame pour le champ et son bouton
    new_frame = Frame(main_frame)
    new_frame.pack(pady=2, anchor="center")
    
    # Créer le nouveau champ d'entrée
    new_entry = Entry(new_frame, width=15)
    new_entry.pack(side="left", padx=2)
    
    # Ajouter à la liste des champs
    entries.append(new_entry)
    
    # Créer le bouton pour ouvrir cette URL
    open_button = Button(new_frame, text="Ouvrir", 
                        command=lambda e=new_entry: actionEvent(None, e))
    open_button.pack(side="left", padx=2)

root = Tk()
root.geometry("350x400")
root.title("Gestionnaire de connexions")

# Frame principal avec alignement au centre
main_frame = Frame(root)
main_frame.pack(pady=10, anchor="center")

# Label principal aligné au centre
lbl = Label(main_frame, text="Entrer IP")
lbl.pack(pady=5)

# Frame pour le premier champ avec boutons
first_frame = Frame(main_frame)
first_frame.pack(pady=5)

# Bouton +1 à gauche du premier champ
add_button = Button(first_frame, text="+1", command=add_new_field)
add_button.pack(side=LEFT, padx=5)

# Premier champ d'entrée
first_entry = Entry(first_frame, width=15)
first_entry.pack(side=LEFT, padx=5)
entries.append(first_entry)

# Bouton ouvrir tous à droite du premier champ
all_button = Button(first_frame, text="Ouvrir Tous", command=open_all_urls)
all_button.pack(side=LEFT, padx=5)

# Frame pour contenir tous les autres champs
fields_frame = Frame(main_frame)
fields_frame.pack(pady=5)

# Lier la touche Entrée globalement à la fonction open_all_urls
root.bind_all("<Return>", lambda event: open_all_urls())

root.mainloop()
