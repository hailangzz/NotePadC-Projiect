# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 14:11:30 2018

@author: Administrator
"""
import PlotChart as pc



def SexModel(OriginDataFrame):
    
    #按照Sex(性别)分组，统计其饼图···
    #Sex=ShenZhenUserData['Sex']
    #SexPie=Sex.groupby(level=0)
    #print(sex.name,sex.index,sex.values)
    groupby_sex=OriginDataFrame.groupby('Sex')
    Sex0=groupby_sex.get_group(0).count()
    Sex1=groupby_sex.get_group(1).count()
    SexGroups=groupby_sex.groups
    #print(SexGroups)
    #print(Sex0['Sex'])
    pc.PiePlot(labels=['男','女'],DataList=[Sex1['Sex'],Sex0['Sex']])
    
        