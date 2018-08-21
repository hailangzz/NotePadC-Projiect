import pandas as pd
import GlobalVariable as GV

def ReadTagInformation(TagFilePath):
    TagData=pd.read_excel(TagFilePath,sheet_name=0,header=0)
    for ColumnName in TagData.columns:
        TagClassifyValueBuff=[]
        if ColumnName not in GV.UserTagClassifyDict:
            #print(ColumnName)
            GV.UserTagClassifyDict[ColumnName]=[]
            #print(TagData[ColumnName])
            if len(TagData[ColumnName])!=0:
                for ColumnsValue in TagData[ColumnName]:
                    ColumnsValue=str(ColumnsValue)
                    if ColumnsValue!='nan':
                        #GV.UserTagClassifyDict[ColumnName][ColumnsValue.split('.0')[0]] = {"map": 0}
                        ColumnsValue=ColumnsValue.split('.0')[0]
                        if ColumnsValue.upper() not in TagClassifyValueBuff:
                            GV.UserTagClassifyDict[ColumnName].append(ColumnsValue)   # 先插入类型值的列表数据，之后填充到类型值比较列表中去（做字母大小的敏感性判断··）···
                        #print(ColumnsValue)
                        #GV.UserTagClassifyDict[ColumnName].append(ColumnsValue)
                        TagClassifyValueBuff.append(ColumnsValue.upper())

                #print(TagClassifyValueBuff)
                #print(ColumnName,GV.UserTagClassifyDict[ColumnName])
                        #print(ColumnsValue.split('.0')[0],type(ColumnsValue))

                    #if ColumnsValue!='' and ColumnsValue not in GV.UserTagClassifyDict[ColumnName]:
                        #GV.UserTagClassifyDict[ColumnName][ColumnsValue]={"map":0}
                        #print (ColumnsValue)
    #print(TagData.index)
    #print(TagData.columns)
    #print(TagData.values)

#TafFilePath=r"./数据库map表初始化源文件.xlsx"
#ReadTagInformation(TafFilePath)