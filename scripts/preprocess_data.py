# Importation des bibliothèques nécessaires
import pandas as pd
import re
import unicodedata

# Charger le fichier TSV dans un DataFrame Pandas
file_path = '/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/Liste_Rebalanced_French.tsv'
df = pd.read_csv(file_path, sep='\t', encoding='utf-8', header=None)

# Examiner la structure du fichier
# Supposons que la colonne 0 contienne l'ID de la phrase et la colonne 1 le texte de la phrase
print(df.head())

# Évaluation de la pertinence de la numérotation
# Étant donné que chaque phrase est numérotée, nous devons décider si l'ID est nécessaire. 
# Dans ce cas, l'ID n'a probablement aucune valeur linguistique et peut être supprimé pour simplifier les données.

# Suppression de la colonne de numérotation (ID de la phrase)
df = df.drop(columns=[0])

# Renommer la colonne de texte pour une meilleure compréhension
df.columns = ['phrase']

# Fonction pour normaliser le texte
def normalize_text(text):
    # 1. Conversion en minuscule
    text = text.lower()
    
    # 2. Normalisation Unicode (en forme NFC pour conserver les accents)
    text = unicodedata.normalize('NFC', text)
    
    # 3. Suppression des caractères de contrôle invisibles
    text = re.sub(r'\s+', ' ', text)  # Remplacer tous les types d'espaces multiples par un espace simple
    
    # 4. Retirer certains caractères spéciaux qui ne sont pas pertinents
    # Conserver la ponctuation et l'apostrophe car ils sont importants en français
    text = re.sub(r"[^\w\s\.,;:!?’'à-ü-]", '', text)
    
    return text

# Application de la fonction de normalisation au DataFrame
df['phrase'] = df['phrase'].apply(normalize_text)

# Fonction de nettoyage final pour les phrases
# Cette fonction conserve la ponctuation essentielle, les accents, et les apostrophes.
# Elle supprime les caractères indésirables comme les symboles étrangers ou les symboles mathématiques.

# Aperçu des phrases normalisées
df.head()

# Sauvegarder les phrases normalisées dans un nouveau fichier CSV
df.to_csv('/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/processed/cleaned_french_sentences.csv', index=False, encoding='utf-8')


# Exemple de vérification des modifications apportées
print("Avant nettoyage :", "Bonjour! Comment ça va aujourd'hui? 😊")
print("Après nettoyage :", normalize_text("Bonjour! Comment ça va aujourd'hui? 😊"))