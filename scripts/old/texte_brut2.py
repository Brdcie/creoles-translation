from pdfminer.high_level import extract_text

def pdf_to_text(pdf_path):
    return extract_text(pdf_path)

# Utilisation
pdf_path='/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf'

text = pdf_to_text(pdf_path)

# Sauvegarder le texte dans un fichier
with open('output2.txt', 'w', encoding='utf-8') as f:
    f.write(text)