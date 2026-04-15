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

// Seletores dos botões de impressão (Adicione o botão de cupom no seu HTML)
const printPdfBtn = document.getElementById('print-btn'); 
const printCupomBtn = document.getElementById('print-btn-cupom'); 

// --- Variáveis Globais ---
let selectedPaymentMethod = null;

// --- Helper: Formatar Moeda ---
const formatCurrency = (value) => {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

// ==========================================
// 1. LÓGICA DO MODAL DE PAGAMENTO
// ==========================================

if (paymentBtn) {
    paymentBtn.addEventListener('click', () => {
        const currentTotal = document.getElementById('total').innerText;
        modalTotalAmount.textContent = formatCurrency(currentTotal);
        paymentModal.style.display = 'block';
    });
}

closePaymentModalBtn.addEventListener('click', () => {
    paymentModal.style.display = 'none';
    resetPaymentUI();
});

window.addEventListener('click', (e) => {
    if (e.target === paymentModal) {
        paymentModal.style.display = 'none';
        resetPaymentUI();
    }
});

paymentMethodButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        paymentMethodButtons.forEach(btn => btn.classList.remove('selected'));
        e.target.classList.add('selected');
        selectedPaymentMethod = e.target.dataset.method;
        
        if (selectedPaymentMethod === 'dinheiro') {
            cashPaymentDetails.classList.remove('hidden');
            confirmPaymentBtn.disabled = true; 
            cashReceivedInput.focus();
        } else {
            cashPaymentDetails.classList.add('hidden');
            confirmPaymentBtn.disabled = false; 
        }
    });
});

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

const resetPaymentUI = () => {
    paymentMethodButtons.forEach(btn => btn.classList.remove('selected'));
    cashPaymentDetails.classList.add('hidden');
    cashReceivedInput.value = '';
    changeAmountEl.textContent = formatCurrency(0);
    confirmPaymentBtn.disabled = true;
    selectedPaymentMethod = null;
};

confirmPaymentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const cashReceived = parseFloat(cashReceivedInput.value) || 0;
    const paymentMethod = document.getElementById('payment-method');
    paymentMethod.value = selectedPaymentMethod;
    const valueReceived = document.getElementById('value-received');
    valueReceived.value = cashReceived;
    confirmPaymentForm.submit();
});


// ==========================================
// 2. FUNÇÃO AUXILIAR: IMPRESSÃO DIRETA (À prova de bugs no Mobile)
// ==========================================
const printHtmlContent = (htmlContent) => {
    // 1. Encontra ou cria a div invisível para a impressão
    let printContainer = document.getElementById('print-container');
    if (!printContainer) {
        printContainer = document.createElement('div');
        printContainer.id = 'print-container';
        document.body.appendChild(printContainer);
    }

    // 2. Atualiza o conteúdo (Pode ser o Cupom Térmico ou o PDF A4)
    printContainer.innerHTML = htmlContent;

    // 3. Aplica um CSS global permanente que gerencia as telas
    let printStyle = document.getElementById('print-style-temp');
    if (!printStyle) {
        printStyle = document.createElement('style');
        printStyle.id = 'print-style-temp';
        printStyle.innerHTML = `
            /* Quando estiver na TELA NORMAL do caixa: esconde o cupom */
            @media screen {
                #print-container { 
                    display: none !important; 
                }
            }
            
            /* Quando abrir a TELA DE IMPRESSÃO: esconde o PDV e mostra só o cupom */
            @media print {
                /* Esconde tudo que está no body, exceto o nosso container */
                body > *:not(#print-container) { 
                    display: none !important; 
                }
                #print-container { 
                    display: block !important; 
                }
                body { 
                    background: white !important; 
                    margin: 0 !important; 
                    padding: 0 !important; 
                }
            }
        `;
        document.head.appendChild(printStyle);
    }

    // 4. Dá 300ms de "respiro" para o celular renderizar as fontes e imagens e chama a impressão
    setTimeout(() => {
        window.print();
        // REMOVIDO: Não fazemos mais "cleanUp" (limpeza). 
        // O @media screen garante que o cupom fique invisível no sistema, 
        // evitando os bugs de tela branca nos celulares!
    }, 300);
};

