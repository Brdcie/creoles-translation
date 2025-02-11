# scripts/prepare_training_data.py
import os
os.system('clear')
import pandas as pd
from pathlib import Path
import sys
from pathlib import Path
# Ajouter le répertoire parent au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
import re
from pathlib import Path
import pandas as pd
from typing import List, Dict
from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from src.french_to_creole import transform_french_to_creole
from src.constants import PRONOUN_MAPPING, PRONOUN_PATTERN, GRAMMAR_MARKERS, TRANSFORMATION_RULES
from src.special_words import SPECIAL_WORDS

@dataclass 
class GrammarPattern:
    french_pattern: str
    creole_pattern: str 
    examples: List[tuple]
    priority: int

def apply_grammar_patterns(df: pd.DataFrame) -> List[Dict]:
    transformed_pairs = []

    patterns = [
        # Négation
        GrammarPattern(
            french_pattern=fr"{PRONOUN_PATTERN}\s+ne\s+(\w+)\s+pas",
            creole_pattern=r"\1 pa ka \2",
            examples=[
                ("je ne mange pas", "an pa ka manjé"),
                ("tu ne parles pas", "ou pa ka palé"),
                ("il ne dort pas", "i pa ka dòmi"),
                ("nous ne marchons pas", "nou pa ka maché"),
                ("vous ne dansez pas", "zò pa ka dansé"),
                ("ils ne courent pas", "yo pa ka kouri")
            ],
            priority=1
        ),
        # Futur proche
        GrammarPattern(
            french_pattern=fr"{PRONOUN_PATTERN}\s+(vais|vas|va|allons|allez|vont)\s+(\w+)",
            creole_pattern=r"\1 kay \2",
            examples=[
                ("je vais manger", "an kay manjé"),
                ("tu vas dormir", "ou kay dòmi"),
                ("il va partir", "i kay pati"),
                ("nous allons marcher", "nou kay maché"),
                ("vous allez danser", "zò kay dansé"),
                ("ils vont travailler", "yo kay travay")
            ],
            priority=2
        ),
        # Imparfait avec "té"
        GrammarPattern(
            french_pattern=fr"{PRONOUN_PATTERN}\s+(étais|étais|était|étions|étiez|étaient)",
            creole_pattern=r"\1 té \2",
            examples=[
                ("j'étais malade", "an té malad"),
                ("il était parti", "i té pati"),
                ("nous avions mangé", "nou té manjé"),
                ("ils étaient fatigués", "yo té las"),
                ("vous étiez contents", "zòt té kontan")
            ],
            priority=1
        ),
        # Passé récent avec "sòti"
        GrammarPattern(
            french_pattern=fr"{PRONOUN_PATTERN}\s+vien[ts]?\s+de\s+(\w+)",
            creole_pattern=r"\1 sòti \2",
            examples=[
                ("je viens de manger", "an sòti manjé"),
                ("il vient de partir", "i sòti pati"),
                ("nous venons d'arriver", "nou sòti rivé"),
                ("ils viennent de finir", "yo sòti fini")
            ],
            priority=1
        ),
        # Futur simple avec "ké"
        GrammarPattern(
            french_pattern=fr"{PRONOUN_PATTERN}\s+(\w+)rai[ts]?",
            creole_pattern=r"\1 ké \2",
            examples=[
                ("je mangerai", "an ké manjé"),
                ("tu dormiras", "ou ké dòmi"),
                ("il partira", "i ké pati"),
                ("nous danserons", "nou ké dansé"),
                ("vous parlerez", "zò ké palé"),
                ("ils finiront", "yo ké fini")
            ],
            priority=1
        )
    ]
    
    for _, row in df.iterrows():
        french_text = row['french'].lower()
        
        for pattern in sorted(patterns, key=lambda x: x.priority):
            match = re.search(pattern.french_pattern, french_text, re.IGNORECASE)
            
            if match:
                # Créer d'abord la phrase créole avec les groupes capturés
                creole_text = pattern.creole_pattern
                
                # Remplacer les groupes capturés
                for i, group in enumerate(match.groups(), 1):
                    if i == 1:  # Si c'est le pronom
                        pronoun = group.lower()
                        replacement = PRONOUN_MAPPING.get(pronoun, pronoun)
                        creole_text = creole_text.replace(f"\\{i}", replacement)
                    else:  # Pour les autres groupes
                        creole_text = creole_text.replace(f"\\{i}", transform_french_to_creole(group))
                
                transformed_pairs.append({
                    'french': french_text,
                    'creole': creole_text,
                    'type': 'grammar_pattern',
                    'confidence': 0.7,
                    'pattern_type': pattern.french_pattern
                })
    
    return transformed_pairs

