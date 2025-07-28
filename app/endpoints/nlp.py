
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ocr.nlp_extractor import extrair_dados_estruturados

router = APIRouter(prefix="/nlp", tags=["NLP"])

class TextoEntrada(BaseModel):
    texto: str

@router.post("/")
async def analisar_texto_nlp(dados: TextoEntrada):
    if not dados.texto or not dados.texto.strip():
        raise HTTPException(status_code=400, detail="Texto não pode ser vazio.")
    resultado = extrair_dados_estruturados(dados.texto)
    return {"entidades": resultado["entidades"]}
