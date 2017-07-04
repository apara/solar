import unittest
import json

from line.line import *
from line.line_builder import LinesFactory, LineFactory, LineBuilder130, LineBuilder140

data_130 = '{"ISDETAIL":"1","SERIAL":"414051706011633","TYPE":"SOLARBRIDGE","STATE":"working","STATEDESCR":"Working","MODEL":"AC_Module_Type_C","DESCR":"Inverter 414051706011633","DEVICE_TYPE":"Inverter","SWVER":"951007408","PORT":"","MOD_SN":"","NMPLT_SKU":"","DATATIME":"2017,07,02,03,05,14","ltea_3phsum_kwh":"58.7856","p_3phsum_kw":"0","vln_3phavg_v":"249.2725","i_3phsum_a":"0","p_mpptsum_kw":"0","v_mppt1_v":"55.5546","i_mppt1_a":"-0.0333","t_htsnk_degc":"26.75","freq_hz":"60.0096","CURTIME":"2017,07,02,03,12,10"}'
data_json_130 = json.loads(data_130)

data_140 = '{"ISDETAIL":"1","SERIAL":"PVS5M562239c","TYPE":"PVS5-METER-C","STATE":"working","STATEDESCR":"Working","MODEL":"PVS5M0400c","DESCR":"Power Meter PVS5M562239c","DEVICE_TYPE":"Power Meter","SWVER":"4","PORT":"","DATATIME":"2017,07,02,03,11,59","ct_scl_fctr":"100","net_ltea_3phsum_kwh":"-293.69","p_3phsum_kw":"1.0417","q_3phsum_kvar":"1.1489","s_3phsum_kva":"1.6128","tot_pf_rto":"0.6459","freq_hz":"60","CAL0":"100","CURTIME":"2017,07,02,03,12,08"}'
data_json_140 = json.loads(data_140)

data_invalid = '{"ISDETAIL":"1","SERIAL":"PVS5M562239c","TYPE":"PVS5-METER-C","STATE":"working","STATEDESCR":"Working","MODEL":"PVS5M0400c","DESCR":"Power Meter PVS5M562239c","DEVICE_TYPE":"FOO","SWVER":"4","PORT":"","DATATIME":"2017,07,02,03,11,59","ct_scl_fctr":"100","net_ltea_3phsum_kwh":"-293.69","p_3phsum_kw":"1.0417","q_3phsum_kvar":"1.1489","s_3phsum_kva":"1.6128","tot_pf_rto":"0.6459","freq_hz":"60","CAL0":"100","CURTIME":"2017,07,02,03,12,08"}'
data_json_invalid = json.loads(data_invalid)

data_130_invalid ='{"ISDETAIL":"1","SERIAL":"414051706011633","TYPE":"SOLARBRIDGE","STATE":"working","STATEDESCR":"Working","MODEL":"AC_Module_Type_C","DESCR":"Inverter 414051706011633","DEVICE_TYPE":"Inverter","SWVER":"951007408","PORT":"","MOD_SN":"","NMPLT_SKU":"","DATATIME":"2017,07,02,03,05,14","ltea_3phsum_kwh":"FOO","p_3phsum_kw":"0","vln_3phavg_v":"249.2725","i_3phsum_a":"0","p_mpptsum_kw":"0","v_mppt1_v":"55.5546","i_mppt1_a":"-0.0333","t_htsnk_degc":"26.75","freq_hz":"60.0096","CURTIME":"2017,07,02,03,12,10"}'

data_json_130_invalid = json.loads(data_130_invalid)


class TestGeneral(unittest.TestCase):
    def test_parse_date(self):
        ts = Line.parse_date('2017,06,07,16,50,00')
        print "TS : " + str(ts)


class TestLineBuilder130(unittest.TestCase):

    def test_build(self):
        result = LineBuilder130().build(data_json_130)
        self.assertIsNot(result, empty_line, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder130().build(data_json_invalid)
        self.assertIs(result, empty_line, 'result must be emptyLine')


class TestLineBuilder140(unittest.TestCase):

    def test_build(self):
        result = LineBuilder140().build(data_json_140)
        self.assertIsNot(result, empty_line, 'result must not be an emptyLine')

    def test_build_not(self):
        result = LineBuilder140().build(data_json_invalid)
        self.assertIs(result, empty_line, 'result must be emptyLine')


class TestLineFactory(unittest.TestCase):
    def test_line_builder(self):

        factory = LineFactory()

        result = factory.build(data_json_130)
        self.assertIsInstance(result, Line130)

        result = factory.build(data_json_140)
        self.assertIsInstance(result, Line140)

        result = factory.build(data_json_invalid)
        self.assertEqual(result, empty_line)

        result = factory.build(data_json_130_invalid)
        self.assertIs(empty_line, result)


class TestLinesFactory(unittest.TestCase):

    def test_lines_builder(self):
        factory = LinesFactory()

        with open("tests/test_line_builder.txt", "r") as file:
            data = file.read()
            results = factory.build(json.loads(data))
            self.assertEqual(len(results), 22)

            for l in results:
                print(l)


