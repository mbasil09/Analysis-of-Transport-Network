#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports
import math
import random
import pandas as pd
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
import collections
from operator import itemgetter
import geopandas
from matplotlib.colors import ListedColormap


# ## Data importing and preprocessing

# In[2]:


# listing the Excels Files

excel_list1 = os.listdir("Raw_Data")
excel_list = []
for i in excel_list1:
    if(i.endswith(".csv")):
        excel_list.append(i)   
excel_list.sort()


# ## Directed Weighted Network Creation

# In[3]:


# Creating networks and stroing them
coordinates = pd.read_csv("Raw_Data/coordinates/sorted_coordinates.csv",header=0,index_col= 0)
print(coordinates)

max_weight = 0
min_weight = 10000000000

graphs = []
passengers = []   # records number of total passengers(month wise)
lbls = []
for i in excel_list:
    path = "Raw_Data/"+i
    excel = pd.read_csv(path ,header=0, index_col=0, usecols = [0,1,2,3,4] ,names=["SNo","city1","city2","to","from"] )
    passengers.append(sum(excel["to"]) + sum(excel["from"]))
    lbls.append(i[:-4])
    G = nx.DiGraph()
    cities = {}
    for i in range(1,len(excel)+1):
        cities[excel["city1"][i]] = (coordinates["Longitude"][excel["city1"][i]],coordinates["Latitude"][excel["city1"][i]])
        cities[excel["city2"][i]] = (coordinates["Longitude"][excel["city2"][i]],coordinates["Latitude"][excel["city2"][i]])
    for i in cities:
        G.add_node(i, pos= cities[i])
    
    print(path)
    for i in range(1,len(excel)+1):
        weight1 = excel["to"][i]
        if(weight1 != 0):
            G.add_edge(excel["city1"][i],excel["city2"][i],weight=weight1)
        weight2 = excel["from"][i]
        if(weight2 != 0):
            G.add_edge(excel["city2"][i],excel["city1"][i],weight=weight2)
        
        max_weight = max(max_weight, weight1, weight2)
        min_weight = min(min_weight, weight1, weight2)
    graphs.append(G)
nx.write_gml(graphs[-7], "test.gml", stringizer = str)
#print(cities)


# In[4]:


