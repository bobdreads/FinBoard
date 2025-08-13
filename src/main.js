import * as echarts from 'echarts';

console.log("JavaScript do FinBoard carregado com sucesso! 🚀");

// Esta função ficará disponível globalmente para ser chamada pelo template
window.renderEquityChart = function() {
    const chartDom = document.getElementById('equity-chart');
    const chartDataEl = document.getElementById('chart-data-json');

    // Se o contêiner do gráfico ou os dados não existirem na página, não faz nada.
    if (!chartDom || !chartDataEl) {
        return;
    }

    const chartData = JSON.parse(chartDataEl.textContent);

    const myChart = echarts.init(chartDom);

    let titleText = 'Curva de Resultado Total Acumulado (em BRL)';
    if (chartData.dates.length === 0) {
        titleText = 'Curva de Resultado Total Acumulado (Sem operações fechadas para exibir)';
    }

    const option = {
        title: { text: titleText, left: 'center', textStyle: { color: '#e5e7eb' } },
        tooltip: { trigger: 'axis', backgroundColor: 'rgba(31, 41, 55, 0.8)', borderColor: '#4b5563', textStyle: { color: '#d1d5db' } },
        xAxis: { type: 'category', data: chartData.dates, axisLine: { lineStyle: { color: '#6b7280' } } },
        yAxis: { type: 'value', axisLine: { lineStyle: { color: '#6b7280' } }, splitLine: { lineStyle: { color: '#374151' } } },
        series: [{
            name: 'Patrimônio',
            data: chartData.values,
            type: 'line',
            smooth: true,
            showSymbol: chartData.values.length < 50,
            itemStyle: { color: '#818cf8' },
            lineStyle: { color: '#6366f1', width: 2 }
        }],
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        backgroundColor: 'rgba(0,0,0,0)'
    };

    myChart.setOption(option);
    window.addEventListener('resize', () => myChart.resize());
}




