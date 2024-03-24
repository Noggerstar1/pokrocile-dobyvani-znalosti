import pandas as pd
import sys

from cleverminer import cleverminer

print("hellos")

df = pd.read_csv('HotelPlusExternal.Export.txt', encoding='cp1250', sep='\t')
df=df[['VTypeOfVisit','GState','GCity','WSky','PersonNights']]


clm = cleverminer(df=df,proc='4ftMiner',
               quantifiers= {'conf':0.6, 'Base':50},
               ante ={
                    'attributes':[
                        {'name': 'GCity', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':2, 'type':'con'},
               succ ={
                    'attributes':[
                        {'name': 'VTypeOfVisit', 'type': 'subset', 'minlen': 1, 'maxlen': 1}
                    ], 'minlen':1, 'maxlen':1, 'type':'con'}
               )


clm.print_summary()
clm.print_rulelist()
clm.print_rule(1)