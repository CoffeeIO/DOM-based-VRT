from yattag import Doc

doc, tag, text = Doc().tagtext()

attr_map = {
    'id': 'test'
}

# id = ('id', 'test')
# attr = (('id', 'test'), ('class', 'ctest'))
with tag('h1'):
    doc.attr(('id', 'test'))
    doc.attr(('class', 'ctest'))
    text('Hello world!')

print(doc.getvalue())
