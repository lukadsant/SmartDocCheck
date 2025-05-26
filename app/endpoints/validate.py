from fastapi import APIRouter, UploadFile, Form, HTTPException
from app.ocr.reader import extrair_texto_da_imagem
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
        "best_similarity": round(best_similarity, 2),
        "direct_match": match_direct,
        "validated": validated
    }

    return result
