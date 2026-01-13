document.addEventListener("DOMContentLoaded", function () {
document.getElementById("top_30_last_day_losers").addEventListener("click", async function() {
    cleanupAll();
        try {
            const gainers_url="/top_30_last_day_losers/"
            const response = await fetch(gainers_url);
            const data = await response.json();
            console.log("Received data:", data);
            const container = document.getElementById("form-container");
                container.innerHTML=`
                
                <div class="top_30_gainers_container">
                    <h1>Top 30 Last Day Loser Companies</h1>
                    <div class="company-list" id="30_companyList"></div>
                </div>
                <div id="gainers_graph_container" class="gainers_graph_container"></div>
                `;
            const companyListDiv = document.getElementById('30_companyList');
            companyListDiv.innerHTML = '';
            Object.entries(data).forEach(([company, details]) => {
                const btn = document.createElement('button');
                btn.className = 'company-btn';
                btn.innerHTML = `<span id="com_name">${company}</span><span class="company-price" id="companyPriceList">${details.final_percent_gain}</span>`;
                const graphContainer = document.getElementById("gainers_graph_container");
                btn.onclick = async () => {
                graphContainer.innerHTML = `
                <style>
                .data-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-family: 'Poppins', sans-serif;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                }

                .data-table th, .data-table td {
                padding: 12px 16px;
                text-align: left;
                border-bottom: 1px solid rgba(0, 0, 0, 0.1);
                color: #333333;
                }

                .data-table th {
                background: #f5f5f5;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                }

                .data-table tr:last-child td {
                border-bottom: none;
                }

                .data-table tr:hover {
                background: #f9f9f9;
                transition: background 0.3s ease;
                }

                h3 {
                margin-bottom: 8px;
                font-family: 'Poppins', sans-serif;
                color: #222222;
                }
                </style>

                <div class="table">
                <h3>${company}</h3>
                <table class="data-table">
                
                    <tr><td><b>High of up gap </b></td><td>${details.g_up_h} %</td></tr>
                    <tr><td><b>Low of up gap</b></td><td>${details.g_up_l} %</td></tr>
                    <tr><td><b>Up gap</b></td><td>${details.up_gap} %</td></tr>
                    <tr><td><b>High of  down gap</b></td><td>${details.g_down_h} %</td></tr>
                    <tr><td><b>Low of down gap</b></td><td>${details.g_down_l} %</td></tr>
                    <tr><td><b>Down gap</b></td><td>${details.down_gap} %</td></tr>
                    <tr><td><b>Final percent gain </b></td><td>${details.final_percent_gain}%</td></tr>
                </table>
                </div>
                <div class="chart">
                <div id="barChart"></div>
                </div>
                `      ;
                const data = [
    {
        x: ["Gap Up High", "Gap Up Low", "Up Gap", "Gap Down High", "Gap Down Low", "Down Gap"],
        y: [details.g_up_h, details.g_up_l, details.up_gap, details.g_down_h, details.g_down_l, details.down_gap],
        type: "bar",
        marker: { color: "skyblue" },
        
        // 👇 Add this part
        text: [details.g_up_h, details.g_up_l, details.up_gap, details.g_down_h, details.g_down_l, details.down_gap],
        textposition: "auto", // can be "inside", "outside", "auto", or "none"
        texttemplate: "%{text}", // ensures raw value is displayed
        insidetextanchor: "middle" // aligns text inside the bar properly
    }
];

const layout = {
    title: "Price Fluctuation Data",
    xaxis: { title: "Fluctuation Data Name" },
    yaxis: { title: "Percentage" },
    uniformtext: { minsize: 12, mode: "hide" } ,// optional: hide overlapping text
    
};
// 👇 Disable the Plotly logo in the modebar
const config = {
  displaylogo: false
};

Plotly.newPlot("barChart", data, layout);

            };
                companyListDiv.appendChild(btn);
            });
            
            
        const firstBtn = companyListDiv.querySelector('.company-btn');
        if (firstBtn) firstBtn.click();
            
        } catch (err) {
            console.error("Error:", err);
        }
        });
});
