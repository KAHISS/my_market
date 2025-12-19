import { showPopup } from '/static/global/js/show_message.js';

// load django configs
const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
console.log(config.urls);

const { csrf_token, urls } = config;
const { createSale, updateSale, deleteSale, script_message } = urls;

const updateSaleList = (product) => {
    const saleList = document.getElementById('cart-items');
    saleList.innerHTML = ```
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
    ```
}
const addItemToCart = async (url, barcode, quantity, buttonElement = null, form = null) => {
    
    if (buttonElement) {
        buttonElement.disabled = true;
    }

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ barcode: barcode, quantity: quantity, barcode: 'true' })
        });

        const data = await response.json();

        if (data.success) {
            showPopup(data.message, 'success');
            updateSaleList(data.product);
        } else {
            showPopup(data.message, 'error');
        }

        return data;
    } catch (error) {
        console.error(error);
        showPopup('Ocorreu um erro ao adicionar ao carrinho. Tente novamente.', 'error');
    } finally {
        if (buttonElement) {
            buttonElement.disabled = false;
        }
    }
}

