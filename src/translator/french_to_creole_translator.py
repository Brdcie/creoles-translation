import re
from src.special_words import SPECIAL_WORDS
from src.constants import PRONOUN_MAPPING, TENSE_PATTERNS, CREOLE_MARKERS, ARTICLE_PATTERNS, TRANSFORMATION_RULES,FIRST_GROUP_EXCEPTIONS,FIRST_GROUP_VERB_PATTERNS,IRREGULAR_VERBS, IRREGULAR_VERB_ROOTS
import logging

class FrenchToCreoleTranslator:
    def __init__(self, phrase: str):
        self.phrase = phrase.lower()
    def detect_tense_irregular(self, verb: str) -> str:
        """Détecte le temps pour les verbes irréguliers."""
        
        # Présent
        if verb in ['fais', 'fait', 'faisons', 'faites', 'font', 'suis', 'es', 'est', 'sommes', 'êtes', 'sont']:
            return 'present'
        
        # Imparfait  
        if verb in ['faisais', 'faisait', 'faisions', 'faisiez', 'faisaient', 'étais', 'était', 'étions', 'étiez', 'étaient']:
            return 'imperfect'
        
        # Futur
        if verb in ['ferai', 'feras', 'fera', 'ferons', 'ferez', 'feront']:
            return 'future'
        
        return None
    def detect_tense(self, verb: str, is_negative: bool = False) -> str:
        verb = verb.lower().strip()
        # 1. Vérifier les verbes irréguliers d'abord
        irregular_tense = self.detect_tense_irregular(verb)
        if irregular_tense:
            markers = CREOLE_MARKERS[irregular_tense]
            return markers['negative'] if is_negative else markers['affirmative']
    
        # 2. Utiliser les patterns réguliers
        for tense, pattern in TENSE_PATTERNS.items():
            if re.match(pattern, verb):
               markers = CREOLE_MARKERS[tense]
            return markers['negative'] if is_negative else markers['affirmative']
        return ''  
    def transform_first_group_verbs(self, word: str) -> str:
        """Transforme les verbes, irréguliers d'abord, puis premier groupe."""
    
        # 1. Vérifier d'abord les verbes irréguliers
        if word in IRREGULAR_VERBS:
            return IRREGULAR_VERBS[word]
    
        # 2. Vérifier si c'est un verbe irrégulier (éviter transformation)
        for root in IRREGULAR_VERB_ROOTS:
             if word.startswith(root[:3]):  # Heuristique simple
                 return word  # Ne pas transformer
    
        # 3. Appliquer les patterns du premier groupe
        for pattern, replacement in FIRST_GROUP_VERB_PATTERNS.items():
            if re.match(pattern, word):
               return re.sub(pattern, replacement, word)
    
        return word
    def is_negative_sentence(self) -> bool:
        """Détecte si la phrase est négative."""
        negative_words = ['ne', 'pas', 'plus', 'jamais', 'rien', 'personne']
        return any(word in self.phrase.split() for word in negative_words)

    def handle_articles(self) -> None:
        if any(word.lower() in SPECIAL_WORDS for word in self.phrase.split()):
            return
        
        for pattern, replace_pattern in ARTICLE_PATTERNS.items():
            if pattern == 'definite_singular':
                self.phrase = re.sub(replace_pattern, r'\2-la', self.phrase)
            elif pattern == 'definite_plural':
                self.phrase = re.sub(replace_pattern, r'sé \1-la', self.phrase)

    def remove_silent_letters(self) -> None:
        logging.debug(f"Avant suppression des lettres muettes : {self.phrase}")
        words = self.phrase.split()
        processed_words = []
        
        for word in words:
            if word.lower() in SPECIAL_WORDS:
                processed_words.append(SPECIAL_WORDS[word.lower()])
                continue
            
            transformations = [
                (r'(?<!v)(?<!a)ille\b', 'i'),
                (r'aire\b', 'è'),
                (r'(?<!s)s$', ''),
                (r'ez\b', 'é'),
                (r'ert\b', 'è'),
                (r'(?<![ea])t$', ''),
                (r'd$', ''),
                (r'er\b', 'é'),
                (r'([bcdfghjklmnpqrstvwxz])c$', r'\1'),
                (r'p$', ''),
                (r'le\b', ''),
                (r'n(?:dre|de)\b', 'nn'),
                (r'(?<![dcjgqzns])e$', ''),
                (r'(?<!e)(?<!eu)r$', ''),
                (r'x$', ''),
                (r'(?<!e)z$', '')
            ]
            
            for pattern, replacement in transformations:
                word = re.sub(pattern, replacement, word)
            processed_words.append(word)
            
        self.phrase = ' '.join(processed_words)
        logging.debug(f"Après suppression des lettres muettes : {self.phrase}")

    def apply_transformations(self) -> None:
        logging.debug(f"Phrase initiale pour transformation en créole : {self.phrase}")
        original_case = [c.isupper() for c in self.phrase]
        self.phrase = self.phrase.lower()
        
        for pattern, replacement in TRANSFORMATION_RULES:
            self.phrase = re.sub(pattern, replacement, self.phrase, flags=re.IGNORECASE)
        
        result_chars = list(self.phrase)
        for i, upper in enumerate(original_case):
            if i < len(result_chars):
                result_chars[i] = result_chars[i].upper() if upper else result_chars[i]
        
        self.phrase = ''.join(result_chars)
    
    def transform(self) -> str:
        if self.phrase.lower() in SPECIAL_WORDS:
            return SPECIAL_WORDS[self.phrase.lower()]
        
        is_negative = self.is_negative_sentence()
        
        # IMPORTANT : Supprimer les mots négatifs AVANT de traiter les articles
        if is_negative:
            negative_words = ['ne', 'pas', 'plus', 'jamais', 'rien', 'personne']
            words = self.phrase.split()
            words = [word for word in words if word not in negative_words]
            self.phrase = ' '.join(words)
            
            # Gérer "de" après négation
            self.phrase = re.sub(r'\bde\s+', '', self.phrase)
        
        self.handle_articles()
        words = self.phrase.split()
        
        i = 0
        while i < len(words) - 1:
            current_word, next_word = words[i].lower(), words[i + 1].lower()
            if current_word in PRONOUN_MAPPING:
                # Transformer le verbe du premier groupe
                transformed_verb = self.transform_first_group_verbs(next_word)
                tense_marker = self.detect_tense(next_word, is_negative)
                creole_pronoun = PRONOUN_MAPPING[current_word]
                
                if tense_marker:
                    words[i:i+2] = [f"{creole_pronoun} {tense_marker} {transformed_verb}"]
                else:
                    words[i:i+2] = [f"{creole_pronoun} {transformed_verb}"]
            i += 1
        
        self.phrase = ' '.join(words)
        self.remove_silent_letters()
        self.apply_transformations()
        return self.phrase
def transform_french_to_creole(phrase: str) -> str:
    if not validate_input(phrase):
        return ValueError("Input must be valid string.")
    translator = FrenchToCreoleTranslator(phrase)
    return translator.transform()

def validate_input(phrase: str) -> bool:
    if not isinstance(phrase, str):
        return False
    if not phrase.split():
        return False
    return True