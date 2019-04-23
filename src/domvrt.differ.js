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
        console.log(newPos);
        var child = obj.findNode(n, newPos, toFind, setPosition, depth + 1);

        if (child['valid']) {
          index++;
        }
        if (child['found']) {
          // Can't return directly inside foreach loop.
          toReturn = child;
        }

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

    return {
      'found' : false,
      'valid' : true
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
    }
    if (newClass != null) {
      node.className = newClass;
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


    preStyles = window.getComputedStyle(node, null);
    preStyles = JSON.parse(JSON.stringify(preStyles))

    node.style[prop] = value;

    postStyles = window.getComputedStyle(node, null);
    var styleDiff = []
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