lbls1 = []
month = {"01":"Jan", "02":"Feb", "03":"March", "04":"April", "05":"May", "06":"June", "07":"July", "08":"Aug", 
        "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
for e in lbls:
    lbls1.append(month[e[2:]]+e[:2])


# In[5]:


# coordinates has city, lat, long -> <class 'pandas.core.frame.DataFrame'>

df = geopandas.read_file("shapefile/india_states.shp")


# In[6]:


print(df)


# In[ ]:





# colors = ['#fafa6e','#72cf85', '#00ffff','#00968e', '#1b6474','#9966ff','#ff66cc','#993366',
#           '#ff5050','#ff3300','#cc3300','#993300','#800000',]
# 
# 
# for i in range(len(lbls)):
#     print(i)
#     df.boundary.plot()
# 
#     #cmap = ListedColormap(['#fafa6e', '#e1f470','#c9ee73', '#b2e777', '#9cdf7c', '#86d780', '#72cf85', '#5ec688', '#4abd8c', '#37b38e',
#     #     '#23aa8f', '#0ba08f', '#00968e', '#008c8b', '#008288', '#007882', '#106e7c', '#1b6474', '#225b6c', '#275162',
#     #     '#2a4858'])
#     cmap = ListedColormap(colors)
#     
# #     edges, weights = zip(*nx.get_edge_attributes(graphs[i],'weight').items())
# #     nx.draw(graphs[i], nx.get_node_attributes(graphs[i],'pos'),node_size = 50, node_color='b', edgelist=edges, 
# #         edge_color=weights, width=1.0, edge_cmap=cmap, vmin=min_weight, vmax=max_weight)
# 
#     try:
#         edges, weights = zip(*nx.get_edge_attributes(graphs[i],'weight').items())
#         nx.draw(graphs[i], nx.get_node_attributes(graphs[i],'pos'),node_size = 50, node_color='b', edgelist=edges, 
#             edge_color=weights, width=1.0, edge_cmap=cmap, vmin=min_weight, vmax=max_weight)
#     except:
#         print("HAHAHA")
#         nx.draw_networkx(graphs[i],nx.get_node_attributes(graphs[i],'pos'),font_color = "red")
#     
#     
# 
# #     figure.set_size_inches(100, 100)
#     
#     
#     sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin = min_weight, vmax=max_weight))
#     sm._A = []
#     cb = plt.colorbar(sm)
#     cb.ax.tick_params(labelsize=15) 
#     cb.set_label(label='Number of Passengers',weight='bold',size = 20)
# 
#     
# 
# 
#     plt.title("Airport Network Of India "+ lbls1[i])
#     
#     figure = plt.gcf()
#     figure.set_size_inches(30, 30)
#     
#     plt.savefig('Output_Files/matplotlib/map/'+lbls[i])
#     #plt.savefig(lbls[i])
#  
#     #plt.show()
#     plt.clf()
#     plt.close()
# 

# ## Network Visualization

# In[7]:


nodes = []
for i in range(len(graphs)):
    nodes.append(len(graphs[i].nodes()))
print(lbls)
plt.plot(nodes, color="red", marker="o")
plt.xlabel("Month Year (MMMYY)")

plt.xticks([i for i in range(66)], labels = lbls1)
plt.ylabel("Number of Active Airports")
plt.title("Number of Active Airports in India")
plt.grid(True)

figure = plt.gcf()
figure.set_size_inches(50, 8)
plt.savefig('Output_Files/matplotlib/nodes')
plt.show()


# In[8]:


nnodes = []
airpor = {} 
for i in range(len(graphs)):
    temp = 0
    for j in graphs[i].nodes():
        if j not in airpor:
            airpor[j]=  1
            temp += 1
    nnodes.append(temp)
nnodes[0] = 0
plt.plot(nnodes, color="red", marker="o")
plt.xlabel("Month,Year (MMMYY)")
plt.xticks([i for i in range(66)], labels = lbls1)
plt.ylabel("Number of New Airports")
plt.title("Number of New Airports in India")
plt.grid(True)
plt.ylim(-1,6)
figure = plt.gcf()
figure.set_size_inches(50, 10)
plt.savefig('Output_Files/matplotlib/newnodes')
plt.show()
plt.clf()
plt.close()


# In[9]:


edges = []
for i in range(len(graphs)):
    edges.append(len(graphs[i].edges()))
plt.plot(edges, color="red", marker="o")
plt.xlabel("Month,Year (MMMYY)")
plt.xticks([i for i in range(66)], labels = lbls1)
plt.ylabel("Number of Active Airport Connections")
plt.title("Number of Active Airport Connections in India")
plt.grid(True)
figure = plt.gcf()
figure.set_size_inches(50, 8)
plt.savefig('Output_Files/matplotlib/edges')
plt.show()
plt.clf()
plt.close()


# In[10]:


plt.plot(passengers, color="red",  marker="o")
plt.xlabel("Month,Year (MMMYY)")
plt.xticks([i for i in range(66)],labels = lbls1)
plt.ylabel("Number of Passengers")
plt.title("Number of Passengers Travelling in India")
plt.grid(True)
figure = plt.gcf()
figure.set_size_inches(50, 8)
plt.savefig('Output_Files/matplotlib/passengers')
plt.show()
plt.clf()
plt.close()


# In[11]:


for i in sorted(airpor.keys()):
    print(i)


# excel = pd.read_csv("Raw_Data/coordinates/sorted_coordinates.csv",header=0)
# tempcity = list(excel["Cities"])
# #print(tempcity)
# for i in sorted(airpor.keys()):
#     if i not in tempcity:
#         print(i)

# In[ ]:





# In[12]:


for i in range(len(graphs)):
    print(lbls1[i])
    G = graphs[i]
    betweenness_dict = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    
    sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)

#     sorted_betweenness = sorted(betweenness_dict.items(), key=itemgetter(1), reverse=True)

    print("Top 10 nodes")
    
    for i in range(len(sorted_betweenness[:10])):
        print(sorted_betweenness[i][0] + " -> " + str(sorted_betweenness[i][1]))


# Degree Distribution

# In[14]:


import sys
for i in range(30):
    print(lbls1[i])
    G = graphs[i]
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
   
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    #print(sorted_degree)

    print("Top 10 nodes")
    for z in range(len(sorted_degree[:10])):
        print(sorted_degree[z][0] + " -> " + str(sorted_degree[z][1]))
    
    
    plt.figure(figsize = (100, 10))
    plt.plot( [y[1] for y in sorted_degree], color="red",  marker="o")
    plt.title("Degree sequence for " + lbls1[i])
    plt.xticks([i for i in range(len(sorted_degree))],labels =[x[0][:10] for x in sorted_degree] )
    plt.grid(True)
    plt.savefig('Output_Files/matplotlib/Degree/ ' + lbls1[i])
    #plt.show()
    plt.clf()
    plt.close()
    print("\n")
    
    
    
    clust_coefficients = nx.clustering(G)
    
    plt.figure(figsize=(100, 10))
    plt.title("Clustering plot for " + lbls1[i])
    plt.bar(*zip(*clust_coefficients.items()))
    plt.savefig('Output_Files/matplotlib/Clust_seq/ ' + lbls1[i])
    plt.clf()
    plt.close()
#     plt.show()
    
    avg_clust_coeff = sum(clust_coefficients.values()) / len(clust_coefficients)  
    
    
    
    plt.figure(figsize = (100, 10))
    plt.title("Degree distribution for " + lbls1[i])
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.grid(True)    
    degree_counter = collections.Counter(degree_dict.values())
#     print(degree_counter)
    degree_counter = dict(sorted(degree_counter.items(), key=itemgetter(0)))
#     print(degree_counter)
    plt.plot(degree_counter.keys(), degree_counter.values(), color="red",  marker="o")
