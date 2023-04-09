#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import sqlite3 
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

from itertools import islice
def sdk_shortest_paths(nx,G, source, target, k):
    return list(
        islice(nx.shortest_simple_paths(G, source, target, 'weight'), k)
    )
#فرض شده که تمام نودهایی که ###############
#OD 
#هستند در همان ابتدای جدول نودها قرار گرفته اند#######################################################
def sdGetAll_KshortestPath(nx,G,k,NodeODCount):    
    All_KShortest_path = []
    for i in range(0,NodeODCount):
        for j in range(0,NodeODCount):
            All_KShortest_path = All_KShortest_path + sdk_shortest_paths(nx,G, i+1, j+1, k)
    return All_KShortest_path        
#################################################################
import numpy as np
import pandas as pd
#--فرض شده سطرها مبدا و ستونها مقصد باشند
def sdGet_ODNumber_Matrix(NodeODCount,FilePathToSave = ""):
    ODNumber_Matrix = np.zeros([NodeODCount,NodeODCount],dtype=int)
    n = 1
    for i in range(0,NodeODCount):
        for j in range(0,NodeODCount):
            ODNumber_Matrix[i,j] = n
            n = n+1
    ## save to xlsx file
    ## convert your array into a dataframe
    if FilePathToSave != "":
        df = pd.DataFrame (ODNumber_Matrix)
        df.to_excel(FilePathToSave, index=False)
    return ODNumber_Matrix
#################################################################
def sdGet_DeltaOD_Matrix(G,ODNumber_Matrix,All_KshortestPathList,ODCount):#کا نشان دهنده تعداد مسیر کوتاهی است که برای هر زوج محاسبه کرده ایم 
    n,m = np.shape(ODNumber_Matrix)
    PathCount = len(All_KshortestPathList )
    # Creating DeltaOD_Matrix as sparse matrix
    DeltaOD_Matrix = csr_matrix((ODCount, len(All_KshortestPathList)), 
                              dtype = int)   
    for ODNumber in range(1,ODCount+1):
        i, j = np.where(ODNumber_Matrix == ODNumber)
        ONode = i + 1
        DNode = j + 1
        #گرفتن اندیس تمام مسیرهایی که ابتدای آن نود ابتدای این زوج باشد و انتهای آن هم نود انتهای این زوج
        all_indexes = [a for a in range(len(All_KshortestPathList)) if All_KshortestPathList[a][0]==ONode 
                      and All_KshortestPathList[a][len(All_KshortestPathList[a])-1]==DNode ]
        for g in range(len(all_indexes)):
             DeltaOD_Matrix[ODNumber-1,all_indexes[g]] = 1        

    return DeltaOD_Matrix
#--------------------------------------------------------------------------

#################################################################
def sdGet_DeltaLink_Matrix(G,LinksList,All_KshortestPathList):
    LinkCount = len(LinksList) 
    PathCount = len(All_KshortestPathList )
    #DeltaLinkMat = np.zeros([LinkCount,len(All_KshortestPathList)],dtype=int)
    DeltaLinkMat = csr_matrix((LinkCount, len(All_KshortestPathList)),dtype = int)    
    for LinkNumber in range(1,LinkCount+1):
            # کنترل اینکه زیر رشته تشکیل شده از ابتدا و انتهای لینک در داخل رشته تشکلیل شده از نودهای متوالی یک مسیر وجود دارد یا خیر            
            strtmp = str(LinksList[LinkNumber-1][0]) + str(LinksList[LinkNumber-1][1])
            all_indexes = [a for a in range(len(All_KshortestPathList)) if (''.join(map(str,All_KshortestPathList[a]) )).find(strtmp)!= -1]
            for g in range(len(all_indexes)):
                DeltaLinkMat[LinkNumber-1,all_indexes[g]] = 1
    return  DeltaLinkMat     
#################################################################
#----------رسم گراف شبکه----
def sdDrawGraph(nx,G,LinkLabel = 'link_id'):
    nx.draw(G,with_labels = True) # برای نمایش لیبل یالها with_labels = True
    #---نمایش وزن یالها
    pos=nx.spring_layout(G) # pos = nx.nx_agraph.graphviz_layout(G)
    labels = nx.get_edge_attributes(G,LinkLabel)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()
    #------


# In[2]:


#دیدن لیست کل جداول دیتابیس
#cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print(cur.fetchall())

#دیدن تمام المانهای داخل ماتریس اسپارس

#DeltaOD_Matrix.toarray()

