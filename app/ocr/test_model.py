import spacy

# Carrega o modelo treinado
nlp = spacy.load("/home/lukadsant/wslcode/SmartDocCheck/app/ocr/custom_ner_model/model-last")

print("Pipes:", nlp.pipe_names)
print("NER Labels:", nlp.get_pipe("ner").labels)

# Use um texto EXATO dos seus dados de treinamento
text_from_training = "Nome: Lucas D'Sant, CPF: 123.456.789-00, Data de nascimento: 01/01/2000"
doc = nlp(text_from_training)

print("\nEntidades reconhecidas (com texto do treinamento):")
for ent in doc.ents:
    print(f"'{ent.text}' ({ent.label_})")

# Mantenha seu teste original para comparação
print("\nEntidades reconhecidas (com texto de teste original):")
text = "Em 01/01/2001 pessoa chamada Ana Paula e seu documento é 123.123.123-10."
doc = nlp(text)
for ent in doc.ents:
    print(f"'{ent.text}' ({ent.label_})")