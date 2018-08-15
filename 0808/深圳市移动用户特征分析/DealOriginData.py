# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 11:16:26 2018

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

ShenZhenUserData = pd.read_table(r'E:\GitLocalRepository\NotePadC++Projiect\0808\ZZResult_0808All\Result_0808_shenzhenuser',
                         header=None,encoding='utf-8',delim_whitespace=True)
ShenZhenUserData.columns=['PhoneNumber', 'Sex', 'Age','UserCity']

#性别分布统计··
SM.SexModel(ShenZhenUserData)   
#按照Sex(性别)分组，统计其饼图···
#Sex=ShenZhenUserData['Sex']
#SexPie=Sex.groupby(level=0)
#print(sex.name,sex.index,sex.values)
groupby_sex=ShenZhenUserData.groupby('Sex')
Sex0=groupby_sex.get_group(0).count()
Sex1=groupby_sex.get_group(1).count()
SexGroups=groupby_sex.groups
#print(SexGroups)
#print(Sex0['Sex'])
#pc.PiePlot(labels=['男','女'],DataList=[Sex1['Sex'],Sex0['Sex']])

######################年龄分组
groupby_age=ShenZhenUserData.groupby('Age')
groupby_sexage=ShenZhenUserData.groupby(['Sex','Age'])
#print(groupby_sexage.groups.keys())
#print(groupby_sexage.groups[(0,27)])
#print(groupby_sexage.groups[(1,27)])
#print(groupby_age.groups.keys())
#print(len(groupby_age.groups[18]),len(groupby_age.groups[19]))
#不同年龄段的人数统计····
AM.AexModel(ShenZhenUserData)

###########分析话费部分
ShenZhenUserPhoneCharge = pd.read_table(r'E:\GitLocalRepository\NotePadC++Projiect\0808\ZZResult_0808All\Result_0808_ShenZhenUserTelePhoneCharge',
                         header=None,encoding='utf-8',delim_whitespace=True)
ShenZhenUserPhoneCharge.columns=['PhoneNumber', 'Sex', 'Age','ARPU']
#groupby_age=ShenZhenUserPhoneCharge.groupby('Sex')
#Sex0=groupby_age.get_group(0)['ARPU'].sum()
#Sex1=groupby_age.get_group(1)['ARPU'].sum()
PCM.PhoneChargeModel(ShenZhenUserPhoneCharge)

###########分析手机品牌
ShenZhenUserPhoneBrand = pd.read_table(r'E:\GitLocalRepository\NotePadC++Projiect\0808\ZZResult_0808All\Result_0808_shenzhenuserphonebrand',
                         header=None,encoding='utf-8',delim_whitespace=True,
                         delimiter='\t')
ShenZhenUserPhoneBrand.columns=['PhoneNumber', 'Sex', 'Age','PhoneBrand']
PBM.PhoneBrandModel(ShenZhenUserPhoneBrand)