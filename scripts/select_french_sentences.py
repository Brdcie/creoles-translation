from collections import Counter
import nltk
from pathlib import Path
import pandas as pd

# Télécharger punkt pour la tokenisation
nltk.download('punkt')

# Définir le chemin de base en utilisant pathlib
base_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/processed/")

# Charger les phrases françaises nettoyées une seule fois
input_file_path = base_path / "cleaned_french_sentences.csv"
french_sentences = pd.read_csv(input_file_path)

# Critères de longueur
french_sentences['length'] = french_sentences['phrase'].apply(lambda x: len(x.split()))
selected_by_length = french_sentences[(french_sentences['length'] > 5) & (french_sentences['length'] <= 15)].sample(50000)

# Critères de fréquence

# Obtenir toutes les phrases et compter la fréquence des mots
all_words = ' '.join(french_sentences['phrase']).split()
word_freq = Counter(all_words)

# Ajouter une colonne indiquant la fréquence moyenne des mots d'une phrase
french_sentences['avg_word_freq'] = french_sentences['phrase'].apply(
    lambda x: sum([word_freq[word] for word in nltk.word_tokenize(x)]) / len(nltk.word_tokenize(x))
)
# Sélectionner des phrases avec des mots à faible fréquence
low_freq_subset = french_sentences[french_sentences['avg_word_freq'] <= 1000]

# Vérifier la taille du sous-ensemble et ajuster l'échantillonnage
if len(low_freq_subset) < 50000:
    print(f"Attention : seulement {len(low_freq_subset)} phrases disponibles avec des mots à faible fréquence.")
    low_freq_sentences = low_freq_subset.sample(len(low_freq_subset), random_state=42)
else:
    low_freq_sentences = low_freq_subset.sample(50000, random_state=42)

# Sélectionner des phrases avec des mots très fréquents et des mots moins fréquents
high_freq_sentences = french_sentences[french_sentences['avg_word_freq'] > 1000].sample(50000, random_state=42)
low_freq_sentences = french_sentences[french_sentences['avg_word_freq'] <= 1000].sample(5762, random_state=42)

# Combiner les deux échantillons pour obtenir un ensemble basé sur la fréquence
selected_sentences_by_frequency = pd.concat([high_freq_sentences, low_freq_sentences]).drop_duplicates()

# Définir le chemin de sortie pour les phrases sélectionnées par fréquence
output_file_path_frequency = base_path / "selected_french_sentences_by_frequency.csv"
selected_sentences_by_frequency.to_csv(output_file_path_frequency, index=False)

# Critères d'adaptation culturelle

# Définir une liste de références culturelles à marquer
cultural_references = ['Tour Eiffel', 'Champs-Élysées', 'Versailles', 'Métro parisien', 'Bastille']

# Ajouter une colonne pour indiquer si la phrase contient une référence culturelle
french_sentences['contains_cultural_reference'] = french_sentences['phrase'].apply(
    lambda x: any(ref in x for ref in cultural_references)
)

# Filtrer les phrases pertinentes (sans références culturelles)
relevant_sentences = french_sentences[~french_sentences['contains_cultural_reference']]

# Filtrer les phrases qui contiennent des références culturelles
cultural_sentences = french_sentences[french_sentences['contains_cultural_reference']]

# Échantillonner des phrases pertinentes (par exemple 80% de l'ensemble)
selected_relevant_sentences = relevant_sentences.sample(frac=0.8, random_state=42)

# Échantillonner des phrases avec références culturelles (par exemple 20% de l'ensemble)
selected_cultural_sentences = cultural_sentences.sample(frac=0.2, random_state=42)

# Combiner les deux échantillons pour obtenir un ensemble équilibré
selected_sentences_with_cultural = pd.concat([selected_relevant_sentences, selected_cultural_sentences]).drop_duplicates()

# Sauvegarder le fichier des phrases sélectionnées
output_file_path_cultural = base_path / "selected_french_sentences_with_cultural.csv"
selected_sentences_with_cultural.to_csv(output_file_path_cultural, index=False)

# Combiner les critères pour sélectionner 100,000 phrases finales

# Combiner les phrases sélectionnées par longueur, fréquence, et adaptation culturelle
combined_sample = pd.concat([selected_by_length, selected_sentences_by_frequency, selected_sentences_with_cultural]).drop_duplicates()

# S'assurer d'avoir 100,000 phrases uniques
if len(combined_sample) >= 100000:
    combined_sample = combined_sample.sample(100000, random_state=42)
else:
    print(f"Attention : le nombre de phrases disponibles est inférieur à 100,000. Total actuel : {len(combined_sample)}")

# Définir le chemin de sortie pour les phrases combinées sélectionnées
output_file_path_combined = base_path / "selected_french_sentences.csv"
combined_sample.to_csv(output_file_path_combined, index=False)
