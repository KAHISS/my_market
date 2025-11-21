export function showPopup(message, type) {
    const popup = document.getElementById('popup');
    popup.innerText = message;
    popup.classList.add('show');
    popup.classList.add(type);

    setTimeout(() => {
        popup.classList.remove('show');
        popup.classList.remove(type);
    }, 3000); // 3 segundos
}