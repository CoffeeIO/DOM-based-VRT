var DomExtractor = (function () {
  var run = function() {
    return extractCurrentApp();
  };

  var extractCurrentApp = function() {
    // Extract DOM elements
  };

  var extractCurrentAppAsJSON = function (){
    var dom = extractCurrentApp();
    // ...

  };

  // Expose functions to call.
  return {
    extractCurrentApp : extractCurrentApp,
    extractCurrentAppAsJSON: extractCurrentAppAsJSON,
    run: run
  }


}) ();
