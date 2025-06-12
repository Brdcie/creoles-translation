
import json
import csv
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Charger le fichier de test
with open("test_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)["pairs"]

pairs = [(d[0].strip().lower(), d[1].strip().lower()) for d in data if isinstance(d, list) and len(d) == 2]

# Charger les tokenizers à partir des données d'entraînement
with open("train_data.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)["pairs"]

input_texts = [f"startseq {fr.strip().lower()} endseq" for fr, _ in train_data]
target_texts = [f"startseq {gcf.strip().lower()} endseq" for _, gcf in train_data]

input_tokenizer = Tokenizer(filters='')
input_tokenizer.fit_on_texts(input_texts)
input_word_index = input_tokenizer.word_index
input_index_word = {v: k for k, v in input_word_index.items()}

target_tokenizer = Tokenizer(filters='')
target_tokenizer.fit_on_texts(target_texts)
target_word_index = target_tokenizer.word_index
target_index_word = {v: k for k, v in target_word_index.items()}

max_encoder_seq_length = max(len(seq.split()) for seq in input_texts)
max_decoder_seq_length = max(len(seq.split()) for seq in target_texts)

# Charger le modèle
model = load_model("seq2seq_fr_gcf.keras")

# Fonction de traduction
def decode_sequence(input_sentence):
    input_seq = input_tokenizer.texts_to_sequences([f"startseq {input_sentence.lower()} endseq"])
    input_seq = pad_sequences(input_seq, maxlen=max_encoder_seq_length, padding='post')
    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_word_index['startseq']
    decoded_sentence = []

    for _ in range(max_decoder_seq_length):
        output_tokens = model.predict([input_seq, target_seq], verbose=0)
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = target_index_word.get(sampled_token_index, '')
        if sampled_word in ['endseq', '']:
            break
        decoded_sentence.append(sampled_word)
        target_seq[0, 0] = sampled_token_index

    return ' '.join(decoded_sentence)

# BLEU + CSV
smoothie = SmoothingFunction().method4
bleu_scores = []

with open("test_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Français", "Référence créole", "Traduction IA", "BLEU score"])

    for fr, gcf in pairs:
        pred = decode_sequence(fr)
        reference = gcf.split()
        candidate = pred.split()
        score = sentence_bleu([reference], candidate, smoothing_function=smoothie)
        bleu_scores.append(score)
        writer.writerow([fr, gcf, pred, f"{score:.4f}"])

print(f"BLEU score moyen sur {len(bleu_scores)} phrases de test : {np.mean(bleu_scores):.4f}")
print("Résultats enregistrés dans 'test_results.csv'")
