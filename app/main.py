from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import upload,ocr,validate,validatemultiple

app = FastAPI(title="Validador inteligente de Documentos")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(upload.router)
app.include_router(ocr.router)
app.include_router(validate.router)
app.include_router(validatemultiple.router)

