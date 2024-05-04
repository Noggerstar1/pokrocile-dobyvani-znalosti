import os
import pandas as pd
from cleverminer import cleverminer

dir_path = os.path.dirname(os.path.realpath(__file__))

traffic_path = os.path.join(dir_path, '../../Traffic_Violations_2023.csv')
weather_path = os.path.join(dir_path, '../../Weather_data.csv')

df = pd.read_csv(traffic_path, encoding='cp1250', sep=',')

df = df[['Accident', 'Belts', 'Personal Injury', 'Alcohol', 'Race']]

df = df[df['Accident'] == 'Yes']




clm = cleverminer(df=df, proc='SD4ftMiner',
                  quantifiers= {'Base1':50, 'Base2':50, 'Ratioconf' : 1.2},
               ante ={
                    'attributes':[
                        {'name': 'Belts', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               succ ={
                    'attributes':[
                        {'name': 'Personal Injury', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               frst ={
                    'attributes':[
                        {'name': 'Race', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'},
               scnd ={
                    'attributes':[
                        {'name': 'Race', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'}
               )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)

