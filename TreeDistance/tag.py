from yattag import Doc

doc, tag, text = Doc().tagtext()

body = 'body'
children = ['div']

div = 'div'
cl = {'class': 'closed'}

node = {
    'tag' : 'body',
    'text': 'outer1',
    'childNodes': [
        {
            'tag' : 'div',
            'text' : 'inner1',
            'childNodes' : []
        },
        {
            'tag' : 'div',
            'text' : 'inner2',
            'childNodes' : []
        }
    ],
}

def print_html(node):

    with tag(node['tag']):
        text(node['text'])
        for n in node['childNodes']:
            print_html(n)

print_html(node)

print(doc.getvalue())
