import pandas as pd

# Vérifier le contenu
df = pd.read_excel('../data/raw/all_book_pairs_modified.xlsx')

# Créer des sections manquantes pour l'urgence
emergency_sections = {
    "medical_emergency": [
        ("J'ai besoin d'un médecin", "An ni bizwen on doktè"),
        ("Appeler une ambulance", "Kriyé on lanbilansi"),
        ("C'est une urgence", "Sa sé on irjans"),
    ],
    "natural_disaster": [
        ("Il y a un cyclone", "Ni on siklòn"),
        ("L'eau monte", "Dlo-la ka monté"),
        ("Il faut évacuer", "Fo-nou évakiyé"),
    ],
    "basic_needs": [
        ("J'ai besoin d'eau", "An ni bizwen dlo"),
        ("Où est l'abri ?", "O labri-la yé ?"),
        ("De la nourriture", "Manjé"),
    ]
}

# Enrichir vos données existantes
enriched_data = {
    "metadata": {
        "original_sources": ["assimil_lessons", "conversation_extracts"],
        "emergency_additions": True
    },
    "pairs": []
}

# Ajouter vos données existantes
for index, row in df.iterrows():
    enriched_data["pairs"].append({
        "id": index + 1,
        "fr": row['french'],
        "gcf": row['creole'],
        "section": row.get('section', 'assimil_lesson'),
        "emergency_context": False
    })

# Ajouter les sections d'urgence manquantes
for section, pairs in emergency_sections.items():
    for fr, gcf in pairs:
        enriched_data["pairs"].append({
            "id": len(enriched_data["pairs"]) + 1,
            "fr": fr,
            "gcf": gcf,
            "section": section,
            "emergency_context": True
        })

# Sauvegarder le JSON amélioré
import json
with open('gcf_fr_translation_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(gcf_fr_translation_dataset.json, f, ensure_ascii=False, indent=2)