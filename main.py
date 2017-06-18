import sys
from configuration import Configuration


def main():
    # Load the configuration
    #
    configuration = Configuration(['./solar.conf', 'conf/solar.conf', '/etc/solar.conf'])

    pass

if __name__ == "__main__":
    sys.exit(main())
