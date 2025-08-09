import * as echarts from 'echarts';

// A função antiga não é mais necessária
// window.renderEquityChart = function() { ... }

// NOVA FUNÇÃO para renderizar os gráficos do dashboard
window.renderDashboardCharts = function() {
    const dailyPlDom = document.getElementById('daily-pl-chart');
    const stackedAreaDom = document.getElementById('stacked-area-chart');

    const dailyPlDataEl = document.getElementById('daily-pl-json');
    const stackedAccountsDataEl = document.getElementById('stacked-accounts-json');

    if (!dailyPlDom || !stackedAreaDom || !dailyPlDataEl || !stackedAccountsDataEl) {
        return;
    }

    const dailyPlData = JSON.parse(dailyPlDataEl.textContent);
    const stackedAccountsData = JSON.parse(stackedAccountsDataEl.textContent);

    const dailyPlChart = echarts.init(dailyPlDom);
    const stackedAreaChart = echarts.init(stackedAreaDom);

    // --- Configuração do Gráfico de Colunas (Superior) ---
    const dailyPlOption = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: dailyPlData.dates },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#374151' } } },
        grid: { left: '3%', right: '4%', bottom: '20%', containLabel: true },
        backgroundColor: 'rgba(0,0,0,0)',
        dataZoom: [{
            type: 'inside',
            start: 0,
            end: 100
        }, {
            start: 0,
            end: 100,
            type: 'slider',
            bottom: 10,
            height: 20
        }],
        series: [{
            name: 'P/L Diário',
            type: 'bar',
            data: dailyPlData.values.map(val => ({
                value: val,
                itemStyle: { color: val >= 0 ? '#4ade80' : '#f87171' } // verde ou vermelho
            }))
        }]
    };

    // --- Configuração do Gráfico de Área Empilhado (Inferior) ---
    const stackedAreaOption = {
        tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
        legend: { data: stackedAccountsData.series.map(s => s.name), bottom: 0, textStyle: { color: '#d1d5db' } },
        grid: { left: '3%', right: '4%', top: '10%', bottom: '15%', containLabel: true },
        backgroundColor: 'rgba(0,0,0,0)',
        xAxis: { type: 'category', boundaryGap: false, data: stackedAccountsData.dates },
        yAxis: { type: 'value', splitLine: { lineStyle: { color: '#374151' } } },
        series: stackedAccountsData.series.map(s => ({
            name: s.name,
            type: 'line',
            stack: 'Total',
            areaStyle: {},
            emphasis: { focus: 'series' },
            data: s.data
        }))
    };

    dailyPlChart.setOption(dailyPlOption);
    stackedAreaChart.setOption(stackedAreaOption);

    // Conecta os dois gráficos para que o zoom de um afete o outro
    echarts.connect([dailyPlChart, stackedAreaChart]);

    window.addEventListener('resize', () => {
        dailyPlChart.resize();
        stackedAreaChart.resize();
    });
}

console.log("JavaScript do FinBoard carregado com sucesso! 🚀");