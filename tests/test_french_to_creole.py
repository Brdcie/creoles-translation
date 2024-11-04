"""
test_french_to_creole_complete.py
--------------------------------
Tests complets pour la traduction français-créole guadeloupéen.
Test unitaires organisés par catégories phonétiques et grammaticales.

Pour exécuter un test spécifique:
pytest test_french_to_creole_complete.py -k "nom_du_test"

Exemple:
pytest test_french_to_creole_complete.py -k "test_phonetique"
pytest test_french_to_creole_complete.py -k "test_articles"
"""

import pytest
from french_to_creole import remove_articles, french_to_creole, remove_silent_letters

# SECTION 1: Tests des transformations phonétiques de base
#------------------------------------------------------------

def test_articles_agglutines():
    """
    Test les mots où l'article fait partie intégrante du mot en créole.
    
    Vérifie:
    - Les mots commençant par 'd' (du, de la)
    - Les mots commençant par 'l' (le, la)
    """
    test_cases = [
        ("du vin", "divin"),
        ("de l'eau", "dlo"),
        ("du riz", "diri"),
        ("l'église", "légliz"),
        ("l'école", "lékòl")
    ]
    for input_phrase, expected in test_cases:
        assert french_to_creole(input_phrase) == expected

def test_phonetique_silent_letters():
    """
    Test la suppression des lettres muettes finales.
    """
    test_cases = [
        ("grand chat blanc", "gran cha blan"),
        ("petit chien doux", "peti chien dou"),
        ("livres intéressants", "livr intéressan"),
        ("nez rouge", "ne rouge"),
        ("riz est bon", "ri es bon"),
        ("trop de temps", "tro de tem"),
        ("corps sain", "cor sain"),
        ("je vais chez lui", "je vai che lui")
    ]
    for input_phrase, expected in test_cases:
        assert remove_silent_letters(input_phrase) == expected

# SECTION 2: Tests des transformations consonantiques
#------------------------------------------------------------

