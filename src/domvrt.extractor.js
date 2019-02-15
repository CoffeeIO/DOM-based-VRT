DomVRT.Extractor = (function (obj) {

  obj.currentAppToJSON = function() {
    return nodeToJSON(document);
  };

  obj.currentApp = function() {
    // Extract DOM elements
  };

  var dts = function(digit) {
    if (digit < 10) {
      return '0' + digit;
    }
    return '' + digit;
  };

  obj.currentAppToFile = function(filename) {

    var jsonObj = obj.currentAppToJSON();

    if (filename == null) {
      var d = new Date();
      var timeStr = d.getFullYear() + '-' + dts(d.getMonth() + 1) + '-' +
       dts(d.getDate()) + '_' + dts(d.getHours()) + ':' + dts(d.getMinutes() +
        ':' + dts(d.getSeconds()));

      var host = (window.location.host).split('.');

      filename = host[0] + '--' + timeStr + '.json';
    }

    var blob = new Blob([JSON.stringify(jsonObj)], {type: "application/json;charset=utf-8"});
    saveAs(blob, filename);
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
          styleSum += child.styleId + child.styleSum + ';';
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
  };

  return obj;

}) (DomVRT.Extractor || {});
