from .Linebuilder import *


class Factory(LineBuilder):
    def __init__(self) -> None:
        super().__init__()
        self.__builders = [LineBuilder130(), LineBuilder140()]

    def build(self, value: str) -> Line:
        return super().build(value)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    def talk(self) -> None:
        return