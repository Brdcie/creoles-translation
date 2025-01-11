# scripts/prepare_training_data.py

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split  # Ajoutez cet import
from french_to_creole import transform_french_to_creole

def load_base_pairs():
    """Charge les paires français-créole de référence"""
    pairs_path = Path("data/raw/creole_french_pairs_reference.csv")
    return pd.read_csv(pairs_path)

def clean_text(text):
    """Nettoie et normalise le texte"""
    text = text.strip()
    text = ' '.join(text.split())  # Normalise les espaces
    return text

def augment_data(df):
    """Amélioration de la fonction d'augmentation"""
    augmented_pairs = []
    
    for _, row in df.iterrows():
        french = clean_text(row['french'])
        creole = clean_text(row['creole'])
        
        # Paire originale
        augmented_pairs.append({
            'french': french,
            'creole': creole,
            'type': 'original'
        })
        
        # Règles de transformation
        generated_creole = transform_french_to_creole(french)
        if generated_creole != creole:
            augmented_pairs.append({
                'french': french,
                'creole': generated_creole,
                'type': 'generated'
            })

    return pd.DataFrame(augmented_pairs)

def split_data(df, test_size=0.1, val_size=0.1):
    """Divise les données en train/val/test"""
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)
    train_df, val_df = train_test_split(train_df, test_size=val_size/(1-test_size), random_state=42)
    
    return train_df, val_df, test_df

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

if __name__ == "__main__":
    main()