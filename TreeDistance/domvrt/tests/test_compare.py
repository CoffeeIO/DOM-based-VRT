from zss import simple_distance, Node, distance as strdist


def strdist(a, b):
        if a == b:
            return 0
        else:
            return 1

def simple_trees():
    A = (
        Node("f")
            .addkid(Node("d")
                .addkid(Node("a"))
                .addkid(Node("c")
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    B = (
        Node("f")
            .addkid(Node("c")
                .addkid(Node("d")
                    .addkid(Node("a"))
                    .addkid(Node("b"))))
            .addkid(Node("e"))
        )
    return A, B

def trees1(): # Random
    A = (
    Node("a")
        .addkid(Node("b")
            .addkid(Node("c"))
            .addkid(Node("d")
                .addkid(Node("e"))
                .addkid(Node("t"))
                .addkid(Node("p"))))
        .addkid(Node("f"))
    )

    B = (
    Node("a")
        .addkid(Node("b")
            .addkid(Node("l"))
            .addkid(Node("d")
                .addkid(Node("e"))
                .addkid(Node("p"))))
        .addkid(Node("f"))
        .addkid(Node("y"))
    )
    return A, B

def trees2(): # Only delete
    A = (
    Node("a")
        .addkid(Node("b")
            .addkid(Node("c")
                .addkid(Node("d")))
            )
    )

    B = (
    Node("a")
    )
    return A, B

def trees3(): # Only insert
    B = (
    Node("a")
        .addkid(Node("b")
            .addkid(Node("c")
                .addkid(Node("d")))
            )
    )

    A = (
    Node("a")
    )
    return A, B

def trees4(): # Only substitution
    A = (
    Node("a")
        .addkid(Node("f")
            .addkid(Node("g")
                .addkid(Node("d")))
            )
    )

    B = (
    Node("a")
        .addkid(Node("b")
            .addkid(Node("c")
                .addkid(Node("d")))
            )
    )
    return A, B

def test_nodes_1():
    (A, B) = trees1()
    expected = 3.0
    dist = simple_distance(A, B, Node.get_children, Node.get_label, strdist, True)
    print("Expected", expected, "Actual", dist[0])
    assert dist[0] == expected

def test_nodes_2():
    (A, B) = trees2()
    expected = 3.0
    dist = simple_distance(A, B, Node.get_children, Node.get_label, strdist, True)
    print("Expected", expected, "Actual", dist[0])
    assert dist[0] == expected

def test_nodes_3():
    (A, B) = trees3()
    expected = 3.0
    dist = simple_distance(A, B, Node.get_children, Node.get_label, strdist, True)
    print("Expected", expected, "Actual", dist[0])
    assert dist[0] == expected

def test_nodes_4():
    (A, B) = trees4()
    dist = simple_distance(A, B, Node.get_children, Node.get_label, strdist, True)
    expected = 2.0
    print("Expected", expected, "Actual", dist[0])
    assert dist[0] == expected
