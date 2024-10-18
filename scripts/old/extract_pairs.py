import re

def extract_pairs(text):
    pairs = []
    lines = text.split('\n')
    for i in range(0, len(lines)-1, 2):
        creole = lines[i].strip()
        french = lines[i+1].strip()
        if creole and french:
            pairs.append((creole, french))
    return pairs

# Lire le contenu du fichier
with open('output1.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Extraire les paires
translation_pairs = extract_pairs(content)

# Afficher quelques paires pour vérification
for creole, french in translation_pairs[:10]:
    print(f"Créole: {creole}")
    print(f"Français: {french}")
    print()