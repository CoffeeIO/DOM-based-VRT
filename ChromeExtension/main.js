chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  var start = new Date()
  scroll(document.body.scrollWidth, document.body.scrollHeight); // Scroll to bottom
  setTimeout(function (){

  // Something you want delayed.
    scroll(0,0); // Scroll to top
    setTimeout(function (){

  // Something you want delayed.
      var dom1 = DomVRT.Extractor.currentAppToFile(null);
      console.log(dom1);

      var end = new Date() - start
      console.info('Execution time: %dms', end)
    }, 250);

  }, 250);

});
