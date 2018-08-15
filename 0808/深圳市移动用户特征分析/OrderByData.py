# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:48:28 2018

@author: Administrator
"""
import numpy as np

def OrderByData(Origin_X,Origin_Y,axis=1,ascending=False):
    
    if axis==1 and ascending==False:
        OrderDict={'X':'',
                   'Y':''}
        Order_X=[]
        Order_Y=[]
        Origin_X=np.array(Origin_X)
        Origin_Y=np.array(Origin_Y)
        
        IndexArgSort=np.argsort(-Origin_Y)
        for index in IndexArgSort:
            Order_X.append(Origin_X[index])
            Order_Y.append(Origin_Y[index])
        
        OrderDict['X']=Order_X
        OrderDict['Y']=Order_Y        
        return OrderDict
    
    elif axis==1 and ascending==True:
        OrderDict={'X':'',
                   'Y':''}
        Order_X=[]
        Order_Y=[]
        Origin_X=np.array(Origin_X)
        Origin_Y=np.array(Origin_Y)
        
        IndexArgSort=np.argsort(Origin_Y)
        for index in IndexArgSort:
            Order_X.append(Origin_X[index])
            Order_Y.append(Origin_Y[index])
        
        OrderDict['X']=Order_X
        OrderDict['Y']=Order_Y        
        return OrderDict
    
    elif axis==0 and ascending==False:
        OrderDict={'X':'',
                   'Y':''}
        Order_X=[]
        Order_Y=[]
        Origin_X=np.array(Origin_X)
        Origin_Y=np.array(Origin_Y)
        
        IndexArgSort=np.argsort(-Origin_X)
        for index in IndexArgSort:
            Order_X.append(Origin_X[index])
            Order_Y.append(Origin_Y[index])
        
        OrderDict['X']=Order_X
        OrderDict['Y']=Order_Y        
        return OrderDict
    
    elif axis==0 and ascending==True:        
        OrderDict={'X':'',
                   'Y':''}
        Order_X=[]
        Order_Y=[]
        Origin_X=np.array(Origin_X)
        Origin_Y=np.array(Origin_Y)
        
       
        IndexArgSort=np.argsort(Origin_X)
        
        for index in IndexArgSort:
            Order_X.append(Origin_X[index])
            Order_Y.append(Origin_Y[index])
        
        OrderDict['X']=Order_X
        OrderDict['Y']=Order_Y
              
        return OrderDict