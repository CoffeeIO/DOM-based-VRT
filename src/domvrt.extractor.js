DomVRT.Extractor = (function (obj) {


  obj.nodeCount = 0;

  obj.currentAppToJSON = function(minify) {
    obj.nodeCount = 0;
    minify = (minify == null) ? false : minify;
    var result = nodeToJSON(document, minify);
    result.minify = minify;
    result['node-count'] = obj.nodeCount;
    result['location'] = {
      'href'     : window.location.href,
      'protocol' : window.location.protocol,
      'host'     : window.location.host
    };

    result.captureWidth = window.innerWidth;
    result.captureHeight= document.body.scrollHeight;


    return result;
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

  obj.currentAppToFile = function(filename, minify) {

    var jsonObj = obj.currentAppToJSON(minify);

    if (filename == null) {
      var d = new Date();
      var timeStr = d.getFullYear() + '-' + dts(d.getMonth() + 1) + '-' +
       dts(d.getDate()) + '--' + dts(d.getHours()) + '-' + dts(d.getMinutes() +
        '-' + dts(d.getSeconds()));

      var host = (window.location.host).replace('.', '-');

      filename = host + '--' + timeStr + '.json';
    }

    var blob = new Blob([JSON.stringify(jsonObj)], {type: "application/json;charset=utf-8"});
    saveAs(blob, filename);
    
    return jsonObj;
  };

  // Based on https://gist.github.com/sstur/7379870
  var nodeToJSON = function (node, minify, position) {
    minify = (minify == null) ? false : minify;
    position = (position == null) ? 1 : position;
    node = node || this;


    var mVal = (minify) ? 1 : 0;

    var jsonMapping = {
      nodeType:   ['nodeType', 'nt'],
      tagName:    ['tagName', 'tn'],
      nodeName:   ['nodeName', 'nn'],
      nodeValue:  ['nodeValue', 'nv'],
      attrs:      ['attrs', 'at'],
      styles:     ['styles', null],
      styleId:    ['styleId', 'si'],
      styleSum:   ['styleSum', 'ss'],
      childNodes: ['childNodes', 'c'],
      level:      ['level', 'l'],
      position:   ['position', 'p'],
      x1 :        ['x1', null],
      y1 :        ['y1', null],
      x2 :        ['x2', null],
      y2 :        ['y2', null],
    };

    // Define node.
    var json = {};

    json[jsonMapping['nodeType'][mVal]] = node.nodeType

    if (jsonMapping['tagName'][mVal] && node.tagName) {
      json[jsonMapping['tagName'][mVal]] = node.tagName.toLowerCase();
    } else
    if (jsonMapping['nodeName'][mVal] && node.nodeName) {
      json[jsonMapping['nodeName'][mVal]] = node.nodeName;
    }
    if (jsonMapping['nodeValue'][mVal] && node.nodeValue) {
      value = node.nodeValue
      if (value.trim() == '') { // Ignore empty text nodes
        return null
      }

      json[jsonMapping['nodeValue'][mVal]] = node.nodeValue;

    }

    // Define attributes.
    if (jsonMapping['attrs'][mVal]) {
      json[jsonMapping['attrs'][mVal]] = {};
      if (node.attributes != null) {
        Array.prototype.forEach.call(node.attributes, function(attr) {
          json[jsonMapping['attrs'][mVal]][attr.name] = attr.value;
        });
      }
    }


    // Define CSS properties.
    if (jsonMapping['styles'][mVal]) {
      var n = node.nodeType;
      var fullStyle = "";

      if (n != 9 && n != 10 && n != 3 && n != 8) {
        json[jsonMapping['styles'][mVal]] = {};
        var stylesObj = window.getComputedStyle(node);
        Array.prototype.forEach.call(stylesObj, function(style) {
          json[jsonMapping['styles'][mVal]][style] = stylesObj.getPropertyValue(style);
          fullStyle += style + ":" + stylesObj.getPropertyValue(style) + ","
        });

        if (jsonMapping['styleId'][mVal]) {
          json[jsonMapping['styleId'][mVal]] = DomVRT.Utils.md5(fullStyle);
        }
      }
    }

    // Store coordinates of nodes.
    if (jsonMapping['x1'][mVal]) {
      rect = null
      if (node.nodeType == 3) {
        var range = document.createRange();
        range.selectNode(node);
        rect = range.getBoundingClientRect();
      }

      if (node.nodeType == 1) {
        rect = node.getBoundingClientRect();
      }
      if (rect != null) {
        json[jsonMapping['x1'][mVal]] = rect.left
        json[jsonMapping['y1'][mVal]] = rect.top
        json[jsonMapping['x2'][mVal]] = rect.right
        json[jsonMapping['y2'][mVal]] = rect.bottom
      }

    }

    if (jsonMapping['position'][mVal]) {
      json[jsonMapping['position'][mVal]] = position;
    }

    // Loop children.
    if (jsonMapping['childNodes'][mVal]) {
      var cLabel = [jsonMapping['childNodes'][mVal]]
      json[cLabel] = [];
      var styleSum = "";

      if (node.childNodes) {
        var index = 0;
        Array.prototype.forEach.call(node.childNodes, function(n) {

          var newPos = position + '.' + index;
          var child = nodeToJSON(n, minify, newPos);

          if (child != null) {
            json[cLabel].push(child);

            if (jsonMapping['styleId'][mVal] && jsonMapping['styleSum'][mVal]) {
              if (child[jsonMapping['styleId'][mVal]] != null) {
                styleSum += child[jsonMapping['styleId'][mVal]] + child[jsonMapping['styleSum'][mVal]] + ';';
              }
            }

            index++;
          }

        });
      }
      if (jsonMapping['styleSum'][mVal]) {
        json[jsonMapping['styleSum'][mVal]] = DomVRT.Utils.md5(styleSum);
      }
    }


    if (node.id == 'debug') {
      console.log('DEBUG: styles');
      console.log(json.styleId, json.styleSum);
      console.log(json.styles);
    }

    obj.nodeCount++;
    return json;
  };

  return obj;

}) (DomVRT.Extractor || {});
