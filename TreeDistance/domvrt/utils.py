import codecs

"""
Utils file for general functions to use across classes.
"""
def save_file(content, filename):
    file = codecs.open(filename, "w", "utf-8")
    file.write(content)
    file.close()

def number_to_string(number):
    if number < 10:
        return '000' + str(number)
    elif number < 100:
        return '00' + str(number)
    elif number < 1000:
        return '0' + str(number)

    return str(number)
