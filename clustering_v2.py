# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 09:45:46 2022

@author: octav
"""


import pandas as pd
import os 
from sklearn.cluster import KMeans
import numpy as np
import folium
import branca.colormap as cm

df = pd.read_csv('{}\{}.csv'.format(os.getcwd(),'df'))

n = 100
x = df[['latitude','longitude']]

#Making and training the kmeans
kmeans = KMeans(n_clusters=n, random_state=0).fit(x)


#Creating a dict with the centers information based on label
centers = {cluster:location for cluster,location in zip([i for i in range(n)],kmeans.cluster_centers_)}


#Adding information to our df
df['cluster'] = kmeans.labels_
df['centroid'] = df['cluster'].map(centers)


df.to_csv('clustered_df.csv')



#Plotting clustered maps to see diferrent clusters -- color map may be the same in different clusters because of the cm.Linear  function 
la = df['latitude'].mean()
lo = df['longitude'].mean()


map1 = folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],
                           zoom_start=14,
                           control_scale=True)


linear = cm.LinearColormap(["green", "yellow", "red"], vmin=df['cluster'].min(), vmax=df['cluster'].max())


for i in range(len(df)):
    
    location = list(np.array(df.iloc[i,[1,2]]))
    
    folium.CircleMarker(location=location,
                        radius=2,
                        weight=3,
                        color=linear(df.iloc[i]['cluster'])).add_to(map1)
    
    
map1.fit_bounds(map1.get_bounds())
map1.save('{}\{}.html'.format(os.getcwd(),'map2'))




