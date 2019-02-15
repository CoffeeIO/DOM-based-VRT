DomVRT.Extractor = (function (obj) {





  // var getClasses = function(elem) {
  //   var arr = [];
  //   if (elem.classList == null) {
  //     return arr;
  //   }
  //   Array.prototype.forEach.call(elem.classList, function(elemClass) {
  //     arr.push(elemClass);
  //   });
  //
  //   return arr;
  // }
  //
  // var getAttributes = function(elem) {
  //   var arr = {};
  //
  //   if (elem.attributes == null) {
  //     return arr;
  //   }
  //   Array.prototype.forEach.call(elem.attributes, function(attr) {
  //     arr[attr.name] = attr.value;
  //   });
  //
  //   return arr;
  // }
  //
  // var loopChild = function(elem) {
  //   var json = {};
  //   // Add attributes of element.
  //   json.tag = elem.tagName;
  //   json.class = getClasses(elem);
  //   json.id = elem.id;
  //   json.text = ""; // Think about how to retrieve this
  //   json.attr = getAttributes(elem);
  //
  //   // Loop through children.
  //   json.nodes = [];
  //   if (elem.childNodes == null) {
  //     return arr;
  //   }
  //   Array.prototype.forEach.call(elem.childNodes, function(node) {
  //     json.nodes.push(loopChild(node));
  //   });
  //
  //   return json;
  // };

  obj.extractCurrentAppAsJSON = function (elem){
    // Loop through all elements
    return nodeToJSON(document);
  };

  obj.extractCurrentApp = function() {
    // Extract DOM elements
  };

  // Based on https://gist.github.com/sstur/7379870
  var nodeToJSON = function (node) {
    node = node || this;

    // Define node.
    var json = {
      nodeType: node.nodeType
    };
    if (node.tagName) {
      json.tagName = node.tagName.toLowerCase();
    } else
    if (node.nodeName) {
      json.nodeName = node.nodeName;
    }
    if (node.nodeValue) {
      json.nodeValue = node.nodeValue;
    }

    // Define attributes.
    json.attrs = {};
    if (node.attributes != null) {
      Array.prototype.forEach.call(node.attributes, function(attr) {
        json.attrs[attr.name] = attr.value;
      });
    }

    // Define CSS properties.
    var n = node.nodeType;
    var fullStyle = "";

    if (n != 9 && n != 10 && n != 3 && n != 8) {
      json.styles = {};
      var stylesObj = window.getComputedStyle(node);
      Array.prototype.forEach.call(stylesObj, function(style) {
        json.styles[style] = stylesObj.getPropertyValue(style);
        fullStyle += style + ":" + stylesObj.getPropertyValue(style) + ","
      });

      json.styleId = DomVRT.Utils.md5(fullStyle);
    }


    // Loop children.
    json.childNodes = [];
    var styleSum = "";

    if (node.childNodes) {
      Array.prototype.forEach.call(node.childNodes, function(node) {
        var child = nodeToJSON(node);
        json.childNodes.push(child);
        if (child.styleId != null) {
          styleSum += child.styleId + child.styleSum;
        }
      });
    }
    json.styleSum = DomVRT.Utils.md5(styleSum);

    if (node.id == 'debug') {
      console.log('DEBUG: styles');
      console.log(json.styleId, json.styleSum);
      console.log(json.styles);
    }

    return json;
  }

  return obj;

}) (DomVRT.Extractor || {});
