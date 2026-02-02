// --- Dados Mockados Iniciais ---
let expenses = [
];

// --- Mapeamentos ---
const MODALITY_MAP = { 'R': 'Varejo', 'W': 'Atacado' };
const STATUS_MAP = { 'P': 'Pendente', 'D': 'Pago', 'C': 'Cancelado' };

// --- Referências DOM ---
const tableBody = document.getElementById('expensesTableBody');
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');
const recordCount = document.getElementById('recordCount');

const modal = document.getElementById('expenseModal');
const expenseForm = document.getElementById('expenseForm');
const modalTitle = document.getElementById('modalTitle');

// --- Inicialização ---
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});

// --- Funções de Renderização ---
function renderTable() {
    const term = searchInput.value.toLowerCase();
    const status = statusFilter.value;

    // Filtra os dados
    const filtered = expenses.filter(exp => {
        const matchesText = exp.category.toLowerCase().includes(term) || 
                            (exp.observation && exp.observation.toLowerCase().includes(term));
        const matchesStatus = status === 'ALL' || exp.status === status;
        return matchesText && matchesStatus;
    });

    // Limpa tabela
    tableBody.innerHTML = '';

    if (filtered.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="6" class="px-6 py-12 text-center text-slate-400">
                    Nenhuma despesa encontrada.
                </td>
            </tr>`;
    } else {
        filtered.forEach(exp => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50 transition group border-b border-slate-50';
            tr.innerHTML = `
                <td class="px-6 py-4">
                    <div class="font-medium text-slate-900">${exp.category}</div>
                    ${exp.observation ? `<div class="text-xs text-slate-500 truncate max-w-[200px]">${exp.observation}</div>` : ''}
                </td>
                <td class="px-6 py-4 text-slate-600">${MODALITY_MAP[exp.modality]}</td>
                <td class="px-6 py-4 text-slate-600">
                    <div class="flex flex-col">
                        <span>${formatDate(exp.pay_by)}</span>
                        ${exp.payday ? `<span class="text-xs text-emerald-600">Pago: ${formatDate(exp.payday)}</span>` : ''}
                    </div>
                </td>
                <td class="px-6 py-4">${getStatusBadge(exp.status)}</td>
                <td class="px-6 py-4 text-right font-medium text-slate-900">${formatCurrency(exp.amount)}</td>
                <td class="px-6 py-4">
                    <div class="flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onclick="editExpense(${exp.id})" class="p-1.5 text-blue-600 hover:bg-blue-50 rounded-md transition" title="Editar">
                            <i data-lucide="edit-2" class="w-4 h-4"></i>
                        </button>
                        <button onclick="deleteExpense(${exp.id})" class="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition" title="Excluir">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </td>
            `;
            tableBody.appendChild(tr);
        });
    }

    // Atualiza contadores e ícones
    recordCount.textContent = `Mostrando ${filtered.length} registros`;
    lucide.createIcons();
}

function updateKPIs() {
    const total = expenses.reduce((acc, curr) => acc + curr.amount, 0);
    const paid = expenses.filter(e => e.status === 'D').reduce((acc, curr) => acc + curr.amount, 0);
    const pending = expenses.filter(e => e.status === 'P').reduce((acc, curr) => acc + curr.amount, 0);

    document.getElementById('kpi-total').textContent = formatCurrency(total);
    document.getElementById('kpi-paid').textContent = formatCurrency(paid);
    document.getElementById('kpi-pending').textContent = formatCurrency(pending);
}

// --- Helpers ---
function formatCurrency(val) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
}

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
}

function getStatusBadge(status) {
    const styles = {
        'P': 'bg-amber-100 text-amber-800 border-amber-200',
        'D': 'bg-emerald-100 text-emerald-800 border-emerald-200',
        'C': 'bg-slate-100 text-slate-600 border-slate-200 line-through'
    };
    return `<span class="px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles[status] || styles['P']}">${STATUS_MAP[status]}</span>`;
}

// --- Modal & Form Logic ---
const openModal = function() {
    modalTitle.textContent = 'Nova Despesa';
    expenseForm.reset();
    document.getElementById('expenseId').value = '';
    // Reset selects to defaults
    document.getElementById('id_modality').value = 'R';
    document.getElementById('id_status').value = 'P';
    document.getElementById('id_payment_method').value = 'C';
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

const closeModal = function() {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
}

const editExpense = function(id) {
    const exp = expenses.find(e => e.id === id);
    if (!exp) return;

    modalTitle.textContent = 'Editar Despesa';
    
    document.getElementById('expenseId').value = exp.id;
    document.getElementById('category').value = exp.category;
    document.getElementById('amount').value = exp.amount;
    document.getElementById('modality').value = exp.modality;
    document.getElementById('payment_method').value = exp.payment_method;
    document.getElementById('status').value = exp.status;
    document.getElementById('pay_by').value = exp.pay_by || '';
    document.getElementById('payday').value = exp.payday || '';
    document.getElementById('observation').value = exp.observation || '';

    modal.classList.remove('hidden');
    modal.classList.add('flex');
}

const deleteExpense = function(id) {
    if (confirm('Tem certeza que deseja excluir esta despesa?')) {
        expenses = expenses.filter(e => e.id !== id);
        renderTable();
        updateKPIs();
    }
}

// Fecha modal ao clicar fora
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});