model =from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
MBartForConditionalGeneration.from_pretrained(\"facebook/mbart-large-50-many-to-many-mmt\")
tokenizer =
MBart50TokenizerFast.from_pretrained(\"facebook/mbart-large-50-many-to-many-mmt\")
class CustomMBartTokenizer(MBart50TokenizerFast):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def apply_creole_rules(self, text):
        # Implémentez ici vos 32 règles de dérivation du créole guadeloupéen
        # Exemple (à adapter selon vos règles réelles) :
        text = text.replace("u ", "i")
        text = text.replace("ss ", "s")
        text = text.replace("ci ", "si")
        text = text.replace("ce", "s")
        # Ajoutez les autres règles...
        return text
    
    def __call__(self, text, *args, **kwargs):
        if isinstance(text, str):
            text = self.apply_creole_rules(text)
        elif isinstance(text, list):
            text = [self.apply_creole_rules(t) for t in text]
        return super().__call__(text, *args, **kwargs)

tokenizer_cust = CustomMBartTokenizer.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
def generate_translation(model, tokenizer_cust, text):
    encoded = tokenizer_cust(text, return_tensors="pt")
    generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer_cust.lang_code_to_id["gcf_XX"])
    return tokenizer_cust.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    tokenizer_cust.src_lang = "fr_XX"
tokenizer_cust.tgt_lang = "gcf_XX"  # Code pour le créole guadeloupéen
    
    