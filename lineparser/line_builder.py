import logging

from lineparser import empty_line, Line130, Line140


class LineBuilder:
    def __init__(self, key):
        self.__key = key

    @property
    def key(self):
        return self.__key

    def can_build(self, key):
        return self.key == key

    def build(self, array):
        return empty_line


class LineBuilder130(LineBuilder):
    KEY = '130'

    def __init__(self):
        LineBuilder.__init__(self, self.KEY)

    def build(self, array):
        return Line130(None, array) if self.can_build(array[0]) else empty_line


class LineBuilder140(LineBuilder):
    KEY = '140'

    def __init__(self):
        LineBuilder.__init__(self, self.KEY)

    def build(self, array):
        return Line140(None, array) if self.can_build(array[0]) else empty_line


class LineFactory:
    def __init__(self):
        self.__builders = [LineBuilder130(), LineBuilder140()]

    def build(self, value):
        # Define empty result
        #
        result = empty_line

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
                if result is not empty_line:
                    break

        # Log lines we could not parse
        #
        if result is empty_line:
            logging.info('%s not parsed', value)

        # Return result
        #
        return result


class LinesFactory:

    def __init__(self):
        self.__lineFactory = LineFactory()
            
    def build(self, data):
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
            if line is not empty_line:
                result.append(line)

        # Return the lines we have built
        #
        return result
