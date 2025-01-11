import re, random
from src.special_words import SPECIAL_WORDS

def e_sound_variation():
    #Retourne aléatoirement une des trois variations possibles du son [ə]
    return random.choice(['i', 'ou', 'è'])

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
        word = re.sub(r'aire\b', 'è', word)  # Remplacer 'aire' en fin de mot par 'è'
        word = re.sub(r's$', '', word)  # Supprimer 's' final
        word = re.sub(r'ez\b', 'é', word)  # Remplacer 'ez' en fin de mot par 'é'
        word = re.sub(r'ert\b', 'è', word)  # Remplacer 'ert' en fin de mot par 'è'
        word = re.sub(r'(?<![ea])t$', '', word)  # Supprimer 't' final sauf après 'e'et 'a'
        word = re.sub(r'd$', '', word)  # Supprimer 'd' final
        word = re.sub(r'er\b', 'é', word)  # Remplacer 'er' en fin de mot par 'é'
        word = re.sub(r'([bcdfghjklmnpqrstvwxz])c$', r'\g<1>', word)  # Supprimer 'c' final après consonne    
        word = re.sub(r'p$', '', word)  # Supprimer 'p' final
        word = re.sub(r'(?<![dcjgqzns])e$', '', word)  # Supprimer 'e' final sauf après 'd' ou 'c' j g z q
        word = re.sub(r'(?<!e)(?<!eu)r$', '', word)  # Supprimer 'r' final sauf après 'e' et 'eur' 
        word = re.sub(r'x$', '', word)  # Supprimer 'x' final
        word = re.sub(r'(?<!e)z$', '', word)  # Supprimer 'z' final sauf après 'e'
        processed_words.append(word)
    
    phrase = ' '.join(processed_words)
    print(f"Après suppression des lettres muettes : {phrase}")
    return phrase

# Étape 2 : Appliquer les règles de transformation du français au créole guadeloupéen
def french_to_creole(phrase):

    """
    Point d'entrée principal pour la traduction français -> créole
    """
    # Vérifier d'abord dans SPECIAL_WORDS
    if phrase.lower() in SPECIAL_WORDS:
        return SPECIAL_WORDS[phrase.lower()]
    # Si pas dans SPECIAL_WORDS, appliquer les règles de transformation
    phrase = remove_silent_letters(phrase)
    return apply_creole_rules(phrase)

