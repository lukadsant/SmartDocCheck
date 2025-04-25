import easyocr
from typing import List

# Instancia o leitor com suporte a português
reader = easyocr.Reader(['pt'], gpu=False)

def extrair_texto_da_imagem(path_imagem: str) -> List[str]:
    resultado = reader.readtext(path_imagem, detail=0)
    return resultado
