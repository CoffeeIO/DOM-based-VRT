import codecs

def save_file(content, filename):
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()