// ==========================================
// 3. EXTRAÇÃO DOS DADOS DA TELA
// ==========================================
const getSaleDetailsFromDOM = () => {
    const saleId = document.getElementById('id-sale').value;
    const client = document.getElementById('client-input').value;
    const seller = document.getElementById('seller').value;
    
    const items = document.querySelectorAll('.cart-item');
    const cartItems = [];
    
    items.forEach(item => {
        const name = item.querySelector('.item-name').innerText;
        const price = parseFloat(item.querySelector('.item-price').innerText.replace('R$', '').replace(',', '.')) || 0;
        const quantity = parseFloat(item.querySelector('.item-quantity-value').value) || 1;
        
        const totalItem = price * quantity; 
        
        cartItems.push({ name, price, quantity, totalItem });
    });
    
    const subtotal = parseFloat(document.getElementById('subtotal').innerText.replace('R$', '').replace(',', '.')) || 0;
    const discount = parseFloat(document.getElementById('discount-input').value) || 0;
    const freight = parseFloat(document.getElementById('frete-input').value) || 0;
    const total = subtotal - discount + freight;
    
    return {
        id: saleId,
        client: client,
        seller: seller,
        cart: cartItems,
        subtotal: subtotal,
        discount: discount,
        freight: freight,
        total: total,
    };
};

