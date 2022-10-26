# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 16:00:29 2022

@author: octav
"""

import pandas as pd
import os

#I put a try and except because os.getcwd() randomly stops working even if its in the same dir
#If it doesn work for you too, just change the path on read_csv below except
try:
    df = pd.read_csv(r'{}\{}'.format(os.getcwd(), 'clustered_df.csv'))

except:
    df = pd.read_csv(r'\Users\octav\Documentos\repo\iteso\programacion2\proyecto\clustered_df.csv')
    


def interface(df):
    
    
    #Getting id of user searching for ride
    exp = int(input('Introduce tu numero de expediente: '))
    
    #getting the cluster of user
    cluster = df.loc[df.id == exp]['cluster'].unique()[0]
    
    #Filtering just users from that cluster
    df2 = df[df['cluster'] == cluster]
    
    #We will see the matching schedules in every day of the week, so we'll iterate over this list
    days = [['id','first_name','lunes_in','lunes_out'],
            ['id','first_name','martes_in','martes_out'],
            ['id','first_name','miercoles_in','miercoles_out'],
            ['id','first_name','jueves_in','jueves_out'],
            ['id','first_name','viernes_in','viernes_out']]
    
    
    #Same with the day names
    days_name = ['Lunes','Martes','Miercoles','Jueves','Viernes']
     
    for i in range(5):
        print(days_name[i])
        ronda(df2,exp, days[i])
        print('')
    
    
    
def ronda(df2,exp,columns_list):
    
    df2 = df2[columns_list]
   
    
    sch_in = df2.loc[df.id == exp].iloc[:,2].unique()[0]
    sch_out = df2.loc[df.id == exp].iloc[:,3].unique()[0]
    
    
    df2 = df2[(df2.iloc[:,2] == sch_in) & (df2.iloc[:,3] == sch_out)]
    df2.set_index(keys=['id'],inplace=True)
    
    print(df2)




if __name__ == '__main__':
    interface(df)
    





























