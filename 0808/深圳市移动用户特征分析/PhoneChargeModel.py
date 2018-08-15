# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 14:56:56 2018

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
    ManAgeHumansListAvg=[]
    WoManAgeHumansListAvg=[]
    
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
                WoManAgeHumansList.append(GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].sum())
                WoManAgeHumansListAvg.append(GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].sum()/GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].count())
        else:
            for AgeNumber in AgeList:                
                #print(GroupBy_SexAge.groups[(SexFlag,AgeNumber)])
                ManAgeHumansList.append(GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].sum())
                ManAgeHumansListAvg.append(GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].sum()/GroupBy_SexAge.get_group((SexFlag,AgeNumber))['ARPU'].count())
    
    #SexRatio=np.array(ManAgeHumansList)/np.array(WoManAgeHumansList)
    
    #TotalHeight=np.array(ManAgeHumansList)+np.array(WoManAgeHumansList)
    #print(AgeList,len(AgeList))
    #print(WoManAgeHumansList,len(WoManAgeHumansList))
    #print(ManAgeHumansList,len(ManAgeHumansList))
    pc.BarPlot(AgeList,WoManAgeHumansList,title="深圳女性不同年龄总话费")
    pc.BarPlot(AgeList,ManAgeHumansList,title="深圳男性不同年龄总话费")
    
    pc.BarPlot(AgeList,WoManAgeHumansListAvg,title="深圳女性不同年龄平均话费")
    pc.BarPlot(AgeList,ManAgeHumansListAvg,title="深圳男性不同年龄平均话费")
    
    

def PhoneChargeModel(OriginDataFrame):
    
    groupby_age=OriginDataFrame.groupby('Sex')
    Sex0_PhoneCharge=groupby_age.get_group(0)['ARPU'].sum()
    Sex1_PhoneCharge=groupby_age.get_group(1)['ARPU'].sum()
    
    Sex0_PhoneCharge_Avg=groupby_age.get_group(0)['ARPU'].sum()/groupby_age.get_group(0)['ARPU'].count()
    Sex1_PhoneCharge_Avg=groupby_age.get_group(1)['ARPU'].sum()/groupby_age.get_group(0)['ARPU'].count()
     
    pc.PiePlot(labels=['男','女'],DataList=[Sex1_PhoneCharge,Sex0_PhoneCharge],title="男、女总话费比例图")
    print("男、女性总话费（6个月）",round(Sex1_PhoneCharge,1),round(Sex0_PhoneCharge,1))
    pc.PiePlot(labels=['男','女'],DataList=[Sex1_PhoneCharge_Avg,Sex0_PhoneCharge_Avg],title="男、女平均话费比例图")
    print("男、女性总话费（6个月）",round(Sex1_PhoneCharge_Avg,1),round(Sex0_PhoneCharge_Avg,1))
    PileData(OriginDataFrame)