def load_base_pairs():
    project_root = Path(__file__).parent.parent
    pairs_path = project_root / "data" / "raw" / "creole_french_pairs_reference.xlsx"
    print(f"Loading file from: {pairs_path}")
    
    # Lire le fichier Excel

    df = pd.read_excel(pairs_path)
    
    #Renommer les colonnes pour correspondre au format attendu
    df = df.rename(columns={
        'Français': 'french', 
        'Kréyol': 'creole'
    })
    
    # Sélectionner uniquement les colonnes nécessaires
    df = df[['french', 'creole']]
    
    # Ajouter une colonne de type et de confiance par défaut
    df['type'] = 'original'
    df['confidence'] = 1.0
    
    return df

def clean_text(text):
    """Nettoie et normalise le texte"""
    text = text.strip()
    text = ' '.join(text.split())  # Normalise les espaces
    return text
def augment_data(df: pd.DataFrame) -> pd.DataFrame:
    augmented_pairs = []

    def validate_vocab_transform(french: str, creole: str) -> bool:
        # Nettoyage du mot
        french = re.sub(r'[.,!?]', '', french)
    
        # Vérifier la longueur minimale (sauf pour les marqueurs grammaticaux)
        if creole.lower() in GRAMMAR_MARKERS:
            return True
        if len(french) < 2 or len(creole) < 2:
            return False      
        return True   
    
    # 1. Conserver les paires originales avec confiance maximale
    original_pairs = [{
        'french': row['french'],
        'creole': row['creole'],
        'type': 'original',
        'confidence': 1.0
    } for _, row in df.iterrows()]
    augmented_pairs.extend(original_pairs)
    
    print(f"\nPaires originales chargées: {len(original_pairs)}")
    
    # Créer un dictionnaire de référence des mots connus
    # Créer un dictionnaire unifié des mots connus
    known_words = {}
    
    # Ajouter les mots de SPECIAL_WORDS
    known_words.update(SPECIAL_WORDS)
    
    # Ajouter les pronoms
    known_words.update(PRONOUN_MAPPING)
    # Ajouter les mots simples du dataset original
    known_words = {
        row['french'].lower(): row['creole'] 
        for _, row in df.iterrows()
        if row['french'].split().__len__() == 1  # Ne prendre que les mots simples
    }
    
    print(f"Mots simples connus: {len(known_words)}")
    print("\nExemples de mots connus:")
    for i, (french, creole) in enumerate(list(known_words.items())[:5]):
        print(f"{i+1}. {french} -> {creole}")
    
    # 2. Générer les paires basées sur le vocabulaire
    vocabulary_pairs = []
    for _, row in df.iterrows():
        french_words = set(row['french'].split())
        
        for word in french_words:
            word_lower = word.lower()
            if word_lower in known_words:
                creole_word = known_words[word_lower]
                confidence = 0.9
                source = "known"
            else:
                creole_word = transform_french_to_creole(word)
                confidence = 0.7
                source = "generated"
                
            if validate_vocab_transform(word, creole_word):
                vocabulary_pairs.append({
                    'french': word,
                    'creole': creole_word,
                    'type': 'vocabulary',
                    'confidence': confidence,
                    'source': source
                })
    
    augmented_pairs.extend(vocabulary_pairs)
    
    print(f"\nPaires de vocabulaire générées: {len(vocabulary_pairs)}")
    print("Distribution des sources:")
    sources_df = pd.DataFrame(vocabulary_pairs)
    print(sources_df['source'].value_counts())
    
    # Retourner le DataFrame sans la colonne temporaire 'source'
    result_df = pd.DataFrame(augmented_pairs)
    if 'source' in result_df.columns:
        result_df = result_df.drop('source', axis=1)
    
    return result_df

def split_data(df, test_size=0.1, val_size=0.1):
    """Divise les données en train/val/test en préservant la distribution des types"""
    
    # Séparation des données originales et augmentées
    original_data = df[df['type'] == 'original']
    augmented_data = df[df['type'] != 'original']
    
    # Division des données originales
    train_orig, test_orig = train_test_split(original_data, test_size=test_size, random_state=42)
    train_orig, val_orig = train_test_split(train_orig, test_size=val_size/(1-test_size), random_state=42)
    
    # Division des données augmentées
    if len(augmented_data) > 0:
        train_aug, test_aug = train_test_split(augmented_data, test_size=test_size, random_state=42)
        train_aug, val_aug = train_test_split(train_aug, test_size=val_size/(1-test_size), random_state=42)
        
        # Concaténation des données
        train_df = pd.concat([train_orig, train_aug])
        val_df = pd.concat([val_orig, val_aug])
        test_df = pd.concat([test_orig, test_aug])
    else:
        train_df = train_orig
        val_df = val_orig
        test_df = test_orig
    
    print("\nDistribution des types:")
    for name, df in [("Train", train_df), ("Validation", val_df), ("Test", test_df)]:
        print(f"\n{name} set:")
        print(df['type'].value_counts())
    
    return train_df, val_df, test_df
