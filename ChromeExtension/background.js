function run() {
  // console.log('clicked button');
  // var newURL = "http://stackoverflow.com/";
  // chrome.tabs.create({ url: newURL });  chrome.tabs.create({ url: newURL });
  // chrome.windows.create({url: newURL}, function (win) {
  //   sendResponse(win);
  // });
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
    chrome.tabs.sendMessage(tabs[0].id, {message: 'ping'}, function(response) {});
  });
}

chrome.browserAction.onClicked.addListener(function(tab) {
  run()

  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;

    processUrls(getUrls(url), getViewports());
  });

});

let domvrtId = 1;

function getUrls(currentUrl = null) {
  let arr = [];

  if (currentUrl) {
    arr.push(currentUrl);
  }

  arr.push(
    // 'https://coffeeio.com/',
    // 'https://mgapcdev.com/',
    // 'https://github.com/MGApcDev/DOM-based-VRT',
  );

  return arr;
}

function getViewports() {
  return [
    600,
    900,
    // 1200,
  ];
}

function processUrls(urls, viewports) {
  let timeout = 0;
  for (const url of urls) {
    for (const viewport of viewports) {
      processUrl(url, viewport, timeout);
      timeout += 5000;
    }
  }
};

function processUrl(url, viewport, timeout) {
  setTimeout(function() {

    let windowName = url + ' : ' +  viewport;
    console.log('%s : %s', url, viewport);

    url = url + '?domVrtRun=true&domVrtViewport=' + viewport;

    chrome.windows.create({
      url: url,
      width: viewport,
      height: 1000,
      // tabId: 'domvrt-' + domvrtId,
    }, function (window) {
      // sendResponse(window);
    });

    domvrtId += 1;
  }, timeout);

}