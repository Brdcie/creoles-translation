import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox
from pathlib import Path

# Path to the uploaded PDF
#pdf_path = "/mnt/data/assimil-9782700561043-guide-francais-creole.pdf"
pdf_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/pdf/assimil-9782700561043-guide-francais-creole.pdf")

# Dictionary to store sentences with their page numbers
sentences_with_pages = []

# Extract text from each page and track page numbers
for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
    page_text = []
    
    for element in page_layout:
        if isinstance(element, LTTextBox):
            page_text.extend(element.get_text().split("\n"))

    # Process lines to extract sentence pairs
    french_sentence = None
    for line in page_text:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        if french_sentence is None:
            french_sentence = line  # Store French sentence
        else:
            creole_sentence = line
            sentences_with_pages.append([creole_sentence, french_sentence, page_num])
            french_sentence = None  # Reset

# Convert to DataFrame
df_with_pages = pd.DataFrame(sentences_with_pages, columns=["Créole", "Français", "Page"])

# Save updated DataFrame to Excel with page numbers
#output_excel_path = "/mnt/data/Tableau_Francais_Creole_Avec_Pages.xlsx"
output_excel_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/all_book_pairs.xlsx")
    

df_with_pages.to_excel(output_excel_path, index=False)

# Provide download link
print(f"Fichier Excel sauvegardé: {output_excel_path}")
