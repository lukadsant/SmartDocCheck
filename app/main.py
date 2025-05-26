from fastapi import FastAPI
from app.endpoints import upload,ocr,validate,validatemultiple

app = FastAPI(title="Validador inteligente de Documentos")

app.include_router(upload.router)
app.include_router(ocr.router)
app.include_router(validate.router)
app.include_router(validatemultiple.router)

