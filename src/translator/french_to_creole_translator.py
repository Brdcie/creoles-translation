import re
from src.special_words import SPECIAL_WORDS
from src.constants import PRONOUN_MAPPING, TENSE_PATTERNS, CREOLE_MARKERS, ARTICLE_PATTERNS, TRANSFORMATION_RULES
import logging

class FrenchToCreoleTranslator:
    def __init__(self, phrase: str):
        self.phrase = phrase.lower()
    
    def detect_tense(self, verb: str) -> str:
        verb = verb.lower().strip()
        for tense, pattern in TENSE_PATTERNS.items():
            if re.match(pattern, verb):
                return CREOLE_MARKERS[tense]
        return ''

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
        
        self.handle_articles()
        words = self.phrase.split()
        
        i = 0
        while i < len(words) - 1:
            current_word, next_word = words[i].lower(), words[i + 1].lower()
            if current_word in PRONOUN_MAPPING:
                tense_marker = self.detect_tense(next_word)
                creole_pronoun = PRONOUN_MAPPING[current_word]
                words[i:i + 2] = [f"{creole_pronoun} {tense_marker} {next_word}" if tense_marker else f"{creole_pronoun} {next_word}"]
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