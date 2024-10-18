from pdfminer.high_level import extract_text
import re

def clean_and_filter_text(text):
    # Start from page 16
    pages = text.split('\f')
    if len(pages) > 16:
        text = '\f'.join(pages[16:])
    
    # Extract content between "1er jour" and "2e jour"
    pattern = r'1er jour(.*?)2e jour'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def extract_translation_pairs(cleaned_text):
    pairs = []
    lines = cleaned_text.split('\n')
    for i in range(len(lines)-1):
        if lines[i].strip().startswith('1.'):
            creole = lines[i].strip()[3:]  # Remove the '1. ' prefix
            if i+1 < len(lines):
                french = lines[i+1].strip()
                if creole and french:
                    pairs.append((creole, french))
    return pairs

# Extract text
#pdf_path = '/chemin/vers/votre/fichier.pdf'
pdf_path = '/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf'
full_text = extract_text(pdf_path)

# Clean and filter
cleaned_text = clean_and_filter_text(full_text)

# Extract translation pairs
translation_pairs = extract_translation_pairs(cleaned_text)

# Display pairs
for creole, french in translation_pairs:
    print(f"Créole: {creole}")
    print(f"Français: {french}")
    print()

# Save pairs to file
with open('translation_pairs.txt', 'w', encoding='utf-8') as f:
    for creole, french in translation_pairs:
        f.write(f"{creole}\t{french}\n")