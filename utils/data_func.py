import pandas as pd
import numpy as np
import datetime


def create_data_loader(gateway, sensors, measurements):
    data_frame = gateway.merge(sensors, on='gateway_id', how='inner')
    data_frame = data_frame.merge(measurements, on='sensor_id', how='inner')
    return data_frame


def column_one(data_frame):
    return data_frame['gateway_id'].drop_duplicates().reset_index(drop=True)


def column_two(data_frame):
    gateway_name = data_frame['gateway_name'].str.replace(
        'gateway_', 'GATEWAY ').str.split(' ').apply(
        lambda x: f"{x[0]} {x[1].zfill(2)}").drop_duplicates().reset_index(drop=True)
    return gateway_name


def column_three(data_frame):
    number_sensor = data_frame.groupby('gateway_name')[
        'sensor_id'].nunique().reset_index()
    number_sensor = number_sensor.loc[:, 'sensor_id'].rename(
        'number_of_registered_sensors')
    return number_sensor


def column_four(data_frame):

    agg_df = data_frame.groupby('gateway_name').agg(
        {'start': 'count', 'frequency': 'count'})

    valid_configurations = (agg_df['start'] == agg_df['frequency']).rename(
        'valid_configurations')

    return valid_configurations.reset_index().loc[:, 'valid_configurations']


def column_five(data_frame):
    data_frame['is_valid'] = (data_frame['start'].notnull()) & (
        data_frame['frequency'].notnull())
    percent_valid = (data_frame.groupby('gateway_name')
                     ['is_valid'].mean() * 100).round(2)
    percent_valid.name = 'percentual_valid_configurations'
    percent_valid = percent_valid.reset_index()
    return percent_valid.loc[:, 'percentual_valid_configurations']


def column_six(data_frame):
    data_frame['valid_config'] = (data_frame['start'].notnull()) & (
        data_frame['frequency'].notnull())
    data_frame['frequency_timedelta'] = pd.to_timedelta(
        data_frame['frequency'])
    data_frame['expected_measurements'] = (pd.Timedelta(
        '24 hours') / data_frame['frequency_timedelta']) * data_frame['valid_config']
    expected_measurements = data_frame.groupby('gateway_name')[
        'expected_measurements'].sum().reset_index(name='expected_measurements')

    return expected_measurements.loc[:, 'expected_measurements']


def column_seven(data_flame):
    data_flame['signal'] = pd.to_numeric(data_flame['signal'], errors='coerce')
    data_flame = data_flame.loc[(data_flame['signal'].notnull()) & (
        data_flame['signal'] < 0)]

    signal_mean_value = data_flame.groupby('gateway_name')[
        'signal'].mean().round(2).reset_index(name='signal_mean_value')

    return signal_mean_value.loc[:, 'signal_mean_value']


def column_eight(data_frame):
    data_result = pd.DataFrame(data_frame.copy())
    data_result['signal_status'] = pd.cut(data_result['signal_mean_value'],
                                          bins=[-np.inf, -100, -90, np.inf],
                                          labels=['Ruim', 'Regular', 'Bom'])
    return data_result


def column_nine(data_frame):
    problem_signals = (data_frame['signal'].isna()) | (
        data_frame['signal'].isin(['None', 'NaN']) | (data_frame['signal'] >= 0))

    signal_issue_count = problem_signals.groupby(
        data_frame['gateway_name']).sum().reset_index(name='signal_issue')

    return signal_issue_count['signal_issue']


def column_ten(data_frame):
    utc_time_now = pd.Timestamp.utcnow()
    data_frame['elapsed_time_since_last_measurement'] = utc_time_now - \
        data_frame.groupby('sensor_id')['datetime'].transform('max')
    elapsed_time = data_frame.groupby('gateway_name')['elapsed_time_since_last_measurement'].min().reset_index(
        name='elapsed_time_since_last_measurement')
    return elapsed_time['elapsed_time_since_last_measurement']


def column_eleven(data_frame):
    data_result = pd.DataFrame(data_frame.copy())
    elapsed_time = data_result['elapsed_time_since_last_measurement']
    data_result['measurement_status'] = np.where(elapsed_time.isnull(), 'nunca coletado',
                                                 np.where(elapsed_time < pd.Timedelta(days=60), 'coletado nos últimos 60 dias',
                                                 'coletado há mais de 60 dias'))
    return data_result


def column_twelve(data_frame):
    filtered_df = data_frame[['sensor_id',
                              'gateway_name', 'datetime']].dropna()

    grouped_df = filtered_df.groupby(['sensor_id', 'gateway_name'])
    pairs = grouped_df.apply(lambda group: sum(
        (group['datetime'].diff() <= pd.Timedelta(hours=1)).dropna())
    ).reset_index(name='one_hour_pairs')

    result = pairs.groupby('gateway_name').agg(
        {'one_hour_pairs': 'sum'}).reset_index()

    result = result.rename(columns={'one_hour_pairs': 'one_hour_groups'})
    return result[['one_hour_groups']]
