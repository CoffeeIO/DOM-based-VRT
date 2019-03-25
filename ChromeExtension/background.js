function run() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
    chrome.tabs.sendMessage(tabs[0].id, {message: 'ping'}, function(response) {});
  });
}

chrome.browserAction.onClicked.addListener(function(tab) {
  run()
});
