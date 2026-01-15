```
# 📧 Classificador Inteligente de Emails (AutoU Challenge)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![AI](https://img.shields.io/badge/AI-Llama%203.3-purple)
![License](https://img.shields.io/badge/License-MIT-grey)

Solução desenvolvida para o desafio técnico da **AutoU**. Esta aplicação utiliza Processamento de Linguagem Natural (NLP) e Inteligência Artificial Generativa para automatizar a triagem de emails corporativos.

## 🚀 Funcionalidades

- **📥 Entrada Flexível:** Upload de arquivos (`.pdf`, `.txt`) ou inserção direta de texto.
- **🧠 Pipeline de NLP:** Pré-processamento "raiz" com NLTK (Tokenização, Remoção de Stopwords e Stemming em Português).
- **🤖 Classificação com IA:** Utiliza o modelo **Llama-3.3-70b** (via Groq) para categorizar emails em *Produtivo* ou *Improdutivo*.
- **✍️ Resposta Automática:** Geração de sugestões de resposta contextualizadas e profissionais.
- **🎨 Interface Moderna:** Frontend responsivo com UX intuitiva (Abas de navegação e feedback visual).

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python, FastAPI, Uvicorn.
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla).
- **IA & NLP:** Groq API (Llama 3), NLTK, PyPDF.
- **Infraestrutura:** Render (Hospedagem), Docker ready.

---

## 📦 Como Executar Localmente

Siga os passos abaixo para rodar o projeto na sua máquina.

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Git instalado.
- Uma chave de API gratuita da [Groq](https://console.groq.com/).

### 2. Clonar o Repositório
```bash
git clone [https://github.com/SEU_USUARIO/desafio-autou-email.git](https://github.com/SEU_USUARIO/desafio-autou-email.git)
cd desafio-autou-email

```

### 3. Criar Ambiente Virtual

Recomendado para isolar as dependências.

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate

```

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 4. Instalar Dependências

```bash
pip install -r requirements.txt

```

### 5. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave da Groq:

```ini
# Arquivo: .env
GROQ_API_KEY="gsk_sua_chave_aqui_xxxxxxxxxxxxx"

```

### 6. Executar a Aplicação

Rode o servidor localmente com o comando:

```bash
uvicorn backend.app.main:app --reload

```

Acesse a interface no seu navegador:
👉 **https://www.google.com/search?q=http://127.0.0.1:8000**

---

## 📂 Estrutura do Projeto

O projeto segue os princípios de **Clean Architecture** e **Separação de Preocupações**:

```text
desafio-autou-email/
├── backend/
│   └── app/
│       ├── main.py       # Controlador de Rotas e Configuração da App
│       ├── services.py   # Regra de Negócio (Lógica de IA e NLP)
│       └── utils.py      # Funções Auxiliares (Logs, Leitura de PDF)
├── frontend/             # Interface do Usuário (Servida estaticamente)
│   ├── assets/
│   │   ├── css/
│   │   └── js/
│   └── index.html
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação

```

---

## 🧪 Como Testar

1. Abra a aplicação no navegador.
2. Escolha a aba **Texto** e digite:
> "Bom dia, gostaria de solicitar um orçamento para 50 licenças de software."


3. Clique em **Processar Email**.
4. **Resultado Esperado:** Categoria *Produtivo* e uma sugestão de orçamento.

---

## ☁️ Deploy (Produção)

A aplicação está pronta para deploy em plataformas como **Render**, **Railway** ou **Heroku**.

**Configuração de Build no Render:**

* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
* **Environment Variables:** Adicionar `GROQ_API_KEY`.

---

## 📝 Licença

Este projeto foi desenvolvido para fins de avaliação técnica.

**Autor:** [Seu Nome Aqui]

```

### Dica Profissional:
Lembre-se de substituir `[SEU_USUARIO]` no link do clone e `[Seu Nome Aqui]` no final. Esse README mostra que você se preocupa com a **Developer Experience (DX)**, ou seja, facilita a vida de quem vai corrigir seu teste.

```
