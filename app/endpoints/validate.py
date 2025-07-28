from fastapi import APIRouter, UploadFile, Form, HTTPException
from app.ocr.reader import extrair_texto_da_imagem
from app.ocr.nlp_extractor import extrair_dados_estruturados
from app.ocr.doc_classifier import detectar_tipo_documento
from app.ocr.regex_extractor import extrair_dados_regex
from difflib import SequenceMatcher

router = APIRouter(prefix="/validate", tags=["Validation"])

@router.post("/")
async def validate_data(
    document: UploadFile,
    user_data: str = Form(...),
):

    try:
        content = await document.read()
        extracted_text_list = extrair_texto_da_imagem(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no OCR: {e}")

    # Junta o texto extraído em uma string única
    texto_unico = ' '.join(extracted_text_list)

    # Classificação do tipo de documento
    tipo_doc = detectar_tipo_documento(texto_unico)

    # NLP: extrai entidades do texto extraído
    entidades_nlp = extrair_dados_estruturados(texto_unico)["entidades"]

    # Regex: extrai dados estruturados por padrões
    dados_regex = extrair_dados_regex(texto_unico)

    user_data_lower = user_data.lower()

    # Busca direta
    match_direct = any(user_data_lower in text.lower() for text in extracted_text_list)

    # Busca por similaridade - pega o melhor score
    best_similarity = 0
    for text in extracted_text_list:
        sim = SequenceMatcher(None, user_data_lower, text.lower()).ratio()
        if sim > best_similarity:
            best_similarity = sim

    threshold = 0.7

    validated = match_direct or best_similarity >= threshold

    result = {
        "input_user": user_data,
        "ocr_extracted_text": extracted_text_list,
        "texto_unico": texto_unico,
        "tipo_documento": tipo_doc,
        "best_similarity": round(best_similarity, 2),
        "direct_match": match_direct,
        "validated": validated,
        "entidades_nlp": entidades_nlp,
        "dados_regex": dados_regex
    }

    return result
