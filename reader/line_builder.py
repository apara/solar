import logging

from reader import Line, emptyLine, Line130, Line140


class LineBuilder:
    def __init__(self, key: str) -> None:
        super().__init__()
        self.__key = key

    @property
    def key(self) -> str:
        return self.__key

    def can_build(self, key: str) -> bool:
        return self.key == key

    def build(self, array) -> Line:
        return emptyLine


class LineBuilder130(LineBuilder):
    KEY = '130'

    def __init__(self) -> None:
        super().__init__(self.KEY)

    def build(self, array) -> Line:
        return Line130(None, array) if self.can_build(array[0]) else emptyLine


class LineBuilder140(LineBuilder):
    KEY = '140'

    def __init__(self) -> None:
        super().__init__(self.KEY)

    def build(self, array) -> Line:
        return Line140(None, array) if self.can_build(array[0]) else emptyLine


class LineFactory:
    def __init__(self) -> None:
        super().__init__()
        self.__builders = [LineBuilder130(), LineBuilder140()]

    def build(self, value: str) -> Line:
        # Define empty result
        #
        result = emptyLine

        # Split the line into parts
        #
        array = value.split()

        # If there is anything in array
        #
        if array:
            # For each builder try to create a line
            #
            for builder in self.__builders:

                # Attempt to build a line
                #
                result = builder.build(array)

                # If we have a line, then break out of the loop
                #
                if result is not emptyLine:
                    break

        # Log lines we could not parse
        #
        if result is emptyLine:
            logging.info('%s not parsed', value)

        # Return result
        #
        return result


class LinesFactory:

    __lineFactory = LineFactory()

    def __init__(self) -> None:
        super().__init__()

    def build(self, data :str):
        # Define result
        #
        result = []

        # Split the lines on end of line
        #
        lines = data.split('\n')

        # For each line, build a line and add to the array
        #
        for line in lines:
            line = self.__lineFactory.build(line)
            if line is not emptyLine:
                result.append(line)

        # Return the lines we have built
        #
        return result
