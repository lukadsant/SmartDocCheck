import subprocess

def train_spacy_model():
    subprocess.run([
        "python", "-m", "spacy", "train",
        "app/ner_training/config.cfg",
        "--output", "app/ocr/custom_ner_model",
        "--paths.train", "app/ner_training/data/annotated/train.spacy",
        "--paths.dev", "app/ner_training/data/annotated/dev.spacy"
    ])

if __name__ == "__main__":
    train_spacy_model()
