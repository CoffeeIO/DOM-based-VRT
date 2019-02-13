var DomExtractor = (function () {
  var run = function() {
    return extractCurrentApp();
  };

  var extractCurrentApp = function() {
    // Extract DOM elements
  };

  var getClasses = function(elem) {
    var arr = [];
    if (elem.classList == null) {
      return arr;
    }
    Array.prototype.forEach.call(elem.classList, function(elemClass) {
      arr.push(elemClass);
    });

    return arr;
  }

  var getAttributes = function(elem) {
    var arr = {};

    if (elem.attributes == null) {
      return arr;
    }
    Array.prototype.forEach.call(elem.attributes, function(attr) {
      arr[attr.name] = attr.value;
    });

    return arr;
  }

  var loopChild = function(elem) {
    var json = {};
    // Add attributes of element.
    json.tag = elem.tagName;
    json.class = getClasses(elem);
    json.id = elem.id;
    json.text = ""; // Think about how to retrieve this
    json.attr = getAttributes(elem);

    // Loop through children.
    json.nodes = [];
    if (elem.childNodes == null) {
      return arr;
    }
    Array.prototype.forEach.call(elem.childNodes, function(node) {
      json.nodes.push(loopChild(node));
    });

    return json;
  };

  var extractCurrentAppAsJSON = function (elem){
    // Loop through all elements
    var json = loopChild(document);

    return json;
  };

  // Expose functions to call.
  return {
    extractCurrentApp : extractCurrentApp,
    extractCurrentAppAsJSON: extractCurrentAppAsJSON,
    run: run,
    test: function () { console.log('test'); },
  }
}) ();
