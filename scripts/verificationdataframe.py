import pandas as pd
from pathlib import Path
# Définir le chemin de base en utilisant pathlib
base_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/processed/")

# Charger les phrases françaises nettoyées une seule fois
input_file_path = base_path / "cleaned_french_sentences.csv"
french_sentences = pd.read_csv(input_file_path)


# Afficher les colonnes disponibles
print(french_sentences.columns)
