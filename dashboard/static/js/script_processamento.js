document.addEventListener("DOMContentLoaded", function () {
    const dados = window.dadosProcessamento || [];
    const colunas = window.colunasProcessamento || [];

    const filtros = {
        ano: document.getElementById("filtro-ano"),
        categoria: document.getElementById("filtro-categoria"),
        subcategoria: document.getElementById("filtro-subcategoria"),
        tipo_estilo: document.getElementById("filtro-tipo_estilo"),
        origem: document.getElementById("filtro-origem"),
        classificacao: document.getElementById("filtro-classificacao")
    };

    const tabelaBody = document.querySelector("table tbody");
    const spanTotalKg = document.getElementById("total-kilogramas");
    const spanTotalRegistros = document.getElementById("total-registros");

    const graficoBarrasCtx = document.getElementById("grafico-barras").getContext("2d");
    const graficoPizzaCtx = document.getElementById("grafico-pizza").getContext("2d");
    let graficoBarras, graficoPizza;

    Object.values(filtros).forEach(filtro => {
        filtro.addEventListener("change", atualizarDashboard);
    });

    function atualizarDashboard() {
        const dadosFiltrados = dados.filter(item => {
            return (!filtros.ano.value || item.ano == filtros.ano.value) &&
                   (!filtros.categoria.value || item.categoria == filtros.categoria.value) &&
                   (!filtros.subcategoria.value || item.subcategoria == filtros.subcategoria.value) &&
                   (!filtros.tipo_estilo.value || item.tipo_estilo == filtros.tipo_estilo.value) &&
                   (!filtros.origem.value || item.origem == filtros.origem.value) &&
                   (!filtros.classificacao.value || item.classificacao == filtros.classificacao.value);
        });

        atualizarTabela(dadosFiltrados);
        atualizarResumo(dadosFiltrados);
        atualizarGraficos(dadosFiltrados);
    }

    function atualizarTabela(dadosFiltrados) {
        tabelaBody.innerHTML = "";

        dadosFiltrados.forEach(item => {
            const linha = document.createElement("tr");
            colunas.forEach(col => {
                const celula = document.createElement("td");
                celula.textContent = item[col] || "";
                linha.appendChild(celula);
            });
            tabelaBody.appendChild(linha);
        });
    }

    function atualizarResumo(dadosFiltrados) {
        const totalKg = dadosFiltrados.reduce((soma, item) => {
            const kg = parseFloat(item.kilogram) || 0;
            return soma + kg;
        }, 0);

        spanTotalKg.textContent = totalKg.toLocaleString("pt-BR", { maximumFractionDigits: 2 });
        spanTotalRegistros.textContent = dadosFiltrados.length;
    }

    function atualizarGraficos(dadosFiltrados) {
        const categorias = {};
        dadosFiltrados.forEach(item => {
            const cat = item.categoria || "Não Informado";
            const kg = parseFloat(item.kilogram) || 0;
            categorias[cat] = (categorias[cat] || 0) + kg;
        });

        const labels = Object.keys(categorias);
        const valores = Object.values(categorias);

        if (graficoBarras) graficoBarras.destroy();
        if (graficoPizza) graficoPizza.destroy();

        graficoBarras = new Chart(graficoBarrasCtx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Kg por Categoria",
                    data: valores,
                    backgroundColor: "#ff7043"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Distribuição por Categoria (Kg)"
                    }
                }
            }
        });

        graficoPizza = new Chart(graficoPizzaCtx, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: labels.map(() => gerarCorAleatoria())
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: "Participação por Categoria (Kg)"
                    }
                }
            }
        });
    }

    function gerarCorAleatoria() {
        const r = Math.floor(Math.random() * 200);
        const g = Math.floor(Math.random() * 200);
        const b = Math.floor(Math.random() * 200);
        return `rgb(${r}, ${g}, ${b})`;
    }

    atualizarDashboard();
});