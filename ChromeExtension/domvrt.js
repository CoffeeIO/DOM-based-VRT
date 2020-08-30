// Define module.
var DomVRT = {};

var module = (typeof module !== 'undefined') ? module : {};

DomVRT.Differ = (function (obj) {

  obj.mergeJSON = function(jsonPre, jsonPost) {

    jsonPre.styleId2 = jsonPost.styleId;
    jsonPre.styleSum2 = jsonPost.styleSum;

    for (var i = 0; i < jsonPre.childNodes.length; i++) {
      var pre = jsonPre.childNodes[i];
      var post = jsonPost.childNodes[i];

      obj.mergeJSON(pre, post);
    }

    return jsonPre;
  };

  var debug = false;

  var compareNode = function(nodePre, nodePost, level, path) {
    var diffArr = [];
    if (level == null) {
      level = 1;
    }

    if (nodePre.styleId != nodePost.styleId) {
      var diff = {};
      diff.path = path;
      diff.changes = {};

      Array.prototype.forEach.call(Object.keys(nodePre.styles), function(key) {
        if (nodePre.styles[key] != nodePost.styles[key]) {
          diff.changes[key] = [nodePre.styles[key], nodePost.styles[key]];
        }
      });

      diffArr.push(diff);
    }

    if (nodePre.styleSum == null || nodePost.styleSum == null) {
      if (debug) console.log('No styleSum');
    }

    if (nodePre.styleSum == nodePost.styleSum) {
      if (debug) console.log('Stopping search');
      return diffArr;
    }

    if (nodePre.childNodes.length == 0) {
      if (debug) console.log('No children');
    }

    if (nodePre.styleId == null || nodePost.styleId == null) {
      if (debug) console.log('No styleId');
    }

    for (var i = 0; i < nodePre.childNodes.length; i++) {
      var pre = nodePre.childNodes[i];
      var post = nodePost.childNodes[i];

      var newPath = path + '|' + i + ':' + pre.tagName;
      diffArr = diffArr.concat(compareNode(pre, post, level+1, newPath));
    }

    return diffArr;
  };

  /**
   *
   */
  obj.compareJSON = function(jsonPre, jsonPost) {
    var res = compareNode(jsonPre, jsonPost);
    return res;
  };

  var MATCH  = "match";
  var UPDATE = "update";
  var INSERT = "insert";
  var REMOVE = "remove";

  obj.mutations = {
    'match'  : [],
    'update' : [],
    'insert' : [],
    'remove' : []
  };

  obj.index = function() {
    obj.nodeCount = 0;
    obj.type = {};
    obj.maxDepth = 0;
    obj.leafs = 0;

    obj.findNode(document, '1', null, true, 0);
    return {
      'nodes' : obj.nodeCount,
      'types' : obj.type,
      'depth' : obj.maxDepth,
      'leafs' : obj.leafs
    };
  };

  obj.nodeCount = 0;
  obj.type = {};
  obj.maxDepth = 0;
  obj.leafs = 0;

  obj.findNode = function(node, position, toFind, setPosition, depth) {
    var subtree = 1;
    position = (position == null) ? 1 : position;
    node = node || this;

    // Define node.
    var json = {};

    if (node.nodeValue) {
      value = node.nodeValue
      if (value.trim() == '') { // Ignore empty text nodes
        return {
          'valid' : false,
          'subtree' : 0
        };
      }
    }

    if (node.nodeType == 1) {
      node.setAttribute("p", position);
    }

    if (position == toFind) {
      console.log('Found `%s`', toFind);
      return {
        'found' : true,
        'valid' : true,
        'node'  : node
      };
    }

    // Loop children.
    if (node.childNodes) {
      var index = 0;
      var toReturn = null;
      Array.prototype.forEach.call(node.childNodes, function(n) {

        var newPos = position + '.' + index;
        // console.log(newPos);
        var child = obj.findNode(n, newPos, toFind, setPosition, depth + 1);

        if (child['valid']) {
          index++;
        }
        if (child['found']) {
          // Can't return directly inside foreach loop.
          toReturn = child;
        }
        subtree += child['subtree'];

      });

      if (toReturn != null) {
        return toReturn;
      }
    }

    if (node.childNodes.length) {
      obj.leafs++;
    }

    obj.nodeCount++;
    if (! (node.nodeType in obj.type)) {
      obj.type[node.nodeType] = 0;
    }
    obj.type[node.nodeType]++;

    if (depth > obj.maxDepth) {
      obj.maxDepth = depth;
    }

    if (node.nodeType == 1) {
      node.setAttribute("st", subtree);
    }

    return {
      'found' : false,
      'valid' : true,
      'subtree' : subtree
    };
  }

  obj.getNode = function(position) {
    // Find tag nodes.
    var node = document.querySelector('*[p="' + position + '"]');
    if (node == null) {
      console.log('Trying to find, node...');
      var result = obj.findNode(document, '1', position);
      console.log(result);
      if (result['node']) {
        node = result['node'];
      }
    }

    if (node == null) {
      console.log('Element `%s` not found', position);
      return null
    }
    return node;
  }

  obj.insertWrapper = function(position, before, after, visible) {
    var node = obj.getNode(position);
    node.outerHTML = before + node.outerHTML + after;

    /*
    {
      node-pre : null,
      node-post :
        {
          position: position,
          nodeType: 1,
          text: null,
        },
      style : null,
      visible : visible,
    }
    */
    obj.add(
      INSERT,
      {
        'node-pre': null,
        'node-post': {
          'position': position,
          'nodeType': 1,
          'text': null,
          'tag': null,
          'html': after + before
        },
        'style' : null,
        'recursive': false,
        'visible' : visible
      }
    );

    return node;
  }

  obj.insert = function(position, html, prepend, visible) {
    var node = obj.getNode(position);

    if (! prepend) {
      // Insert child.
      node.innerHTML = html;
    } else {
      // Insert at index.
      node.outerHTML += html;
    }

    if (prepend) {
      var x = position.lastIndexOf('.');
      var y = position.substr(x + 1, position.length)
      var newX = Number(y) + 1;

      var base = position.substr(0, x + 1)

      newPosition = base + newX;
      console.log('newPos: ' , newPosition);
    } else {
      newPosition = position + '.0';
      console.log('newPos: ' , newPosition);
    }

    /*

    // Allow to multiple inserts on newPosition.
    {
      node-pre : null,
      node-post :
        {
          position: newPosition,
          nodeType: ?,
          text: ?,
        },
      style : null,
      recursive: true,
      visible : visible,
    }
    */

    obj.add(
      INSERT,
      {
        'node-pre': null,
        'node-post': {
          'position': newPosition,
          'nodeType': null,
          'text': null,
          'tag': null,
          'html': html
        },
        'style' : null,
        'recursive': true,
        'visible' : visible
      }
    );

    return node;
  };

  obj.remove = function(position, visible, isWrapper) {
    var node = obj.getNode(position);


    if (isWrapper) {
      var parent = node.parentNode;
      var children = node['childNodes'];

      html = ""
      Array.prototype.forEach.call(children, function(child) {
        if (child.nodeType == 3) {
          html += child['nodeValue'];
        } else if (true) {
          html += child.outerHTML;
        }

        console.log(child);

      });

      console.log("Setting: ", html);

      node.outerHTML = html;

    } else {
      node.remove();
    }

    /*
    // If (! isWrapper): Allow to multiple removes on position.
    {
      node-pre :
        {
          position: position,
          nodeType: node['nodeType'],
          text: node['nodeValue'],
        },
      node-post : null,
      style : null,
      recursive: !isWrapper
      visible : visible,
    }
    */
    obj.add(
      REMOVE,
      {
        'node-pre': {
          'position': position,
          'nodeType': node['nodeType'],
          'text': node['nodeValue'],
          'tag': node['tagName']
        },
        'node-post': null,
        'style' : null,
        'recursive': !isWrapper,
        'visible' : visible
      }
    );


    return node;
  };

  obj.updateText = function(position, visible, newText) {
    var node = obj.getNode(position);
    if (node == null || node.nodeType != 3) {
      console.log('Invalid operation');
      return;
    }
    node['nodeValue'] = newText;

    /*
    {
      node-pre :
        {
          position: position,
          nodeType: node['nodeType'],
          text: node['nodeValue'],
        },
      node-post :
        {
          position: position,
          nodeType: node['nodeType'],
          text: newText,
        },
      style : null,
      visible : visible,
    }
    */

    obj.add(
      UPDATE,
      {
        'node-pre': {
          'position': position,
          'nodeType': node['nodeType'],
          'text': node['nodeValue']
        },
        'node-post': {
          'position': position,
          'nodeType': node['nodeType'],
          'text': newText
        },
        'style' : null,
        'recursive': false,
        'visible' : visible
      }
    );

    return node;
  };

  obj.updateTag = function(position, visible, newId, newClass) {
    var node = obj.getNode(position);
    if (node == null || node.nodeType != 1) {
      console.log('Invalid operation');
      return;
    }
    var nodeId = node.id;
    var nodeClass = node.className;

    if (newId != null) {
      node.id = newId;
    } else {
      newId = node.id;
    }
    if (newClass != null) {
      node.className = newClass;
    } else {
      newClass = node.className
    }

    /*
    {
      node-pre :
        {
          position: position,
          nodeType: node['nodeType'],
          attr: {
            'id' : nodeId,
            'class' : nodeClass,
          },
        },
      node-post :
        {
          position: position,
          nodeType: node['nodeType'],
          attr: {
            'id' : newId,
            'class' : newClass,
          },
        },
      style : null,
      visible : visible,
    }
    */
    obj.add(
      UPDATE,
      {
        'node-pre': {
          'position': position,
          'nodeType': node['nodeType'],
          'attr': {
            'id' : nodeId,
            'class' : nodeClass,
          }
        },
        'node-post': {
          'position': position,
          'nodeType': node['nodeType'],
          'attr': {
            'id' : newId,
            'class' : newClass,
          }
        },
        'style' : null,
        'recursive': visible,
        'visible' : visible
      }
    );

    return node;
  };


  obj.match = function(position, visible, prop, value) {
    var node = obj.getNode(position);

    preStyles = DomVRT.Extractor.getAllStyles(node);
    preStyles = JSON.parse(JSON.stringify(preStyles))

    node.style[prop] = value;

    postStyles = DomVRT.Extractor.getAllStyles(node);
    postStyles = JSON.parse(JSON.stringify(postStyles))

    // console.log('Map');
    // console.log(preStyles);
    // console.log(postStyles);

    var styleDiff = [];
    Array.prototype.forEach.call(Object.keys(postStyles), function(property) {
      if (preStyles[property] != postStyles[property]) {
        console.log('Style diff: {%s} - `%s` | `%s` ', property, preStyles[property], postStyles[property]);
        styleDiff.push([
          preStyles[property],
          postStyles[property],
          property
        ])
      }

    });

    /*
    {
      node-pre :
        {
          position: position,
          nodeType: 1,
        },
      node-post :
        {
          position: position,
          nodeType: 1,
        },
      style : styleDiff,
      visible : visible,
    }
    */
    obj.add(
      MATCH,
      {
        'node-pre': {
          'position': position,
          'nodeType': 1
        },
        'node-post': {
          'position': position,
          'nodeType': 1
        },
        'style' : styleDiff,
        'recursive': visible,
        'visible' : visible
      }
    );

    return node;
  };

  obj.add = function(type, data) {
    if ([MATCH, UPDATE, INSERT, REMOVE].indexOf(type) == -1) {
      console.log('Type: %s not found');
      return;
    }
    console.log("type is %s", type);

    obj.mutations[type].push(data);
  }

  var dts = function(digit) {
    if (digit < 10) {
      return '0' + digit;
    }
    return '' + digit;
  };

  obj.saveMutations = function(filename) {
    if (filename == null) {
      var d = new Date();
      var timeStr = d.getFullYear() + '-' + dts(d.getMonth() + 1) + '-' +
       dts(d.getDate()) + '--' + dts(d.getHours()) + '-' + dts(d.getMinutes() +
        '-' + dts(d.getSeconds()));

      var host = (window.location.host).replace('.', '-');

      filename = host + '--' + timeStr + '-mutation.json';
    }

    var blob = new Blob([JSON.stringify(obj.mutations)], {type: "application/json;charset=utf-8"});
    saveAs(blob, filename);

    return obj.mutations;
  };

  return obj;

}) (DomVRT.Differ || {});

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
    // filename = filename ? filename : getFilename();

    // html2canvas(document.querySelector('html')).then(canvas => {
    //   canvas.toBlob(function(blob) {
    //     saveAs(blob, filename + '.png');
    //   });
    // });


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

