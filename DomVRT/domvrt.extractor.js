var DomExtractor = (function () {
  var run = function() {
    return extractCurrentApp();
  };


  // Based on https://gist.github.com/sstur/7379870
  var nodeToJSON = function (node) {
    node = node || this;

    // Define node.
    var obj = {
      nodeType: node.nodeType
    };
    if (node.tagName) {
      obj.tagName = node.tagName.toLowerCase();
    } else
    if (node.nodeName) {
      obj.nodeName = node.nodeName;
    }
    if (node.nodeValue) {
      obj.nodeValue = node.nodeValue;
    }

    // Define attributes.
    var attrs = {};
    if (node.attributes != null) {
      Array.prototype.forEach.call(node.attributes, function(attr) {
        attrs[attr.name] = attr.value;
      });
    }
    obj.attrs = attrs;

    // Define CSS properties.
    var n = node.nodeType;
    var fullStyle = "";

    if (n != 9 && n != 10 && n != 3 && n != 8) {
      var styleObj = {};
      var styles = window.getComputedStyle(node);
      Array.prototype.forEach.call(styles, function(style) {
        styleObj[style] = styles.getPropertyValue(style);
        fullStyle += style + ":" + styles.getPropertyValue(style) + ","
      });

      obj.styles = styleObj;
      obj.styleId = md5(fullStyle);
    }


    // Loop children.
    obj.childNodes = [];
    var styleSum = "";
    if (node.childNodes) {
      Array.prototype.forEach.call(node.childNodes, function(node) {
        var child = nodeToJSON(node);
        obj.childNodes.push(child);
        if (child.styleId != null) {
          styleSum += child.styleId;
        }
      });
    }
    obj.styleSum = md5(styleSum);

    return obj;
  }

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
    var json = nodeToJSON(document);

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
