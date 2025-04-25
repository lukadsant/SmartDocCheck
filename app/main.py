from fastapi import FastAPI
from app.endpoints import upload

app = FastAPI(title="Validador inteligente de Documentos")

app.include_router(upload.router)
app.include_router(ocr.router)
