// --- Seletores do DOM ---
const paymentBtn = document.getElementById('payment-btn');
const paymentModal = document.getElementById('payment-modal');
const closePaymentModalBtn = document.getElementById('close-payment-modal');
const modalTotalAmount = document.getElementById('modal-total-amount');
const paymentMethodButtons = document.querySelectorAll('.payment-method-btn');
const cashPaymentDetails = document.getElementById('cash-payment-details');
const cashReceivedInput = document.getElementById('cash-received');
const changeAmountEl = document.getElementById('change-amount');
const confirmPaymentForm = document.getElementById('payment-form');
const confirmPaymentBtn = document.getElementById('confirm-payment-btn');
const printBtn = document.getElementById('print-btn');

// --- DADOS DE EXEMPLO (Simulando uma venda pronta) ---
// Em produção, isso viria da sua lógica de carrinho
let selectedPaymentMethod = null;


// --- Helper: Formatar Moeda ---
const formatCurrency = (value) => {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

// --- 1. Lógica do Modal de Pagamento ---

// Abrir Modal
if (paymentBtn) {
    paymentBtn.addEventListener('click', () => {
        const currentTotal = document.getElementById('total').innerText;
        modalTotalAmount.textContent = formatCurrency(currentTotal);
        paymentModal.style.display = 'block';
    });
}

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
    const currentTotal = document.getElementById('total').innerText;
    const cashReceived = parseFloat(cashReceivedInput.value) || 0;
    const change = cashReceived - parseFloat(currentTotal.replace('R$', '').replace(',', '.')) || 0;

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

const generateSaleOrder = (saleDetails) => {
    // Gera as linhas da tabela de itens
    const itemsHtml = saleDetails.cart.map(item => `
        <tr>
            <td>${item.reference || '000000'}</td>
            <td>${item.name}</td>
            <td style="text-align: center;">UN</td>
            <td style="text-align: center;">${item.quantity}</td>
            <td style="text-align: right;">${formatCurrency(item.price)}</td>
        </tr>
    `).join('');

    const now = new Date();

    const saleOrderHtml = `
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; color: #000; font-size: 11px; }
                .header-table { width: 100%; border-bottom: 2px solid #000; margin-bottom: 5px; }
                .company-name { font-size: 18px; font-weight: bold; }
                
                .info-section { width: 100%; border-bottom: 1px solid #000; margin-bottom: 10px; padding: 5px 0; }
                .info-row { display: flex; justify-content: space-between; margin-bottom: 4px; }
                
                .title-bar { 
                    display: flex; justify-content: space-between; align-items: center;
                    border-bottom: 1px solid #000; padding: 5px 0; font-weight: bold; font-size: 14px;
                }

                table.items-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                table.items-table th { border-bottom: 1px solid #000; text-align: left; padding: 5px; }
                table.items-table td { padding: 5px; }

                .footer { margin-top: 30px; border-top: 1px solid #000; padding-top: 10px; }
                .footer-container { display: flex; justify-content: space-between; }
                .totals-box { width: 250px; }
                .total-row { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 3px; }
                
                .signature { margin-top: 20px; text-align: right; }
                
                @media print {
                    @page {
                        margin: 0; /* Remove margens do navegador */
                    }
                    body {
                        margin: 0.5cm; /* Margem mínima para não cortar o texto */
                    }
                    .no-print {
                        display: none;
                    }
                }
            </style>
        </head>
        <body>
            <table class="header-table">
                <tr>
                    <td width="10%"><img src="/static/global/images/logo.ico" alt="Logo" width="60"></td>
                    <td width="60%">
                        <div class="company-name">ATACADINHO CRISTÃO</div>
                        <div>Rua São Sebastião - Centro - Belo Campo-BA 45160-000</div>
                    </td>
                    <td width="30%" style="text-align: right;">
                        (77) 98856-1490<br>
                        CNPJ 51.603.548/0001-67
                    </td>
                </tr>
            </table>

            <div class="title-bar">
                <span>VENDA #${saleDetails.id}</span>
                <span style="font-size: 11px;">Hora: ${now.toLocaleTimeString()} &nbsp; Data: ${now.toLocaleDateString()}</span>
            </div>

            <div class="info-section">
                <div class="info-row">
                    <span><strong>Cliente:</strong> ${saleDetails.client}</span>
                </div>
                <div class="info-row">
                    <span><strong>Endereço:</strong></span>
                    <span><strong>Cidade:</strong> BELO CAMPO</span>
                    <span><strong>UF:</strong></span>
                </div>
            </div>

            <table class="items-table">
                <thead>
                    <tr>
                        <th>Referencia</th>
                        <th>Descrição do Item</th>
                        <th style="text-align: center;">uni</th>
                        <th style="text-align: center;">Quantia</th>
                        <th style="text-align: right;">Valor Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${itemsHtml}
                </tbody>
            </table>

            <div class="footer">
                <div class="footer-container">
                    <div class="details">
                        <p><strong>Vendedor:</strong> ${saleDetails.seller}</p>
                        <p><strong>Situação Atual:</strong> Entrega direta para o cliente</p>
                    </div>
                    <div class="totals-box">
                        <div class="total-row"><span>VALOR PRODUTOS:</span> <span>${formatCurrency(saleDetails.subtotal || 0)}</span></div>
                        <div class="total-row"><span>FRETE:</span> <span>${formatCurrency(saleDetails.freight || 0)}</span></div>
                        <div class="total-row"><span>VALOR DESCONTO:</span> <span>${formatCurrency(saleDetails.discount || 0)}</span></div>
                        <div class="total-row" style="font-size: 14px; border-top: 1px solid #000; padding-top: 5px;">
                            <span>VALOR TOTAL:</span> <span>${formatCurrency(saleDetails.total)}</span>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 20px;">GRATO PELA PREFERÊNCIA</div>
                <div class="signature">
                    Visto _________________________________________________
                </div>
            </div>
        </body>
        </html>
    `;

    const win = window.open('', '', 'width=900,height=600');
    win.document.write(saleOrderHtml);
    win.document.close();
    // Aguarda carregar imagens (logo) antes de imprimir
    win.onload = () => {
        win.print();
        win.close();
    };
};

confirmPaymentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const cashReceived = parseFloat(cashReceivedInput.value) || 0;
    console.log(cashReceived);
    const paymentMethod = document.getElementById('payment-method');
    paymentMethod.value = selectedPaymentMethod;
    const valueReceived = document.getElementById('value-received');
    console.log(valueReceived);
    valueReceived.value = cashReceived;

    confirmPaymentForm.submit();
});

printBtn.addEventListener('click', () => {
    const saleId = document.getElementById('id-sale').value;
    const client = document.getElementById('client-input').value;
    const seller = document.getElementById('seller').value;
    const items = document.querySelectorAll('.cart-item');
    const cartItems = [];
    items.forEach(item => {
        const name = item.querySelector('.item-name').innerText;
        const price = parseFloat(item.querySelector('.item-price').innerText.replace('R$', '').replace(',', '.'));
        const quantity = item.querySelector('.item-quantity-value').innerText;
        cartItems.push({ name, price, quantity });
    });
    const subtotal = parseFloat(document.getElementById('subtotal').innerText.replace('R$', '').replace(',', '.'));
    const discount = parseFloat(document.getElementById('discount-input').value) || 0;
    const freight = parseFloat(document.getElementById('frete-input').value) || 0;
    const total = subtotal - discount + freight;
    const saleDetails = {
        id: saleId,
        client: client,
        seller: seller,
        cart: cartItems,
        subtotal: subtotal,
        discount: discount,
        freight: freight,
        total: total,
    }; 

    generateSaleOrder(saleDetails);
});