def apply_creole_rules(phrase):
    print(f"Phrase initiale pour transformation en créole : {phrase}")
    #Enregistrer la casse originale
    original_case = [c.isupper() for c in phrase]
    
    # Convertir la phrase en minuscules pour le traitement
    phrase = phrase.lower()

    # Définir une liste de tuples (pattern, replacement) ordonnée du plus spécifique au plus général
    transformation_rules = [
        # Règle 7 : +transformer les graphies de [ã] : an, am, en, em --> an
        # Remarque Sylviane devient Sylviàn, butane devient bitàn et conserve bien la prononciation de la deuxième syllable.
        (r'am', 'an'),              # Remplacer 'am' par 'an'
        (r'en', 'an'),              # Remplacer 'en' par 'an'
        (r'em', 'an'),              # Remplacer 'em' par 'an'
        # Règle 9 : Transformer le son [ʒ] en 'j'
        (r'g(?=[eiéy])', 'j'),        # Remplacer 'g' par 'j' s'il est suivi de 'e', 'i', 'y','é'
        (r'ge', 'j'),                # Remplacer 'ge' par j
        (r'je', 'j'),                # Remplacer 'je' par j
        (r'j', 'j'),                  # Remplacer 'j' par 'j' (consistance)
        # Règle 10 : Transformer les graphies du son [ɛ̃] en 'en'
        (r'eune\b', 'en'),           # Remplacer 'eune' par 'en' (prioritaire)
        (r'eim', 'en'),              # Remplacer 'eim' par 'en'
        (r'yn', 'en'),               # Remplacer 'yn' par 'en'
        (r'ein', 'en'),              # Remplacer 'ein' par 'en'
        (r'aim', 'en'),              # Remplacer 'aim' par 'en'
        (r'ain', 'en'),              # Remplacer 'ain' par 'en'
        (r'im', 'en'),               # Remplacer 'im' par 'en'
         # Règle 6 : Transformer les graphies du son [e] en 'é'
        (r'ez\b', 'é'),               # Remplacer 'ez' en fin de mot par 'é'
        (r'et\b', 'é'),               # Remplacer 'et' en fin de mot par 'é'
        (r'ed\b', 'é'),               # Remplacer 'ed' en fin de mot par 'é'
        (r'ei', 'é'),                 # Remplacer 'ei' par 'é'
        #(r'ef\b', 'é'),               # Remplacer 'ef' en fin de mot par 'é'
        (r'eh', 'é'),                 # Remplacer 'eh' par 'é'
       # (r'hé', 'é'),                 # Remplacer 'hé' par 'é'
        (r'ée', 'é'),                 # Remplacer 'ée' par 'é'
        (r'ay\b', 'é'),               # Remplacer 'ay' en fin de mot par 'é'
        (r'ey\b', 'é'),               # Remplacer 'ey' en fin de mot par 'é'
        (r'e(?=(\w)\1)', 'é'),        # Remplacer 'e' suivi d'une consonne double par 'é'
        (r'aire\b','è'),              # Remplacer 'aire' en fin de mot par 'è'
        (r'ai', 'é'),                 # Remplacer 'ai' en fin de mot par 'é'
         # Règle 3 : graphies du son [s] en créole guadeloupéen
         (r'tion', 'syon'),          # Remplacer 'tion' par 'syon' en premier car plus spécifique
         (r'(?<=[aeéiouAEIOU])s(?=[aeéiouAEIOU])', 'z'),
         (r'ss', 's'),               # Remplacer 'ss' par 's'
         (r'ce\b', 's'),             # Remplacer 'ce' en fin de mot par 's'
         (r'ç', 's'),                # Remplacer 'ç' par 's'
         (r'sc(?=[ei])', 's'),       # Remplacer 'sc' par 's' s'il est suivi de 'e' ou 'i'
         (r'c(?=[eéiy])(?!h)', 's'),  # Remplacer 'c' par 's' s'il est suivi de 'e', 'i', 'y' et pas de 'h'
        # Règle 5 : Transformer toutes les graphies du son [k] en 'k'
        (r'ck', 'k'),                # Remplacer 'ck' par 'k'
        (r'qu', 'k'),                # Remplacer 'qu' par 'k'
        (r'q', 'k'),                 # Remplacer 'q' par 'k'
        (r'c$', 'k'),                # Remplacer 'c' par 'k'
        (r'ch(?=œ)', 'k'),           # Remplacer 'ch' par 'k' devant œ
        (r'c(?=[aou])(?!h)', 'k'),    # Remplacer 'c' par 'k' suivi de 'a', 'o', 'u' et pas de 'h'
        (r'c(?=[^aeiou\s])(?!h)', 'k'),   # Remplacer 'c' par 'k' suivi d'une consonne et pas de 'h'
        # Règle 18 mutation du son [œr]
         (r'heureu', 'éré'),        # Cas spécifique pour 'heureux'
         (r'eurre\b', 'è'),          # Remplacer 'eurre' en fin de mot par 'è'
         (r'œu\b', 'è'),           # Remplacer 'œur' en fin de mot par 'è'
         (r'eur(?=[a-zà-ü])', 'ér'), # 'eur' en milieu de mot → 'ér'
         (r'heur', 'è'),        # 'heur' → 'è'
         (r'eur\b', 'è'),        # 'eur' en fin de mot → 'è'
      # Règle 14 Graphies du son [wa] : oi oua ua wa 
        (r'oi', 'wa'),              # Remplacer 'oi' par 'wa'
        (r'oua', 'wa'),              # Remplacer 'oua' par 'wa'
        (r'bua', 'wa'),              # Remplacer 'oua' par 'wa'
        (r'ua', 'wa'),              # Remplacer 'ua' par 'wa'

        # Règle 2 : Mutation de la lettre 'u' en 'i', 
        (r'(?<![aoeœ])u', 'i'),   # Remplacer 'u' par 'i' sauf après 'a' et 'o' 'e' et 'œ'
        # Règle 3 : graphies du son [s] en créole guadeloupéen
         (r'tion', 'syon'),          # Remplacer 'tion' par 'syon' en premier car plus spécifique
         (r'ss', 's'),               # Remplacer 'ss' par 's'
         (r'ce\b', 's'),             # Remplacer 'ce' en fin de mot par 's'
         (r'ç', 's'),                # Remplacer 'ç' par 's'
         (r'sc(?=[ei])', 's'),       # Remplacer 'sc' par 's' s'il est suivi de 'e' ou 'i'
         (r'c(?=[eéiy])(?!h)', 's'),  # Remplacer 'c' par 's' s'il est suivi de 'e', 'i', 'y' et pas de 'h'

        # Règle 4 : Mutation du son [Ø]'e' ou 'eu' en 'é'
        (r'eu\b', 'é'),            # Remplacer 'eu' par 'é'
        (r'\be\b', 'é'),             # Remplacer 'e' par 'é'
        # Règle 21 : Transformer le 'mm' en 'nm'
        (r'(?<=[aeiouAEIOU])mm(?=[aeiouAEIOU])', 'nm'),
        # Règle 20 : doublement du n entre deux voyelles si la première voyelle est un a
        (r'an([aeiou])', 'ann\\1'),  # Remplacer 'ana/e/i/o/u' par 'anna/e/i/o/u'
        # Règle 1 : Supprimer le 'e' final (au cas où il n'a pas été supprimé précédemment)
        (r'e$', ''),                  # Supprimer 'e' final
        (r'de', 'd'),                 # remplacer'de' par 'd'

        # Règle 13 : Graphies du son [f]
        (r'f', 'f'),              # Remplacer 'f' par 'f' (consistance)
        (r'ff', 'f'),              # Remplacer 'ff' par 'f'
        (r'ph', 'f'),              # Remplacer 'ph' par 'f'
        
        # Règle 15  Disparition de la consonne 'r' à la fin d'une syllable
        # si le son 'r' est conservé, il s'écrit 'w'
        (r'or', 'ò'),              # Remplacer 'or' par 'ò'
        (r'ar(?=[bcdfghjklmnpqrstvwxyz])', 'a'),

        (r'ir', 'i'),              # Remplacer 'ir par 'i'
        (r'er', 'è'),              # Remplacer 'er' par 'è'
        (r'our', 'ou'),            # Remplacer 'our' par 'ou'
        (r'ur', 'i'),              # Remplacer 'ur' par 'i'
        # Règle 16  Disparition de 're' à la fin d'une syllable = conservation de re en début de mot
        #quid des mot composés ?
        (r'(?<!^)re', ''),
         # Règle 12 : Transformer les graphies du son [ε] en 'è'
        (r'ê', 'è'),              # Remplacer 'ê' par 'è'
        (r'es\b', 'è'),               # Remplacer 'es' par 'è'
        (r'est\b', 'è'),               # Remplacer 'est' par 'è'
        (r'aî\b', 'è'),               # Remplacer 'aî'  par 'è'
        (r'ei', 'é'),                 # Remplacer 'ei' par 'è'
        (r'ë\b', 'è'),               # Remplacer 'ë' par 'è'
        (r'eh', 'é'),                 # Remplacer 'eh' par 'é'
        (r'ée', 'é'),                 # Remplacer 'ée' par 'é'
        #(r'ay\b', 'é'),               # Remplacer 'ay' en fin de mot par 'é'
        (r'ey\b', 'é'),               # Remplacer 'ey' en fin de mot par 'é'    
        # Règle 22 :
         (r'([^vm])ille\b', '\\1i'),    # 'ille' devient 'i' quand prononcé [ij]
         (r'le\b', ''),                 # 'le' final disparaît
         (r'(?<=a)ll', 'l'),  # Remplacer 'll' par 'l' lorsqu'il est précédé de 'a'
        # Règle 23 : Graphies du son [g] 
        (r'gu(?=[ei])', 'g'),  # 'gu' devant 'e/i' devient 'g' (guitare -> gita)
        (r'g(?=[aouéè])', 'g'),  # maintenir 'g' devant a/o/u (gâteau -> gato)
        (r'c(?=on)', 'g'),     # 'c' suivi de 'on' devient 'g' (seconde -> segond)
        # Règle 24 : Graphies du son [ij]
         (r'ill(?=[aeou])', 'y'),    # 'maillot' -> 'mayo', mais pas 'ville'
         (r'll(?=[aeou])', 'y'),     # 'papillon' -> 'papiyon'
         (r'(?<!s)i(?=[aou])', 'y'),  # 'marier' -> 'mayé' mais N'applique pas la règle si précédé de 's'
         (r'ï', 'y'),                # 'Haïti' -> 'Ayiti'
         (r'ye\b', 'y'),             # 'papaye' -> 'papay'
        # Règle 25 : 'ndre' et 'nde' -> 'nn' avec exceptions
         (r'prendre\b', 'pran'),      # exception: 'prendre' -> 'pran'
         (r'grande?\b', 'gran'),      # exception: 'grand(e)' -> 'gran'
         (r'n(?:dre|de)\b', 'nn'),    # règle générale: 'ndre/nde' -> 'nn'
        # Règle 26 : 'm(b/br/bl)e' final -> 'nm'
         (r'm(?:b(?:re|le)|be)\b', 'nm'),    # 'mbre/mble/mbe' en fin de mot devient 'nm' 
        # Règle 8 : Transformer les graphies du son [o] en 'o'
        # Remarque : téléphone devient téléfòn et se prononce comme en français; en forme --> anfòm
        (r'eau', 'o'),                # Remplacer 'eau' par 'o'
        (r'au', 'o'),                 # Remplacer 'au' par 'o'
        # Règle 11 pour 'x' entre voyelles : 'x' -> 'ks'
        # Remarque : +en fait le X peut etre s, ks, gz, z
        (r'(?<=[aeéiouyAEIOUY])x(?=[aeéiouyAEIOUY])', 'ks'),
     
    ]
    # Appliquer les règles de transformation
    for pattern, replacement in transformation_rules:
     old_phrase = phrase
     phrase = re.sub(pattern, replacement, phrase, flags=re.IGNORECASE)
     if old_phrase != phrase:
        print(f"Après {pattern} → {replacement} : {phrase}")
    result = ''.join(c.upper() if upper else c for c, upper in zip(phrase, original_case))
    print(f"Phrase finale transformée en créole : {phrase}")
    return result

# Fonction principale pour effectuer la transformation complète
def transform_french_to_creole(phrase):
    # Première vérification : phrase complète dans SPECIAL_WORDS
    if phrase.lower() in SPECIAL_WORDS:
        return SPECIAL_WORDS[phrase.lower()]
    
    # Deuxième vérification : expressions avec apostrophe
    for special_word in SPECIAL_WORDS:
        if special_word.lower() in phrase.lower():
            return SPECIAL_WORDS[special_word.lower()]
    
    # Si aucune correspondance trouvée, traiter mot par mot
    words = phrase.split()
    transformed_words = []
    for word in words:
        word_lower = word.lower()
        if word_lower in SPECIAL_WORDS:
            transformed_words.append(SPECIAL_WORDS[word_lower])
        else:
            # Appliquer uniquement french_to_creole qui contient déjà remove_silent_letters
            word = french_to_creole(word)
            transformed_words.append(word)
    
    return ' '.join(transformed_words)
