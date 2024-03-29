import pandas as pd
from cleverminer import cleverminer

df = pd.read_csv('../../Traffic_Violations_2023.csv', encoding='cp1250', sep=',')

df = df[['Accident', 'Belts', 'Personal Injury']]

df = df[df['Accident'] == 'Yes']

clm = cleverminer(df=df, proc='4ftMiner',
                  quantifiers={'conf': 0.6, 'Base': 50},
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