DomVRT.Utils = (function (obj) {

  // http://www.myersdaily.org/joseph/javascript/md5.js
  function md5cycle(x, k) {
    var a = x[0], b = x[1], c = x[2], d = x[3];

    a = ff(a, b, c, d, k[0], 7, -680876936);
    d = ff(d, a, b, c, k[1], 12, -389564586);
    c = ff(c, d, a, b, k[2], 17,  606105819);
    b = ff(b, c, d, a, k[3], 22, -1044525330);
    a = ff(a, b, c, d, k[4], 7, -176418897);
    d = ff(d, a, b, c, k[5], 12,  1200080426);
    c = ff(c, d, a, b, k[6], 17, -1473231341);
    b = ff(b, c, d, a, k[7], 22, -45705983);
    a = ff(a, b, c, d, k[8], 7,  1770035416);
    d = ff(d, a, b, c, k[9], 12, -1958414417);
    c = ff(c, d, a, b, k[10], 17, -42063);
    b = ff(b, c, d, a, k[11], 22, -1990404162);
    a = ff(a, b, c, d, k[12], 7,  1804603682);
    d = ff(d, a, b, c, k[13], 12, -40341101);
    c = ff(c, d, a, b, k[14], 17, -1502002290);
    b = ff(b, c, d, a, k[15], 22,  1236535329);

    a = gg(a, b, c, d, k[1], 5, -165796510);
    d = gg(d, a, b, c, k[6], 9, -1069501632);
    c = gg(c, d, a, b, k[11], 14,  643717713);
    b = gg(b, c, d, a, k[0], 20, -373897302);
    a = gg(a, b, c, d, k[5], 5, -701558691);
    d = gg(d, a, b, c, k[10], 9,  38016083);
    c = gg(c, d, a, b, k[15], 14, -660478335);
    b = gg(b, c, d, a, k[4], 20, -405537848);
    a = gg(a, b, c, d, k[9], 5,  568446438);
    d = gg(d, a, b, c, k[14], 9, -1019803690);
    c = gg(c, d, a, b, k[3], 14, -187363961);
    b = gg(b, c, d, a, k[8], 20,  1163531501);
    a = gg(a, b, c, d, k[13], 5, -1444681467);
    d = gg(d, a, b, c, k[2], 9, -51403784);
    c = gg(c, d, a, b, k[7], 14,  1735328473);
    b = gg(b, c, d, a, k[12], 20, -1926607734);

    a = hh(a, b, c, d, k[5], 4, -378558);
    d = hh(d, a, b, c, k[8], 11, -2022574463);
    c = hh(c, d, a, b, k[11], 16,  1839030562);
    b = hh(b, c, d, a, k[14], 23, -35309556);
    a = hh(a, b, c, d, k[1], 4, -1530992060);
    d = hh(d, a, b, c, k[4], 11,  1272893353);
    c = hh(c, d, a, b, k[7], 16, -155497632);
    b = hh(b, c, d, a, k[10], 23, -1094730640);
    a = hh(a, b, c, d, k[13], 4,  681279174);
    d = hh(d, a, b, c, k[0], 11, -358537222);
    c = hh(c, d, a, b, k[3], 16, -722521979);
    b = hh(b, c, d, a, k[6], 23,  76029189);
    a = hh(a, b, c, d, k[9], 4, -640364487);
    d = hh(d, a, b, c, k[12], 11, -421815835);
    c = hh(c, d, a, b, k[15], 16,  530742520);
    b = hh(b, c, d, a, k[2], 23, -995338651);

    a = ii(a, b, c, d, k[0], 6, -198630844);
    d = ii(d, a, b, c, k[7], 10,  1126891415);
    c = ii(c, d, a, b, k[14], 15, -1416354905);
    b = ii(b, c, d, a, k[5], 21, -57434055);
    a = ii(a, b, c, d, k[12], 6,  1700485571);
    d = ii(d, a, b, c, k[3], 10, -1894986606);
    c = ii(c, d, a, b, k[10], 15, -1051523);
    b = ii(b, c, d, a, k[1], 21, -2054922799);
    a = ii(a, b, c, d, k[8], 6,  1873313359);
    d = ii(d, a, b, c, k[15], 10, -30611744);
    c = ii(c, d, a, b, k[6], 15, -1560198380);
    b = ii(b, c, d, a, k[13], 21,  1309151649);
    a = ii(a, b, c, d, k[4], 6, -145523070);
    d = ii(d, a, b, c, k[11], 10, -1120210379);
    c = ii(c, d, a, b, k[2], 15,  718787259);
    b = ii(b, c, d, a, k[9], 21, -343485551);

    x[0] = add32(a, x[0]);
    x[1] = add32(b, x[1]);
    x[2] = add32(c, x[2]);
    x[3] = add32(d, x[3]);

  }

  function cmn(q, a, b, x, s, t) {
    a = add32(add32(a, q), add32(x, t));
    return add32((a << s) | (a >>> (32 - s)), b);
  }

  function ff(a, b, c, d, x, s, t) {
    return cmn((b & c) | ((~b) & d), a, b, x, s, t);
  }

  function gg(a, b, c, d, x, s, t) {
    return cmn((b & d) | (c & (~d)), a, b, x, s, t);
  }

  function hh(a, b, c, d, x, s, t) {
    return cmn(b ^ c ^ d, a, b, x, s, t);
  }

  function ii(a, b, c, d, x, s, t) {
    return cmn(c ^ (b | (~d)), a, b, x, s, t);
  }

  function md51(s) {
    txt = '';
    var n = s.length,
    state = [1732584193, -271733879, -1732584194, 271733878], i;
    for (i=64; i<=s.length; i+=64) {
      md5cycle(state, md5blk(s.substring(i-64, i)));
    }
    s = s.substring(i-64);
    var tail = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0];
    for (i=0; i<s.length; i++)
    tail[i>>2] |= s.charCodeAt(i) << ((i%4) << 3);
    tail[i>>2] |= 0x80 << ((i%4) << 3);
    if (i > 55) {
    md5cycle(state, tail);
    for (i=0; i<16; i++) tail[i] = 0;
    }
    tail[14] = n*8;
    md5cycle(state, tail);
    return state;
  }

  /* there needs to be support for Unicode here,
   * unless we pretend that we can redefine the MD-5
   * algorithm for multi-byte characters (perhaps
   * by adding every four 16-bit characters and
   * shortening the sum to 32 bits). Otherwise
   * I suggest performing MD-5 as if every character
   * was two bytes--e.g., 0040 0025 = @%--but then
   * how will an ordinary MD-5 sum be matched?
   * There is no way to standardize text to something
   * like UTF-8 before transformation; speed cost is
   * utterly prohibitive. The JavaScript standard
   * itself needs to look at this: it should start
   * providing access to strings as preformed UTF-8
   * 8-bit unsigned value arrays.
   */
  function md5blk(s) { /* I figured global was faster.   */
    var md5blks = [], i; /* Andy King said do it this way. */
    for (i=0; i<64; i+=4) {
    md5blks[i>>2] = s.charCodeAt(i)
    + (s.charCodeAt(i+1) << 8)
    + (s.charCodeAt(i+2) << 16)
    + (s.charCodeAt(i+3) << 24);
    }
    return md5blks;
  }

  var hex_chr = '0123456789abcdef'.split('');

  function rhex(n)
  {
    var s='', j=0;
    for(; j<4; j++)
    s += hex_chr[(n >> (j * 8 + 4)) & 0x0F]
    + hex_chr[(n >> (j * 8)) & 0x0F];
    return s;
  }

  function hex(x) {
    for (var i=0; i<x.length; i++)
      x[i] = rhex(x[i]);
    return x.join('');
  }

  function md5(s) {
    return hex(md51(s));
  }

  obj.md5 = function(s) {
    return md5(s);
  }

  /* this function is much faster,
  so if possible we use it. Some IEs
  are the only ones I know of that
  need the idiotic second function,
  generated by an if clause.  */

  function add32(a, b) {
    return (a + b) & 0xFFFFFFFF;
  }

  if (md5('hello') != '5d41402abc4b2a76b9719d911017c592') {
    function add32(x, y) {
      var lsw = (x & 0xFFFF) + (y & 0xFFFF),
          msw = (x >> 16) + (y >> 16) + (lsw >> 16);
      return (msw << 16) | (lsw & 0xFFFF);
    }
  }

  return obj;

}) (DomVRT.Utils || {});

// Export module to node.
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = DomVRT;
}
