# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 13:41:46 2018

@author: Administrator
"""
import PlotChart as pc
import OrderByData as OBD
import numpy as np

def EveryBrandPlot(WoManAgeHumansList_BrandSeries,ManAgeHumansList_BrandSeries,AgeList,WoManPhoneBrandList,ManPhoneBrandList):
    #计算不同年龄段使用手机的女生总人数···：
    EveryAgeWoManNumber=[]     
    EveryAgeManNumber=[]
    for AgeIndex in range(len(AgeList)):                
        UsePhoneWoManNumber=0        
        for WoManPhoneBrand in WoManAgeHumansList_BrandSeries[AgeIndex].index:
            UsePhoneWoManNumber+=WoManAgeHumansList_BrandSeries[AgeIndex][WoManPhoneBrand]
        EveryAgeWoManNumber.append(UsePhoneWoManNumber)        
                
        UsePhoneManNumber=0
        for ManPhoneBrand in ManAgeHumansList_BrandSeries[AgeIndex].index:
            UsePhoneManNumber+=ManAgeHumansList_BrandSeries[AgeIndex][ManPhoneBrand]
        EveryAgeManNumber.append(UsePhoneManNumber)
      
    #不同年龄段女性的使用不同手机的频数统计显示····    
    for WoManPhoneBrand in WoManPhoneBrandList:
        PhongBrandNumberList=[]
        for AgeIndex in range(len(AgeList)):            
            if WoManPhoneBrand in WoManAgeHumansList_BrandSeries[AgeIndex].index:
                PhongBrandNumberList.append(WoManAgeHumansList_BrandSeries[AgeIndex][WoManPhoneBrand])
            else:
                PhongBrandNumberList.append(0)
        #print(WoManPhoneBrand,len(AgeList),len(PhongBrandNumberList))
        pc.BarPlot(AgeList,PhongBrandNumberList,title="不同年龄段女性\""+WoManPhoneBrand+"\"手机频数")
    
    for WoManPhoneBrand in WoManPhoneBrandList:
        PhongBrandNumberPercentList=[]
        for AgeIndex in range(len(AgeList)):            
            if WoManPhoneBrand in WoManAgeHumansList_BrandSeries[AgeIndex].index:
                PhongBrandNumberPercentList.append(WoManAgeHumansList_BrandSeries[AgeIndex][WoManPhoneBrand]/EveryAgeWoManNumber[AgeIndex])
            else:
                PhongBrandNumberPercentList.append(0) 
                
        pc.BarPlot(AgeList,PhongBrandNumberPercentList,title="不同年龄段女性\""+WoManPhoneBrand+"\"手机占有率")
        
    for ManPhoneBrand in ManPhoneBrandList:
        PhongBrandNumberPercentList=[]
        for AgeIndex in range(len(AgeList)):            
            if ManPhoneBrand in ManAgeHumansList_BrandSeries[AgeIndex].index:
                PhongBrandNumberPercentList.append(ManAgeHumansList_BrandSeries[AgeIndex][ManPhoneBrand]/EveryAgeManNumber[AgeIndex])
            else:
                PhongBrandNumberPercentList.append(0) 
                
        pc.BarPlot(AgeList,PhongBrandNumberPercentList,title="不同年龄段男性\""+ManPhoneBrand+"\"手机占有率")
    
    
def AgeStairPhoneBrand(OriginDataFrame,WoManPhoneBrandList,ManPhoneBrandList):
    SexList=[]
    AgeList=[]
    ManAgeHumansList_BrandSeries=[]
    WoManAgeHumansList_BrandSeries=[]
    
    GroupBy_SexAge=OriginDataFrame.groupby(['Sex','Age'])
    SexAgeListBuff=GroupBy_SexAge.groups.keys()
    for complexindex in SexAgeListBuff:
        SexList.append(complexindex[0])
        AgeList.append(complexindex[1])
    SexList=list(set(SexList))    
    AgeList=sorted(list(set(AgeList)))
    
    
    for SexFlag in SexList:
        WoManPhoneBrand=[]
        #WoManPhoneBrandcount=[]
        ManPhoneBrand=[]  
        if SexFlag==0:
            for AgeNumber in AgeList:
                #PhoneBrandList=[]
                #PhoneBrandNumberList=[]                
                #PhoneBrandList=list(GroupBy_SexAge.get_group((0,18))['PhoneBrand'].value_counts().index)
                #PhoneBrandNumberList=list(GroupBy_SexAge.get_group((0,18))['PhoneBrand'].value_counts().values)
                #GroupBy_SexAge.get_group((SexFlag,AgeNumber))['PhoneBrand'].sum()                
                #for 
                #WoManAgeHumansList.append(len(GroupBy_SexAge.groups[(SexFlag,AgeNumber)]))
                PhoneBrandSeries=GroupBy_SexAge.get_group((SexFlag,AgeNumber))['PhoneBrand'].value_counts()[:10]
                WoManAgeHumansList_BrandSeries.append(PhoneBrandSeries)
                
                for PhoneBrand in PhoneBrandSeries.index:
                    if PhoneBrand not in WoManPhoneBrand:
                        WoManPhoneBrand.append(PhoneBrand)
                        #WoManPhoneBrandcount.append(PhoneBrandSeries[PhoneBrand])                        
            WoManPhoneBrand=list(set(WoManPhoneBrand))
           # print(WoManPhoneBrand,WoManPhoneBrandcount)
                
                
        else:
            for AgeNumber in AgeList:
                #ManAgeHumansList.append(len(GroupBy_SexAge.groups[(SexFlag,AgeNumber)]))
                PhoneBrandSeries=GroupBy_SexAge.get_group((SexFlag,AgeNumber))['PhoneBrand'].value_counts()[:10]
                ManAgeHumansList_BrandSeries.append(PhoneBrandSeries)
                for PhoneBrand in PhoneBrandSeries.index:
                    if PhoneBrand not in WoManPhoneBrand:
                        ManPhoneBrand.append(PhoneBrand)
            ManPhoneBrand=list(set(ManPhoneBrand))            
            #print(ManPhoneBrand,len(ManAgeHumansList_BrandSeries))   
    
    EveryBrandPlot(WoManAgeHumansList_BrandSeries,ManAgeHumansList_BrandSeries,AgeList,WoManPhoneBrandList,ManPhoneBrandList)
    

def PhoneBrandModel(OriginDataFrame):
    
    groupby_age=OriginDataFrame.groupby('Sex')
    Sex0_PhoneBrand=groupby_age.get_group(0)['PhoneBrand']
    Sex1_PhoneBrand=groupby_age.get_group(1)['PhoneBrand']
    
    #只分析前 20 的手机品牌····
    ManPhoneBrandList=[]    
    WoManPhoneBrandList=[]
    ManPhoneBrandCountList=[]    
    WoManPhoneBrandCountList=[]
    
    ManPhoneBrandList=list(Sex1_PhoneBrand.value_counts()[:12].index)
    ManPhoneBrandCountList=list(Sex1_PhoneBrand.value_counts()[:12].values)
    
    WoManPhoneBrandList=list(Sex0_PhoneBrand.value_counts()[:12].index)
    WoManPhoneBrandCountList=list(Sex0_PhoneBrand.value_counts()[:12].values)
    
    print(ManPhoneBrandList,ManPhoneBrandCountList)
    print(WoManPhoneBrandList,WoManPhoneBrandCountList)
    #print(Sex0_PhoneBrand.value_counts()[:20],type(Sex0_PhoneBrand.value_counts()),
           #Sex0_PhoneBrand.value_counts().name)
           
    pc.BarPlot(WoManPhoneBrandList,WoManPhoneBrandCountList,title="深圳女性手机品牌统计",x_ticks=True)
    pc.BarPlot(ManPhoneBrandList,ManPhoneBrandCountList,title="深圳男性不同年龄总话费",x_ticks=True)
    
    AgeStairPhoneBrand(OriginDataFrame,WoManPhoneBrandList,ManPhoneBrandList)