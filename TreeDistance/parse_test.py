import domvrt

parser = domvrt.parser.Parser()
differ = domvrt.differ.Differ()
tester = domvrt.tester.Tester()

before_obj = parser.parse('github-com--2019-02-23--17-5-08.json')
before_root = parser.toTree(before_obj)

parser.printTree(before_root)

after_obj = parser.parse('github-com--2019-02-23--17-5-08-(1).json')
after_root = parser.toTree(after_obj)

parser.printTree(after_root)


tester.generate_test();
