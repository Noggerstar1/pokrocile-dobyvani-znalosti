from datetime import datetime
import pandas as pd
import os
from cleverminer import cleverminer

def convert_to_24hr(date_str):
    dt = datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")
    return dt.strftime("%m/%d/%Y %H:%M:%S")

def categorize_temperature(temp):
    if temp < 47 or temp > 82:
        return 'unusual'
    else:
        return 'normal'

def categorize_wind(wind):
    if wind > 6.3:
        return 'windy'
    else:
        return 'not-windy'

dir_path = os.path.dirname(os.path.realpath(__file__))

traffic_path = os.path.join(dir_path, '../../Traffic_Violations_2023.csv')
weather_path = os.path.join(dir_path, '../../Weather_data.csv')

traffic = pd.read_csv(traffic_path, encoding='cp1250', sep=',')
weather = pd.read_csv(weather_path, encoding='cp1250', sep=',')

weather['Datetime'] = pd.to_datetime(weather['DateTime'], format='%m/%d/%Y %I:%M:%S %p')
weather = weather.dropna(subset=['DateTime'])
weather = weather.drop_duplicates(subset=['DateTime'])
weather['DateTime'] = [convert_to_24hr(ts) for ts in weather['DateTime']]
weather['DateTime'] = pd.to_datetime(weather['DateTime'])
weather = weather.sort_values(by='DateTime')

traffic = traffic.drop_duplicates(subset='SeqID', keep='first')
traffic = traffic[traffic['Accident'] == 'Yes']
traffic['Date Of Stop Timestamp'] = pd.to_datetime(traffic['Date Of Stop'])

cutoff_date = pd.to_datetime("07/31/2023")
traffic = traffic[traffic['Date Of Stop Timestamp'] <= cutoff_date]

traffic_df = pd.DataFrame(traffic)
weather_df = pd.DataFrame(weather)

traffic_df['Datetime'] = pd.to_datetime(traffic_df['Date Of Stop'] + ' ' + traffic_df['Time Of Stop'])
traffic_df['Datetime Rounded'] = traffic_df['Datetime'].dt.round('h')

data = pd.merge(traffic_df, weather_df, left_on='Datetime Rounded', right_on='DateTime', how='left')

data['WasRaining'] = data['RAIN'] > 0
data['Temperature'] = data['TMP10-DK'].apply(categorize_temperature)
data['Wind'] = data['SPD10-DK'].apply(categorize_wind)

data = data[['Date Of Stop', 'Time Of Stop', 'Personal Injury', 'Wind', 'Temperature', 'WasRaining', 'Accident']]


clm = cleverminer(df=data, proc='4ftMiner',
                  quantifiers={'conf': 0.6, 'Base': 50},
                  ante={
                      'attributes': [
                          # Replace Temperature with Wind or WasRaining attribute if you want data for that case
                          {'name': 'Temperature', 'type': 'subset', 'minlen': 1, 'maxlen': 1},

                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Personal Injury', 'type': 'subset', 'minlen': 1, 'maxlen': 1},

                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)
