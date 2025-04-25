from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.file_handler import save_upload_file
import os

router = APIRouter(prefix="/upload", tags=["Upload"])
UPLOAD_DIR = "uploads"

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo precisa ser uma imagem.")
    
    filepath = await save_upload_file(file, UPLOAD_DIR)
    return JSONResponse(content={"message": "Arquivo salvo com sucesso.", "path": filepath})