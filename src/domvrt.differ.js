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
    obj.findNode(document, '1', null, true);
    return obj.nodeCount;
  };

  obj.nodeCount = 0;

  obj.findNode = function(node, position, toFind, setPosition) {
    position = (position == null) ? 1 : position;
    node = node || this;

    // Define node.
    var json = {};

    if (node.nodeValue) {
      value = node.nodeValue
      if (value.trim() == '') { // Ignore empty text nodes
        return {
          'valid' : false
        };
      }
    }

    if (node.nodeType == 1) {
      node.setAttribute("p", position);
      if (position == toFind) {
        return {
          'found' : true,
          'valid' : true,
          'node'  : node
        };
      }
    }

    // Loop children.
    if (node.childNodes) {
      var index = 0;
      Array.prototype.forEach.call(node.childNodes, function(n) {

        var newPos = position + '.' + index;

        var child = obj.findNode(n, newPos, toFind, setPosition);

        if (child['valid']) {
          index++;
        }
        if (child['found']) {
          return child;
        }

      });
    }

    obj.nodeCount++;

    return {
      'found' : false,
      'valid' : true
    };
  }

  obj.add = function(position, type, style, visible, affectChildren) {
    if ([MATCH, UPDATE, INSERT, REMOVE].indexOf(type) == -1) {
      console.log('Type: %s not found');
      return;
    }
    console.log("type is %s", type);

    var node = document.querySelector('*[p="' + position + '"]');
    if (node == null) {
      var result = obj.findNode(document, '1', position);
      if (result['node']) {
        node = result['node'];
      }
    }

    if (node == null) {
      console.log('Element not found');
      return;
    }


    // Find element and perform change.
    document.querySelector('*')
    if (type == MATCH) {

    } else if (type == UPDATE) {

    } else if (type == INSERT) {

    } else if (type == REMOVE) {

      if (affectChildren) {

      } else {

      }
    }

    obj.mutations[type].push({
      'position' : position,
      'style'    : style,
      'visible'  : visible,
      'affect-children' : affectChildren
    })
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
