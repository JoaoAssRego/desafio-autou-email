import os
import json
import nltk
from dotenv import load_dotenv
from groq import Groq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
from .utils import logger  # Importando o logger configurado

# Carrega ambiente
load_dotenv()

# Configuração do Cliente Groq
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    logger.critical("A chave GROQ_API_KEY não foi encontrada!")

client = Groq(api_key=api_key)

# Configuração NLTK (Executa ao importar o arquivo)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('stemmers/rslp')
except LookupError:
    logger.warning("Baixando recursos do NLTK...")
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('rslp')
    nltk.download('punkt_tab')

def preprocess_text_nlp(text: str):
    """Realiza o pipeline de NLP: Tokenização -> Stopwords -> Stemming."""
    try:
        logger.info(f"Iniciando NLP. Tamanho entrada: {len(text)}")
        
        text_lower = text.lower()
        tokens = word_tokenize(text_lower, language='portuguese')
        
        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        
        stemmer = RSLPStemmer()
        stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
        
        processed_text = " ".join(stemmed_tokens)
        
        logger.debug(f"NLP Concluído: {processed_text[:50]}...")
        return text, processed_text

    except Exception as e:
        logger.error(f"Erro no NLP: {e}")
        return text, text

def analyze_with_groq(original_text: str):
    """Envia o texto para a IA classificar."""
    prompt = f"""
    Atue como assistente de triagem.
    Analise o email: "{original_text}"

    Tarefas:
    1. Classifique: "Produtivo" ou "Improdutivo".
    2. Sugira resposta curta e profissional.

    Retorne JSON estrito:
    {{
        "category": "Produtivo" ou "Improdutivo",
        "response": "Sua sugestão..."
    }}
    """

    try:
        logger.info("Chamando API Groq (Llama 3.3)...")
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Responda apenas JSON válido."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        
        content = completion.choices[0].message.content
        logger.info("Resposta da IA recebida.")
        return json.loads(content)

    except Exception as e:
        logger.error(f"Erro na Groq: {e}")
        return {
            "category": "Erro",
            "response": "Falha no serviço de IA."
        }