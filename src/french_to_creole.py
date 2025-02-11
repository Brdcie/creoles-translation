import re
from src.special_words import SPECIAL_WORDS
from src.constants import PRONOUN_MAPPING, TENSE_PATTERNS, CREOLE_MARKERS, ARTICLE_PATTERNS, TRANSFORMATION_RULES

# Étape 2 : Appliquer les règles de transformation du français au créole guadeloupéen

def detect_tense(verb: str) -> str:
   verb = verb.lower().strip()
   for tense, pattern in TENSE_PATTERNS.items():
       if re.match(pattern, verb):
           return CREOLE_MARKERS[tense]
   # Étape 2 : Appliquer les règles de transformation du français au créole guadeloupéen 
   return ''
def handle_articles(phrase: str) -> str:
   if any(word.lower() in SPECIAL_WORDS for word in phrase.split()):
       return phrase
       
   for pattern, replace_pattern in ARTICLE_PATTERNS.items():
       if pattern == 'definite_singular':
           phrase = re.sub(replace_pattern, r'\2-la', phrase)
       elif pattern == 'definite_plural':
           phrase = re.sub(replace_pattern, r'sé \1-la', phrase)
           
   return phrase


# Étape 1 : Supprimer les lettres muettes
def remove_silent_letters(phrase):
    print(f"Avant suppression des lettres muettes : {phrase}")
    words = phrase.split()
    processed_words = []
    for word in words:
        # Vérifier d'abord si le mot est dans SPECIAL_WORDS
        if word.lower() in SPECIAL_WORDS:
            processed_words.append(SPECIAL_WORDS[word.lower()])
            continue  # Passer au mot suivant
        # Si le mot n'est pas spécial, appliquer les règles
        # Dans remove_silent_letters()
        word = re.sub(r'(?<!v)(?<!a)ille\b', 'i', word)  # remplacer 'ille' en fin de mot par 'i' sauf après 'v' et 'a'
        word = re.sub(r'aire\b', 'è', word)  # Remplacer 'aire' en fin de mot par 'è'
        word = re.sub(r'(?<!s)s$', '', word)  # Supprimer 's' final sauf après 's'
        word = re.sub(r'ez\b', 'é', word)  # Remplacer 'ez' en fin de mot par 'é'
        word = re.sub(r'ert\b', 'è', word)  # Remplacer 'ert' en fin de mot par 'è'
        word = re.sub(r'(?<![ea])t$', '', word)  # Supprimer 't' final sauf après 'e'et 'a'
        word = re.sub(r'd$', '', word)  # Supprimer 'd' final
        word = re.sub(r'er\b', 'é', word)  # Remplacer 'er' en fin de mot par 'é'
        word = re.sub(r'([bcdfghjklmnpqrstvwxz])c$', r'\g<1>', word)  # Supprimer 'c' final après consonne    
        word = re.sub(r'p$', '', word)  # Supprimer 'p' final
        word = re.sub(r'le\b', '',word)               # 'le' final disparaît
        word = re.sub(r'n(?:dre|de)\b', 'nn', word)   # règle générale: 'ndre/nde' -> 'nn'
        word = re.sub(r'(?<![dcjgqzns])e$', '', word)  # Supprimer 'e' final sauf après 'd' ou 'c' j g z q ou s
        word = re.sub(r'(?<!e)(?<!eu)r$', '', word)  # Supprimer 'r' final sauf après 'e' et 'eur' 
        word = re.sub(r'x$', '', word)  # Supprimer 'x' final
        word = re.sub(r'(?<!e)z$', '', word)  # Supprimer 'z' final sauf après 'e'
        processed_words.append(word)
    
    phrase = ' '.join(processed_words)
    print(f"Après suppression des lettres muettes : {phrase}")
    return phrase

def apply_transformations(phrase: str) -> str:
   original_case = [c.isupper() for c in phrase]
   phrase = phrase.lower()
   
   for pattern, replacement in TRANSFORMATION_RULES:
       phrase = re.sub(pattern, replacement, phrase, flags=re.IGNORECASE)
       
   result_chars = list(phrase)
   for i, upper in enumerate(original_case):
       if i < len(result_chars):
           result_chars[i] = result_chars[i].upper() if upper else result_chars[i]
           
   return ''.join(result_chars)
def french_to_creole(phrase: str) -> str:
   if phrase.lower() in SPECIAL_WORDS:
       return SPECIAL_WORDS[phrase.lower()]
       
   phrase = handle_articles(phrase)
   words = phrase.split()
   
   i = 0
   while i < len(words)-1:
       current_word = words[i].lower()
       next_word = words[i+1].lower()
       
       if current_word in PRONOUN_MAPPING:
           tense_marker = detect_tense(next_word)
           creole_pronoun = PRONOUN_MAPPING[current_word]
           
           if tense_marker:
               words[i:i+2] = [f"{creole_pronoun} {tense_marker} {next_word}"]
           else:
               words[i:i+2] = [f"{creole_pronoun} {next_word}"]
       i += 1
   
   phrase = ' '.join(words)
   phrase = remove_silent_letters(phrase)
   return apply_transformations(phrase)

def apply_creole_rules(phrase):
    """Applique les règles de transformation du français vers le créole.
    Chaque transformation est tracée pour faciliter le débogage.
    
    Args:
        phrase (str): La phrase à transformer
        
    Returns:
        str: La phrase transformée
    """
    print(f"Phrase initiale pour transformation en créole : {phrase}")
    #Enregistrer la casse originale
    original_case = [c.isupper() for c in phrase]
    
    # Convertir la phrase en minuscules pour le traitement
    phrase = phrase.lower()

    # Définir une liste de tuples (pattern, replacement) ordonnée du plus spécifique au plus général
    # Appliquer les règles de transformation
    for pattern, replacement in TRANSFORMATION_RULES:
     old_phrase = phrase
     phrase = re.sub(pattern, replacement, phrase, flags=re.IGNORECASE)
     result = phrase  # Garder le mot transformé tel quel
     if len(original_case) > 0:  # S'il y avait des majuscules dans le mot d'origine
        # Appliquer la casse d'origine uniquement sur les caractères existants
        result_chars = list(result)
        for i, upper in enumerate(original_case):
            if i < len(result_chars):  # Ne traiter que les caractères existants
                result_chars[i] = result_chars[i].upper() if upper else result_chars[i]
        result = ''.join(result_chars)

    return result

# Fonction principale pour effectuer la transformation complète
def transform_french_to_creole(phrase: str) -> str:
   words = phrase.split()
   transformed_words = []
   
   for word in words:
       if word.lower() in SPECIAL_WORDS:
           transformed_words.append(SPECIAL_WORDS[word.lower()])
       else:
           transformed_words.append(french_to_creole(word))
           
   return ' '.join(transformed_words)