def test_consonnes_k_sound():
    """
    Test les transformations du son [k].
    """
    test_cases = [
        ("cactus", "kaktis"),
        ("quoi", "kwa"),
        ("coq", "kok"),
        ("qui", "ki"),
        ("que", "k")
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

def test_consonnes_x_and_s():
    """
    Test la transformation des sons 'x' et 's' entre voyelles.
    """
    assert 'ks' in french_to_creole("taxi")
    assert 'ks' in french_to_creole("examen")
    assert 'z' in french_to_creole("maison")
    assert 'x' in french_to_creole("texte")

def test_consonnes_mm_to_nm():
    """
    Test la transformation de 'mm' en 'nm' entre voyelles.
    """
    test_cases = [
        ("femme", "fenm"),
        ("pomme", "ponm"),
        ("programmation", "progranmation"),
        ("ammir", "anmir"),
        ("mamman", "manman"),
        ("FEMME", "FENM")
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

# SECTION 3: Tests des transformations vocaliques
#------------------------------------------------------------

def test_voyelles_u_to_i():
    """
    Test la transformation du son [u].
    """
    test_cases = [
        ("une pomme", "on pom"),
        ("quand", "kan"),
        ("lune", "lin")
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

@pytest.mark.parametrize("input_word, expected_output", [
    ("plein", "plen"),
    ("faim", "fen"),
    ("synthèse", "sentèz")
])
def test_voyelles_nasales(input_word, expected_output):
    """
    Test la transformation des voyelles nasales.
    """
    assert french_to_creole(input_word) == expected_output

# SECTION 4: Tests des expressions idiomatiques
#------------------------------------------------------------

@pytest.mark.parametrize("french_phrase, expected_creole", [
    ("dépêche-toi", "ba kò a-w bann"),
    ("dépêchons-nous", "annou pòté mannèv"),
    ("il fait beau", "ka fè bèl botan"),
    ("il est furieux", "i bresé"),
    ("il fait nuit", "i ja fè lannuit")
])
def test_expressions_idiomatiques(french_phrase, expected_creole):
    """
    Test les expressions idiomatiques spécifiques.
    """
    assert french_to_creole(french_phrase.lower()) == expected_creole.lower()

# SECTION 5: Tests des structures grammaticales
#------------------------------------------------------------

@pytest.mark.parametrize("french_phrase, expected_creole", [
    ("je parle", "an ka palé"),
    ("ils parlent", "yo ka palé"),
    ("je parlerai", "an ké palé"),
    ("il ne parle pas", "i pa ka palé"),
    ("il ne parlera pas", "i pé ké palé")
])
def test_grammaire_temps_verbaux(french_phrase, expected_creole):
    """
    Test les différents temps verbaux.
    """
    assert french_to_creole(french_phrase.lower()) == expected_creole.lower()

@pytest.mark.parametrize("french_phrase, expected_creole", [
    ("la maison", "kaz-la"),
    ("les maisons", "sé kaz-la"),
    ("ma maison", "kaz an-mwen"),
    ("leurs maisons", "kaz a-yo")
])
def test_grammaire_articles_possessifs(french_phrase, expected_creole):
    """
    Test les articles et les possessifs.
    """
    assert french_to_creole(french_phrase.lower()) == expected_creole.lower()

# SECTION 6: Tests des cas spéciaux
#------------------------------------------------------------

@pytest.mark.parametrize("french_word, expected_variations", [
    ("comme", ["kon", "konm"]),
    ("fenêtre", ["founèt", "finét"]),
    ("lit", ["kabann", "kouch"]),
    ("voiture", ["loto", "vwati"])
])
def test_cas_speciaux_variations(french_word, expected_variations):
    """
    Test les mots ayant plusieurs formes acceptées.
    """
    result = french_to_creole(french_word.lower())
    assert result in expected_variations

if __name__ == "__main__":
    pytest.main(["-v"])
def test_wa_sound_transformation():
    """
    Test les différentes graphies du son [wa].
    
    Vérifie:
    - 'oi' -> 'wa'
    - 'oua' -> 'wa'
    - 'bua' -> 'wa'
    """
    test_cases = [
        ("boire", "bwè"),     # oi -> wa + autre règle
        ("moi", "mwa"),       # oi -> wa simple
        ("ouais", "wè"),      # oua -> wa + autre règle
        ("bouée", "bwé"),     # bua -> wa
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected
def test_e_sound_variations():
    """
    Test la transformation du son [ə] avec ses variations possibles.
    
    Vérifie que:
    - Le 'e' se transforme en 'i', 'ou' ou 'è'
    - La transformation n'a pas lieu en début de mot
    - La transformation n'a pas lieu avant voyelle
    """
    # Collecter plusieurs variations pour un même mot
    variations = set()
    for _ in range(20):
        result = french_to_creole("genou")
        variations.add(result)
    
    # Vérifier que nous avons au moins 2 variations parmi ['jinou', 'jounou', 'jènou']
    expected_variations = {'jinou', 'jounou', 'jènou'}
    assert len(variations.intersection(expected_variations)) >= 2

    # Vérifier que la transformation n'a pas lieu en début de mot
    assert french_to_creole("epicerie") == "épicerie"  # 'e' initial préservé
def test_mm_nm_transformation():
    """
    Test la transformation de 'mm' en 'nm'.
    Vérifie:
    - Transformation entre voyelles
    - Non-transformation dans d'autres contextes
    """
    test_cases = [
        ("femme", "fanm"),       # transformation + nasalisation
        ("pomme", "ponm"),       # transformation simple
        ("sommeil", "sonmèy"),   # transformation + autre règle
        ("immédiat", "inmédya"), # transformation en début de mot
        ("mmm", "mmm")          # pas de transformation sans voyelles
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

def test_r_final_transformation():
    """
    Test la disparition ou transformation du 'r' à la fin d'une syllabe.
    Règle 15 dans french_to_creole.py
    
    Vérifie:
    - 'ar' -> 'a'
    - 'or' -> 'ò'
    - 'ir' -> 'i'
    - 'er' -> 'è'
    - 'our' -> 'ou'
    - 'ur' -> 'i'
    """
    test_cases = [
        ("parler", "palé"),     # er final
        ("partir", "pati"),     # ir final
        ("pour", "pou"),        # our final
        ("dormir", "dòmi"),     # or dans le mot + ir final
        ("sûr", "si"),          # ur final
        ("marché", "maché")     # ar dans le mot
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

def test_k_sound_variations():
    """
    Test les différentes graphies du son [k].
    Règle 5 dans french_to_creole.py
    
    Vérifie:
    - 'qu' -> 'k'
    - 'c + a/o/u' -> 'k'
    - 'ck' -> 'k'
    - 'q' -> 'k'
    """
    test_cases = [
        ("quoi", "kwa"),        # qu spécial
        ("que", "k"),           # qu en fin de mot
        ("coq", "kok"),         # c initial + q final
        ("cactus", "kaktis"),   # c + a
        ("occuper", "okipé"),   # c + u
        ("stock", "stok"),      # ck final
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

def test_nasal_transformations():
    """
    Test les transformations des sons nasaux.
    Règles 7 et 10 dans french_to_creole.py
    
    Vérifie:
    - 'an/am' -> 'an'
    - 'en/em' -> 'an'
    - 'ein/ain/eim' -> 'en'
    - Exceptions et cas spéciaux
    """
    test_cases = [
        ("champ", "chan"),      # am -> an
        ("temps", "tan"),       # em -> an
        ("plein", "plen"),      # ein -> en
        ("pain", "pen"),        # ain -> en
        ("simple", "senp"),     # im -> en
        ("frein", "fren"),      # ein -> en
        ("faim", "fen"),        # aim -> en
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected

def test_e_sound_transformations():
    """
    Test les différentes graphies du son [e].
    Règle 6 dans french_to_creole.py
    
    Vérifie:
    - 'er/ez/et' final -> 'é'
    - 'ei' -> 'é'
    - 'ée' -> 'é'
    - 'ay/ey' final -> 'é'
    """
    test_cases = [
        ("parler", "palé"),     # er final
        ("nez", "né"),          # ez final
        ("fait", "fé"),         # ait final
        ("pied", "pyé"),        # ied final
        ("née", "né"),          # ée final
        ("Bay", "bé"),          # ay final
        ("volleyball", "volébol")  # ey dans le mot
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected
def test_multiple_rules_combinations():
    """
    Test les mots nécessitant l'application de plusieurs règles.
    
    Vérifie:
    - L'ordre correct d'application des règles
    - Leurs interactions
    - Les terminaisons spéciales comme 'tion' -> 'syon'
    """
    test_cases = [
        ("université", "inivèsité"),      # u->i, s->z, é final
        ("excellence", "èksélans"),       # x->ks, ce->s, en->an
        ("pharmacien", "fanmasyen"),      # ph->f, ci->sy, en->an
        ("circulation", "sikilasyon"),    # c->s, u->i, tion->syon
        ("question", "kèsyon"),           # qu->k, tion->syon
        ("imagination", "imajinasyon"),   # g->j, tion->syon
        ("attention", "atansyon"),        # tion->syon, en->an
        ("condition", "kondisyon"),       # tion->syon
        ("position", "pozisyon"),         # tion->syon, s->z
    ]
    for input_word, expected in test_cases:
        assert french_to_creole(input_word) == expected
def test_s_sound_and_tion_transformation():
    """
    Test les transformations du son [s] incluant 'tion'.
    Règle 3 dans french_to_creole.py
    
    Vérifie dans l'ordre:
    1. 'tion' -> 'syon' (règle prioritaire)
    2. 'ss' -> 's'
    3. 'ce' final -> 's'
    4. 'ç' -> 's'
    5. 'sc + e/i' -> 's'
    6. 'c + e/i/y' -> 's'
    """
    test_cases = [
        # Tests de la terminaison 'tion'
        ("action", "aksyon"),          # tion simple
        ("attention", "atansyon"),     # tion avec nasale
        ("constitution", "konstitisyon"), # tion avec autres règles
        ("tradition", "tradisyon"),    # tion préservé malgré d autres règles
        
        # Tests des autres règles du son [s]
        ("poisson", "pwason"),        # ss -> s
        ("glace", "glas"),           # ce final -> s
        ("façade", "fasad"),         # ç -> s
        ("science", "syans"),        # sc -> s
        ("céleste", "sélès"),        # c + e
        ("citron", "sitron"),        # c + i
        
        # Tests de combinaisons
        ("récréation", "rékréasyon"),  # é + tion
        ("position", "pozisyon"),      # s intervocalique + tion
        ("collection", "kolèksyon"),   # combinaison multiple
        ("situation", "sitiyasyon"),   # combinaison avec i
        ("émotions", "émosyon"),       # tion + s final
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"     
def test_n_doubling_after_a():
    """
    Test le doublement du 'n' entre voyelles après 'a'.
    Règle 20 dans french_to_creole.py
    
    Vérifie:
    - Doublement du n entre 'a' et une voyelle
    - Application avant la suppression du 'e' final
    """
    test_cases = [
        ("banane", "bannann"),     # cas typique
        ("canne", "kann"),         # autre exemple
        ("ananas", "annanna"),     # double application
        ("manioc", "manyòk"),      # pas de doublement car i après n
        ("piano", "pyano"),        # pas de doublement car i avant n
        ("canard", "kanna"),       # application avec autres règles
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"  

def test_ille_and_le_endings():
    """
    Test les transformations des terminaisons 'ille' et 'le'.
    Règle 22 dans french_to_creole.py
    
    Vérifie:
    - 'ille' devient 'i' quand il se prononce [ij]
    - 'le' final disparaît
    - Cas particuliers pour 'ville', 'mille' où 'ille' ne se prononce pas [ij]
    """
    test_cases = [
        ("fille", "fi"),          # ille prononcé [ij] -> i
        ("famille", "fami"),      # ille prononcé [ij] -> i
        ("béquille", "béki"),     # ille prononcé [ij] -> i
        ("grille", "gri"),        # ille prononcé [ij] -> i
        ("ville", "vil"),         # ille ne se prononce pas [ij], seul le disparaît
        ("mille", "mil"),         # ille ne se prononce pas [ij], seul le disparaît
        ("ficelle", "fisè"),      # le final disparaît
        ("pile", "pi"),           # le final disparaît
        ("table", "tab"),         # le final disparaît
        ("quille", "ki"),         # ille prononcé [ij] -> i
        ("gentille", "janti"),    # ille prononcé [ij] -> i
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"
def test_g_sound_transformation():
    """
    Test les transformations des graphies du son [g].
    Règle 23 dans french_to_creole.py
    
    Vérifie:
    - 'gu' + e/i devient 'g'
    - 'g' reste 'g' devant a/o/u
    - 'c' devient 'g' dans certains contextes
    """
    test_cases = [
        ("guitare", "gita"),      # gu + i -> g
        ("gâteau", "gato"),       # g + a reste g
        ("seconde", "sigond"),    # c -> g devant on
        ("guerre", "gè"),         # gu + e -> g
        ("guidon", "gidon"),      # gu + i -> g
        ("garçon", "gason"),      # g simple préservé
        ("gondole", "gondol")     # g simple préservé
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"
def test_ij_sound_transformation():
    """
    Test les transformations du son [ij].
    Règle 24 dans french_to_creole.py
    
    Vérifie:
    - 'ill' + voyelle -> 'y'
    - 'll' + voyelle -> 'y'
    - 'i' + voyelle -> 'y'
    - 'ï' -> 'y'
    - 'ye' final -> 'y'
    """
    test_cases = [
        ("marier", "mayé"),       # i + e -> y
        ("barrière", "bayè"),     # i + è -> y
        ("maillot", "mayo"),      # ill + o -> y
        ("papillon", "papiyon"),  # ll + o -> y
        ("billet", "biyé"),       # i + e -> y
        ("Moïse", "Moyiz"),      # ï -> y
        ("Haïti", "Ayiti"),      # ï -> y
        ("papaye", "papay"),     # ye final -> y
        ("pied", "pyé"),         # i + e -> y
        ("famille", "fami"),     # ne pas transformer 'ille' final
        ("ville", "vil")         # ne pas transformer 'll' sans voyelle après
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"

def test_ndre_nde_transformation():
    """
    Test les transformations de 'ndre' et 'nde' en 'nn'.
    Règle 25 dans french_to_creole.py
    
    Vérifie:
    - Exceptions spécifiques:
        * 'prendre' -> 'pran'
        * 'grand(e)' -> 'gran'
    - Cas généraux:
        * 'ndre' final -> 'nn'
        * 'nde' final -> 'nn'
    """
    test_cases = [
        # Exceptions
        ("prendre", "pran"),       # exception spécifique
        ("grande", "gran"),        # exception spécifique
        ("grand", "gran"),         # exception spécifique
        
        # Cas généraux
        ("vendre", "vann"),        # ndre -> nn
        ("marchande", "machann"),  # nde -> nn + autres règles
        ("lavande", "lavann"),     # nde -> nn
        ("pondre", "ponn"),        # ndre -> nn
        ("descendre", "désann"),   # ndre -> nn + autres règles
        ("attendre", "atann"),     # ndre -> nn
        ("monde", "monn"),         # nde -> nn
        ("bande", "bann"),         # nde -> nn
        ("confondre", "konfonn"),  # ndre -> nn + autres règles
        
        # Cas où la règle ne s'applique pas
        ("gronder", "gronné"),     # ne pas transformer 'nd' quand pas suivi de 're' ou 'e' final
        ("mandoline", "mandolin"), # ne pas transformer 'nd' au milieu du mot
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"

def test_mbre_mble_transformation():
    """
    Test les transformations de 'mbre', 'mble', 'mbe' en 'nm'.
    Règle 26 dans french_to_creole.py
    
    Vérifie:
    - 'mbre' final -> 'nm'
    - 'mble' final -> 'nm'
    - 'mbe' final -> 'nm'
    - Interactions avec d'autres règles
    """
    test_cases = [
        # Cas avec 'mbre'
        ("jambre", "janm"),       # mbre -> nm
        ("chambre", "chanm"),     # mbre -> nm
        ("décembre", "désanm"),   # mbre -> nm + autres règles
        ("novembre", "novanm"),   # mbre -> nm + autres règles
        ("septembre", "sèptanm"), # mbre -> nm + autres règles
        
        # Cas avec 'mbe'
        ("tombe", "tonm"),        # mbe -> nm
        ("bombe", "bonm"),        # mbe -> nm
        ("colombe", "kolonm"),    # mbe -> nm
        
        # Cas avec 'mble'
        ("ensemble", "ansanm"),   # mble -> nm + autres règles
        ("ressemble", "résanm"),  # mble -> nm + autres règles
        ("tremble", "tranm"),     # mble -> nm
        
        # Cas où la règle ne s'applique pas
        ("nombre", "nonm"),       # ne pas transformer 'mb' au milieu du mot
        ("bambou", "banbou"),     # ne pas transformer 'mb' non suivi de 'e' final
        ("membre", "manm"),       # autre règle s'applique
    ]
    for input_word, expected in test_cases:
        result = french_to_creole(input_word)
        assert result == expected, f"Pour {input_word}, attendu {expected} mais obtenu {result}"