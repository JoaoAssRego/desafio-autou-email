import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .utils import logger, extract_text_from_pdf
from .services import preprocess_text_nlp, analyze_with_groq

app = FastAPI(title="Classificador de Emails")

# Permite que qualquer origem acesse a API (útil para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process_email(
    file: UploadFile = File(None), 
    emailText: str = Form(None)
):
    content = ""
    source_type = ""

    # Lógica de seleção de entrada
    if file:
        file_bytes = await file.read()
        if file.filename.endswith('.pdf'):
            content = extract_text_from_pdf(file_bytes)
            source_type = "PDF"
        elif file.filename.endswith('.txt'):
            content = file_bytes.decode('utf-8')
            source_type = "TXT"
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado. Use .txt ou .pdf")
            
    elif emailText:
        content = emailText.strip()
        source_type = "Texto Direto"
    
    if not content:
        raise HTTPException(status_code=400, detail="Conteúdo vazio.")

    logger.info(f"Processando requisição via {source_type}")

    # Passo A: Pipeline de NLP (Tokenização, Stemming)
    original, processed = preprocess_text_nlp(content)
    
    # Passo B: Inteligência Artificial (Groq/Llama 3)
    result = analyze_with_groq(original)
    
    return result

# Monolito para Deploy

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
    logger.info(f"Frontend montado com sucesso a partir de: {FRONTEND_DIR}")
else:
    logger.warning(f"Pasta frontend não encontrada em {FRONTEND_DIR}. A interface web não será servida.")