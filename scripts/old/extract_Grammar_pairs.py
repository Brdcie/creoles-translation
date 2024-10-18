import re
import csv
from pdfminer.high_level import extract_text

CSV_HEADERS = ['french', 'creole', 'source', 'lesson']

pdf_path = '/Users/brigitte/Dropbox/0-GWADA/Gwadeloupeen_traduction/assimil-9782700561043-guide-francais-creole.pdf'
full_text = extract_text(pdf_path)

def extract_all_lessons(full_text):
    lessons = []
    lesson_pattern = r'➚\s*(\d+e?r?\s*jour)(.*?)(?=➚\s*\d+e?r?\s*jour|\Z)'
    matches = re.findall(lesson_pattern, full_text, re.DOTALL)
    for day, content in matches:
        lessons.append((day.strip(), content.strip()))
    return lessons

def extract_grammar_pairs(text):
    pairs = []
    
    # Pattern 1 and 3
    pattern1_3 = r'\*\*(.*?)\*\*,\s*\*(.*?)\*[;.]'
    pairs.extend([(french.strip(), creole.strip(), "grammar_notes") 
                  for creole, french in re.findall(pattern1_3, text)])
    
    # Pattern 2
    pattern2 = r'(.*?),\s*(.*?)(?=\n|$)'
    for line in text.split('\n'):
        if ',' in line and '*' not in line:
            match = re.search(pattern2, line)
            if match:
                creole, french = match.groups()
                pairs.append((french.strip(), creole.strip(), "grammar_notes"))
    
    return pairs

# Extract all lessons
lessons = extract_all_lessons(full_text)

# Process all lessons and extract grammar pairs
all_grammar_pairs = []
for day, lesson_content in lessons:
    grammar_section = re.search(r'Notes de grammaire(.*?)(?=Entraînement|$)', lesson_content, re.DOTALL)
    if grammar_section:
        pairs = extract_grammar_pairs(grammar_section.group(1))
        all_grammar_pairs.extend([(french, creole, source, day) for french, creole, source in pairs])

# Write all grammar pairs to the CSV file
with open('creole_french_all_grammar_pairs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
    writer.writeheader()
    
    for french, creole, source, lesson in all_grammar_pairs:
        writer.writerow({
            'french': french,
            'creole': creole,
            'source': source,
            'lesson': lesson
        })

# Print sample results
print("Sample grammar pairs:")
for i, (french, creole, source, lesson) in enumerate(all_grammar_pairs[:10]):
    print(f"{i+1}. Lesson: {lesson}")
    print(f"   Creole: {creole}")
    print(f"   French: {french}")
    print(f"   Source: {source}")
    print()

print(f"Total grammar pairs extracted and written to CSV: {len(all_grammar_pairs)}")