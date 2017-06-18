from datetime import datetime


class LineId(str):
    def __init__(self, value=None):
        str.__init__(value)


# Line base class
#
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
            self.watts = array[4]

    def __str__(self):
        return \
            ' id: ' + (self.id if self.id else 'None') + \
            ' type: ' + (self.type if self.type else 'None') + \
            ' ts: ' + self.ts.__str__() + \
            ' serial: ' + self.serial + \
            ' description: ' + self.description + \
            ' watts: ' + self.watts

    @staticmethod
    def parse_date(value):
        return datetime.strptime(value, '%Y%m%d%H%M%S')


emptyLine = Line()


# Type 130
#
class Line130(Line):
    def __init__(self, lid=None, array=None):
        Line.__init__(self, lid, array)
        if array:
            self.peakAcPower = array[5]
            

# Type 140
#
class Line140(Line):
    def __init__(self, lid=None, array=None):
        Line.__init__(self, lid, array)


