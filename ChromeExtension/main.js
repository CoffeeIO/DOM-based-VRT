chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  var start = new Date()
  scroll(0,0); // Scroll to top
  var dom1 = DomVRT.Extractor.currentAppToFile(null);
  console.log(dom1);
  
  var end = new Date() - start
  console.info('Execution time: %dms', end)
});
