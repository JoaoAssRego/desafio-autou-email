// Seleção dos elementos do DOM
const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const fileLabelText = document.getElementById('fileLabelText');
const emailTextInput = document.getElementById('emailText');

// Elementos de Resultado
const resultArea = document.getElementById('result-area');
const resultCategory = document.getElementById('resultCategory');
const resultResponse = document.getElementById('resultResponse');

// Elementos das Abas
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// --- 1. LÓGICA DAS ABAS (UX/UI) ---
tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove 'active' de todos
        tabButtons.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        // Ativa o clicado
        btn.classList.add('active');
        const targetId = btn.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');

        // Limpa o campo da aba que foi ocultada
        if (targetId === 'tab-file') {
            emailTextInput.value = ''; // Se foi para arquivo, limpa texto
        } else {
            fileInput.value = ''; // Se foi para texto, limpa arquivo
            fileLabelText.textContent = 'Clique ou arraste o arquivo aqui';
            fileLabelText.style.color = '#64748b';
            fileLabelText.style.fontWeight = 'normal';
        }
    });
});

// --- 2. FEEDBACK VISUAL DE ARQUIVO ---
fileInput.addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
        fileLabelText.textContent = `Selecionado: ${this.files[0].name}`;
        fileLabelText.style.color = '#2563eb';
        fileLabelText.style.fontWeight = 'bold';
    }
});

// --- 3. ENVIO DO FORMULÁRIO (CONEXÃO BACKEND) ---
form.addEventListener('submit', async function(e) {
    e.preventDefault();

    // Validação
    const hasFile = fileInput.files.length > 0;
    const hasText = emailTextInput.value.trim().length > 0;

    if (!hasFile && !hasText) {
        alert("Por favor, preencha o campo da aba ativa (Arquivo ou Texto).");
        return;
    }

    // Feedback de Carregamento
    const submitBtn = document.querySelector('.btn-submit');
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent = "Processando com IA...";
    submitBtn.disabled = true;
    
    // Esconde resultado anterior
    resultArea.style.display = 'none';

    // Monta o Payload
    const formData = new FormData();
    if (hasFile) {
        formData.append('file', fileInput.files[0]);
    }
    formData.append('emailText', emailTextInput.value);

    try {
        // Conecta com o Backend (ajuste a URL se necessário)
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Erro desconhecido no servidor');
        }

        const data = await response.json();

        // --- EXIBE RESULTADO ---
        resultArea.style.display = 'block';

        // Atualiza Texto e Cor da Categoria
        resultCategory.textContent = data.category;
        resultCategory.className = 'category-badge'; // Reseta classes
        
        if (data.category === 'Produtivo') {
            resultCategory.classList.add('cat-productive');
        } else if (data.category === 'Improdutivo') {
            resultCategory.classList.add('cat-improductive');
        } else {
            resultCategory.classList.add('cat-error');
        }

        resultResponse.textContent = data.response;
        
        // Scroll suave
        resultArea.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error('Erro:', error);
        alert(`Ocorreu um erro: ${error.message}`);
    } finally {
        // Restaura botão
        submitBtn.textContent = originalBtnText;
        submitBtn.disabled = false;
    }
});