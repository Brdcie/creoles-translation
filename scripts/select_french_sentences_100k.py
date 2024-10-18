import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Télécharger les stop words français
nltk.download('stopwords')
french_stop_words = stopwords.words('french')

# Définir le chemin de base en utilisant pathlib
base_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/processed/")
input_file_path = base_path / "cleaned_french_sentences.csv"

# Charger les phrases françaises nettoyées
french_sentences = pd.read_csv(input_file_path)

# Étape 1 : Filtrer selon les critères de longueur et de fréquence

# Critères de longueur
french_sentences['length'] = french_sentences['phrase'].apply(lambda x: len(x.split()))
selected_by_length = french_sentences[(french_sentences['length'] > 5) & (french_sentences['length'] <= 15)]

# Critères de fréquence des mots
# Obtenir toutes les phrases et compter la fréquence des mots
all_words = ' '.join(french_sentences['phrase']).split()
word_freq = Counter(all_words)

# Ajouter une colonne indiquant la fréquence moyenne des mots d'une phrase
french_sentences['avg_word_freq'] = french_sentences['phrase'].apply(
    lambda x: sum([word_freq[word] for word in nltk.word_tokenize(x)]) / len(nltk.word_tokenize(x))
)

# Sélectionner des phrases avec des mots fréquents et moins fréquents
high_freq_sentences = french_sentences[french_sentences['avg_word_freq'] > 1000]
low_freq_sentences = french_sentences[french_sentences['avg_word_freq'] <= 1000]

# Étape 2 : Combiner les phrases filtrées et échantillonner 100,000 phrases
combined_filtered_sentences = pd.concat([selected_by_length, high_freq_sentences, low_freq_sentences]).drop_duplicates()

# Échantillonner 100,000 phrases à partir des phrases filtrées
sample_size = 100000
french_sentences_sample = combined_filtered_sentences.sample(n=sample_size, random_state=42)

# Sauvegarder l'échantillon dans un nouveau fichier CSV
sample_output_file_path = base_path / "selected_french_sentences_sample_100k_filtered.csv"
french_sentences_sample.to_csv(sample_output_file_path, index=False)

# Étape 3 : Utiliser TF-IDF pour vectoriser les phrases de l'échantillon et faire du clustering
vectorizer = TfidfVectorizer(max_features=1000, stop_words=french_stop_words)
X = vectorizer.fit_transform(french_sentences_sample['phrase'])

# Appliquer KMeans pour identifier des catégories potentielles
num_categories = 5  # Vous pouvez ajuster ce nombre après la première analyse
kmeans = KMeans(n_clusters=num_categories, random_state=42)
french_sentences_sample['category'] = kmeans.fit_predict(X)

# Définir des labels textuels pour chaque catégorie (facultatif, ajustez après analyse)
category_labels = {
    0: 'Vie Quotidienne',
    1: 'Culture et Patrimoine',
    2: 'Situations d’Urgence',
    3: 'Conversations Formelles',
    4: 'Tourisme et Loisirs'
}

# Mapper les catégories numériques vers des labels textuels
french_sentences_sample['category_label'] = french_sentences_sample['category'].map(category_labels)

# Sauvegarder avec les catégories ajoutées sous forme de texte
output_file_path = base_path / "selected_french_sentences_sample_100k_filtered_with_categories.csv"
french_sentences_sample.to_csv(output_file_path, index=False)
