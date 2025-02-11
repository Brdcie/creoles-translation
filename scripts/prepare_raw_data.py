import pandas as pd

# Lire le fichier XLSX
# Lister toutes les feuilles disponibles
xl = pd.ExcelFile('/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/creole_french_pairs_reference.xlsx')
print("Feuilles disponibles:", xl.sheet_names)

# Lire la feuille spécifique
df = pd.read_excel(xl, sheet_name='Kreyol-Français')
print("\nColonnes dans la feuille sélectionnée:", df.columns.tolist())

# Réorganiser les colonnes dans le bon ordre
df = df[['Français', 'Kréyol']]  # Sélectionne et réordonne les colonnes

# Renommer les colonnes pour le format standard
df.columns = ['french', 'creole']

# Nettoyage basique des données
df = df.dropna()  # Supprime les lignes vides

# Sauvegarde au format CSV
output_path = '/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/creole_french_pairs_reference.csv'
df.to_csv(output_path, index=False, encoding='utf-8')


# Vérification
df_verification = pd.read_csv(output_path, encoding='utf-8')