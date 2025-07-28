from nlp_extractor import extrair_dados_estruturados

texto="João da Silva nasceu em 10 de janeiro de 1990 em São Paulo. e tem como cpf 088.794.450-73"
resultado = extrair_dados_estruturados(texto)
print(resultado)

#