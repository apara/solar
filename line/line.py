from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *


class LineId(str):
    def __init__(self, value=None):
        str.__init__(value)


class Line:

    def __init__(self, lid=None, array=None):
        # Assign id of the line
        #
        self.id = lid

        # Assign type of the line
        #
        if array:
            self.type = array[0]
            self.ts = self.parse_date(array[1])
            self.serial = array[2]
            self.description = array[3]
            self.total_lifetime_energy_kwh = array[4]

    def __str__(self):
        return \
            self.pv('id') + \
            self.pv('type') + \
            self.pv('ts') + \
            self.pv('serial') + \
            self.pv('description') + \
            self.pv('total_lifetime_energy_kwh')

    @staticmethod
    def parse_date(value):
        return datetime.strptime(value, '%Y%m%d%H%M%S')

    def pv(self, attribute_name):
        return ' ' + attribute_name + ': ' + self.vn(attribute_name)

    def vn(self, attribute_name):
        value = getattr(self, attribute_name)
        return str(value) if value else 'None'


empty_line = Line()


# Type 130
#
class Line130(Line):
    def __init__(self, lid=None, array=None):
        Line.__init__(self, lid, array)
        if array:
            self.avg_ac_power_kw = float(array[5])
            self.avg_ac_voltage_v = float(array[6])
            self.avg_ac_current_a = float(array[7])
            self.avg_dc_power_kw = float(array[8])
            self.avg_dc_voltage_v = float(array[9])
            self.avg_dc_current_a = float(array[10])
            self.inverter_temp_c = float(array[11])
            self.avg_op_frequency_hz = float(array[12])
            self.unknown = array[13]

            self.inverter_temp_f = self.inverter_temp_c * 9.0 / 5.0 + 32.0

    def __str__(self):
        return \
            Line.__str__(self) + \
            self.pv('avg_ac_power_kw') + \
            self.pv('avg_ac_voltage_v') + \
            self.pv('avg_ac_current_a') + \
            self.pv('avg_dc_power_kw') + \
            self.pv('avg_dc_voltage_v') + \
            self.pv('avg_dc_current_a') + \
            self.pv('inverter_temp_c') + \
            self.pv('inverter_temp_f') + \
            self.pv('avg_op_frequency_hz') + \
            self.pv('unknown')


# Type 140
#
class Line140(Line):
    def __init__(self, lid=None, array=None):
        Line.__init__(self, lid, array)



metadata = MetaData()

# Define line table
#
lineTable = Table(
    'line',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement="auto"),
    Column('type', Integer, nullable=False),
    Column('ts', DateTime, nullable=False),
    Column('serial', String, nullable=False),
    Column('description', String, nullable=False),
    Column('total_lifetime_energy_kwh', Float, nullable=False),
    Column('avg_ac_power_kw', Float),
    Column('avg_ac_voltage_v', Float),
    Column('avg_ac_current_a', Float),
    Column('avg_dc_power_kw', Float),
    Column('avg_dc_voltage_v', Float),
    Column('avg_dc_current_a', Float),
    Column('inverter_temp_c', Float),
    Column('avg_op_frequency_hz', Float),
    Column('unknown', String),
    Column('inverter_temp_f', Float),
)

# Add index
#
Index('idx_line_type_ts_serial', lineTable.c.type, lineTable.c.serial, lineTable.c.ts, unique=True)


