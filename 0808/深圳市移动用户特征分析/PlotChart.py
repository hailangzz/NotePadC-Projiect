# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:39:09 2018

@author: Administrator
"""
import matplotlib.pyplot as plt

def PiePlot(labels,DataList,title=""):
    explode = []
    for DataItem in range(len(DataList)):
        if DataItem==0:
            explode.append(0.05)
        else:
            explode.append(0.01)
        DataItem+=1
    
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    plt.axes(aspect=1)
    plt.pie(x=DataList, labels=labels, explode=explode,autopct='%3.1f %%',
        shadow=True, labeldistance=1.1, startangle = 90,pctdistance = 0.6)
    plt.title(title)
    plt.show()


def BarPlot(labels,DataList,title="",x_ticks=False):
    x_values=[]
    x_ticks_text=[]
    y_values=[]
    
    if x_ticks==False:
        
        x_values=labels
        x_ticks_text=labels
        y_values=DataList
        
        fig=plt.figure(1)
        ax1=plt.subplot(111)
        rect=ax1.bar(x=x_values,height=y_values,color="lightblue")    
        plt.xticks(x_values,x_ticks_text,fontsize=8)    
        plt.xlim(18,60)    
        #plt.grid(color='b' ,linestyle='--')
        ax1.grid(True)
        plt.title(title)
        plt.show()
        
    else:
        for x_index in range(1,len(labels)+1):
            x_values.append(x_index)
            x_ticks_text.append(labels[x_index-1])
            
        y_values=DataList
        fig=plt.figure(1)
        ax1=plt.subplot(111)
        rect=ax1.bar(x=x_values,height=y_values,color="lightblue")    
        plt.xticks(x_values,x_ticks_text,fontsize=10,rotation=45)    
        #plt.xlim(18,60)    
        #plt.grid(color='b' ,linestyle='--')
        ax1.grid(True)
        plt.title(title)
        plt.show()
    
    
    
def PileBarPlot(labels,WoManDataList1,ManDataList2,SexRatio,TotalHeight):
    x_values=[]
    y_values=[]
    x_values=labels
    y_valuesWoMan=WoManDataList1
    y_valuesMan=ManDataList2
    
    SexRatio=list(SexRatio)
    
    TotalHeight=list(TotalHeight)
    
    plt.subplot(111)
    plt.bar(x=x_values,height=y_valuesWoMan,color="blue",label='WoMan')
    plt.bar(x=x_values,height=y_valuesMan,color="red",bottom=y_valuesWoMan,label='Man')
    
    #编辑数据点比例说明····
    SexRatioindex=0
    for a,b in zip(x_values[0:40],TotalHeight[0:40]):        
        plt.text(a, b+0.05, '%.2f' % SexRatio[SexRatioindex] , ha='center', va= 'bottom',fontsize=8)
        SexRatioindex+=1
    
    plt.xticks(x_values,x_values,fontsize=8)    
    plt.xlim(x_values[0],x_values[40])    
    #plt.grid(color='b' ,linestyle='--')
    #plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()