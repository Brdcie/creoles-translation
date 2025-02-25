from src.translator.french_to_creole_translator import transform_french_to_creole


def main():
    while True:
        phrase = input("Enter a French sentence: ")
        trad = transform_french_to_creole(phrase)
        print("Creole Translation:", trad)
        if phrase.lower() in ["o wouvwè", "au revoir", 'bye']:
            break


if __name__ == "__main__":
    main()