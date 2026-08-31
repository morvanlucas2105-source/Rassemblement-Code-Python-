from tkinter import *
import webbrowser

champs1url1="https://"
champs1url2=":4343/admin/"

def actionEvent(event):
    lbl.configure(text = "Votre IP est "+ entry.get())
    champs1url = champs1url1 + entry.get() + champs1url2
    webbrowser.open(champs1url)

root = Tk()
root.geometry("300x150")
entry = Entry(root)

# Association de l'évènement actionEvent au champ de saisie
entry.bind("<Return>", actionEvent)
lbl = Label(root, text="Entrer IP")
entry.pack()
lbl.pack()
root.mainloop()