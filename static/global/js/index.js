// Toggle sidebar
document.querySelector('.menu-toggle').addEventListener('click', function() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
    
    const mainContent = document.querySelector('.main-content');
    mainContent.classList.toggle('expanded');
});

// Modal functions
function openAddProductModal() {
    document.getElementById('addNewRegister').classList.remove('hidden');
}

function closeAddProductModal() {
    document.getElementById('addNewRegister').classList.add('hidden');
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('addNewRegister');
    if (event.target === modal) {
        closeAddProductModal();
    }
}