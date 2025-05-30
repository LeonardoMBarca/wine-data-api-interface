const linhasOriginal = window.dadosComercio;
const colunas = window.colunasComercio;

const filtros = {
    ano: document.getElementById('filtro-ano'),
    categoria: document.getElementById('filtro-categoria'),
    subcategoria: document.getElementById('filtro-subcategoria'),
    tipo_estilo: document.getElementById('filtro-tipo'),
    processamento: document.getElementById('filtro-processamento')
};

let graficoBarras = null;
let graficoPizza = null;

function aplicarFiltros() {
    const linhasFiltradas = linhasOriginal.filter(linha => {
        return (!filtros.ano.value || linha.ano == filtros.ano.value) &&
               (!filtros.categoria.value || linha.categoria == filtros.categoria.value) &&
               (!filtros.subcategoria.value || linha.subcategoria == filtros.subcategoria.value) &&
               (!filtros.tipo_estilo.value || linha.tipo_estilo == filtros.tipo_estilo.value) &&
               (!filtros.processamento.value || linha.processamento == filtros.processamento.value);
    });

    renderizarTabela(linhasFiltradas);
    atualizarResumo(linhasFiltradas);
    atualizarGraficos(linhasFiltradas);
}

function renderizarTabela(dados) {
    const corpo = document.querySelector('tbody');
    corpo.innerHTML = '';

    for (const linha of dados) {
        const tr = document.createElement('tr');
        for (const coluna of colunas) {
            const td = document.createElement('td');
            td.textContent = linha[coluna];
            tr.appendChild(td);
        }
        corpo.appendChild(tr);
    }
}

function atualizarResumo(dados) {
    const totalLitros = dados.reduce((soma, linha) => soma + parseFloat(linha.litros || 0), 0);
    document.getElementById('total-litros').textContent = totalLitros.toLocaleString('pt-BR', { minimumFractionDigits: 2 });
    document.getElementById('total-registros').textContent = dados.length;
}

function atualizarGraficos(dados) {
    if (graficoBarras) graficoBarras.destroy();
    if (graficoPizza) graficoPizza.destroy();

    // Agrupar litros por subcategoria
    const litrosPorSub = {};
    for (const linha of dados) {
        const chave = linha.subcategoria || 'Indefinido';
        litrosPorSub[chave] = (litrosPorSub[chave] || 0) + parseFloat(linha.litros || 0);
    }

    // Gráfico de barras
    const barrasCtx = document.getElementById('grafico-barras').getContext('2d');
    graficoBarras = new Chart(barrasCtx, {
        type: 'bar',
        data: {
            labels: Object.keys(litrosPorSub),
            datasets: [{
                label: 'Litros por Subcategoria',
                data: Object.values(litrosPorSub),
                backgroundColor: 'rgba(54, 162, 235, 0.7)'
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });

    const porEstilo = {};
    for (const linha of dados) {
        const chave = linha.tipo_estilo || 'Indefinido';
        porEstilo[chave] = (porEstilo[chave] || 0) + parseFloat(linha.litros || 0);
    }

    const pizzaCtx = document.getElementById('grafico-pizza').getContext('2d');
    graficoPizza = new Chart(pizzaCtx, {
        type: 'pie',
        data: {
            labels: Object.keys(porEstilo),
            datasets: [{
                data: Object.values(porEstilo),
                backgroundColor: ['#e74c3c', '#3498db', '#2ecc71', '#f1c40f', '#9b59b6']
            }]
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    for (const f in filtros) {
        filtros[f].addEventListener('change', aplicarFiltros);
    }
    aplicarFiltros();
});