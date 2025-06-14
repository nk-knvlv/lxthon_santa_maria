// Проверка состояния сервера каждые 5 минут
const SERVER_HEALTH_CHECK_INTERVAL = 5 * 60 * 1000;

async function checkServerHealth() {
  try {
    const response = await fetch('http://localhost:8000/health');
    if (!response.ok) {
      console.error('Server health check failed');
      chrome.action.setIcon({ path: "icons/icon48_red.png" });
    } else {
      chrome.action.setIcon({ path: "icons/icon48.png" });
    }
  } catch (error) {
    console.error('Server connection error:', error);
    chrome.action.setIcon({ path: "icons/icon48_red.png" });
  }
}

// Периодическая проверка сервера
setInterval(checkServerHealth, SERVER_HEALTH_CHECK_INTERVAL);

// Первая проверка при запуске
checkServerHealth();

// Обработчик сообщений от popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'check_server') {
    checkServerHealth().then(() => sendResponse({ success: true }));
    return true;
  }
});