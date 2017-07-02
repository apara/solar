import json
from utils import *
from line import empty_line, Line130, Line140


class LineBuilder:
    def __init__(self, key):
        self.__key = key

    @property
    def key(self):
        return self.__key

    def can_build(self, device):
        return self.key == device['DEVICE_TYPE']

    def build(self, device):
        return \
            self.new_line(device) \
            if self.can_build(device) \
            else empty_line

    def new_line(self, device=None):
        return empty_line


class LineBuilder130(LineBuilder):
    KEY = 'Inverter'

    def __init__(self):
        LineBuilder.__init__(self, self.KEY)

    def new_line(self, device=None):
        return Line130(None, device)


class LineBuilder140(LineBuilder):
    KEY = 'Power Meter'

    def __init__(self):
        LineBuilder.__init__(self, self.KEY)

    def new_line(self, device=None):
        return Line140(None, device)


class LineFactory(LogMixin):

    def __init__(self):
        self.__builders = [LineBuilder130(), LineBuilder140()]

    def build(self, device):
        # Define empty result
        #
        result = empty_line

        # For each builder try to create a line
        #
        for builder in self.__builders:

            # Attempt to build a line, if there are any exceptions skip this line
            #
            try:
                result = builder.build(device)
            except Exception as e:
                self.logger.warn("Exception while trying to read device: {0}".format(e))

            # If we have a line, then break out of the loop
            #
            if result is not empty_line:
                break

        # Log lines we could not parse
        #
        if result is empty_line:
            self.logger.debug('NOT PARSED: {0}'.format(device))

        # Return result
        #
        return result


class LinesFactory(LogMixin):

    def __init__(self):
        self.__lineFactory = LineFactory()
            
    def build(self, data):
        # Define result
        #
        result = []

        # Parse data into JSON
        #
        try:
            # parse json text
            #
            parsed = json.loads(data)

            # Make sure it's a succeed
            #
            if parsed['result'] == 'succeed':
                # For each device
                #
                for device in parsed['devices']:
                    # Build reporting line
                    #
                    line = self.__lineFactory.build(device)

                    # If it's not an empty line
                    #
                    if line is not empty_line:
                        result.append(line)
                        
        except Exception as e:
            self.logger.exception(e)

        # Return the lines we have built
        #
        return result
