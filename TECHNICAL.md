# Documentation Technique (En Développement)

## Architecture Proposée

### Structure des Répertoires

traduction-creole-guadeloupeen/
├── data/               # Données d'entraînement et analyses
│   ├── raw/           # Données brutes collectées
│   ├── processed/     # Données en cours de nettoyage
│   └── validation/    # Résultats de validation
├── src/               # Code source principal
│   ├── preprocessing/ # [En développement] Nettoyage des données
│   ├── translation/   # [En développement] Moteur de traduction
│   └── validation/    # [En développement] Outils de validation
├── scripts/           # Scripts utilitaires
└── tests/            # Tests unitaires en cours d'implémentation

## État Actuel des Données

### Corpus Initial
- **Total** : 2605 paires de phrases
- **Répartition prévue** :
  - Train : 2084 paires (80%)
  - Validation : 260 paires (10%)
  - Test : 261 paires (10%)

### Format des Données en Développement
#### data/training/
- **train.csv** (Structure prévue)
  - french: Texte en français
  - creole: Traduction en créole
  - type: Type de données
  - confidence: Score de confiance (0-1)

#### data/analysis/
- **single_word_translations.csv** (En cours de validation)
  - french: Mot en français
  - creole: Traduction en créole
  - confidence: Score de confiance
  - transformation_type: Type de transformation
  - priority_category: Catégorie fonctionnelle
  - validation_score: Score de qualité

## Catégories Fonctionnelles (En cours de raffinement)
1. **Emergency**: Vocabulaire médical et d'urgence
2. **Location**: Termes géographiques et directions
3. **Common Verbs**: Verbes d'usage fréquent
4. **Time**: Expressions temporelles
5. **Basic**: Vocabulaire quotidien essentiel

## Système de Validation (À développer)
- Validation basée sur les règles phonologiques
- Analyse des transformations morphologiques
- Vérification des cas spéciaux
- Scores de confiance pour chaque traduction

## Pipeline de Traduction Prévu
1. Prétraitement du texte
2. Application des règles linguistiques
3. Traduction par le modèle
4. Post-traitement et validation
5. Génération du score de confiance

## Prochaines Étapes Techniques
1. Implémentation du moteur de traduction
2. Développement des outils de validation
3. Création de l'API
4. Développement de l'interface utilisateur
5. Mise en place du système de feedback

## Notes pour les Développeurs
- Le projet est en phase active de développement
- Les composants sont susceptibles de changer
- La documentation sera mise à jour régulièrement