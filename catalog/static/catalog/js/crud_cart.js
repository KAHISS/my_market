const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
const { csrf_token, urls } = config;

const addItemToCart = async (url, id, quantity) => {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ productId: id, quantity: quantity })
    });

    const data = await response.json();

    import(urls.script_message).then((module) => {
        if (data.success) {
            module.showPopup(data.message, 'success');
        } else {
            module.showPopup(data.message, 'error');
        }
    });
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
        e.preventDefault();
        const quantity = parseInt(document.getElementById('quantity').value);
        const productId = parseInt(singleButton.id); 
        addItemToCart(urls.add_to_cart, productId, quantity);
    });
}