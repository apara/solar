from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create a declarative base class
#
DbLineBase = declarative_base()


# DbLine base class
#
class DbLine(DbLineBase):
    __tablename__ = 'line'

    id = Column('id', Integer, primary_key=True, autoincrement="auto")
    type = Column('type', Integer, nullable=False)
    ts = Column('ts', DateTime, nullable=False)
    serial = Column('serial', String(64), nullable=False)
    description = Column('description', String(255), nullable=False)
    total_lifetime_energy_kwh = Column('total_lifetime_energy_kwh', Float, nullable=False)
    total_lifetime_energy_delta_kwh = Column('total_lifetime_energy_delta_kwh', Float)

    __mapper_args__ = {
        'polymorphic_on': type,
        # 'polymorphic_identity': '0'
    }

    __table_args__ = (
        UniqueConstraint(serial, ts),
    )

    def from_line(self, line):
        # Configure common parameters
        # 
        self.type = line.type
        self.ts = line.ts
        self.serial = line.serial
        self.description = line.description
        self.total_lifetime_energy_kwh = line.total_lifetime_energy_kwh

        # Return self
        #
        return self

    def insert(self, session):
        # Find previous entity, if any
        #
        previous_line = \
            session \
                .query(DbLine) \
                .filter(DbLine.serial == self.serial) \
                .order_by(DbLine.ts.desc()) \
                .limit(1) \
                .one_or_none()

        # If we have a previous line, then configure to the difference, otherwise it is what it is
        #
        self.total_lifetime_energy_delta_kwh = \
            self.total_lifetime_energy_kwh - previous_line.total_lifetime_energy_kwh \
            if previous_line else self.total_lifetime_energy_kwh

        # Add us to the session
        #
        session.add(self)


# Db Line Type 130
#
class DbLine130(DbLine):
    avg_ac_power_kw = Column('avg_ac_power_kw', Float, nullable=False)
    avg_ac_voltage_v = Column('avg_ac_voltage_v', Float, nullable=False)
    avg_ac_current_a = Column('avg_ac_current_a', Float, nullable=False)
    avg_dc_power_kw = Column('avg_dc_power_kw', Float, nullable=False)
    avg_dc_voltage_v = Column('avg_dc_voltage_v', Float, nullable=False)
    avg_dc_current_a = Column('avg_dc_current_a', Float, nullable=False)
    inverter_temp_c = Column('inverter_temp_c', Float, nullable=False)
    avg_op_frequency_hz = Column('avg_op_frequency_hz', Float, nullable=False)
    unknown = Column('unknown', String(255), nullable=False)
    inverter_temp_f = Column('inverter_temp_f', Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 130
    }

    def from_line(self, line):
        super(DbLine130, self).from_line(line)
        
        # Configure parameters
        #
        self.avg_ac_power_kw = line.avg_ac_power_kw
        self.avg_ac_voltage_v = line.avg_ac_voltage_v
        self.avg_ac_current_a = line.avg_ac_current_a
        self.avg_dc_power_kw = line.avg_dc_power_kw
        self.avg_dc_voltage_v = line.avg_dc_voltage_v
        self.avg_dc_current_a = line.avg_dc_current_a
        self.inverter_temp_c = line.inverter_temp_c
        self.avg_op_frequency_hz = line.avg_op_frequency_hz
        self.unknown = line.unknown
        self.inverter_temp_f = line.inverter_temp_f

        # Return self
        #
        return self

    def insert(self, session):

        # Insert as normal
        #
        super(DbLine130, self).insert(session)


# Db Line Type 140
#
class DbLine140(DbLine):

    __mapper_args__ = {
        'polymorphic_identity': 140
    }

    def from_line(self, line):
        super(DbLine140, self).from_line(line)

        # Return self
        #
        return self


class DbLineManager:
    def __init__(self, configuration):
        # Create the engine
        #
        self.__engine = \
            create_engine(
                'mysql+mysqlconnector://{}:{}@{}/{}'.format(
                    configuration.db_user,
                    configuration.db_password,
                    configuration.db_host,
                    configuration.db_name
                )
            )

        # Create a session
        #
        self.__Session = sessionmaker(bind=self.__engine)

        # Create the schema, if needed
        #
        DbLineBase.metadata.create_all(self.__engine)

    def insert(self, line):
        # Create a new session
        #
        session = None

        try:
            session = self.__Session()
            line.to_dbline().insert(session)
            session.commit()
        finally:
            session.close()


        

        
        






