import camelot
import pandas as pd
import re

# Configuration
PDF_PATH = '../data/raw/PDF/assimil-9782700561043-guide-francais-creole.pdf'
START_PAGE = 65
END_PAGE = 183
OUTPUT_XLSX = 'couples_bilingues.xlsx'

# Liste des chapitres pour Source 2
CHAPTERS = [
    "Premiers contacts",
    "Rencontre et présentation",
    "Temps, dates, fêtes",
    "Appels à l’aide",
    "Voyager",
    "En ville",
    "À la montagne, à la plage, à la campagne, dans la mangrove",
    "Hébergement",
    "Nourriture",
    "Achats et souvenirs",
    "Rendez-vous professionnels",
    "Santé"
]

def extract_tables_with_camelot(pdf_path, start_page, end_page):
    """
    Extrait les tableaux du PDF entre start_page et end_page en utilisant Camelot.
    Retourne une liste de DataFrames pandas.
    """
    print("Extraction des tableaux avec Camelot...")
    tables = camelot.read_pdf(
        pdf_path,
        pages=f"{start_page}-{end_page}",
        flavor='stream',  # 'stream' pour les tableaux sans bordures explicites
        strip_text='\n',
        edge_tol=500  # Ajuster en fonction de la mise en page
    )
    print(f"Nombre de tableaux extraits : {len(tables)}")
    return tables
def process_tables(tables):
    """
    Traite les tableaux extraits et organise les données avec les colonnes requises.
    """
    data = []

    for table in tables:
        df = table.df
        page_number = table.page  # Récupérer le numéro de page du tableau

        # Afficher des informations sur le tableau extrait
        print(f"Page {page_number} : tableau avec {df.shape[0]} lignes et {df.shape[1]} colonnes")

        # Supposons que la première ligne est l'en-tête, vérifier et ignorer si nécessaire
        if any(keyword.lower() in df.iloc[0, 0].lower() for keyword in ["kréyol", "français"]):
            df = df[1:]  # Ignorer la première ligne

        # Vérifier si le tableau a au moins deux colonnes
        if df.shape[1] < 2:
            print(f"Page {page_number} : tableau ignoré, nombre de colonnes insuffisant.")
            continue

        for index, row in df.iterrows():
            # Vérifier si les deux colonnes existent
            if len(row) < 2:
                # Passer cette ligne si elle n'a pas deux colonnes
                continue

            # Extraire les valeurs créole et français
            french = row[0].strip()
            creole = row[1].strip()

            # Vérifier si les deux colonnes ne sont pas vides
            if creole and french:
                data.append({
                    'Kréyol': creole,
                    'Français': french,
                    'Source': 'Conversation',
                    'Source 2': f'Page {page_number}'  # Remplacer par le numéro de page
                })

    return data


def identify_chapter(line):
    """
    Identifie si une ligne correspond à un chapitre et retourne le nom du chapitre.
    """
    for chapter in CHAPTERS:
        if chapter.lower() in line.lower():
            return chapter
    return None


def main():
    # Extraire les tableaux
    tables = extract_tables_with_camelot(PDF_PATH, START_PAGE, END_PAGE)

    if not tables:
        print("Aucun tableau extrait. Vérifiez le chemin du fichier PDF et la plage des pages.")
        return

    # Traiter les tableaux pour extraire les paires bilingues avec les numéros de page
    bilingual_data = process_tables(tables)

    if not bilingual_data:
        print("Aucune paire bilingue extraite. Vérifiez la structure des tableaux dans le PDF.")
        return

    print(f"Nombre de couples extraits : {len(bilingual_data)}")

    # Créer un DataFrame pandas
    df = pd.DataFrame(bilingual_data, columns=['Kréyol', 'Français', 'Source', 'Source 2'])

    # Sauvegarder le DataFrame dans un fichier Excel
    print(f"Sauvegarde des données dans {OUTPUT_XLSX}...")
    df.to_excel(OUTPUT_XLSX, index=False, engine='openpyxl')

    print("Extraction et sauvegarde terminées avec succès.")

if __name__ == "__main__":
    main()
