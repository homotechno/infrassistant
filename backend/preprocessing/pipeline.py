import re
import json
import pymorphy3
from pathlib import Path
from backend.utils.glossary import load_glossary

class Preprocessor:
    """
    Text preprocessing pipeline:
    - Lowercasing
    - Glossary-based normalization
    - Cyrillic/Latin tokenization
    - Lemmatization using pymorphy3
    """

    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer(lang='ru')
        self.glossary = {
            k.lower(): v.lower()
            for k, v in load_glossary().items()
        }

    def apply_glossary(self, text: str) -> str:
        """
        Applies glossary substitutions using regex.
        """
        for term, norm in self.glossary.items():
            text = re.sub(r'\b' + re.escape(term) + r'\b', norm, text)
        return text

    def lemmatize(self, tokens):
        """
        Lemmatizes list of tokens.
        """
        return [self.morph.parse(token)[0].normal_form for token in tokens]

    def preprocess_text(self, text: str) -> str:
        """
        Full pipeline for preprocessing a single text string.
        """
        text = text.lower()
        text = self.apply_glossary(text)
        tokens = re.findall(r"[a-zа-яё]+", text)
        lemmas = self.lemmatize(tokens)
        return " ".join(lemmas)

    def preprocess_file(self, input_path: str) -> str:
        """
        Loads text from file, applies preprocessing, returns result.
        """
        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        return self.preprocess_text(raw_text)

    def preprocess_directory(self, input_dir: str, output_dir: str):
        """
        Preprocesses all .txt files in a directory and saves results.
        """
        Path(output_dir).mkdir(exist_ok=True)
        for path in Path(input_dir).glob("*.txt"):
            processed = self.preprocess_file(str(path))
            out_path = Path(output_dir) / path.name
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(processed)
            print(f"Processed {path.name} -> {out_path}")
