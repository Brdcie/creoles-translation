import os

pdf_path ="/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf"
if os.path.exists(pdf_path):
    print("Le fichier existe.")
else:
    print("Le fichier n'existe pas. Vérifiez le chemin.")