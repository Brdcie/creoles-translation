"""
test_french_to_creole.py
--------------------------------
Tests structurés par règles pour la traduction français-créole guadeloupéen.
Règles 1-26 + règles spéciales (articles agglutinés)

Pour exécuter les tests :
pytest test_french_to_creole.py -v            # Tous les tests
pytest test_french_to_creole.py -k "rule_00"  # Tests préliminaires
pytest test_french_to_creole.py -k "rule_02"  # Test règle spécifique
"""

import pytest
from src.french_to_creole import french_to_creole, remove_silent_letters

# SECTION 0: Tests préliminaires
#------------------------------------------------------------

def test_rule_00_remove_silent_letters():
    """
    Test de la première étape: suppression des lettres muettes.
    Vérifie :
    - Les suppressions simples (s, p, x final)
    - Les cas après 'e' (ez, et)
    - Les exceptions (après d, c, j, g)
    """
    test_cases = [
        # Suppressions simples
        ("temps", "tem"),          # 's' final
        ("trop", "tro"),          # 'p' final
        ("voix", "voi"),          # 'x' final
        ("grand", "gran"),         # 'd' final
        ("franc", "fran"),         # 'c' final
        
        # Cas après 'e'
        ("nez", "né"),           # transfo 'z' après 'e'
        ("parlez", "parlé"),     # conservation 'z' après 'e'
        ("mangez", "mangé"),     # conservation 'z' après 'e'
        ("galet", "galet"),        # conservation du 't' après 'e'
        
        # Exceptions
        ("garde", "garde"),       # conservation 'e' après 'd'
        ("place", "place"),       # conservation 'e' après 'c'
        ("plage", "plage"),       # conservation 'e' après 'g'
        ("chat", "chat"),       # conservation 't' après 'a'
        
        # Combinaisons multiples
        ("livres intéressants", "liv intéressan"),  # plusieurs lettres muettes
        ("grands champs verts", "gran cham vè"),     # plusieurs mots
        #autres
        ("salaire","salè")
    ]
    for input_phrase, expected in test_cases:
        result = remove_silent_letters(input_phrase)
        assert result == expected, f"Pour '{input_phrase}', attendu '{expected}' mais obtenu '{result}'"

