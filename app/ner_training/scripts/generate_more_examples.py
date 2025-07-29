import json
import random
from datetime import datetime, timedelta

def generate_cpf():
    """Gera um CPF aleatório no formato ###.###.###-##"""
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"

def generate_random_date(start_year=1950, end_year=2005):
    """Gera uma data aleatória no formato DD/MM/AAAA."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.strftime("%d/%m/%Y")

def generate_name():
    """Gera um nome aleatório simples ou composto."""
    first_names = ["João", "Maria", "Pedro", "Ana", "Lucas", "Mariana", "Gabriel", "Laura", "Bruno", "Beatriz"]
    last_names = ["Silva", "Santos", "Oliveira", "Souza", "Lima", "Costa", "Pereira", "Rodrigues", "Almeida", "Nascimento"]
    
    name_types = ["simple", "compound", "surname_first"]
    name_type = random.choice(name_types)

    if name_type == "simple":
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    elif name_type == "compound":
        return f"{random.choice(first_names)} {random.choice(last_names)} {random.choice(last_names)}"
    else: # surname_first, just for variety
        return f"{random.choice(last_names)}, {random.choice(first_names)}"


def generate_example(template_id):
    """Gera um único exemplo com anotações."""
    name = generate_name()
    cpf = generate_cpf()
    dob = generate_random_date()

    templates = [
        # Template 1: Padrão "Nome: X, CPF: Y, Data de nascimento: Z"
        f"Nome: {name}, CPF: {cpf}, Data de nascimento: {dob}",
        # Template 2: Padrão "Dados Pessoais: Nome: X. CPF: Y. Nasc: Z"
        f"Dados Pessoais: Nome: {name}. CPF: {cpf}. Nasc: {dob}",
        # Template 3: Padrão "Nome Completo: X - CPF: Y - Data Nasc: Z"
        f"Nome Completo: {name} - CPF: {cpf} - Data Nasc: {dob}",
        # Template 4: Ordem diferente: "CPF: Y, Nome: X, Nascimento: Z"
        f"CPF: {cpf}, Nome: {name}, Nascimento: {dob}",
        # Template 5: Apenas nome e CPF
        f"Nome: {name}, CPF: {cpf}",
        # Template 6: Apenas nome e Data de Nascimento
        f"Nome: {name}, Data de nascimento: {dob}",
        # Template 7: Apenas CPF e Data de Nascimento
        f"CPF: {cpf}, Data de nascimento: {dob}"
    ]
    
    text = templates[template_id % len(templates)] # Seleciona um template circularmente

    entities = []
    
    # Encontra e anota as entidades no texto gerado
    # Importante: Esses cálculos de offset são MUITO SENSÍVEIS aos templates!
    # Qualquer alteração nos templates de texto acima exigirá recálculo cuidadoso dos offsets.

    # Anotar NOME
    name_start = text.find(name)
    if name_start != -1:
        entities.append([name_start, name_start + len(name), "NOME"])

    # Anotar CPF
    cpf_start = text.find(cpf)
    if cpf_start != -1:
        entities.append([cpf_start, cpf_start + len(cpf), "CPF"])

    # Anotar DATA_NASCIMENTO
    dob_start = text.find(dob)
    if dob_start != -1:
        entities.append([dob_start, dob_start + len(dob), "DATA_NASCIMENTO"])
    
    # Ordenar as entidades por posição inicial para consistência (importante para spaCy)
    entities.sort(key=lambda x: x[0])

    return {"text": text, "entities": entities}

def generate_dataset(num_examples=100):
    """Gera um conjunto de dados completo com múltiplos exemplos."""
    dataset = []
    for i in range(num_examples):
        dataset.append(generate_example(i)) # Passa 'i' para ciclar pelos templates
    return dataset

if __name__ == "__main__":
    output_dev_json_path = "app/ner_training/data/annotated/dev.json"
    output_train_json_path = "app/ner_training/data/annotated/train.json" # Para usar no treino, se quiser gerar por aqui

    # Gerar para dev.json (10-20 exemplos é um bom começo para dev)
    print("Gerando exemplos para dev.json...")
    dev_data = generate_dataset(num_examples=20) # Ajuste a quantidade aqui
    with open(output_dev_json_path, 'w', encoding='utf-8') as f:
        json.dump(dev_data, f, ensure_ascii=False, indent=2)
    print(f"Gerados {len(dev_data)} exemplos e salvos em {output_dev_json_path}")

    # Gerar para train.json (100-200 exemplos é um bom começo para treino)
    # Se você já tem um train.json, você pode querer APENSAR a ele, não sobrescrever.
    # Por segurança, este script SOBRESCREVE. Adapte se precisar apensar.
    print("\nGerando exemplos para train.json...")
    train_data = generate_dataset(num_examples=200) # Ajuste a quantidade aqui
    with open(output_train_json_path, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    print(f"Gerados {len(train_data)} exemplos e salvos em {output_train_json_path}")

    # Exemplo de como um dos exemplos gerados se parece (para depuração)
    print("\nExemplo de um dos dados gerados:")
    print(json.dumps(train_data[0], ensure_ascii=False, indent=2))

    # Teste os offsets de um exemplo gerado
    print("\nVerificando offsets do primeiro exemplo gerado:")
    first_example = train_data[0]
    text_to_check = first_example["text"]
    entities_to_check = first_example["entities"]
    for start, end, label in entities_to_check:
        print(f"'{text_to_check[start:end]}' ({label})")