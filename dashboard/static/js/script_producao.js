document.addEventListener("DOMContentLoaded", function () {
    const dados = window.dadosProducao || [];
    const colunas = window.colunasProducao || [];

    const filtros = {
        ano: document.getElementById("filtro-ano"),
        categoria: document.getElementById("filtro-categoria"),
        subcategoria: document.getElementById("filtro-subcategoria"),
        tipo_estilo: document.getElementById("filtro-tipo_estilo"),
        processamento: document.getElementById("filtro-processamento")
    };

    const tbody = document.querySelector("tbody");
    const totalLitrosSpan = document.getElementById("total-litros");
    const totalRegistrosSpan = document.getElementById("total-registros");

    const graficoBarras = new Chart(document.getElementById("grafico-barras"), {
        type: 'bar',
        data: { labels: [], datasets: [{ label: 'Litros', data: [], backgroundColor: '#9c27b0' }] },
        options: { responsive: true }
    });

    const graficoPizza = new Chart(document.getElementById("grafico-pizza"), {
        type: 'pie',
        data: { labels: [], datasets: [{ label: 'Litros', data: [], backgroundColor: [] }] },
        options: { responsive: true }
    });

    function aplicarFiltros() {
        return dados.filter(item => {
            return (!filtros.ano.value || item.ano == filtros.ano.value)
                && (!filtros.categoria.value || item.categoria == filtros.categoria.value)
                && (!filtros.subcategoria.value || item.subcategoria == filtros.subcategoria.value)
                && (!filtros.tipo_estilo.value || item.tipo_estilo == filtros.tipo_estilo.value)
                && (!filtros.processamento.value || item.processamento == filtros.processamento.value);
        });
    }

    function atualizarTabela(filtrados) {
        tbody.innerHTML = "";
        filtrados.forEach(item => {
            const tr = document.createElement("tr");
            colunas.forEach(coluna => {
                const td = document.createElement("td");
                td.textContent = item[coluna] || "";
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }

    function calcularResumo(filtrados) {
        const totalLitros = filtrados.reduce((soma, item) => {
            const valor = parseFloat(item.litros) || 0;
            return soma + valor;
        }, 0);

        totalLitrosSpan.textContent = totalLitros.toLocaleString("pt-BR", { minimumFractionDigits: 0 });
        totalRegistrosSpan.textContent = filtrados.length;
    }

    function atualizarGraficos(filtrados) {
        const porCategoria = {};
        filtrados.forEach(item => {
            const cat = item.categoria || "Não informado";
            const litros = parseFloat(item.litros) || 0;
            porCategoria[cat] = (porCategoria[cat] || 0) + litros;
        });

        const labels = Object.keys(porCategoria);
        const valores = Object.values(porCategoria);

        graficoBarras.data.labels = labels;
        graficoBarras.data.datasets[0].data = valores;
        graficoBarras.update();

        graficoPizza.data.labels = labels;
        graficoPizza.data.datasets[0].data = valores;
        graficoPizza.data.datasets[0].backgroundColor = labels.map(() => gerarCorAleatoria());
        graficoPizza.update();
    }

    function gerarCorAleatoria() {
        const r = Math.floor(Math.random() * 200);
        const g = Math.floor(Math.random() * 200);
        const b = Math.floor(Math.random() * 200);
        return `rgb(${r}, ${g}, ${b})`;
    }

    function atualizarDashboard() {
        const filtrados = aplicarFiltros();
        atualizarTabela(filtrados);
        calcularResumo(filtrados);
        atualizarGraficos(filtrados);
    }

    Object.values(filtros).forEach(select => {
        if (select) {
            select.addEventListener("change", atualizarDashboard);
        }
    });

    atualizarDashboard();
});
