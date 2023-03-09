import pandas as pd
from utils.data_func import *

gateway = pd.read_pickle('databases/gateway.pkl')
sensors = pd.read_pickle('databases/sensors.pkl')
measurements = pd.read_pickle('databases/measurements.pkl')

gateway.rename(columns={'id': 'gateway_id', 'name': 'gateway_name'}, inplace=True)
sensors.rename(columns={'id': 'sensor_id', 'gatewayId': 'gateway_id',
               'gatewayId': 'gateway_id'}, inplace=True)
measurements.rename(columns={'id': 'measurements_id',
                    'sensor': 'sensor_id'}, inplace=True)


data_frame = create_data_loader(gateway, sensors, measurements)

column_one = column_one(data_frame)
column_two = column_two(data_frame)
column_three = column_three(data_frame)
column_four = column_four(data_frame)
column_five = column_five(data_frame)
column_six = column_six(data_frame)
column_seven = column_seven(data_frame)
column_eight = column_eight(pd.concat(
    [column_one, column_two, column_three, column_four, column_five, column_six, column_seven], axis=1)
)
column_nine = column_nine(data_frame)
column_ten = column_ten(data_frame)
column_eleven = column_eleven(pd.concat(
    [column_eight, column_nine, column_ten], axis=1)
)
column_twelve = column_twelve(data_frame)
result_data_frame = pd.concat(
    [column_eleven, column_twelve], axis=1
)

print(result_data_frame)