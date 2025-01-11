# tests/test_prepare_training_data.py

import pytest
from scripts.prepare_training_data import load_base_pairs, augment_data

def test_load_base_pairs():
    df = load_base_pairs()
    assert len(df) > 0
    assert 'french' in df.columns
    assert 'creole' in df.columns

def test_augment_data():
    sample_df = pd.DataFrame({
        'french': ['Je mange du pain'],
        'creole': ['An ka manjé pen']
    })
    augmented = augment_data(sample_df)
    assert len(augmented) >= len(sample_df)
    assert 'type' in augmented.columns