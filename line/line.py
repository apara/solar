from datetime import datetime
from .db import *
from pytz import UTC


class LineId(str):
    def __init__(self, value=None):
        str.__init__(value)


class Line:

    def __init__(self, lid=None, device=None):
        # Assign id of the line
        #
        self.id = lid

        # Assign type of the line
        #
        if device:
            self.ts = self.parse_date(device['DATATIME'])
            self.serial = device['SERIAL']
            self.description = device['DESCR']

    def __str__(self):
        return \
            self.pv('id') + \
            self.pv('type') + \
            self.pv('ts') + \
            self.pv('serial') + \
            self.pv('description') 

    @staticmethod
    def parse_date(value):
        return datetime.strptime(value, '%Y,%m,%d,%H,%M,%S').replace(tzinfo=UTC)

    def pv(self, attribute_name):
        return ' ' + attribute_name + ': ' + self.vn(attribute_name)

    def vn(self, attribute_name):
        value = getattr(self, attribute_name)
        return str(value) if value is not None else 'None'

    def to_dbline(self):
        return DbLine().from_line(self)


empty_line = Line()


# Type 130
#
class Line130(Line):
    def __init__(self, lid=None, device=None):
        Line.__init__(self, lid, device)
        self.type = 130

        if device:
            self.total_lifetime_energy_kwh = float(device['ltea_3phsum_kwh'])

            self.avg_ac_power_kw = float(device['p_3phsum_kw'])
            self.avg_ac_voltage_v = float(device['vln_3phavg_v'])
            self.avg_ac_current_a = float(device['i_3phsum_a'])

            self.avg_dc_power_kw = float(device['p_mpptsum_kw'])
            self.avg_dc_voltage_v = float(device['v_mppt1_v'])
            self.avg_dc_current_a = float(device['i_mppt1_a'])

            self.inverter_temp_c = float(device['t_htsnk_degc'])
            self.avg_op_frequency_hz = float(device['freq_hz'])
            self.unknown = 0

            self.inverter_temp_f = self.inverter_temp_c * 9.0 / 5.0 + 32.0

    def __str__(self):
        return \
            Line.__str__(self) + \
            self.pv('total_lifetime_energy_kwh') + \
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

    def to_dbline(self):
        return DbLine130().from_line(self)


# Type 140
#
class Line140(Line):
    def __init__(self, lid=None, device=None):
        Line.__init__(self, lid, device)
        self.type = 140

    def to_dbline(self):
        return DbLine140().from_line(self)

