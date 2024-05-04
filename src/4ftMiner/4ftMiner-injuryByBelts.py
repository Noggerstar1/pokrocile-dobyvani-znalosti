import os
import pandas as pd
from cleverminer import cleverminer

dir_path = os.path.dirname(os.path.realpath(__file__))

traffic_path = os.path.join(dir_path, '../../Traffic_Violations_2023.csv')

df = pd.read_csv(traffic_path, encoding='cp1250', sep=',')

df = df[['Accident', 'Belts', 'Personal Injury', 'SeqID']]

df = df[df['Accident'] == 'Yes']

df = df.drop_duplicates(subset='SeqID', keep='first')

clm = cleverminer(df=df, proc='4ftMiner',
                  quantifiers={'conf': 0.5, 'Base': 20},
                  ante={
                      'attributes': [
                          {'name': 'Belts', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'},
                  succ={
                      'attributes': [
                          {'name': 'Personal Injury', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                      ], 'minlen': 1, 'maxlen': 1, 'type': 'con'}
                  )

clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)