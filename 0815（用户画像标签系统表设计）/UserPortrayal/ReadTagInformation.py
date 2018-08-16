import pandas as pd
import GlobalVariable as GV

def ReadTagInformation(TafFilePath):
    TagData=pd.read_excel(TafFilePath,sheet_name=0,header=0)
    for ColumnName in TagData.columns:
        if ColumnName not in GV.UserTagClassifyDict:
            #print(ColumnName)
            GV.UserTagClassifyDict[ColumnName]={}
            #print(TagData[ColumnName])
            if len(TagData[ColumnName])!=0:
                for ColumnsValue in TagData[ColumnName]:
                    ColumnsValue=str(ColumnsValue)
                    if ColumnsValue!='nan' and ColumnsValue not in GV.UserTagClassifyDict[ColumnName]:
                        GV.UserTagClassifyDict[ColumnName][ColumnsValue] = {"map": 0}
                        #print(ColumnsValue.split('.0')[0],type(ColumnsValue))

                    #if ColumnsValue!='' and ColumnsValue not in GV.UserTagClassifyDict[ColumnName]:
                        #GV.UserTagClassifyDict[ColumnName][ColumnsValue]={"map":0}
                        #print (ColumnsValue)
    #print(TagData.index)
    #print(TagData.columns)
    #print(TagData.values)




TafFilePath=r"./数据库map表初始化源文件.xlsx"
ReadTagInformation(TafFilePath)