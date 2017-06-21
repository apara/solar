import unittest

from line.line import *
from line.line_builder import LinesFactory, LineFactory, LineBuilder130, LineBuilder140

data_130 = '130	20170607165000	414051708000326	AC_Module_Type_C		2.6567	0.1372	250.4849	0.6821	0.1425	56.1571	2.8915	32	60.0186	0'
data_array_130 = data_130.split()
data_140 = '140	20170607165000	PVS5M562239c	PVS5M0400c	100	2.58	-2.1741	0.9378	2.4009	-0.896	60	0'
data_array_140 = data_140.split()
data_invalid = '999	20170607165000	PVS5M562239c	PVS5M0400c	100	2.58	-2.1741	0.9378	2.4009	-0.896	60	0'
data_array_invalid = data_invalid.split()
data_130_invalid = '130	20170607165000	414051708000326	AC_Module_Type_C		2.6567	0.1372	250.4849POST'
data_array_130_invalid = data_130_invalid.split()


class TestLineBuilder130(unittest.TestCase):

    def test_build(self):
        result = LineBuilder130().build(data_array_130)
        self.assertIsNot(result, empty_line, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder130().build(data_array_invalid)
        self.assertIs(result, empty_line, 'result must be emptyLine')


class TestLineBuilder140(unittest.TestCase):

    def test_build(self):
        result = LineBuilder140().build(data_array_140)
        self.assertIsNot(result, empty_line, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder140().build(data_array_invalid)
        self.assertIs(result, empty_line, 'result must be emptyLine')


class TestLineFactory(unittest.TestCase):
    def test_line_builder(self):

        factory = LineFactory()

        result = factory.build(data_130)
        self.assertIsInstance(result, Line130)

        result = factory.build(data_140)
        self.assertIsInstance(result, Line140)

        result = factory.build(data_invalid)
        self.assertEqual(result, empty_line)

        result = factory.build(data_130_invalid)
        self.assertIs(empty_line, result)


class TestLinesFactory(unittest.TestCase):

    __DATA = \
        data_130 + '\n' + \
        data_140 + '\n' + \
        data_invalid + '\n'
            
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


