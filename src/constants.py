# Mapping unifié des pronoms
PRONOUN_MAPPING = {
    'je': 'an',      # Standardisé sur 'an' plutôt que 'an/mwen'
    'tu': 'ou',
    'il': 'i',
    'elle': 'i',
    'nous': 'nou',
    'vous': 'zòt',
    'ils': 'yo',
    'elles': 'yo'
}

# Pattern pour la détection des pronoms
PRONOUN_PATTERN = r"(je|tu|il|elle|nous|vous|ils|elles)"

# Patterns de temps verbaux
TENSE_PATTERNS = {
    'future': r'^.*(?:rai|ras|ra|rons|rez|ront)$',
    'imperfect': r'^.*(?:ais|ait|ions|iez|aient)$',
    'present': r'^.*(?:e|es|ons|ez|ent)$',
    'past': r'^(?:ai|as|a|avons|avez|ont|suis|es|est|sommes|êtes|sont)\s+.*(?:é|i|u|t)$'
}

CREOLE_MARKERS = {
    'present': {
        'affirmative': 'ka',
        'negative': 'pa ka'
    },
    'future': {
        'affirmative': 'ké',
        'negative': 'pé ké'
    },
    'imperfect': {
        'affirmative': 'té ka',
        'negative': 'pa té ka'
    },
    'past': {
        'affirmative': 'té',
        'negative': 'pa té'
    },
    'conditional': {
        'affirmative': 'té ké',
        'negative': 'pa té ké'
    }
}

# Mots avec fonction grammaticale
GRAMMAR_MARKERS = {
    'ki': 'interrogative',  # marqueur interrogatif
    'pa': 'negation',      # marqueur de négation
    'ni': 'avoir',         # verbe avoir
    'la': 'definite_article'  # article défini (suffixe)
}

# Patterns d'articles
ARTICLE_PATTERNS = {
    'definite_singular': r'(le|la) (\w+)',
    'definite_plural': r'les (\w+)',
    'indefinite': r'(un|une|des) (\w+)'
}
TRANSFORMATION_RULES = [
    # Règle tt
        (r'tt', 't'),              # Remplacer 'tt' par 't'
        # Règle 21 : Transformer le 'mm' en 'nm'
        (r'(?<=[aeiouAEIOU])mm(?=[aeiouAEIOU])', 'nm'),
        (r'(?<=[aoiAOI])m(?=[aoiAOI])', 'nm'),
        
        # Règle 7 : +transformer les graphies de [ã] : an, am, en, em --> an
        # Remarque Sylviane devient Sylviàn, butane devient bitàn et conserve bien la prononciation de la deuxième syllable.
        (r'am', 'an'),              # Remplacer 'am' par 'an'
        (r'one', 'òn'),
        # 'en' → 'an' uniquement au début du mot ou avant une consonne
        (r'\ben|en(?=[bcdfghjklmnpqrstvwxz])|(?<=[mdtr])ent?\b', 'an'),
        #(r'en', 'an'),              # Remplacer 'en' par 'an'
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
        (r'eh', 'é'),                 # Remplacer 'eh' par 'é'
        (r'ée', 'é'),                 # Remplacer 'ée' par 'é'
        (r'ay\b', 'é'),               # Remplacer 'ay' en fin de mot par 'é'
        (r'ey\b', 'é'),               # Remplacer 'ey' en fin de mot par 'é'
        (r'e(?=(\w)\1)', 'é'),        # Remplacer 'e' suivi d'une consonne double par 'é'
        (r'aire\b','è'),              # Remplacer 'aire' en fin de mot par 'è'
        (r'ai\b', 'é'),                 # Remplacer 'ai' en fin de mot par 'é'
        (r'aill\b', 'ay'),                 # Remplacer 'ai' en fin de mot par 'é'

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
        
        # Règle 20 : doublement du n entre deux voyelles si la première voyelle est un a
        (r'an([aeiou])', 'ann\\1'),  # Remplacer 'ana/e/i/o/u' par 'anna/e/i/o/u'
        # Règle 1 : Supprimer le 'e' final (au cas où il n'a pas été supprimé précédemment)
        (r'e$', ''),                  # Supprimer 'e' final
        (r'de', 'd'),                 # remplacer'de' par 'd'
        # Règle 13 : Graphies du son [f]
        (r'ff', 'f'),              # Remplacer 'ff' par 'f'
        (r'ph', 'f'),              # Remplacer 'ph' par 'f'
        
        # Règle 15  Disparition de la consonne 'r' à la fin d'une syllable
        # si le son 'r' est conservé, il s'écrit 'w'
        (r'or', 'ò'),              # Remplacer 'or' par 'ò'
        (r'ar(?=[bcdfghjklmnpqrstvwxyz])', 'a'),
        (r'ir', 'i'),              # Remplacer 'ir par 'i'
        (r'er', 'è'),              # Remplacer 'er' par 'è'
        (r'eu', 'è'),              # Remplacer 'er' par 'è'
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
         (r'ail\b', 'ay'),             # 'papaye' -> 'papay'

        # Règle 26 : 'm(b/br/bl)e' final -> 'nm'
         (r'm(?:b(?:re|le)|be)\b', 'nm'),    # 'mbre/mble/mbe' en fin de mot devient 'nm' 
        # Règle 8 : Transformer les graphies du son [o] en 'o'
        # Remarque : téléphone devient téléfòn et se prononce comme en français; en forme --> anfòm
        (r'eau', 'o'),                # Remplacer 'eau' par 'o'
        (r'au', 'o'),                 # Remplacer 'au' par 'o'
        #(r'phone\b', 'fòn'),  # Règle spécifique pour 'phone'
        # Règle 11 pour 'x' entre voyelles : 'x' -> 'ks'
        # Remarque : +en fait le X peut etre s, ks, gz, z
        (r'(?<=[aeéiouyAEIOUY])x(?=[aeéiouyAEIOUY])', 'ks'),
        # Règle 17 : Mutation du son [ə]
        (r'(?<=[bcdfghjklmnpqrstvwxz])e(?=[bcdghjklpqtvwxz])', 'i'),
        # Règle 19 :
        # R devient w devant o/ò
        (r'r(?=[oò])', 'w'),  # rose → wòz, roche → wòch
        # R devient w dans les groupes consonantiques suivis de o/ò/è
        (r'(?<=[bcdfghjklmnpqstvxz])r(?=[oòè])', 'w'),  # crapaud → krapo, noir → nwè
        # R initial reste r devant é/i 
       (r'\br(?=[éi])', 'r'),  # René → réné, riz → ri
        # R après consonne reste r devant é/i
       (r'(?<=[bcdfghjklmnpqstvxz])r(?=[éi])', 'r'),  # crédit → krédi
]