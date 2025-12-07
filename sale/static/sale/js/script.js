// --- DADOS DE EXEMPLO (Simulando uma venda pronta) ---
// Em produção, isso viria da sua lógica de carrinho
let cart = [
    { name: 'Refrigerante Cola 2L', price: 8.50, quantity: 2 },
    { name: 'Salgadinho Queijo 150g', price: 6.99, quantity: 1 },
    { name: 'Pão de Forma', price: 7.20, quantity: 1 }
];
let currentTotal = 31.19; // Total fixo do exemplo
let discountPercent = 0;
let selectedPaymentMethod = null;

// --- Seletores do DOM ---
const paymentBtn = document.getElementById('payment-btn');
const paymentModal = document.getElementById('payment-modal');
const closePaymentModalBtn = document.getElementById('close-payment-modal');
const modalTotalAmount = document.getElementById('modal-total-amount');
const paymentMethodButtons = document.querySelectorAll('.payment-method-btn');
const cashPaymentDetails = document.getElementById('cash-payment-details');
const cashReceivedInput = document.getElementById('cash-received');
const changeAmountEl = document.getElementById('change-amount');
const confirmPaymentBtn = document.getElementById('confirm-payment-btn');

// --- Helper: Formatar Moeda ---
const formatCurrency = (value) => {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

// --- 1. Lógica do Modal de Pagamento ---

// Abrir Modal
paymentBtn.addEventListener('click', () => {
    modalTotalAmount.textContent = formatCurrency(currentTotal);
    paymentModal.style.display = 'block';
});

// Fechar Modal
closePaymentModalBtn.addEventListener('click', () => {
    paymentModal.style.display = 'none';
    resetPaymentUI();
});

// Fechar ao clicar fora
window.addEventListener('click', (e) => {
    if (e.target === paymentModal) {
        paymentModal.style.display = 'none';
        resetPaymentUI();
    }
});

// Seleção do Método de Pagamento
paymentMethodButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        // Remove seleção anterior
        paymentMethodButtons.forEach(btn => btn.classList.remove('selected'));
        
        // Adiciona nova seleção
        e.target.classList.add('selected');
        selectedPaymentMethod = e.target.dataset.method;
        
        // Lógica específica para Dinheiro
        if (selectedPaymentMethod === 'dinheiro') {
            cashPaymentDetails.classList.remove('hidden');
            confirmPaymentBtn.disabled = true; // Espera digitar o valor
            cashReceivedInput.focus();
        } else {
            cashPaymentDetails.classList.add('hidden');
            confirmPaymentBtn.disabled = false; // Libera para cartão/pix
        }
    });
});

// Cálculo de Troco em Tempo Real
cashReceivedInput.addEventListener('input', () => {
    const cashReceived = parseFloat(cashReceivedInput.value) || 0;
    const change = cashReceived - currentTotal;

    if (change < 0) {
        changeAmountEl.textContent = "Faltam R$ " + Math.abs(change).toFixed(2);
        confirmPaymentBtn.disabled = true;
    } else {
        changeAmountEl.textContent = formatCurrency(change);
        confirmPaymentBtn.disabled = false;
    }
});

// Função para limpar a UI do modal ao fechar
const resetPaymentUI = () => {
    paymentMethodButtons.forEach(btn => btn.classList.remove('selected'));
    cashPaymentDetails.classList.add('hidden');
    cashReceivedInput.value = '';
    changeAmountEl.textContent = formatCurrency(0);
    confirmPaymentBtn.disabled = true;
    selectedPaymentMethod = null;
};

// --- 2. Lógica de Geração da Notinha ---

const generateReceipt = (saleDetails) => {
    // Gera o HTML da lista de itens
    const itemsHtml = saleDetails.cart.map(item => `
        <tr class="receipt-item">
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>${formatCurrency(item.price * item.quantity)}</td>
        </tr>
    `).join('');

    const now = new Date();

    // Estrutura HTML completa do Recibo
    const receiptHtml = `
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>Recibo</title>
            <style>
                body { font-family: 'Courier New', monospace; width: 300px; margin: 0 auto; color: #000; }
                .header { text-align: center; border-bottom: 1px dashed #000; padding-bottom: 10px; margin-bottom: 10px; }
                h2 { margin: 0; font-size: 16px; }
                p { margin: 2px 0; font-size: 12px; }
                table { width: 100%; font-size: 12px; }
                th, td { text-align: left; padding: 2px 0; }
                th { border-bottom: 1px dashed #000; }
                .totals { margin-top: 10px; border-top: 1px dashed #000; padding-top: 10px; font-size: 12px; }
                .flex { display: flex; justify-content: space-between; margin-bottom: 3px; }
                .bold { font-weight: bold; }
                .footer { text-align: center; margin-top: 20px; font-size: 10px; }
                @media print { body { margin: 0; } }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>MERCADO EXEMPLO</h2>
                <p>${now.toLocaleDateString()} - ${now.toLocaleTimeString()}</p>
                <p>*** NÃO É DOCUMENTO FISCAL ***</p>
            </div>
            <table>
                <thead><tr><th>Item</th><th>Qtd</th><th>Total</th></tr></thead>
                <tbody>${itemsHtml}</tbody>
            </table>
            <div class="totals">
                <div class="flex bold"><span>TOTAL:</span><span>${formatCurrency(saleDetails.total)}</span></div>
                <div class="flex"><span>Forma:</span><span>${saleDetails.paymentMethod.toUpperCase()}</span></div>
                ${saleDetails.paymentMethod === 'dinheiro' ? `
                <div class="flex"><span>Recebido:</span><span>${formatCurrency(saleDetails.cashReceived)}</span></div>
                <div class="flex"><span>Troco:</span><span>${formatCurrency(saleDetails.change)}</span></div>
                ` : ''}
            </div>
            <div class="footer"><p>Obrigado e volte sempre!</p></div>
        </body>
        </html>
    `;

    // Abre janela, escreve e imprime
    const win = window.open('', '', 'width=640,height=480');
    win.document.write(receiptHtml);
    win.document.close();
    win.onload = () => {
        win.print();
        win.close();
    };
};

// --- 3. Ação Final: Botão Confirmar ---

confirmPaymentBtn.addEventListener('click', () => {
    const cashReceived = parseFloat(cashReceivedInput.value) || 0;
    
    const saleDetails = {
        cart: cart,
        total: currentTotal,
        paymentMethod: selectedPaymentMethod,
        cashReceived: cashReceived,
        change: (selectedPaymentMethod === 'dinheiro') ? (cashReceived - currentTotal) : 0
    };

    // 1. Gera notinha
    generateReceipt(saleDetails);

    // 2. Fecha modal e limpa
    paymentModal.style.display = 'none';
    resetPaymentUI();
    
    // Aqui você adicionaria o código para limpar o carrinho real
    alert("Venda finalizada e recibo gerado!");
});

