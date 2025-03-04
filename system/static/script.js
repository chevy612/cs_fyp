let chart;

async function search() {
    const keyword = document.getElementById('keyword').value;
    if (!keyword) return alert('Please enter a keyword');

    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    loader.style.display = 'block';
    results.style.display = 'none';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword })
        });
        const data = await response.json();

        loader.style.display = 'none';
        results.style.display = 'block';

        // Sentiment Bar
        const bar = document.getElementById('sentiment-bar');
        bar.innerHTML = `
            <div class="positive" style="width: ${data.percentages.positive}%">Positive: ${data.percentages.positive.toFixed(1)}%</div>
            <div class="neutral" style="width: ${data.percentages.neutral}%">Neutral: ${data.percentages.neutral.toFixed(1)}%</div>
            <div class="negative" style="width: ${data.percentages.negative}%">Negative: ${data.percentages.negative.toFixed(1)}%</div>
        `;

        // Overall Score with Classified Sentiment in parentheses
        document.getElementById('overall-score').textContent = `${data.overall_score.toFixed(1)} (${data.overall_classified})`;

        // Time Series Chart
        if (chart) chart.destroy();
        const ctx = document.getElementById('timeSeriesChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.time_series.dates,
                datasets: [{
                    label: 'Sentiment Score',
                    data: data.time_series.scores,
                    borderColor: '#1a73e8',
                    fill: false
                }]
            },
            options: { scales: { y: { min: -1, max: 1 } } }
        });
    } catch (error) {
        console.error('Error:', error);
        loader.style.display = 'none';
        alert('An error occurred while processing your request.');
    }
}