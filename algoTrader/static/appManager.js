
window.eventManager = (function () {
  const listeners = [];
  return {
    add(target, type, callback, options) {
      if (!target) return;
      target.addEventListener(type, callback, options);
      listeners.push({ target, type, callback, options });
    },
    remove(target, type, callback, options) {
      target.removeEventListener(type, callback, options);
      // remove from list
      for (let i = listeners.length - 1; i >= 0; i--) {
        const l = listeners[i];
        if (l.target === target && l.type === type && l.callback === callback) {
          listeners.splice(i, 1);
        }
      }
    },
    clearAll() {
      for (const { target, type, callback, options } of listeners) {
        try { target.removeEventListener(type, callback, options); } catch (e) {}
      }
      listeners.length = 0;
    }
  };
})();

window.resourceManager = (function () {
  const sockets = new Set();
  const intervals = new Set();
  const timeouts = new Set();
  const observers = new Set();

  return {
    registerSocket(ws) { if (ws) sockets.add(ws); },
    unregisterSocket(ws) { sockets.delete(ws); },
    registerInterval(id) { intervals.add(id); },
    registerTimeout(id) { timeouts.add(id); },
    registerObserver(obs) { observers.add(obs); },

    closeAll() {
      // WebSockets
      for (const ws of sockets) {
        try { ws.removeEventListener && ws.close(); } catch (e) {}
      }
      sockets.clear();

      // intervals
      for (const id of intervals) clearInterval(id);
      intervals.clear();

      // timeouts
      for (const id of timeouts) clearTimeout(id);
      timeouts.clear();

      // MutationObservers or other observers
      for (const obs of observers) {
        try { obs.disconnect(); } catch (e) {}
      }
      observers.clear();
    }
  };
})();

function cleanupAll() {
  // remove DOM event listeners
  window.eventManager && window.eventManager.clearAll();
  // close sockets, intervals, observers
  window.resourceManager && window.resourceManager.closeAll();

  // optional: clear shared DOM area
  const main = document.getElementById('form-container');
  if (main) main.innerHTML = '';
}