def classify_transformation(row):
    """
    Classifie le type de transformation appliquée.
    """
    french = row['french'].lower()
    creole = row['creole'].lower()
    
    if french == creole:
        return 'identical'
    elif french in SPECIAL_WORDS and SPECIAL_WORDS[french] == creole:
        return 'special_word'
    elif len(french) > len(creole):
        return 'reduction'
    elif len(french) < len(creole):
        return 'expansion'
    else:
        return 'mutation'

def determine_priority(row):
    """
    Détermine la catégorie de priorité du mot.
    """
    french = row['french'].lower()
    
    priority_categories = {
        'emergency': {'urgence', 'aide', 'secours', 'médical', 'blessé', 'danger'},
        'location': {'nord', 'sud', 'est', 'ouest', 'route', 'ville', 'chemin'},
        'common_verbs': {'être', 'avoir', 'aller', 'faire', 'dire', 'voir', 'venir'},
        'time': {'jour', 'heure', 'mois', 'année', 'matin', 'soir'},
        'basic': {'eau', 'nourriture', 'maison', 'famille', 'travail'}
    }
    
    for category, words in priority_categories.items():
        if french in words:
            return category
    
    return 'standard'

def validate_translation(row):
    """
    Valide la traduction et retourne un score.
    """
    french = row['french'].lower()
    creole = row['creole'].lower()
    
    score = 1.0
    
    if french in SPECIAL_WORDS:
        return 1.0 if SPECIAL_WORDS[french] == creole else 0.5
    
    if len(creole) < len(french) * 0.5 or len(creole) > len(french) * 1.5:
        score *= 0.8
    
    if not any(re.search(pattern, french) for pattern, _ in TRANSFORMATION_RULES):
        score *= 0.9
    
    return round(score, 2)

def analyze_single_word_vocabulary():
    """
    Analyse le vocabulaire de mots simples et crée des fichiers CSV et Excel enrichis.
    """
    print("\nDébut de l'analyse du vocabulaire...")
    
    try:
        # Charger le fichier train.csv
        df = pd.read_csv("data/training/train.csv")
        print(f"Fichier train.csv chargé : {len(df)} entrées")
        
        # Filtrer pour le type 'vocabulary' et un seul mot
        vocab_df = df[df['type'] == 'vocabulary']
        single_word_df = vocab_df[vocab_df['french'].str.split().str.len() == 1]
        print(f"Mots simples filtrés : {len(single_word_df)} entrées")
        
        # Enrichir avec des catégories et analyses
        analysis = pd.DataFrame({
            'french': single_word_df['french'],
            'creole': single_word_df['creole'],
            'confidence': single_word_df['confidence'],
            'length_diff': single_word_df.apply(lambda x: len(x['creole']) - len(x['french']), axis=1),
            'transformation_type': single_word_df.apply(classify_transformation, axis=1),
            'priority_category': single_word_df.apply(determine_priority, axis=1),
            'validation_score': single_word_df.apply(validate_translation, axis=1)
        })
        
        # Statistiques par catégorie
        category_stats = analysis.groupby('priority_category').agg({
            'french': 'count',
            'confidence': 'mean',
            'validation_score': 'mean'
        }).reset_index()
        
        # Créer les dossiers de sortie
        output_dir = Path("data/analysis")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder les fichiers
        files_to_save = {
            'single_word_translations.xlsx': analysis,
            'single_word_translations.csv': analysis,
            'category_statistics.xlsx': category_stats,
            'validation_results.csv': analysis[['french', 'creole', 'validation_score']]
        }
        
        for filename, data in files_to_save.items():
            filepath = output_dir / filename
            if filename.endswith('.xlsx'):
                data.to_excel(filepath, index=False)
            else:
                data.to_csv(filepath, index=False)
            print(f"Fichier sauvegardé : {filepath}")
        
        # Afficher un résumé
        print(f"\nAnalyse du vocabulaire complétée:")
        print(f"Nombre total d'entrées: {len(analysis)}")
        print("\nDistribution par catégorie:")
        print(category_stats)
        
        return analysis
        
    except Exception as e:
        print(f"Erreur lors de l'analyse du vocabulaire : {str(e)}")
        return None

def main():
    # Charge et augmente les données
    pairs_df = load_base_pairs()
    augmented_df = augment_data(pairs_df)
    
    # Divise les données
    train_df, val_df, test_df = split_data(augmented_df)
    
    # Crée le dossier de sortie
    output_dir = Path("data/training")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarde les ensembles
    train_df.to_csv(output_dir / "train.csv", index=False)
    val_df.to_csv(output_dir / "val.csv", index=False)
    test_df.to_csv(output_dir / "test.csv", index=False)
    
    print(f"Ensembles sauvegardés dans {output_dir}")
    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # Analyse du vocabulaire à un mot
    print("\nDébut de l'analyse du vocabulaire ...:")
    analyze_single_word_vocabulary()
    
if __name__ == "__main__":
    main()
