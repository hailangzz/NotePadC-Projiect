# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 14:47:10 2018

@author: Administrator
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PlotChart as pc
import SexModel as SM
import AgeModel as AM
import PhoneChargeModel as PCM
import PhoneBrandModel as PBM

AList=[]
series1=pd.Series([10,20,30],index=['A','B','C'],name="数值")
name=series1.name
index=list(series1.index)
values=series1.values
print (series1.name)
print(series1.index)
print(series1.values)



ShenZhenUserPhoneBrand = pd.read_table(r'E:\GitLocalRepository\NotePadC++Projiect\0808\ZZResult_0808All\Result_0808_shenzhenuserphonebrand',
                         header=None,encoding='utf-8',delim_whitespace=True,
                         delimiter='\t')
ShenZhenUserPhoneBrand.columns=['PhoneNumber', 'Sex', 'Age','PhoneBrand']
GroupBy_SexAge=ShenZhenUserPhoneBrand.groupby(['Sex','Age'])
SexAgeListBuff=GroupBy_SexAge.groups.keys()

PhoneBrandList=list(GroupBy_SexAge.get_group((0,18))['PhoneBrand'].value_counts().index)
PhoneBrandNumberList=list(GroupBy_SexAge.get_group((0,18))['PhoneBrand'].value_counts().values)
PhoneBrandSeries=GroupBy_SexAge.get_group((0,18))['PhoneBrand'].value_counts()[:10]
PhoneBrandSeries1=GroupBy_SexAge.get_group((0,29))['PhoneBrand'].value_counts()[:10]
PhoneBrandSeries2=GroupBy_SexAge.get_group((0,39))['PhoneBrand'].value_counts()[:10]
AList.append(PhoneBrandSeries)
AList.append(PhoneBrandSeries1)
AList.append(PhoneBrandSeries2)