def test_rule_00_agglutinated_words():
    """
    Test la transformation des mots agglutinés en créole guadeloupéen.
    Cette règle vérifie la bonne conversion des expressions avec articles agglutinés
    comme "l'église" -> "légliz" ou "du vin" -> "diven".
    """
    test_cases = [
        # Tests avec l'article "l'"
        ("l'église", "légliz"),
        ("l'orage", "lòraj"),
        ("l'eau", "dlo"),
        ("l'argent", "lajan"),
        ("l'heure", "lè"),
        
        # Tests avec "du/de l'"
        ("du vin", "diven"),
        ("de l'essence", "lésans"),
        
        # Tests avec "la"
        ("la nuit", "lannuit"),
        ("la mer", "lanmè"),
        
        # Tests de cas composés
        ("au bord de la mer", "bòdlanmè"),
        ("grand bois", "granbwa")
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur d'agglutination : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_02_u_to_i():
    """
    Test la règle 2 : transformation du 'u' en 'i'
    Cette règle transforme la lettre 'u' en 'i', 
    avec des exceptions pour 'qui', 'que', 'quand', 'quoi'
    et traite correctement la position de l'article défini.
    """
    test_cases = [
        # Cas standards
        ("une", "on"),       # Exception : article indéfini
        ("un", "on"),        # Exception : article indéfini
        ("lune", "lin"),
        ("plume", "plim"),
        
        # Exceptions
        ("qui", "ki"),       # Exception gérée par SPECIAL_WORDS
        ("que", "ke"),       # Exception gérée par SPECIAL_WORDS
        ("quoi", "kwa"),     # Exception gérée par SPECIAL_WORDS
    
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de transformation u→i : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_03_s_sound() :
    """ # Règle 3 : graphies du son [s] en créole guadeloupéen
         (r'tion', 'syon'),          # Remplacer 'tion' par 'syon' en premier car plus spécifique
         (r'ss', 's'),               # Remplacer 'ss' par 's'
         (r'ce\b', 's'),             # Remplacer 'ce' en fin de mot par 's'
         (r'ç', 's'),                # Remplacer 'ç' par 's'
         (r'sc(?=[ei])', 's'),       # Remplacer 'sc' par 's' s'il est suivi de 'e' ou 'i'
         (r'c(?=[eiy])(?!h)', 's'),  # Remplacer 'c' par 's' s'il est suivi de 'e', 'i', 'y' et pas de 'h'
    """
    test_cases = [
        # Cas standards
        ("opération", "opérasyon"), 
        ("chasse", "chas"),
        ("place", "plas"),
        ("science", "sians"),
        ("maçon", "mason"),
    
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de transformation son S : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_04_eu_sound():
    """
    # Règle 4 : Mutation du son [Ø]'e' ou 'eu' en 'é'
    Cas testés :
    - (r'\beu\b', ''),     # Remplacer 'eu' seul par rien
    - (r'\be\b', 'é'),     # Remplacer 'e' seul par 'é'  
    """
    test_cases = [
        # Cas standards
        ("peu", "pé"),           # 'eu' en syllabe finale
        ("feu", "fé"),           # 'eu' en syllabe finale
        ("deux", "dé"),          # 'eux' en finale
        ("creux", "kré"),        # 'eux' après consonne multiple
        ("mieux", "mié"),        # 'ieux' en finale
        
        # Cas spéciaux
        ("heureux", "éré"),      # 'eu' en milieu de mot
        ("bleu", "blé"),         # 'eu' après groupe consonantique
    ]
    
    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de transformation son EU : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_05_k_sound():
    r"""
    # Règle 5 : Transformer toutes les graphies du son [k] en 'k'
    Cas testés :
    ...
    - (r'c(?=[^aeiou\s])(?!h)', 'k')  # c + consonne -> k (sauf si suivi de h)
    ...
    """
    test_cases = [
        # Cas standards
        ("quoi", "kwa"),           # Cas spécial
        ("quatre", "kat"),         # qu -> k
        ("sac", "sak"),           # c final -> k
        ("casse", "kas"),         # c + a -> k
        ("couleur", "koulè"),     # c + ou -> k
        ("croire", "kwè"),        # cas spécial
        ("quatorze", "katòz"),
        ("quarante", "karant"),
        ("faire","fè"),
    
        # Cas complexes
        ("acoustique", "akoustik"), # Multiple transformations
        ("public", "piblik"),      # Multiple transformations
        ("bloquer", "bloké"),      # qu + er final
        
        # Exceptions
        ("chocolat", "chokola"),   # ch n'est pas affecté
    ]
    
    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de transformation son K : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_06_e_sound_to_e():
    """
    Test de la règle 6 : transformation des graphies du son [e] en 'é'.
    Cas testés :
    - 'er', 'ez', 'et', 'ed' en fin de mot
    - Transformation de 'ei', 'ef', 'eh', 'ée', 'ay', 'ey'
    """
    test_cases = [
        # Cas standards
        ("parler", "palé"),        # 'er' en fin de mot
        ("chantez", "chanté"),      # 'ez' en fin de mot
        ("jouet", "joué"),          # 'et' en fin de mot
        ("crédit", "krédi"),            # 'ed' en fin de mot
        ("plein", "plen"),          # 'ei' transformé
        ("chef", "chef"),            # 'ef' en fin de mot
        ("meh", "mé"),              # 'eh' transformé
        ("allée", "alé"),          # 'ée' transformé
        ("balai", "balé"),          # 'ay' transformé
        ("seigneur", "ségnè"),        # 'ey' transformé
        ("nez", "né"),              # 'e' transformé en 'é' (règle appliquée normalement)
        ("balayage","balayaj"),
        ("ballet", "balé"),          # 'ay' transformé

        # Cas complexes
        ("chercher", "chèché"),  # Multiple transformations
        ("beignet", "bégné"),         # 'ei' et 'et'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de transformation son E : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_simplify_ll_after_a():
    """
    Test la simplification de 'll' en 'l' après 'a'.
    """
    test_cases = [
        ("allet", "alé"),  # 'll' → 'l' après 'a'
        ("ballon", "balon"),  # 'll' → 'l' après 'a'
        ("salle", "sal"),  # 'll' → 'l' après 'a'
    ]
    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur de simplification : pour '{french}'\n"
            f"→ Attendu : '{expected_creole}'\n"
            f"→ Obtenu : '{result}'"
        )
def test_rule_07_nasal_vowel_to_an():
    """
    Test de la Règle 7 : transformer 'am', 'en', 'em' en 'an'.
    """
    test_cases = [
        # Cas standards
        ("ample", "anpl"),          # 'am' → 'an'
        ("enfant", "anfan"),        # 'en' → 'an'
        ("ensemble", "ansanbl"),    # 'en' et 'em' → 'an'
        ("temps", "tan"),           # 'em' → 'an'
        ("rentrée", "rantré"),      # 'en' → 'an'
        ("document", "dokiman")
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_09_soft_g_to_j():
    """
    Test de la Règle 9 : transformer 'g' suivi de 'e', 'i', ou 'y' en 'j'.
    """
    test_cases = [
        ("manger", "manjé"),        # 'ger' → 'jé'
        ("gérant", "jéran"),        # 'g' → 'j'
        ("page", "paj"),            # 'ge' → 'j'
        ("genou", "jounou"),        # 'ge' → 'j'
        ("gilet", "jilé"),          # 'gi' → 'ji'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_10_nasal_vowel_to_en():
    """
    Test de la Règle 10 : transformer 'aim', 'ain', 'im', 'ein', etc., en 'en'.
    """
    test_cases = [
        ("important", "enpòtan"),  # 'im' → 'en'
        ("pain", "pen"),           # 'ain' → 'en'
        ("faim", "fen"),           # 'aim' → 'en'
        ("plein", "plen"),         # 'ein' → 'en'
        ("syndicat", "sendika"),    # 'yn' → 'en'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_18_oeur_to_er():
    """
    Test de la Règle 18 : transformer les graphies du son [œr].
    """
    test_cases = [
        ("heureux", "éré"),         # Cas spécifique
        ("fleur", "flè"),           # 'œur' → 'è'
        ("chœur", "kè"),           # 'œur' → 'è'
        ("bonheur", "bonè"),       # 'eur' → 'è' en fin de mot
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_21_mm_to_nm():
    """
    Test de la Règle 21 : transformer 'mm' en 'nm' entre deux voyelles.
    """
    test_cases = [
        ("comme", "kon"),         # 'mm' → 'nm'
        ("flamme", "flanm"),       # 'mm' → 'nm'
        ("commencer", "konmansé"), # 'mm' → 'nm' dans un mot plus long
        ("femme", "fanm"),     # 'mm' → 'nm'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )

def test_rule_01_remove_final_e():
    """
    Test de la Règle 1 : supprimer le 'e' final.
    """
    test_cases = [
        ("table", "tabl"),         # 'e' final supprimé
        ("chose", "choz"),         # 'e' final supprimé
        ("femme", "fanm"),         # 'e' final supprimé après application d'autres règles
        ("grande", "gran"),        # 'e' final supprimé après 'd'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_13_f_sound():
    """
    Test de la Règle 13 : transformer les graphies du son [f].
    """
    test_cases = [
        ("photo", "foto"),         # 'ph' → 'f'
        ("effet", "éfé"),          # 'ff' → 'f'
        ("téléphone", "téléfon"),  # 'ph' → 'f'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )
def test_rule_14_wa_sound():
    """
    Test de la Règle 14 : transformer les graphies du son [wa].
    """
    test_cases = [
        ("poisson", "pwason"), # 'oi' → 'wa'
        ("bois", "bwa"),        # 'oi' → 'wa'
        ("Guadeloupe", "Gwadloup"), #ua, wa
        ("gouache", "gwach"), #oua, wa

    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )

def test_rule_15_r_disappearance():
    """
    Test de la Règle 15 : disparition ou transformation de 'r' en fin de syllabe.
    """
    test_cases = [
        ("sortir", "sòti"),    # 'or' → 'ò' ir' → 'i'
        ("fermé", "fèmé"),    # 'er' → 'è'
        ("tour", "tou"),      # 'our' → 'ou'
        ("dur", "di"),        # 'ur' → 'i'
        ("Bernard", "Bèna"),  # 'ar' → 'a'
    ]

    for french, expected_creole in test_cases:
        result = french_to_creole(french)
        assert result == expected_creole, (
            f"Erreur pour '{french}': attendu '{expected_creole}', obtenu '{result}'"
        )


        