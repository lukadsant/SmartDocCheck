from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.file_handler import save_upload_file
from app.ocr.reader import extrair_texto_da_imagem

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/")
async def ocr_em_imagem(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem.")
    
    path = await save_upload_file(file, "uploads")
    texto = extrair_texto_da_imagem(path)

    return {"texto_extraído": texto}
