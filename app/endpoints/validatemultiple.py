from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from app.ocr.reader import extrair_texto_da_imagem
from difflib import SequenceMatcher
import json

router = APIRouter(prefix="/validate", tags=["Validation"])

@router.post("/multiple")
async def validate_multiple(
    document: UploadFile,
    user_inputs: str = Form(...)
):
    try:
        content = await document.read()
        extracted_text_list = extrair_texto_da_imagem(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no OCR: {e}")

    try:
        inputs_dict = json.loads(user_inputs)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de 'user_inputs' inválido. Deve ser JSON.")

    extracted_text_joined = " ".join(extracted_text_list).lower()
    threshold = 0.7
    results = {}

    for field, user_value in inputs_dict.items():
        user_value_lower = user_value.lower()

        # Busca direta
        match_direct = user_value_lower in extracted_text_joined

        # Busca por similaridade
        best_similarity = 0
        for text in extracted_text_list:
            sim = SequenceMatcher(None, user_value_lower, text.lower()).ratio()
            if sim > best_similarity:
                best_similarity = sim

        validated = match_direct or best_similarity >= threshold

        results[field] = {
            "input_user": user_value,
            "best_similarity": round(best_similarity, 2),
            "direct_match": match_direct,
            "validated": validated
        }

    return {
        "inputs": inputs_dict,
        "ocr_extracted_text": extracted_text_list,
        "results": results
    }
