from typing import Dict, List, Tuple
from pdfminer.high_level import extract_text
import pandas as pd
import re
from pathlib import Path
import os

os.system('clear')

class ConversationExtractor:
    """Extrait uniquement les paires de traduction à partir des tableaux."""
    
    def __init__(self):
        self.sections = [
            "Premiers contacts",
            "Rencontre et présentation", 
            "Temps, dates, fêtes",
            "Appels à l'aide",
            "Voyager",
            "En ville",
            "À la montagne, à la plage, à la campagne, dans la mangrove",
            "Hébergement",
            "Nourriture",
            "Achats et souvenirs",
            "Rendez-vous professionnels",
            "Santé"
        ]
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            full_text = ""
            found_first_section = False
            
            for page_num in range(65, 183):
                page_text = extract_text(pdf_path, page_numbers=[page_num])
                if "En Guadeloupe, le fait de parler français" in page_text:
                    found_first_section = True
                
                if found_first_section:
                    full_text += page_text
            
            return full_text
        except Exception as e:
            print(f"Erreur lors de l'extraction du texte: {e}")
            return ""

    def clean_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    def extract_table_pairs(self, text: str) -> List[Tuple[str, str]]:
        pairs = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            separators = ['|', '//', '➞', '/', ':']
            for sep in separators:
                if sep in line:
                    if sep == ':' and (':/' in line or line.endswith(':')):
                        continue
                    parts = line.split(sep, 1)
                    if len(parts) == 2:
                        creole, french = parts[0].strip(), parts[1].strip()
                        if creole and french:
                            pairs.append((creole, french))
                            break
        return pairs

    def save_to_excel(self, pairs: List[Tuple[str, str]], output_file: str = "conversation_pairs.xlsx"):
        df = pd.DataFrame(pairs, columns=['creole', 'french'])
        df.to_excel(output_file, index=False)

    def extract_all(self, pdf_path: str) -> List[Tuple[str, str]]:
        text = self.extract_text_from_pdf(pdf_path)
        text = self.clean_text(text)
        return self.extract_table_pairs(text)

def main():
    pdf_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/pdf/assimil-9782700561043-guide-francais-creole.pdf")
    output_path = Path("/Users/brigitte/Dropbox/0-GWADA/traduction-creole-guadeloupeen/data/raw/conversation_pairs.xlsx")
    
    extractor = ConversationExtractor()
    pairs = extractor.extract_all(pdf_path)
    extractor.save_to_excel(pairs, output_path)
    
    print(f"\nNombre total de paires extraites: {len(pairs)}")

if __name__ == "__main__":
    main()
