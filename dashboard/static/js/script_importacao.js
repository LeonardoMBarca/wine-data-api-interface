document.addEventListener('DOMContentLoaded', () => {
    const dados = window.dadosImportacao;
    const colunas = window.colunasImportacao;

    const filtroAno = document.getElementById('filtro-ano');
    const filtroCategoria = document.getElementById('filtro-categoria');
    const filtroPais = document.getElementById('filtro-pais');

    const tabelaBody = document.querySelector('table tbody');
    const totalKgSpan = document.getElementById('total-kilograms');
    const totalDollarsSpan = document.getElementById('total-dollars');
    const totalRegistrosSpan = document.getElementById('total-registros');

    const ctxBarras = document.getElementById('grafico-barras').getContext('2d');
    const ctxPizza = document.getElementById('grafico-pizza').getContext('2d');

    let graficoBarras;
    let graficoPizza;

    function aplicarFiltros() {
        const ano = filtroAno.value;
        const categoria = filtroCategoria.value;
        const pais = filtroPais.value;

        return dados.filter(item => {
            return (!ano || item.ano == ano) &&
                   (!categoria || item.categoria == categoria) &&
                   (!pais || item.pais == pais);
        });
    }

    function atualizarTabela(dadosFiltrados) {
        tabelaBody.innerHTML = '';
        dadosFiltrados.forEach(item => {
            const tr = document.createElement('tr');
            colunas.forEach(col => {
                const td = document.createElement('td');
                td.textContent = item[col] || '';
                tr.appendChild(td);
            });
            tabelaBody.appendChild(tr);
        });
    }

    function atualizarTotais(dadosFiltrados) {
        let totalKg = 0;
        let totalDollars = 0;

        dadosFiltrados.forEach(item => {
            totalKg += parseFloat(item.kilograms) || 0;
            totalDollars += parseFloat(item.dollars) || 0;
        });

        totalKgSpan.textContent = totalKg.toLocaleString();
        totalDollarsSpan.textContent = totalDollars.toLocaleString('en-US', { minimumFractionDigits: 2 });
        totalRegistrosSpan.textContent = dadosFiltrados.length;
    }

    function atualizarGraficos(dadosFiltrados) {
        const porAno = {};
        const porCategoria = {};

        dadosFiltrados.forEach(item => {
            const ano = item.ano;
            const categoria = item.categoria;
            const kg = parseFloat(item.kilograms) || 0;

            porAno[ano] = (porAno[ano] || 0) + kg;
            porCategoria[categoria] = (porCategoria[categoria] || 0) + kg;
        });

        const anos = Object.keys(porAno);
        const valoresAno = Object.values(porAno);

        const categorias = Object.keys(porCategoria);
        const valoresCategoria = Object.values(porCategoria);

        if (graficoBarras) graficoBarras.destroy();
        if (graficoPizza) graficoPizza.destroy();

        graficoBarras = new Chart(ctxBarras, {
            type: 'bar',
            data: {
                labels: anos,
                datasets: [{
                    label: 'Kg importados por ano',
                    data: valoresAno,
                    backgroundColor: '#fbbc05'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: 'Importação por Ano (Kg)' }
                }
            }
        });

        graficoPizza = new Chart(ctxPizza, {
            type: 'pie',
            data: {
                labels: categorias,
                datasets: [{
                    label: 'Kg por categoria',
                    data: valoresCategoria,
                    backgroundColor: categorias.map((_, i) => `hsl(${i * 40 % 360}, 70%, 65%)`)
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Distribuição por Categoria (Kg)' }
                }
            }
        });
    }

    function atualizarTudo() {
        const dadosFiltrados = aplicarFiltros();
        atualizarTabela(dadosFiltrados);
        atualizarTotais(dadosFiltrados);
        atualizarGraficos(dadosFiltrados);
    }

    filtroAno.addEventListener('change', atualizarTudo);
    filtroCategoria.addEventListener('change', atualizarTudo);
    filtroPais.addEventListener('change', atualizarTudo);

    atualizarTudo();
});