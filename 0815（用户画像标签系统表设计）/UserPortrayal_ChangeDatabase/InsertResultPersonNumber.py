# 说明 ： 最终插入结果人数覆盖记录···
import GlobalVariable as GV

def GetResultBatchAndValueMap(MysqlObject):
    BatchAndValueMapList=[]
    BatchAndValueMap=['BatchMap','ClassifyValueMap']
    MysqlCommand = "select BatchMap,ClassifyValueMap from %s.ResultPersonNumber;" % MysqlObject._UseDatabase
    # print(MysqlCommand)
    MysqlObject._MysqlCursor.execute(MysqlCommand)
    BatchAndValueMapTupleList = MysqlObject._MysqlCursor.fetchall()
    if BatchAndValueMapTupleList:
        for BatchAndValueMapTuple in BatchAndValueMapTupleList:
            BatchAndValueMap[0]=BatchAndValueMapTuple[0]
            BatchAndValueMap[1] = BatchAndValueMapTuple[1]
            BatchAndValueMapList.append(BatchAndValueMap)

    return BatchAndValueMapList

def InsertResultPersonNumber(MysqlObject):
    ExistBatchAndValueMapList=GetResultBatchAndValueMap(MysqlObject)
    InsertBatchAndValueMap=['BatchMap','ClassifyValueMap']
    InsertBatchAndValueMap[0]=GV.FinalResultRegisterDict['BatchMap']
    for FirstFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"]:
        if FirstFloorKey=='MainClassTotal':
            for SecondFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey]:
                InsertBatchAndValueMap[1]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ClassifyValueDict']['主标签汇总值']["ClassifyValueMap"]
                if InsertBatchAndValueMap not in ExistBatchAndValueMapList:
                    # 此时插入结果覆盖人数记录···
                    TotalPopulation=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ClassifyValueDict']['主标签汇总值']["PersonNumber"]
                    InsertClassifyValueCommand = "insert into %s.ResultPersonNumber (BatchMap,ClassifyValueMap,TotalPopulation)  " \
                                                 "values (%d,%d,%d);" % (
                                                 MysqlObject._UseDatabase,
                                                 InsertBatchAndValueMap[0],
                                                 InsertBatchAndValueMap[1],
                                                 TotalPopulation)
                    MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                    MysqlObject._MysqlDatabase.commit()

        elif FirstFloorKey=='MainClass':
            for SecondFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey]:
                for ThirdlyFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"]:
                    if ThirdlyFloorKey=='ClassifyValue':
                        for FourthlyFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]:
                            InsertBatchAndValueMap[1] =GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]['ClassifyValueMap']
                            if InsertBatchAndValueMap not in ExistBatchAndValueMapList:
                                TotalPopulation =GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]['PersonNumber']
                                InsertClassifyValueCommand = "insert into %s.ResultPersonNumber (BatchMap,ClassifyValueMap,TotalPopulation)  " \
                                                             "values (%d,%d,%d);" % (
                                                                 MysqlObject._UseDatabase,
                                                                 InsertBatchAndValueMap[0],
                                                                 InsertBatchAndValueMap[1],
                                                                 TotalPopulation)
                                MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                MysqlObject._MysqlDatabase.commit()

                    elif ThirdlyFloorKey=='ChildClass':
                        for FourthlyFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]:
                            for FifthFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]:
                                if FifthFloorKey=='ChildClassTotal':
                                    InsertBatchAndValueMap[1] =GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]['ClassifyValueMap']
                                    if InsertBatchAndValueMap not in ExistBatchAndValueMapList:
                                        TotalPopulation =GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]['PersonNumber']
                                        InsertClassifyValueCommand = "insert into %s.ResultPersonNumber (BatchMap,ClassifyValueMap,TotalPopulation)  " \
                                                                     "values (%d,%d,%d);" % (
                                                                         MysqlObject._UseDatabase,
                                                                         InsertBatchAndValueMap[0],
                                                                         InsertBatchAndValueMap[1],
                                                                         TotalPopulation)
                                        MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                        MysqlObject._MysqlDatabase.commit()
                                elif FifthFloorKey == 'ClassifyValue':
                                    for SixthFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]:
                                        InsertBatchAndValueMap[1]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey][SixthFloorKey]['ClassifyValueMap']
                                        if InsertBatchAndValueMap not in ExistBatchAndValueMapList:
                                            TotalPopulation =GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey][SixthFloorKey]['PersonNumber']
                                            InsertClassifyValueCommand = "insert into %s.ResultPersonNumber (BatchMap,ClassifyValueMap,TotalPopulation)  " \
                                                                         "values (%d,%d,%d);" % (
                                                                             MysqlObject._UseDatabase,
                                                                             InsertBatchAndValueMap[0],
                                                                             InsertBatchAndValueMap[1],
                                                                             TotalPopulation)
                                            MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                            MysqlObject._MysqlDatabase.commit()


