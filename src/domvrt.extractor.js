DomVRT.Extractor = (function (obj) {

  obj.nodeCount = 0;

  obj.processUrls = function(urls, viewports) {
    for (const url of urls) {
      for (const viewport of viewports) {
        obj.processUrl(url, viewport);
      }
    }
  };

  obj.processUrl = function(url, viewport) {
    let windowName = url + ' : ' +  viewport;
    console.log('%s : %s', url, viewport);

  }

  obj.currentAppToJSON = function(minify) {
    console.log('Running DomVRT Extractor');

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

    result['mutations'] = DomVRT.Differ.mutations;

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
    filename = filename ? filename : getFilename();

    html2canvas(document.querySelector('html')).then(canvas => {
      canvas.toBlob(function(blob) {
        saveAs(blob, filename + '.png');
      });
    });


    // domtoimage.toBlob(document.getElementById('html'))
    //   .then(function (blob) {
    //       saveAs(blob, filename + '.png');
    //   });

    // setTimeout(function(){
    var jsonObj = obj.currentAppToJSON(minify);
    // var blob = new Blob([JSON.stringify(jsonObj)], {type: "application/json;charset=utf-8"});
    // saveAs(blob, filename + '.json');
    // }, 3000);

    return jsonObj;
  };

  var getFilename = function() {
    var d = new Date();
    var timeStr = d.getFullYear() + '-' + dts(d.getMonth() + 1) + '-' +
      dts(d.getDate()) + '--' + dts(d.getHours()) + '-' + dts(d.getMinutes() +
      '-' + dts(d.getSeconds()));

    var host = (window.location.host).replace('.', '-');
    let path = (window.location.pathname).replace('/', '-');
    const urlParams = new URLSearchParams(window.location.search);
    const viewport = urlParams.get('domVrtViewport');

    // filename = host + '-' + path + '--' + viewport + '--' + timeStr + '';
    filename = timeStr + '--' + host + '-' + path + '--' + viewport;

    return filename;
  }

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

    if (node.nodeType == 1) {
      node.setAttribute("p", position)
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
        // var stylesObj = window.getComputedStyle(node);
        var stylesObj = obj.getAllStyles(node);
        // json['allStyle'] = allStylesObj;

        Array.prototype.forEach.call(Object.keys(stylesObj), function(style) {
          json['styles'][style] = stylesObj[style];
          fullStyle += style + ":" + stylesObj[style] + ","
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
        rect = obj.getRect(range, false);
      }

      if (node.nodeType == 1) {
        rect = obj.getRect(node, true);
      }

      if (rect != null) {
        json[jsonMapping['x1'][mVal]] = rect.left
        json[jsonMapping['y1'][mVal]] = rect.top + window.scrollY
        json[jsonMapping['x2'][mVal]] = rect.right
        json[jsonMapping['y2'][mVal]] = rect.bottom + window.scrollY
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

    if (obj.nodeCount > obj.limit) {
      console.log('Hit: ' + obj.limit);
      obj.limit = obj.limit * 2;
    }

    return json;
  };

  obj.limit = 10;

  obj.getStyle = function(node, style) {
    var display = window.getComputedStyle(node).getPropertyValue('display');
    var value = window.getComputedStyle(node).getPropertyValue(style);
    var dynamicStyles = ['height', 'width', 'perspective-origin', 'transform-origin'];

    if (display != "none") {
      // if (dynamicStyles.indexOf(style) != -1) {
        node.style.display = "none";
        value = window.getComputedStyle(node).getPropertyValue(style);
        // console.log(value);
        node.style.display = display;
      // }
    }

    return value;
  };

  obj.getAllStyles = function(node) {
    var display = window.getComputedStyle(node).getPropertyValue('display');
    var styles = window.getComputedStyle(node);

    if (display != "none") {
        node.style.display = "none";
        styles = window.getComputedStyle(node);
        // console.log(value['perspectiveOrigin']);
    }

    var map = {};
    Array.prototype.forEach.call(Object.keys(styles), function(style) {
      if (isNaN(style)) {
        map[style] = styles[style];
      }
    });
    // console.log('print map');
    // console.log(map['text-transform']);
    // console.log(map);


    node.style.display = display;

    return map;
  };

  obj.getRect = function(node, hasStyle) {
    if (! hasStyle) {
      return node.getBoundingClientRect();
    }
    var style = window.getComputedStyle(node);
    var margin = {
        left: parseInt(style["margin-left"]),
        right: parseInt(style["margin-right"]),
        top: parseInt(style["margin-top"]),
        bottom: parseInt(style["margin-bottom"])
    };
    var padding = {
        left: parseInt(style["padding-left"]),
        right: parseInt(style["padding-right"]),
        top: parseInt(style["padding-top"]),
        bottom: parseInt(style["padding-bottom"])
    };
    var border = {
        left: parseInt(style["border-left"]),
        right: parseInt(style["border-right"]),
        top: parseInt(style["border-top"]),
        bottom: parseInt(style["border-bottom"])
    };


    var rect = node.getBoundingClientRect();
    rect = {
        left: rect.left - margin.left,
        right: rect.right + margin.right,
        top: rect.top - margin.top,
        bottom: rect.bottom + margin.bottom
    };
    rect['x'] = rect.left;
    rect['y'] = rect.top;
    rect.width = rect.right - rect.left;
    rect.height = rect.bottom - rect.top;
    return rect;
  };

  return obj;

}) (DomVRT.Extractor || {});
