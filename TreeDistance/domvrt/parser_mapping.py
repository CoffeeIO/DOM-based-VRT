class ParserMapping(object):
    """
    The ParserMapping class was an attempt to create an abstraction layer
    between stored DOM and property names.
    From this smaller extraction files could be saved.
    The class is still used in certain part, but is not fully supported.
    """
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

    def get_mapping_names(self):
        tagName = self.get('tagName')
        nodeType = self.get('nodeType')
        nodeName = self.get('nodeName')
        nodeValue = self.get('nodeValue')
        position = self.get('position')
        childNodes = self.get('childNodes')
        attrs = self.get('attrs')

        return (tagName, nodeType, nodeName, nodeValue, position, childNodes, attrs)
