class LineId(str):
    def __init__(self, value: str = None) -> None:
        super().__init__(value)


# Line base class
#
class Line:
    def __init__(self, lid: LineId=None) -> None:
        super().__init__()
        self.id = lid
                

emptyLine = Line()


# Type 130
#
class Line130(Line):
    def __init__(self, lid: object = None, array: object = None) -> None:
        super().__init__(lid)
        print(array)


# Type 140
class Line140(Line):
    def __init__(self, lid: LineId=None, array=None) -> None:
        super().__init__(lid)
        print(array)


