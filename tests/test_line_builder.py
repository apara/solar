import unittest

from reader.line import *
from reader.line_builder import LinesFactory, LineFactory, LineBuilder130, LineBuilder140

__GLOBAL_DATE = '20170607165000'

class TestLineBuilder130(unittest.TestCase):

    def test_build(self):
        result = LineBuilder130().build(['130', '20170607165000'])
        self.assertIsNot(result, emptyLine, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder130().build(['120', '20170607165000'])
        self.assertIs(result, emptyLine, 'result must be emptyLine')


class TestLineBuilder140(unittest.TestCase):

    def test_build(self):
        result = LineBuilder140().build(['140', '20170607165000'])
        self.assertIsNot(result, emptyLine, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder140().build(['120', '20170607165000'])
        self.assertIs(result, emptyLine, 'result must be emptyLine')


class TestLineFactory(unittest.TestCase):
    def test_line_builder(self):

        factory = LineFactory()

        result = factory.build('130\t20170607165000')
        self.assertIsInstance(result, Line130)

        result = factory.build('140\t20170607165000')
        self.assertIsInstance(result, Line140)

        result = factory.build('150\t20170607165000')
        self.assertEqual(result, emptyLine)


class TestLinesFactory(unittest.TestCase):

    __DATA = \
        '130\t20170607165000\n' \
        '140\t20170607165000\n' \
        '150\t20170607165000\n'
            
    def test_lines_builder(self):
        factory = LinesFactory()
        results = factory.build(self.__DATA)
        self.assertEqual(len(results), 2)

        with open("tests/test_line_builder.txt", "r") as file:
            data = file.read()
            results = factory.build(data)
            self.assertEqual(len(results), 22)

            for l in results:
                print(l)


