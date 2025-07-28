import re
from typing import Dict

def extrair_dados_regex(texto: str) -> Dict[str, str]:
    dados = {}

    cpf_match = re.search(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto)
    if cpf_match:
        dados['cpf'] = cpf_match.group()

    data_match = re.findall(r'\d{2}/\d{2}/\d{4}', texto)
    if data_match:
        dados['data_nascimento'] = data_match[0]
        if len(data_match) > 1:
            dados['validade'] = data_match[-1]

    return dados
