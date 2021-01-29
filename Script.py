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

# In[22]:


# Creating networks and stroing them
coordinates = pd.read_csv("Raw_Data/coordinates/sorted_coordinates.csv",header=0,index_col= 0)
print(coordinates)

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
    graphs.append(G)
nx.write_gml(graphs[-7], "test.gml", stringizer = str)
#print(cities)


# In[26]:


nx.draw_networkx(graphs[0],nx.get_node_attributes(graphs[0],'pos'))
nx.write_gml(graphs[0], "test.gml.gz", stringizer = str)


# # ## Network Visualization

# # In[4]:


# nodes = []
# for i in range(len(graphs)):
#     nodes.append(len(graphs[i].nodes()))

# plt.plot(nodes, color="red", marker="o")
# plt.xlabel("Year/Month (YYMM)")
# plt.xticks([i for i in range(66)], labels = lbls)
# plt.ylabel("Number of Active Airports")
# plt.title("Number of Active Airports in India")
# plt.grid(True)
# figure = plt.gcf()
# figure.set_size_inches(50, 8)
# plt.savefig('Output_Files/matplotlib/nodes')
# plt.show()


# # In[5]:


# nnodes = []
# airpor = {} 
# for i in range(len(graphs)):
#     temp = 0
#     for j in graphs[i].nodes():
#         if j not in airpor:
#             airpor[j]=  1
#             temp += 1
#     nnodes.append(temp)
# nnodes[0] = 0

# plt.plot(nnodes, color="red", marker="o")
# plt.xlabel("Year/Month (YYMM)")
# plt.xticks([i for i in range(66)], labels = lbls)
# plt.ylabel("Number of New Airports")
# plt.title("Number of New Airports in India")
# plt.grid(True)
# plt.ylim(-1,6)
# figure = plt.gcf()
# figure.set_size_inches(50, 10)
# plt.savefig('Output_Files/matplotlib/newnodes')
# plt.show()


# # In[6]:


# edges = []
# for i in range(len(graphs)):
#     edges.append(len(graphs[i].edges()))

# plt.plot(edges, color="red", marker="o")
# plt.xlabel("Year/Month (YYMM)")
# plt.xticks([i for i in range(66)], labels = lbls)
# plt.ylabel("Number of Active Airport Connections")
# plt.title("Number of Active Airport Connections in India")
# plt.grid(True)
# figure = plt.gcf()
# figure.set_size_inches(50, 8)
# plt.savefig('Output_Files/matplotlib/edges')
# plt.show()


# # In[7]:


# plt.plot(passengers, color="red",  marker="o")
# plt.xlabel("Year/Month (YYMM)")
# plt.xticks([i for i in range(66)],labels = lbls)
# plt.ylabel("Number of Passengers")
# plt.title("Number of Passengers Travelling in India")
# plt.grid(True)
# figure = plt.gcf()
# figure.set_size_inches(50, 8)
# plt.savefig('Output_Files/matplotlib/passengers')
# plt.show()


# # In[9]:


# for i in sorted(airpor.keys()):
#     print(i)


# # excel = pd.read_csv("Raw_Data/coordinates/sorted_coordinates.csv",header=0)
# # tempcity = list(excel["Cities"])
# # #print(tempcity)
# # for i in sorted(airpor.keys()):
# #     if i not in tempcity:
# #         print(i)

# # In[23]:





# # In[ ]:





# # In[ ]:




