import { showPopup } from '/static/global/js/show_message.js';

// load django configs
const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
console.log(config.urls);

// separate urls and csrf_token
const { csrf_token, urls } = config;
const { createSale, updateSale, deleteSale, script_message } = urls;

// getting elements
const formAddItem = document.getElementById('add-item-form');
const idSale = document.getElementById('id-sale').value;

const updateSaleList = (product, created) => {
    const saleList = document.getElementById('cart-items');
    if (created) {
        saleList.innerHTML = `
        <li class="cart-item" data-id="7891000000010">
            <span class="item-name">Refrigerante Cola 2L</span>
            <div class="item-quantity">
                <button class="quantity-btn decrease" data-id="7891000000010">-</button>
                <input type="number" class="quantity-input" value="1" min="1" data-id="7891000000010">
                <button class="quantity-btn increase" data-id="7891000000010">+</button>
            </div>
            <span class="item-price">R$&nbsp;8,50</span>
            <button class="remove-btn" data-id="7891000000010">×</button>
        </li>
        `
    } else {
        saleList.innerHTML = '';
    }
}
const addItemToCart = async (url, barcode, quantity, actionElement = null) => {
    
    if (actionElement) {
        actionElement.disabled = true;
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ barcode: barcode, quantity: quantity, sale_id: idSale })
        });

        const data = await response.json();

        if (data.success) {
            showPopup(data.message, 'success');
            updateSaleList(data.product, data.created);
        } else {
            showPopup(data.message, 'error');
        }

        return data;
    } catch (error) {
        showPopup('Ocorreu um erro ao adicionar ao carrinho. Tente novamente.', 'error');
    } finally {
        if (actionElement) {
            actionElement.disabled = false;
        }
    }
}

// event listeners
formAddItem.addEventListener('submit', async (event) => {
    event.preventDefault();

    const barcodeInput = document.getElementById('barcode-input');
    const url = formAddItem.action; // Pega a URL direto do atributo action do form
    const quantity = document.getElementById('quantity').value || 1;

    if (barcodeInput) {
        addItemToCart(url, barcodeInput.value, quantity, barcodeInput);
    }
});
