class ParserMapping(object):
    """docstring for ParserMapping."""

    def __init__(self, minify):
        self.minify = minify
        self.mVal = 1 if minify else 0

    mVal = 0

    # Mapping of minified names.
    jsonMapping = {
      'nodeType':   ['nodeType', 'nt'],
      'tagName':    ['tagName', 'tn'],
      'nodeName':   ['nodeName', 'nn'],
      'nodeValue':  ['nodeValue', 'nv'],
      'attrs':      ['attrs', 'at'],
      'styles':     ['styles', None],
      'styleId':    ['styleId', 'si'],
      'styleSum':   ['styleSum', 'ss'],
      'childNodes': ['childNodes', 'c'],
      'level':      ['level', 'l'],
      'position':   ['position', 'p'],
    }

    def get(self, name):
        return self.jsonMapping[name][self.mVal]