#     for key in degree_counter.keys():
#         plt.plot(key, degree_counter[key], color="red",  marker="o")
    plt.xticks([t for t in range(max(degree_counter.keys())+1)])        
#     plt.show()
    plt.savefig('Output_Files/matplotlib/Degree_Dist/ ' + lbls1[i])
    plt.clf()
    plt.close() 
    
    
    
    plt.figure(figsize = (125, 10))
    plt.title("Clustering coeff vs Degree plot for " + lbls1[i])
    plt.xlabel("Degree")
    plt.ylabel("Clustering coefficient")
    plt.grid(True)
    degrees_coeffs = {}
    for city in clust_coefficients.keys():
        degrees_coeffs[degree_dict[city]] = clust_coefficients[city]
    degrees_coeffs = dict(sorted(degrees_coeffs.items(), key=itemgetter(0)))
    plt.plot(degrees_coeffs.keys(), degrees_coeffs.values(), color="red",  marker="o")
    plt.xticks([t for t in range(max(degrees_coeffs.keys())+1)])
    plt.savefig('Output_Files/matplotlib/Ck_plots/ ' + lbls1[i])
    print("HAHA",sys.getsizeof(523)) 
    plt.clf()
    print("HAHA",sys.getsizeof(G)) 
    plt.close()

    
    print("Average clustering coefficient for", lbls1[i], "is", avg_clust_coeff)
    


# In[15]:


for i in range(30,len(graphs)):
    print(lbls1[i])
    G = graphs[i]
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
   
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    #print(sorted_degree)

    print("Top 10 nodes")
    for z in range(len(sorted_degree[:10])):
        print(sorted_degree[z][0] + " -> " + str(sorted_degree[z][1]))
    
    
    plt.figure(figsize = (100, 10))
    plt.plot( [y[1] for y in sorted_degree], color="red",  marker="o")
    plt.title("Degree sequence for " + lbls1[i])
    plt.xticks([i for i in range(len(sorted_degree))],labels =[x[0][:10] for x in sorted_degree] )
    plt.grid(True)
    plt.savefig('Output_Files/matplotlib/Degree/ ' + lbls1[i])
    #plt.show()
    plt.clf()
    plt.close()
    print("\n")
    
    
    
    clust_coefficients = nx.clustering(G)
    
    plt.figure(figsize=(100, 10))
    plt.title("Clustering plot for " + lbls1[i])
    plt.bar(*zip(*clust_coefficients.items()))
    plt.savefig('Output_Files/matplotlib/Clust_seq/ ' + lbls1[i])
    plt.clf()
    plt.close()
#     plt.show()
    
    avg_clust_coeff = sum(clust_coefficients.values()) / len(clust_coefficients)  
    
    
    
    plt.figure(figsize = (100, 10))
    plt.title("Degree distribution for " + lbls1[i])
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.grid(True)    
    degree_counter = collections.Counter(degree_dict.values())
#     print(degree_counter)
    degree_counter = dict(sorted(degree_counter.items(), key=itemgetter(0)))
#     print(degree_counter)
    plt.plot(degree_counter.keys(), degree_counter.values(), color="red",  marker="o")
#     for key in degree_counter.keys():
#         plt.plot(key, degree_counter[key], color="red",  marker="o")
    plt.xticks([t for t in range(max(degree_counter.keys())+1)])        
#     plt.show()
    plt.savefig('Output_Files/matplotlib/Degree_Dist/ ' + lbls1[i])
    plt.clf()
    plt.close() 
    
    
    
    plt.figure(figsize = (125, 10))
    plt.title("Clustering coeff vs Degree plot for " + lbls1[i])
    plt.xlabel("Degree")
    plt.ylabel("Clustering coefficient")
    plt.grid(True)
    degrees_coeffs = {}
    for city in clust_coefficients.keys():
        degrees_coeffs[degree_dict[city]] = clust_coefficients[city]
    degrees_coeffs = dict(sorted(degrees_coeffs.items(), key=itemgetter(0)))
    plt.plot(degrees_coeffs.keys(), degrees_coeffs.values(), color="red",  marker="o")
    plt.xticks([t for t in range(max(degrees_coeffs.keys())+1)])
    plt.savefig('Output_Files/matplotlib/Ck_plots/ ' + lbls1[i])
    print("HAHA",sys.getsizeof(523)) 
    plt.clf()
    print("HAHA",sys.getsizeof(G)) 
    plt.close()

    
    print("Average clustering coefficient for", lbls1[i], "is", avg_clust_coeff)


# In[ ]:





# In[ ]:


# TODO: plots for in and out degree

in_degree_freq = nx.degree_histogram(G)
#out_degree_freq = degree_histogram(G, out_degree=True)
degrees = range(len(in_degree_freq))
plt.figure(figsize=(12, 8)) 
plt.loglog(range(len(in_degree_freq)), in_degree_freq, 'go-', label='in-degree') 
# plt.loglog(range(len(out_degree_freq)), out_degree_freq, 'bo-', label='out-degree')
plt.xlabel('Degree')
plt.ylabel('Frequency')


# In[ ]:





# In[ ]:




