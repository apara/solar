from datetime import datetime

class LineId(str):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)


# Line base class
#
class Line:
    def __init__(self, lid: LineId=None, array: object = None) -> None:
        super().__init__()

        # Assign id of the line
        #
        self.id = lid

        # Assign type of the line
        #
        if array:
            self.type = array[0]
            self.ts = self.parse_date(array[1])

    def __str__(self) -> str:
        return \
            super().__str__() + \
            ' id: ' + (self.id if self.id else 'None') + \
            ' type: ' + (self.type if self.type else 'None') + \
            ' ts: ' + self.ts.__str__()

    @staticmethod
    def parse_date(value:str)->datetime:
        return datetime.strptime(value, '%Y%m%d%H%M%S')


emptyLine = Line()


# Type 130
#
class Line130(Line):
    def __init__(self, lid: object = None, array: object = None) -> None:
        super().__init__(lid, array)


# Type 140
#
class Line140(Line):
    def __init__(self, lid: LineId=None, array: object = None) -> None:
        super().__init__(lid, array)


