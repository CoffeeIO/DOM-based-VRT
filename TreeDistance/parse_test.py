import domvrt

parser = domvrt.parser.Parser()
differ = domvrt.differ.Differ()
tester = domvrt.tester.Tester()

before_obj = parser.parse('github-com--2019-02-23--17-5-08.json')
before_root = parser.to_tree(before_obj)

parser.print_tree(before_root)

after_obj = parser.parse('github-com--2019-02-23--17-5-08-(1).json')
after_root = parser.to_tree(after_obj)

parser.print_tree(after_root)

tester.generate_test(True);
