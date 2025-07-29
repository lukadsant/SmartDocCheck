import spacy
from spacy.tokens import DocBin
import json
from pathlib import Path

def convert_json_to_spacy(json_path, output_path):
    nlp = spacy.blank("pt") # Usamos nlp.blank("pt") para um tokenizer básico em português
    db = DocBin()
    
    # Adicionar contadores e set para labels
    num_docs_processed = 0
    num_docs_with_ents = 0
    all_labels_found = set()
    invalid_spans_count = 0

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em: {json_path}")
        return # Encerrar a função se o arquivo não existir
    except json.JSONDecodeError:
        print(f"ERRO: Erro de decodificação JSON em: {json_path}. Verifique a formatação do JSON.")
        return # Encerrar a função se o JSON for inválido

    print(f"\nProcessando arquivo: {json_path}")
    print("-" * 30)

    for i, example in enumerate(training_data):
        text = example.get("text")
        entities = example.get("entities")

        if not text or not isinstance(text, str):
            print(f"AVISO: Exemplo {i+1} em '{json_path}' não tem texto válido. Pulando.")
            continue
        if not entities or not isinstance(entities, list):
            print(f"AVISO: Exemplo {i+1} em '{json_path}' não tem entidades válidas. Pulando.")
            continue

        doc = nlp.make_doc(text)
        ents = []
        doc_has_valid_ents = False

        for start, end, label in entities:
            # Validação básica dos offsets
            if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end > len(text) or start >= end:
                print(f"ATENÇÃO: Offsets inválidos ({start}-{end}) para '{label}' no texto: '{text}' (Exemplo {i+1} em {json_path}). Pulando esta entidade.")
                invalid_spans_count += 1
                continue

            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
                all_labels_found.add(label) # Adiciona o label ao conjunto
                doc_has_valid_ents = True
            else:
                # Se span for None, significa que o char_span não conseguiu criar o span
                # Isso geralmente acontece por offsets errados ou caracteres multi-byte
                print(f"ATENÇÃO: Não foi possível criar span para '{label}' em '{text[start:end]}' no texto: '{text}' (offsets: {start}-{end}, Exemplo {i+1} em {json_path}). Verifique os offsets e caracteres especiais.")
                invalid_spans_count += 1
        
        if doc_has_valid_ents: # Adiciona o doc ao DocBin apenas se tiver pelo menos uma entidade válida
            doc.ents = ents
            db.add(doc)
            num_docs_with_ents += 1
        else:
            print(f"AVISO: Documento '{text}' (Exemplo {i+1} em {json_path}) não foi adicionado ao DocBin por não conter entidades válidas.")
        
        num_docs_processed += 1

    db.to_disk(output_path)
    print("-" * 30)
    print(f"Processamento concluído para {json_path}.")
    print(f"✔ Total de exemplos no JSON: {len(training_data)}")
    print(f"✔ Documentos processados com sucesso e adicionados ao DocBin: {num_docs_with_ents}")
    print(f"✔ Labels únicos encontrados e adicionados: {list(all_labels_found) if all_labels_found else 'Nenhum!'}")
    print(f"⚠ Spans inválidos/ignorados devido a offsets incorretos ou problemas: {invalid_spans_count}")
    print(f"Salvo DocBin em: {output_path}")

if __name__ == "__main__":
    data_dir = Path("app/ner_training/data/annotated")
    data_dir.mkdir(parents=True, exist_ok=True) # Garante que o diretório existe

    convert_json_to_spacy(data_dir / "train.json", data_dir / "train.spacy")
    convert_json_to_spacy(data_dir / "dev.json", data_dir / "dev.spacy")