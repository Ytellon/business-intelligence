from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Gateway(Base):
    __tablename__ = 'gateways'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    gateway_id = Column(String, unique=True)
    gateway_name = Column(String, unique=True)
    number_of_registered_sensors = Column(Integer)
    valid_configurations = Column(Boolean)
    percentual_valid_configurations = Column(Float)
    expected_measurements = Column(Float)
    signal_mean_value = Column(Float)
    signal_status = Column(String)
    signal_issue = Column(Float)
    elapsed_time_since_last_measurement = Column(DateTime)
    measurement_status = Column(String)
    one_hour_groups = Column(Integer)
