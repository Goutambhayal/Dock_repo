document.addEventListener("DOMContentLoaded", function () {
const tradingBot=document.getElementById("Companies_LTP");
tradingBot.addEventListener('click',async function(){
(function(){
  // Use the existing global arrays/objects: companies, REAL_COMPANY_TOKENS, currentChart
  const wsScheme = (location.protocol === 'https:') ? 'wss' : 'ws';
  const socket = new WebSocket(wsScheme + '://' + window.location.host + '/ws/trading-bot-data/');

  socket.addEventListener('open', (evt) => {
    console.log("WebSocket connected for trading bot data");
  });

  socket.addEventListener('message', (evt) => {
    try {
      const data = JSON.parse(evt.data);
      // data.type can be "prices_snapshot" (initial) or "prices_update" (periodic)
      const prices = data.trades || {};
      // prices is an object like {"11956": 523.75, "277": 314.20, ...}
      // Update company objects and UI similarly to polling approach
      companies.forEach((company, idx) => {
        const token = REAL_COMPANY_TOKENS[idx];
        if (token && prices[token] !== undefined) {
          company.price = prices[token];
          const timeIndex = getCurrentMinuteIndex();
          if (timeIndex >= 0 && timeIndex < company.priceData.length) {
            company.priceData[timeIndex] = company.price;
          }
          const priceSpan = document.getElementById(`companyPriceList${idx}`);
          if (priceSpan) priceSpan.textContent = `₹${company.price}`;
        }
      });

      // update currently shown chart
      if (typeof currentChart !== 'undefined' && currentChart) {
        currentChart.updateChart();
      }
    } catch (e) {
      console.error("WS parse error:", e, evt.data);
    }
  });

  socket.addEventListener('close', (evt) => {
    console.warn("WebSocket closed:", evt);
    // attempt reconnect with backoff
    attemptReconnect();
  });

  socket.addEventListener('error', (err) => {
    console.error("WebSocket error:", err);
    socket.close();
  });

  // Reconnect logic (simple exponential backoff)
  let reconnectAttempts = 0;
  function attemptReconnect() {
    reconnectAttempts++;
    const delay = Math.min(30, Math.pow(2, reconnectAttempts)) * 1000; // up to 30s
    console.log(`Attempting reconnect in ${delay/1000}s`);
    setTimeout(() => {
      // create new socket and reassign handlers by reloading page or re-executing setup
      window.location.reload(); // simplest option — refresh UI state and reconnect
    }, delay);
  }

  // Optional: expose socket for debugging
  window.__livePriceSocket = socket;
})();
});
});