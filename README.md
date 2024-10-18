guadeloupean-creole-translation/
│
├── data/
│   ├── raw/                      # Contient les données brutes (fichiers originaux)
│   │   └── Liste_Rebalanced_French.tsv
│   ├── processed/                # Contient les données prétraitées
│   │   └── cleaned_french_sentences.csv
│   └── augmentation/             # Contient les données augmentées (utilisées pour l'entraînement)
│       └── augmented_creole_pairs.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb # Notebook pour l'exploration et la visualisation des données
│   ├── 02_data_preprocessing.ipynb # Notebook pour le prétraitement des données
│   └── 03_model_training.ipynb   # Notebook pour l'entraînement du modèle
│
├── scripts/
│   ├── preprocess_data.py        # Script pour normaliser et prétraiter les données (comme celui que vous avez fourni)
│   ├── data_augmentation.py      # Script pour générer des données augmentées
│   └── train_model.py            # Script pour entraîner le modèle de traduction
│
├── models/
│   └── mbart_fine_tuned/         # Modèles entraînés, checkpoints
│
├── src/
│   ├── translation_tool.py       # Code source principal pour implémenter l'outil de traduction
│   └── utils.py                  # Utilitaires divers (fonction de normalisation, etc.)
│
├── web_app/
│   ├── app.py                    # Application Web (par exemple, Flask) pour proposer la traduction en ligne
│   └── templates/                # Templates HTML pour l'interface utilisateur
│       └── index.html
│
├── requirements.txt              # Liste des dépendances nécessaires au projet
├── README.md                     # Description du projet, comment l'utiliser, comment contribuer
├── LICENSE                       # Licence open source pour le projet
└── .gitignore                    # Fichiers à ignorer par Git (données sensibles, fichiers temporaires, etc.)
