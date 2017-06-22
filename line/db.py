from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from configuration import Configuration


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

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': '0'
    }


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


# Db Line Type 140
#
class DbLine140(DbLine):

    __mapper_args__ = {
        'polymorphic_identity': 140
    }


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

        # Create the schema, if needed
        #
        DbLineBase.metadata.create_all(self.__engine)

        

        
        






