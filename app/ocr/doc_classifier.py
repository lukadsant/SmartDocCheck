def detectar_tipo_documento(texto: str) -> str:
    texto = texto.lower()

    if 'carteira de identidade' in texto or 'registro geral' in texto:
        return 'RG'
    elif 'carteira nacional de habilitação' in texto or 'cnh' in texto:
        return 'CNH'
    elif 'certificado' in texto:
        return 'Certificado'
    elif 'cpf' in texto:
        return 'CPF'
    return 'Desconhecido'
