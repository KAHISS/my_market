const djangoConfig = document.getElementById('django-config').textContent;
const config = JSON.parse(djangoConfig);

const { csrf_token, urls } = config;

console.log(csrf_token)
console.log(urls)

let products = null;
const getList = async (url) => {
    const response = await fetch(url);
    const data = await response.json();
    console.log(data.products[49].stock)
}

getList(urls.product_list);
