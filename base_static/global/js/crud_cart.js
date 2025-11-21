import { showPopup } from '/static/global/js/show_message.js';

const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
const { csrf_token, urls } = config;

// 1. Melhoria: Receber o botão para poder desabilitá-lo
const addItemToCart = async (url, id, quantity, buttonElement = null) => {
    
    // Bloqueia o botão para evitar clique duplo
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
            body: JSON.stringify({ productId: id, quantity: quantity })
        });
        console.log(response)

        const data = await response.json();

        if (data.success) {
            showPopup(data.message, 'success');
        } else {
            showPopup(data.message, 'error');
        }
    } catch (error) {
        console.error(error);
        showPopup('Ocorreu um erro ao adicionar ao carrinho. Tente novamente.', 'error');
    } finally {
        if (buttonElement) {
            buttonElement.disabled = false;
        }
    }
}

// --- EVENT LISTENERS ---

const buttons = document.querySelectorAll('.add-to-cart-btn');
if (buttons.length > 0) {
    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = parseInt(e.currentTarget.id);
            addItemToCart(urls.add_to_cart, productId, 1, e.currentTarget);
        });
    });
}

const singleButton = document.querySelector('button[name="product_id"]');
if (singleButton) {
    singleButton.addEventListener('click', (e) => {
        e.preventDefault();
        const quantityInput = document.getElementById('quantity');
        const quantity = parseInt(quantityInput.value);
        const productId = parseInt(singleButton.id); 
        
        if (quantity > 0) {
            addItemToCart(urls.add_to_cart, productId, quantity, singleButton);
        } else {
            showPopup('A quantidade deve ser maior que zero.', 'error');
        }
    });
}

// CORREÇÃO CRÍTICA DO TERCEIRO BLOCO
const quantityButtons = document.querySelectorAll('.quantity-btn.plus');
if (quantityButtons.length > 0) {
    quantityButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const unit = parseInt(e.currentTarget.dataset.unit);
            const productId = parseInt(e.currentTarget.parentNode.id);
            console.log(`Adicionando Produto: ${productId}, Qtd: ${unit}`);       
            if (productId) {
                addItemToCart(urls.add_to_cart, productId, unit, e.currentTarget);
            } else {
                console.error("ID do produto não encontrado no botão de quantidade");
            }
        });
    });
}