import domvrt

test_tree = domvrt.TestTree()

def run_netflix():
    f = "netflix--"
    basef = "www-netflix.com--"

    comb = basef + "comb"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"
    pos = basef + "element-pos"
    dim = basef + "element-dim"
    base1 = basef + "default"

    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")

def run_fitness():
    f = "fitness--"
    basef = "www-fitnessworld.com--"
    comb = basef + "comb"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"
    pos = basef + "element-pos"
    dim = basef + "element-dim"
    base1 = basef + "default"

    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")

def run_wiki():
    f = "wiki--"
    basef = "en-wikipedia.org--"

    comb = basef + "comb"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"
    pos = basef + "element-pos"
    dim = basef + "element-dim"
    base1 = basef + "default"
    base2 = basef + "default2"

    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base2, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")

def run_apple():
    f = "apple--"
    basef = "www-apple.com--"

    comb = basef + "comb"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"
    pos = basef + "element-pos"
    dim = basef + "element-dim"
    base1 = basef + "default"

    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")

def run_github():
    f = "github--"
    basef = "github-com--"

    comb = basef + "comb"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"
    pos = basef + "element-pos"
    dim = basef + "element-dim"
    base1 = basef + "default"

    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")



def run_eboks():
    f = "eboks--"
    basef = "www-e-boks.com--"

    base1 = basef + "default"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"

    pos = basef + "element-pos"
    dim = basef + "element-dim"
    comb = basef + "comb"


    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")

def run_medium():
    f = "medium--"
    basef = "medium-com--"

    base1 = basef + "default"
    remove = basef + "remove"
    insert = basef + "insert"
    update = basef + "update"
    style = basef + "element-style"

    pos = basef + "element-pos"
    dim = basef + "element-dim"
    comb = basef + "comb"


    run(base1, remove, f + "remove")
    run(base1, insert, f + "insert")
    run(base1, update, f + "update")
    run(base1, style, f + "element-style")
    run(base1, pos, f + "element-pos")
    run(base1, dim, f + "element-dim")
    run(base1, comb, f + "comb")


def run(file1, file2, folder):
    f = "data-test/"
    d = "data-test/"
    json = ".json"
    png = ".png"

    img1 = d + file1 + png
    img2 = d + file2 + png

    file1 = f + file1 + json
    file2 = f + file2 + json

    test_tree.diff(file1, file2, 'custom', folder + '--custom-', img1, img2, True)
    test_tree.diff(file1, file2, 'zhang', folder + '--zhang-', img1, img2, True)


run_netflix()
run_fitness()
run_wiki()
run_apple()
run_github()
run_medium()
run_eboks()
