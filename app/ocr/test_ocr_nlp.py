from reader import extrair_texto_da_imagem
from nlp_extractor import extrair_dados_estruturados
from regex_extractor import extrair_dados_regex
from doc_classifier import detectar_tipo_documento
# Caminho da imagem de teste
imgdir = '../../uploads/3aa01d8e5ae84c75a8c272c59dfe23cc_Carteira-de-Identidade-Nacional.png'

# OCR Extrai o texto da imagem
texto_extraido = extrair_texto_da_imagem(imgdir)
texto_unico = ' '.join(texto_extraido)
print('Texto extraído:')
print(texto_extraido)


# Classificação
tipo_doc = detectar_tipo_documento(texto_unico)
print(f'\nTipo de documento detectado: {tipo_doc}')


# NLP
resultado_nlp = extrair_dados_estruturados(texto_unico)
print('\nEntidades reconhecidas (spaCy):')
print(resultado_nlp)

# Regex
resultado_regex = extrair_dados_regex(texto_unico)
print('\nDados reconhecidos por regex:')
print(resultado_regex)

# Resultado final combinado
resultado_final = {
    'tipo_documento': tipo_doc,
    'texto': texto_unico,
    'entidades_nlp': resultado_nlp['entidades'],
    'dados_regex': resultado_regex
}
print('\nResultado final:')
print(resultado_final)
