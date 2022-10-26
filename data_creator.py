# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 21:22:54 2022

@author: octav
"""
from shapely.geometry import Polygon, Point
import random
import pandas as pd
import folium
import os
from faker import Faker
import json




#Numero de alumnos 
n = 13000

zmg_polygon = Polygon([(20.756429285842973, -103.43429263648916),
(20.74101860249208, -103.45351871070791),
(20.730743941418762, -103.47205813941885),
(20.740215919716448, -103.57505496559072),
(20.715089797012403, -103.57883151588369),
(20.718220755332595, -103.47617801246572),
(20.705696533863104, -103.47343143043447),
(20.691244223189553, -103.47205813941885),
(20.673257202515146, -103.46793826637197),
(20.64418588149608, -103.48592868847274),
(20.620409504546863, -103.48764530224227),
(20.609162627185647, -103.4725391010704),
(20.572604543523816, -103.50275150341415),
(20.533144128689067, -103.50172153515243),
(20.506617150190046, -103.43717685741805),
(20.556451919263743, -103.35237613720321),
(20.57541701487203, -103.27718845409774),
(20.604342282696933, -103.28748813671493),
(20.61944551903031, -103.28542820019149),
(20.631655551249622, -103.27409854931258),
(20.673419303159907, -103.29006305736922),
(20.69782971699487, -103.30362430614852),
(20.712281399965715, -103.30499759716415),
(20.731548166675996, -103.31426731151961),
(20.73893311058856, -103.34173313183211),
(20.763011945169627, -103.36439243358993),
(20.7811488007994, -103.3549510578575),
(20.785803040854876, -103.40009799999618)])



def generate_random(n, polygon):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    
    while len(points) < n:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            points.append((pnt.x,pnt.y))
    return points







#Getting random points within polygon
points = (generate_random(n, zmg_polygon))


#creating a dataframe with the information 
df = pd.DataFrame(points, columns =['latitude', 'longitude'])


#Adding student id
df['id'] = [i+1 for i in range(n)]
df.set_index("id", inplace = True)



#Adding gender
gender = ['M','F']
gender_weigths = [0.80,0.20]
df['gender'] = [random.choices(gender,weights=gender_weigths)[0] for _ in range(n)]



#Adding age

#Randomizing age category with weigths
ages_cat = [1,2,3]
ages_weights = [0.5548,0.3872,0.058]
df['age_cat'] = [random.choices(ages_cat,weights=ages_weights) for _ in range(n)]

#Getting the age based on the category
ages = []
for value in df['age_cat']:  
    
    if value[0] == 1:
        ages.append(random.randint(17, 18))
        
    if value[0] == 2:
        ages.append(random.randint(19, 20))
        
    if value[0]== 3:
        ages.append(random.randint(21, 25))
     
 
#Creating the column and dropping age_cat
df['age'] = ages
df.drop(labels='age_cat',axis=1,inplace=True)


#adding career
careers = pd.read_csv('carreras.csv')['CARRERA'].tolist()
careers = [x.strip() for x in careers]



careers_weigth = pd.read_csv('carreras.csv')['PESO'].tolist()


df['career'] = [random.choices(careers,weights=careers_weigth)[0] for _ in range(n)]



#Adding department
departments= pd.read_csv('departamentos.csv')['departamento'].tolist()
departments = [x.strip() for x in departments]

departments_weigth = pd.read_csv('departamentos.csv')['peso'].tolist()


df['department'] = [random.choices(departments,weights=departments_weigth)[0] for _ in range(n)]


#Adding names

#library to fake names
fake = Faker()


df['first_name'] = [fake.name().split()[0] for _ in range(n)]
df['last_name'] = [fake.name().split()[1] for _ in range(n)]



#Creating schedules

#Start schedule
schedule_in = [7,9,11,13,16,18]
schedule_in_weigths = [0.32,0.40,0.08,0.08,0.06,0.06]

df['lunes_in'] = [random.choices(schedule_in,schedule_in_weigths)[0] for _ in range(n)]
df['martes_in'] = [random.choices(schedule_in,schedule_in_weigths)[0] for _ in range(n)]
df['miercoles_in'] = [random.choices(schedule_in,schedule_in_weigths)[0] for _ in range(n)]
df['jueves_in'] = [random.choices(schedule_in,schedule_in_weigths)[0] for _ in range(n)]
df['viernes_in'] = [random.choices(schedule_in,schedule_in_weigths)[0] for _ in range(n)]




def out_schedule(serie):
    '''
    Function that takes the entry hour and calculates possible exit hours based on the previous information
    
    Parameters
    ----------
    serie : df serie
        DESCRIPTION.
        
    Returns
    -------
    list.
    '''
    out_list = []
    
    for i in serie:
                
        if i == 7:
            out_list.append(random.choice([2,4,6,8,11,13])+i)
            
        elif i == 9:
            out_list.append(random.choice([2,4,6,9,11])+i)
            
        elif i == 11:
            out_list.append(random.choice([2,4,7,9])+i)
            
        elif i == 13:
            out_list.append(random.choice([2,5,7])+i)
            
        elif i == 16:
            out_list.append(random.choice([2,4])+i)
            
        else:
            out_list.append(2+i)
            
        
    return out_list
        
        

df['lunes_out'] = out_schedule(df.lunes_in)
df['martes_out'] = out_schedule(df.martes_in)
df['miercoles_out'] = out_schedule(df.miercoles_in)
df['jueves_out'] = out_schedule(df.jueves_in)
df['viernes_out'] = out_schedule(df.viernes_in)       





#saving the df in the same folder
df.to_csv('df.csv')

# --------------- Plotting ------------------------------

#The html file will be saved in the same folder where this file is saved
#Creating a map with coordinates
la = df['latitude'].mean()
lo = df['longitude'].mean()


map1 = folium.Map(location=[la,lo],
                           zoom_start=14,
                           control_scale=True)



def plotDot(row,color,radius,weigth=4):
    
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=radius,
                        weight=weigth,
                        color=color).add_to(map1)
    

df.apply(plotDot, axis=1,color='#4169E1',radius=5)

map1.fit_bounds(map1.get_bounds())
map1.save('{}\{}.html'.format(os.getcwd(),'map1'))





