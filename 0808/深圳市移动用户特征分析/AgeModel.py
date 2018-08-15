# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:15:03 2018

@author: Administrator
"""

import PlotChart as pc
import OrderByData as OBD
import numpy as np

def PileData(OriginDataFrame):
    SexList=[]
    AgeList=[]
    ManAgeHumansList=[]
    WoManAgeHumansList=[]
    GroupBy_SexAge=OriginDataFrame.groupby(['Sex','Age'])
    SexAgeListBuff=GroupBy_SexAge.groups.keys()
    for complexindex in SexAgeListBuff:
        SexList.append(complexindex[0])
        AgeList.append(complexindex[1])
    SexList=list(set(SexList))    
    AgeList=sorted(list(set(AgeList)))
    
    for SexFlag in SexList:
        if SexFlag==0:
            for AgeNumber in AgeList:
                WoManAgeHumansList.append(len(GroupBy_SexAge.groups[(SexFlag,AgeNumber)]))
        else:
            for AgeNumber in AgeList:
                ManAgeHumansList.append(len(GroupBy_SexAge.groups[(SexFlag,AgeNumber)]))
    
    SexRatio=np.array(ManAgeHumansList)/np.array(WoManAgeHumansList)
    
    TotalHeight=np.array(ManAgeHumansList)+np.array(WoManAgeHumansList)
    #print(AgeList,len(AgeList))
    #print(WoManAgeHumansList,len(WoManAgeHumansList))
    #print(ManAgeHumansList,len(ManAgeHumansList))
    pc.PileBarPlot(AgeList,WoManAgeHumansList,ManAgeHumansList,SexRatio,TotalHeight)

def AexModel(OriginDataFrame):
    AgeList=[]
    AgeHumansList=[]
    groupby_age=OriginDataFrame.groupby('Age')
    AgeListBuff=groupby_age.groups.keys()
    for AgeItem in AgeListBuff:
        AgeList.append(AgeItem)
        AgeHumansList.append(len(groupby_age.groups[AgeItem]))

        #print(AgeItem,len(groupby_age.groups[AgeItem]))
    
    #print(len(AgeHumansList),len(AgeList))
    
    OrderData=OBD.OrderByData(AgeList,AgeHumansList,axis=0,ascending=True)
    pc.BarPlot(OrderData['X'],OrderData['Y'])
    PileData(OriginDataFrame)
    
        
        