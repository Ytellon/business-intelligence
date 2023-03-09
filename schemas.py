from pydantic import BaseModel
from datetime import datetime

class CreateGateway(BaseModel):
    message: str

class StandardOutput(BaseModel):
    message: str

class ErrorOutput(BaseModel):
    error: str
  
class GatewayInput(BaseModel):
    gateway_id: str
    gateway_name: str
    number_of_registered_sensors: int
    valid_configurations: bool
    percentual_valid_configurations: float
    expected_measurements: float
    signal_mean_value: float
    signal_status: str
    signal_issue: float
    elapsed_time_since_last_measurement: datetime
    measurement_status: str
    one_hour_groups: int
