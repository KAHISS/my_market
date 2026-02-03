import { showPopup } from '/static/global/js/show_message.js';

// load django configs
const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);

// separate urls and csrf_token
const { csrf_token, urls } = config;
const { searchProduct, deleteSale } = urls;

// getting elements
const formAddItem = document.getElementById('add-item-form');
const formSummary = document.getElementById('summary-form');
const idSale = document.getElementById('id-sale').value;
const status = document.getElementById('status').value || 'pendente';

// functions
const addListeners = () => {
    // remove items
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            event.preventDefault();
            const item_id = event.target.getAttribute('data-id');
            const url = event.target.getAttribute('data-url');
            removeItemFromCart(url, item_id);
        });
    });

    // update quantity adding or removing
    document.querySelectorAll('.quantity-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            const barcode = event.target.getAttribute('data-barcode');
            const quantity = event.target.classList.contains('increase') ? 1 : -1;
            const url = formAddItem.action;
            addItemToCart(url, barcode, quantity, event.target);
        });
    });
}

const updateSaleList = (sale, item=null, created=false) => {
    // add or update item
    if (item && !item.remove) {
        const saleList = document.getElementById('cart-items');
        if (created) {
            const newItem = `
            <li class="cart-item" id="${item.id}">
                <span class="item-name">${item.name}</span>
                <div class="item-quantity">
                    <button class="quantity-btn decrease" data-barcode="${item.barcode}">-</button>
                    <input type="number" class="item-quantity-value" value="${item.quantity}" min="1" readonly>
                    <button class="quantity-btn increase" data-barcode="${item.barcode}">+</button>
                </div>
                <span class="item-price">R$&nbsp;${item.subtotal}</span>
                <button class="remove-btn" data-id="${item.id}" data-url="${item.url_remove}">×</button>
            </li>
            `

            saleList.insertAdjacentHTML('beforeend', newItem);
            
            addListeners();

            const no_itens = document.getElementById('no-items');
            if (no_itens) {
                no_itens.remove();
            }

        } else {
            const itemElement = document.getElementById(item.id);
            const quantityInput = itemElement.querySelector('.item-quantity-value');
            quantityInput.value = item.quantity;
            const priceInput = itemElement.querySelector('.item-price');
            priceInput.innerText = `R$ ${item.subtotal}`;
        } 
    } else if (item && item.remove) {
        document.getElementById(item.id).remove();
    }

    // update sale summary
    document.getElementById('client-input').value = sale.client;
    document.getElementById('subtotal').innerText = `R$ ${sale.subtotal}`;
    document.getElementById('total').innerText = `R$ ${sale.total_price}`;
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
            updateSaleList(data.sale, data.item, data.created);
            showPopup(data.message, 'success');
        } else {
            showPopup(data.message, 'error');
        }

        return data;
    } catch (error) {
        showPopup('Ocorreu um erro no carrinho. Tente novamente.', 'error');
        console.error(error);
    } finally {
        if (actionElement) {
            actionElement.disabled = false;
        }
    }
}

const updateSaleSummary = async (url, client, discount, freight, modality = null) => {

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ client: client, discount: discount, freight: freight, sale_id: idSale, modality: modality })
        });

        const data = await response.json();

        if (data.success) {
            showPopup(data.message, 'success');
            updateSaleList(data.sale);

        } else {
            showPopup(data.message, 'error');
        }

        return data;
    } catch (error) {
        showPopup('Ocorreu um erro ao atualizar o resumo da venda. Tente novamente.', 'error');
        console.log(error);
    }
}

const removeItemFromCart = async (url, item_id) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ item_id: item_id, sale_id: idSale })
        });

        const data = await response.json();

        if (data.success) {
            updateSaleList(data.sale, data.item);
            showPopup(data.message, 'success');
        } else {
            showPopup(data.message, 'error');
        }
        return data;
    } catch (error) {
        showPopup('Ocorreu um erro ao remover o item do carrinho. Tente novamente.', 'error');
    }
}

// event listeners
if (formAddItem) {
    formAddItem.addEventListener('submit', async (event) => {
        event.preventDefault();

        const barcodeInput = document.getElementById('barcode-input');
        const url = formAddItem.action; // Pega a URL direto do atributo action do form
        const quantity = document.getElementById('quantity').value || 1;

        if (barcodeInput) {
            await addItemToCart(url, barcodeInput.value, quantity, barcodeInput);
            barcodeInput.value = ''
            barcodeInput.focus();
        }
    });
}

formSummary.addEventListener('submit', async (event) => {
    event.preventDefault();

    const client = document.getElementById('client-input').value || 'consumidor';
    const discount = document.getElementById('discount-input').value || 0;
    const url = formSummary.action;
    const freight = document.getElementById('frete-input').value || 0;
    const modalitySelect = document.getElementById('sale-modality-select');

    if (status == 'pendente') {
        const data = await updateSaleSummary(url, client, discount, freight, status, modalitySelect.value);
        document.getElementById('discount-input').value = `${parseFloat(data.sale.discount)}`;
        document.getElementById('frete-input').value = `${parseFloat(data.sale.freight)}`;
    } else if (status == 'pago') {
        showPopup('A venda já está paga.', 'info');
    } else if (status == 'cancelado') {
        showPopup('A venda já foi cancelada.', 'info');
    }
});

document.getElementById('sale-modality-select').addEventListener('change', async (event) => {
    const modality = event.target.value;
    const client = document.getElementById('client-input').value || 'consumidor';
    const discount = document.getElementById('discount-input').value || 0;
    const url = formSummary.action;
    const freight = document.getElementById('frete-input').value || 0;

    if (status == 'pendente') {
        const data = await updateSaleSummary(url, client, discount, freight, modality);
    } else if (status == 'pago') {
        showPopup('A venda já está paga.', 'info');
    } else if (status == 'cancelado') {
        showPopup('A venda já foi cancelada.', 'info');
    }
});

addListeners();

document.querySelectorAll('.product-item').forEach(item => {
    item.addEventListener('click', () => {
        const barcode = item.getAttribute('data-barcode');
        addItemToCart(formAddItem.action, barcode, 1);
    });
})
