# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 13:47:41 2018

@author: Administrator
"""
import pandas as pd
import numpy as np

FileCur=open(r'E:\GitLocalRepository\NotePadC++Projiect\0802\Task1Dir\TestList.txt','r')
PreviousLoanAppList_buf=FileCur.readlines()
PreviousLoanAppList=[]
for EachAPPName in PreviousLoanAppList_buf:
    EachAPPName=EachAPPName.split()[0]
    PreviousLoanAppList.append(EachAPPName)

ExcelDataFrame=pd.read_excel(r'E:\GitLocalRepository\NotePadC++Projiect\0802\Task1Dir\ExcelTest.xlsx')

part1=ExcelDataFrame.loc[:,['appname','values']] 
part2=ExcelDataFrame.iloc[3] 
part3=ExcelDataFrame.iloc[[1,2,4],[0,1]]

part4=ExcelDataFrame[ExcelDataFrame['appname'].isin(PreviousLoanAppList)]
part4=part4.sort_values(by='values',ascending=False)