// ==========================================
// 4. GERADOR DE PDF (A4)
// ==========================================
const generateSaleOrderPDF = (saleDetails) => {
    const itemsHtml = saleDetails.cart.map(item => `
        <tr>
            <td>000000</td>
            <td>${item.name}</td>
            <td style="text-align: center;">UN</td>
            <td style="text-align: center;">${item.quantity}</td>
            <td style="text-align: right;">${formatCurrency(item.totalItem)}</td>
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
                .title-bar { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #000; padding: 5px 0; font-weight: bold; font-size: 14px; }
                table.items-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
                table.items-table th { border-bottom: 1px solid #000; text-align: left; padding: 5px; }
                table.items-table td { padding: 5px; }
                .footer { margin-top: 30px; border-top: 1px solid #000; padding-top: 10px; }
                .footer-container { display: flex; justify-content: space-between; }
                .totals-box { width: 250px; }
                .total-row { display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 3px; }
                .signature { margin-top: 20px; text-align: right; }
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
                    <td width="30%" style="text-align: right;">(77) 98856-1490<br>CNPJ 51.603.548/0001-67</td>
                </tr>
            </table>

            <div class="title-bar">
                <span>VENDA #${saleDetails.id}</span>
                <span style="font-size: 11px;">Hora: ${now.toLocaleTimeString()} &nbsp; Data: ${now.toLocaleDateString()}</span>
            </div>

            <div class="info-section">
                <div class="info-row"><span><strong>Cliente:</strong> ${saleDetails.client}</span></div>
                <div class="info-row"><span><strong>Endereço:</strong></span><span><strong>Cidade:</strong> BELO CAMPO</span><span><strong>UF:</strong></span></div>
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
                        <div class="total-row"><span>VALOR PRODUTOS:</span> <span>${formatCurrency(saleDetails.subtotal)}</span></div>
                        <div class="total-row"><span>FRETE:</span> <span>${formatCurrency(saleDetails.freight)}</span></div>
                        <div class="total-row"><span>VALOR DESCONTO:</span> <span>${formatCurrency(saleDetails.discount)}</span></div>
                        <div class="total-row" style="font-size: 14px; border-top: 1px solid #000; padding-top: 5px;">
                            <span>VALOR TOTAL:</span> <span>${formatCurrency(saleDetails.total)}</span>
                        </div>
                    </div>
                </div>
                <div style="margin-top: 20px;">GRATO PELA PREFERÊNCIA</div>
                <div class="signature">Visto _________________________________________________</div>
            </div>
        </body>
        </html>
    `;

    // Usa a nova função de impressão via CSS
    printHtmlContent(saleOrderHtml);
};

// ==========================================
// 5. GERADOR DE CUPOM (Bobina 80mm) - FONTE MAIOR
// ==========================================
const generateSaleOrderCupom = (saleDetails) => {
    const itemsHtml = saleDetails.cart.map(item => `
        <tr>
            <td class="col-desc">${item.name}</td>
            <td class="col-qtd">${item.quantity}x</td>
            <td class="col-total">${formatCurrency(item.totalItem)}</td>
        </tr>
    `).join('');

    const now = new Date();

    const saleOrderHtml = `
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <style>
                @page { margin: 0; }
                /* AUMENTADO: font-size base de 12px para 15px */
                body { font-family: 'Courier New', Courier, monospace; width: 80mm; margin: 0 auto; padding: 4mm; color: #000; font-size: 40px; line-height: 1.4; }
                
                .text-center { text-align: center; }
                .text-right { text-align: right; }
                .bold { font-weight: bold; }
                .dashed-line { border-bottom: 1px dashed #000; margin: 8px 0; }
                .logo { max-width: 55px; margin-bottom: 4px; } /* Aumentei um pouco a logo também */
                
                /* AUMENTADO: Nome da empresa de 15px para 20px */
                .company-name { font-size: 20px; font-weight: bold; }
                
                /* AUMENTADO: Informações gerais de 11px para 14px */
                .header-info { font-size: 14px; }
                
                /* AUMENTADO: Tabela de itens de 11px para 14px */
                table.items-table { width: 100%; border-collapse: collapse; margin-top: 5px; font-size: 14px; }
                table.items-table th { border-bottom: 1px dashed #000; padding-bottom: 5px; text-align: left; }
                table.items-table td { padding: 4px 0; vertical-align: top; }
                
                /* Ajuste nas larguras das colunas para os textos maiores caberem melhor */
                .col-desc { width: 50%; }
                .col-qtd { width: 20%; text-align: center; }
                .col-total { width: 30%; text-align: right; }
                
                .totals-container { margin-top: 8px; }
                
                /* AUMENTADO: Linhas de total de 11px para 14px */
                .total-row { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 14px; }
                
                /* AUMENTADO: Destaque do TOTAL de 14px para 18px */
                .total-row.destaque { font-size: 18px; font-weight: bold; border-top: 1px dashed #000; padding-top: 6px; margin-top: 4px;}
            </style>
        </head>
        <body>
            <div class="text-center">
                <img src="/static/global/images/logo.ico" alt="Logo" class="logo"><br>
                <span class="company-name">ATACADINHO CRISTÃO</span><br>
                <span class="header-info">(77) 98856-1490<br>CNPJ: 51.603.548/0001-67</span>
            </div>
            
            <div class="dashed-line"></div>
            
            <div>
                <span class="bold" style="font-size: 16px;">VENDA #${saleDetails.id}</span><br>
                <span class="header-info">Data: ${now.toLocaleDateString()} Hora: ${now.toLocaleTimeString()}</span><br>
                <span class="header-info">Vendedor: ${saleDetails.seller}</span>
            </div>
            
            <div class="dashed-line"></div>
            
            <table class="items-table">
                <thead><tr><th class="col-desc">DESCRIÇÃO</th><th class="col-qtd">QTD</th><th class="col-total">TOTAL</th></tr></thead>
                <tbody>${itemsHtml}</tbody>
            </table>
            
            <div class="dashed-line"></div>
            
            <div class="totals-container">
                <div class="total-row"><span>SUBTOTAL:</span><span>${formatCurrency(saleDetails.subtotal)}</span></div>
                <div class="total-row"><span>FRETE:</span><span>${formatCurrency(saleDetails.freight)}</span></div>
                <div class="total-row"><span>DESCONTO:</span><span>${formatCurrency(saleDetails.discount)}</span></div>
                <div class="total-row destaque"><span>TOTAL PAGO:</span><span>${formatCurrency(saleDetails.total)}</span></div>
            </div>
            
            <div class="dashed-line"></div>
            
            <div class="text-center header-info" style="margin-top: 15px;">
                Situação: Entrega direta para o cliente<br><br>GRATO PELA PREFERÊNCIA
            </div>
        </body>
        </html>
    `;

    // Usa a função de impressão via CSS
    printHtmlContent(saleOrderHtml);
};

// ==========================================
// 6. EVENTOS DE CLIQUE DOS BOTÕES DE IMPRESSÃO
// ==========================================

// Imprimir em A4 (Seu botão original)
if (printPdfBtn) {
    printPdfBtn.addEventListener('click', () => {
        const saleDetails = getSaleDetailsFromDOM();
        generateSaleOrderPDF(saleDetails);
    });
}

// Imprimir em Bobina Térmica (Seu novo botão)
if (printCupomBtn) {
    printCupomBtn.addEventListener('click', () => {
        const saleDetails = getSaleDetailsFromDOM();
        generateSaleOrderCupom(saleDetails);
    });
}