import spacy
from typing import Dict, Any

# Carrega o modelo de português do spaCy
nlp = spacy.load('pt_core_news_sm')

def extrair_dados_estruturados(texto: str) -> Dict[str, Any]:
    doc = nlp(texto)
    dados = {
        'entidades': [
            {'texto': ent.text, 'label': ent.label_}
            for ent in doc.ents
        ]
    }
    return dados
