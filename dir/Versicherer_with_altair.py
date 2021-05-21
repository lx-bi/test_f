# -*- coding: utf-8 -*-
"""
Created on Thu May 20 15:27:01 2021

@author: lihua.xu 
test
"""

import altair as alt
import pandas as pd
import datetime as dt
#import matplotlib.pyplot as plt
#import seaborn as sns

from IPython.display import display


base_data=pd.read_excel('H:\Auagabe\Abgleich_Bestand_und_Acc_status.xlsx')
#display(base_data.head(n=2))
#action_count = base_data.groupby('VERSICHERER')['ACTIONID'].count().sort_values(ascending=False).to_frame().reset_index()
today = dt.datetime.today().year
#print(today)



bd = base_data.copy()
bd['age'] = today - base_data['GEBURTSDATUM'].dt.year

columns = ['VERTRAGID','VERSICHERER','ACTIONID','ERSTZULASSUNG','ÜBERMITTELT_AM','VERSICHERUNGSBEGINN','age']
bd = pd.DataFrame(bd,columns=columns)

##f,ax=plt.subplots(figsize=(10,8))
##sns.boxplot(y='age',data=bd,ax=ax)
##plt.show()

#display(bd.head(n=2))
brush = alt.selection(type='interval')
#interval = alt.selection_interval()

point=alt.Chart(bd).mark_point().encode(
        x= 'age',
        y='count()',
        #color='VERSICHERER',
        color=alt.condition(brush,'VERSICHERER',alt.value('lightgray')),
        tooltip = 'VERSICHERER'
       # column='VERSICHERER'
        ).add_selection(
        brush  
)

bars= alt.Chart(bd).mark_bar().encode(
    y = 'VERSICHERER',
    color='VERSICHERER',
    x='count(VERSICHERER)',
    
).transform_filter(
    brush
)

bars2 = alt.Chart(bd).mark_bar().encode(
    alt.Y(field='VERSICHERER',type='nominal',sort=alt.EncodingSortField(field='VERSICHERER', op='count',order='descending')),
    alt.X('count(VERSICHERER):Q',sort='ascending'),
    alt.Color('VERSICHERER:N'),
   # color='VERSICHERER',
   # x='count(VERSICHERER)',
    
).transform_filter(
    brush
)


chart = alt.vconcat(point , bars2)
chart1= alt.vconcat(chart,bars)

chart1.save('chart1.html')
#chart1=alt.vconcat(chart,bars2)

chart1
