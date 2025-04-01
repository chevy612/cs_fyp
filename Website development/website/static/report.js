function showSentimentBar(sentimentScore) {
    // Create a container for the sentiment bar
    const sentimentBarContainer = document.createElement('div');
    sentimentBarContainer.style.width = '100%';
    sentimentBarContainer.style.backgroundColor = '#e0e0e0';
    sentimentBarContainer.style.borderRadius = '5px';
    sentimentBarContainer.style.overflow = 'hidden';
    sentimentBarContainer.style.margin = '10px 0';

    // Create the sentiment bar
    const sentimentBar = document.createElement('div');
    sentimentBar.style.width = `${sentimentScore}%`;
    sentimentBar.style.height = '20px';
    sentimentBar.style.backgroundColor = sentimentScore > 50 ? 'green' : 'red';
    sentimentBar.style.borderRadius = '5px';

    // Append the sentiment bar to the container
    sentimentBarContainer.appendChild(sentimentBar);

    // Append the container to the body or a specific element in your report HTML
    document.body.appendChild(sentimentBarContainer);
}


document.addEventListener('DOMContentLoaded', function() {
    // Get the data from the template
    //const timeSeriesData = JSON.parse(document.getElementById('timeSeriesData').textContent);
    let sentimentBarData, topWordsData, quarterlySentimentData;

    try {
        const rawSentimentBarData = document.getElementById('sentimentBarData').textContent;
        sentimentBarData = rawSentimentBarData ? JSON.parse(rawSentimentBarData) : {};
    }
    catch (e) {
        console.error("Error parsing sentimentBarData", e);
        sentimentBarData = {};
    }
    try {
        const rawQuarterlySentimentData = document.getElementById('quarterlySentimentData').textContent;
        quarterlySentimentData = rawQuarterlySentimentData ? JSON.parse(rawQuarterlySentimentData) : {};
    } catch (e) {
        console.error("Error parsing quarterlySentimentData", e);
        quarterlySentimentData = {};
    }

    try{
        topWordsData = JSON.parse(document.getElementById('topWordsData').textContent || '{}');
    }catch(e){
        console.log("Error parsing topWordsData", e);
        topWordsData = {};
    }

    console.log("Quarterly Sentiment Data",quarterlySentimentData);
    console.log("Sentiment Bar Data", sentimentBarData);
    console.log("Positive Sentiment", sentimentBarData.Positive);


    const topWordsArray = Object.entries(topWordsData).map(([word, count]) => ({word, count}));
    //const topWordsData = JSON.parse(document.getElementById('topWordsData').textContent);
    //const quarterlySentimentData = JSON.parse(document.getElementById('quarterlySentimentData').textContent);

    // Plot the time series chart
    //plotTimeSeriesGraph(timeSeriesData);

    // Plot the quarterly sentiment chart
    plotQuarterlySentiment(quarterlySentimentData);

    // Display the sentiment bar
    plotSentimentBar(sentimentBarData);

    // Display the top words
    showTopWords(topWordsArray);


    function plotSentimentBar(data) {
        if (!data || typeof data.Positive === 'undefined' || typeof data.Neutral === 'undefined' || typeof data.Negative === 'undefined') {
            console.error("Invalid data for sentiment bar:", data);
            return;
        }

        // Calculate the total and percentages
        const total = data.Positive + data.Neutral + data.Negative;
        const positivePercentage = (data.Positive / total) * 100;
        const neutralPercentage = (data.Neutral / total) * 100;
        const negativePercentage = (data.Negative / total) * 100;

        const options = {
            chart: {
                type: 'bar',
                height: 150,
                stacked: true,
            },
            plotOptions: {
                bar: {
                    horizontal: true
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val.toFixed(2) + "%"; // Show percentage on the bar
                },
                style: {
                    colors: ['#fff'] // Set label color to white for better visibility
                }
            },
            series: [
                {
                    name: 'Positive',
                    data: [positivePercentage]
                },
                {
                    name: 'Neutral',
                    data: [neutralPercentage]
                },
                {
                    name: 'Negative',
                    data: [negativePercentage]
                }
            ],
            xaxis: {
                max: 100, // Ensure the x-axis is scaled to 100%
                labels: {
                    show: false // Hide x-axis labels
                },
                axisBorder: {
                    show: false // Hide x-axis border
                },
                axisTicks: {
                    show: false // Hide x-axis ticks
                }
            },
            yaxis: {
                labels: {
                    show: false // Hide y-axis labels
                },
                axisBorder: {
                    show: false // Hide y-axis border
                },
                axisTicks: {
                    show: false // Hide y-axis ticks
                }
            },
            colors: ['#00cc00', '#ff9900', '#ff0000'], // Green, Orange, Red
            title: {
                text: 'Sentiment Distribution',
                align: 'center'
            },
            legend: {
                position: 'right',
                horizontalAlign: 'center'
            },
            stroke: {
                width: 1,
                colors: ['#fff']
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val.toFixed(2) + "%";
                    }
                }
            }
        };

        const chart = new ApexCharts(document.querySelector("#sentimentBarChart"), options);
        chart.render();
    }

        

    function showTopWords(topWords) {
        const topWordsContainer = document.getElementById('top-words');
        topWordsContainer.innerHTML = `
            <div class="top-words-wrapper">
                ${Object.entries(topWords).map(([word, count]) => `<div class="top-word-item">${word} ${count}</div>`).join('')}
            </div>
        `;
    }

    function plotQuarterlySentiment(data) {
        const quarters = data.map(q => q.quarter).sort(); // Sort quarters in ascending order

        // Prepare the series data for ApexCharts
        console.log("Quarterly Sentiment Data", quarters);
        const series = [
            {
                name: 'Negative',
                data: quarters.map(q => {
                    const entry = data.find(e => e.quarter === q);
                    return entry ? entry.Negative ||0 : 0;

                })
                    
            },
            {
                name: 'Neutral',
                data: quarters.map(q => {
                    const entry = data.find(e => e.quarter === q);
                    return entry ? entry.Neutral ||0 : 0;
                })
            },
            {
                name: 'Positive',
                data: quarters.map(q => {
                    const entry = data.find(e => e.quarter === q);
                    return entry ? entry.Positive ||0 : 0;
                })
            }
        ];

        const options = {
            chart: {
                type: 'bar',
                height: 400,
                stacked: true // Enable stacking
            },
            series: series,
            xaxis: {
                categories: quarters, // Formatted quarters as x-axis labels
                title: {
                    text: 'Quarter'
                }
            },
            yaxis: {
                title: {
                    text: 'Sentiment Count'
                },
                min: 0 // Ensure y-axis starts at 0
            },
            colors: ['#ff0000', '#ff9900', '#00cc00'], // Red, Orange, Green
            title: {
                text: 'Quarterly Sentiment',
                align: 'center'
            },
            legend: {
                position: 'right'
            },
            dataLabels: {
                enabled: false // Disable data labels on bars for cleaner look
            },
            plotOptions: {
                bar: {
                    columnWidth: '50%' // Adjust bar width
                }
            }
        };

        const chart = new ApexCharts(document.querySelector("#quarterlySentimentChart"), options);
        chart.render();
    }

    function plotQuarterlySentiment_old(quarterlySentimentData) {
        const quarters = Object.keys(quarterlySentimentData);
        //const positiveSentiments = quarterlySentimentData.map(data => data.positive);
        //const neutralSentiments = quarterlySentimentData.map(data => data.neutral);
        //const negativeSentiments = quarterlySentimentData.map(data => data.negative);
        
        
        console.log("Quarterly Sentiment Data", quarterlySentimentData);

        const positiveTrace = {
            x: quarters,
            y: quarters.map(quarter => quarterlySentimentData[quarter].Positive),
            name: 'Positive',
            type: 'bar',
            marker: { color: 'green' }
        };
    
        const neutralTrace = {
            x: quarters,
            y: quarters.map(quarter => quarterlySentimentData[quarter].Neutral),
            name: 'Neutral',
            type: 'bar',
            marker: { color: 'gray' }
        };
    
        const negativeTrace = {
            x: quarters,
            y: quarters.map(quarter => quarterlySentimentData[quarter].Negative),
            name: 'Negative',
            type: 'bar',
            marker: { color: 'red' }
        };

        const traces = [positiveTrace, neutralTrace, negativeTrace];
    
        const layout = {
            title: 'Quarterly Sentiment Analysis',
            barmode: 'stack',
            xaxis: { title: 'Quarter' },
            yaxis: { title: 'Sentiment Count' }
        };
    
        Plotly.newPlot('quarterlySentimentChart', traces, layout);
    }


});



function plotTimeSeriesGraph(timeSeriesData) {
    const dates = timeSeriesData.date;
    const sentimentScores = timeSeriesData.sentiment;

    const timeSeriesTrace = {
        x: dates,
        y: sentimentScores,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sentiment Score',
        line: { color: 'rgba(75, 192, 192, 1)' }
    };

    const timeSeriesLayout = {
        title: 'Sentiment Over Time',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Sentiment Score' }
    };

    Plotly.newPlot('timeSeriesChart', [timeSeriesTrace], timeSeriesLayout);
}


