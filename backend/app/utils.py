import logging
from logging.handlers import RotatingFileHandler
import io
from pypdf import PdfReader
from fastapi import HTTPException

def setup_logger():
    """Configura e retorna o logger da aplicação."""
    logger = logging.getLogger("api_emails")
    
    # Se o logger já tiver handlers, não adiciona de novo (evita duplicidade no reload)
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler Arquivo
    file_handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # Handler Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Instância global do logger para ser importada
logger = setup_logger()

def extract_text_from_pdf(file_bytes):
    """Lê bytes de um arquivo PDF e retorna texto."""
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        
        logger.info(f"PDF processado. Páginas: {len(reader.pages)}")
        return text
    except Exception as e:
        logger.error(f"Erro ao ler PDF: {e}")
        raise HTTPException(status_code=400, detail="Arquivo PDF inválido ou corrompido.")