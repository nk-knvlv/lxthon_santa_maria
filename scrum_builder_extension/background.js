chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: () => {
      console.log('Extension activated!');
    }
  });
});