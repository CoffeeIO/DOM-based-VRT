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

  return obj;

}) (DomVRT.Differ || {});
