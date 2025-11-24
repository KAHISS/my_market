export function showPopup(message, type) {
    const popup = document.getElementById('popup');
    const p = document.createElement('p');
    p.innerText = message;
    popup.appendChild(p);
    p.classList.add('show');
    p.classList.add(type);

    setTimeout(() => {
        popup.removeChild(p);
    }, 2 * 1000);
}
