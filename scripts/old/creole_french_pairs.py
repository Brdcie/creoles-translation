import csv
import re

# Fonction pour nettoyer les phrases créoles
def clean_creole(text):
    return re.sub(r'^\d+\.\s*', '', text).strip()

# Lire le fichier translation_pairs.txt et écrire dans un nouveau fichier CSV
with open('translation_pairs.txt', 'r', encoding='utf-8') as input_file, \
     open('creole_french_pairs.csv', 'w', newline='', encoding='utf-8') as output_file:

    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Écrire l'en-tête du CSV
    csv_writer.writerow(['Créole', 'Français'])

    for line in input_file:
        parts = line.strip().split('\t')
        if len(parts) == 3:  # S'assurer que nous avons bien 3 parties (jour, créole, français)
            _, creole, french = parts
            # Nettoyer la phrase créole en retirant le numéro au début
            creole_clean = clean_creole(creole)
            # Écrire la paire créole-français nettoyée dans le CSV
            csv_writer.writerow([creole_clean, french])

print("Le fichier 'creole_french_pairs.csv' a été créé avec succès.")