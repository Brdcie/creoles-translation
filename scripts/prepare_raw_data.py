import pandas as pd

# Lire le fichier XLSX
df = pd.read_excel('/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/creole_french_pairs_reference.xlsx')

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
# Afficher quelques lignes contenant des accents
accents_check = df[df['french'].str.contains('[éèêëàâäôöûüç]', na=False) | 
                   df['creole'].str.contains('[éèêëàâäôöûüç]', na=False)]
print("\nExemples de lignes avec accents :")
print(accents_check.head())
print("Premières lignes du fichier transformé :")
print(df.head())
print(f"\nNombre total de paires : {len(df)}")