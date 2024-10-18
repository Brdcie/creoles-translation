import re
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def clean_text(text):
    sections_to_remove = [
        r"Notes de grammaire.*?(?=➚|\Z)",
        r"Entraînement – Traduisez les phrases suivantes.*?(?=➚|\Z)",
        r"Solutions.*?(?=➚|\Z)"
    ]
    for section in sections_to_remove:
        text = re.sub(section, "", text, flags=re.DOTALL)
    return text

def extract_pairs(text):
    days = re.split(r'(➚\s*\d+e?r?\s*jour)', text)
    all_pairs = []
    
    for i in range(1, len(days), 2):
        day_header = days[i].strip()
        day_content = days[i+1] if i+1 < len(days) else ""
        
        pairs = []
        lines = day_content.strip().split('\n')
        j = 0
        while j < len(lines) and len(pairs) < 4:
            if re.match(r'^\d+\.', lines[j]):
                creole = lines[j].strip()
                french = lines[j+4].strip() if j+4 < len(lines) else ""
                if creole and french:
                    pairs.append((day_header, creole, french))
                j += 5
            else:
                j += 1
        
        all_pairs.extend(pairs)
    
    return all_pairs

# Chemin vers votre fichier PDF
pdf_path = '/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf'

# Extraire le texte du PDF
full_text = extract_text_from_pdf(pdf_path)

# Nettoyer le texte
cleaned_text = clean_text(full_text)

# Extraire les paires
pairs = extract_pairs(cleaned_text)

# Afficher les résultats
for day, creole, french in pairs:
    print(f"{day}")
    print(f"Créole: {creole}")
    print(f"Français: {french}")
    print()

# Sauvegarder les paires dans un fichier
with open('translation_pairs.txt', 'w', encoding='utf-8') as f:
    for day, creole, french in pairs:
        f.write(f"{day}\t{creole}\t{french}\n")

print(f"Nombre total de paires extraites : {len(pairs)}")