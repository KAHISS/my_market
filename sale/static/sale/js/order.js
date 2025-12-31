const printOrderBtn = document.getElementById('print-order');

const generateSaleOrder = (saleDetails) => {
    // Gera as linhas da tabela de itens
    const itemsHtml = saleDetails.cart.map(item => `
        <tr>
            <td>${item.reference || '000000'}</td>
            <td>${item.name}</td>
            <td style="text-align: center;">R$ ${item.price}</td>
            <td style="text-align: center;">${item.quantity}</td>
            <td style="text-align: center;">${item.subtotal}</td>
            <td style="text-align: right;">R$ ${item.discount}</td>
            <td style="text-align: right;">${item.total}</td>
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
                <span>PEDIDO #${saleDetails.id}</span>
                <span style="font-size: 11px;">Hora: ${now.toLocaleTimeString()} &nbsp; Data: ${now.toLocaleDateString()}</span>
            </div>

            <div class="info-section">
                <div class="info-row">
                    <span><strong>Cliente:</strong> ${saleDetails.client}</span>
                </div>
                <div class="info-row">
                    <span><strong>Endereço:</strong></span>
                    <span><strong>Cidade:</strong></span>
                    <span><strong>UF:</strong></span>
                </div>
            </div>

            <table class="items-table">
                <thead>
                    <tr>
                        <th>Referencia</th>
                        <th>Descrição do Item</th>
                        <th style="text-align: right;">Preço</th>
                        <th style="text-align: right;">Quantidade</th>
                        <th style="text-align: center;">Subtotal</th>
                        <th style="text-align: right;">Desconto</th>
                        <th style="text-align: right;">Total</th>
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
                        <div class="total-row"><span>VALOR PRODUTOS:</span> <span>${saleDetails.subtotal}</span></div>
                        <div class="total-row"><span>VALOR DESCONTO:</span> <span>${saleDetails.discount}</span></div>
                        <div class="total-row" style="font-size: 14px; border-top: 1px solid #000; padding-top: 5px;">
                            <span>VALOR TOTAL:</span> <span>${saleDetails.total}</span>
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

if (printOrderBtn) {
    printOrderBtn.addEventListener('click', () => {
        const orderId = document.getElementById('id-order').value;
        const client = document.getElementById('client').value;
        const seller = document.getElementById('seller').value;
        const items = document.querySelectorAll('.cart-item');
        const cartItems = [];
        items.forEach(item => {
            const name = item.querySelector('.item-title').innerText;
            const quantity = item.querySelector('.item-quantity').innerText;
            const price = item.querySelector('.item-sale-price').innerText;
            const subtotal = item.querySelector('.item-subtotal').innerText;
            const discount = item.querySelector('.item-discount').innerText;
            const total = item.querySelector('.item-total-price').innerText;
            cartItems.push({ name, price, quantity, subtotal, discount, total });
        });
        const total = document.querySelector('.subtotal').innerText;
        const discount = document.querySelector('.text-discount').innerText;
        const currentTotal = document.querySelector('.total').innerText;
        const saleDetails = {
            id: orderId,
            client: client,
            seller: seller,
            cart: cartItems,
            subtotal: total,
            discount: discount,
            total: currentTotal,
        }; 

        generateSaleOrder(saleDetails);
    });
}
