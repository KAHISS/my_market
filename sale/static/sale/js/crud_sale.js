import { showPopup } from '/static/global/js/show_message.js';

// load django configs
const djangoConfig = document.getElementById('django-cfg').textContent;
const config = JSON.parse(djangoConfig);
const { csrf_token, urls } = config;
const { createSale, updateSale, deleteSale } = urls;


