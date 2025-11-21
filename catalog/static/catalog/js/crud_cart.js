import { showPopup } from '/static/global/js/show_message.js';

const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
const { csrf_token, urls } = config;

const addItemToCart = async (url, id, quantity) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ productId: id, quantity: quantity })
        });

        const data = await response.json();

        if (data.success) {
            showPopup(data.message, 'success');
        } else {
            showPopup(data.message, 'error');
        }
    } catch (error) {
        showPopup('Verifique se você está logado, sua conexão com a internet e tente novamente.', 'error');
    }

}

const buttons = document.querySelectorAll('.add-to-cart-btn');
if (buttons.length > 0) {
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            const productId = parseInt(e.currentTarget.id);
            addItemToCart(urls.add_to_cart, productId, 1);
        });
    });
}

const singleButton = document.querySelector('button[name="product_id"]');
if (singleButton) {
    singleButton.addEventListener('click', (e) => {
        const quantity = parseInt(document.getElementById('quantity').value);
        const productId = parseInt(singleButton.id); 
        addItemToCart(urls.add_to_cart, productId, quantity);
    });
}

const quantityButtons = document.querySelectorAll('.quantity-btn');
if (quantityButtons.length > 0) {
    quantityButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const unit = parseInt(e.currentTarget.dataset.unit)
            const form = e.currentTarget.form.id;
            console.log(form, unit);
            addItemToCart(urls.add_to_cart, form, unit);
        });
    });
}
