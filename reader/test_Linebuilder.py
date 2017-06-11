import unittest
from reader.Linebuilder import LinesFactory, LineFactory, LineBuilder130, LineBuilder140
from reader.Line import *


class TestLineBuilder130(unittest.TestCase):

    def test_build(self):
        result = LineBuilder130().build(['130', 'foo'])
        self.assertIsNot(result, emptyLine, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder130().build(['120', 'foo'])
        self.assertIs(result, emptyLine, 'result must be emptyLine')


class TestLineBuilder140(unittest.TestCase):

    def test_build(self):
        result = LineBuilder140().build(['140', 'foo'])
        self.assertIsNot(result, emptyLine, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder140().build(['120', 'foo'])
        self.assertIs(result, emptyLine, 'result must be emptyLine')


class TestLineFactory(unittest.TestCase):
    def test_line_builder(self):

        factory = LineFactory()

        result = factory.build('130\tfoo')
        self.assertIsInstance(result, Line130)

        result = factory.build('140\tfoo')
        self.assertIsInstance(result, Line140)

        result = factory.build('150\tfoo')
        self.assertEqual(result, emptyLine)


class TestLinesFactory(unittest.TestCase):

    __DATA = \
        '130\tfoo\n' \
        '140\tfoo\n' \
        '150\tfoo\n' 

    def test_lines_builder(self):
        factory = LinesFactory()
        result = factory.build(self.__DATA)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()

