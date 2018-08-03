# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:47:57 2018

@author: Administrator
"""

import pandas as pd
import numpy as np

FileCur=open(r'E:\GitLocalRepository\NotePadC++Projiect\0802\Task1Dir\PreviousLoanAppList.txt','r')
PreviousLoanAppList_buf=FileCur.readlines()
PreviousLoanAppList=[]
for EachAPPName in PreviousLoanAppList_buf:
    EachAPPName=EachAPPName.split()[0]
    PreviousLoanAppList.append(EachAPPName)

ExcelDataFrame=pd.read_excel(r'E:\GitLocalRepository\NotePadC++Projiect\0802\Task1Dir\全部应用行为（6月份）.xlsx',header=0)

PartData=ExcelDataFrame[ExcelDataFrame['APP名称'].isin(PreviousLoanAppList)]
ResulrDataFrame=PartData.loc[:,['APP名称','用户数']].sort_values(by='用户数',ascending=False)