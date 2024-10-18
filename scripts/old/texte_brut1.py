import PyPDF2

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Utilisation
pdf_path = '/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf'
text = pdf_to_text(pdf_path)

# Sauvegarder le texte dans un fichier
with open('output1.txt', 'w', encoding='utf-8') as f:
    f.write(text)
