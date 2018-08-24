import copy
# 说明：用来操作 ClassifyValue 数据表···

def GetExistClassifyValueInfoDict(MysqlObject):
    # 获取已经存在的 ClassifyValue 表详细记录信息
    try:
        ExistClassifyValueInfoDict = {}  # 例如：ExistClassifyValueInfoDict{2:[1,'男','性别']}
        SelectClassifyValueCommand = "select ClassifyValueMap,TagClassifyMap,ClassifyValue,FatherTagName  from %s.ClassifyValue;" % (MysqlObject._UseDatabase)
        MysqlObject._MysqlCursor.execute(SelectClassifyValueCommand)
        ExistClassifyValueTupleList = MysqlObject._MysqlCursor.fetchall()
        if ExistClassifyValueTupleList:
            for ExistClassifyValueTuple in ExistClassifyValueTupleList:
                if ExistClassifyValueTuple[0] not in ExistClassifyValueInfoDict:
                    ExistClassifyValueInfoDict[ExistClassifyValueTuple[0]] = [ExistClassifyValueTuple[1],ExistClassifyValueTuple[2],ExistClassifyValueTuple[3]]
        return ExistClassifyValueInfoDict
    except Exception as result:
        print("获取 ClassifyValue 表记录错误！ %s" % result)

def InsertClassifyValueRegister(MysqlObject):
    ExistClassifyValueInfoDict=copy.deepcopy(GetExistClassifyValueInfoDict(MysqlObject))
    ExistClassifyValueInfoList=[]
    for ExistClassifyValueMap in ExistClassifyValueInfoDict:
        ExistClassifyValueInfoList.append(ExistClassifyValueInfoDict[ExistClassifyValueMap])

    for FirstFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"]:
        if FirstFloorKey=='MainClass':
            for SecondFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey]:
                if 'ClassifyValue' in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]:
                    for FourthlyFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ClassifyValue']:
                        ResultRegisterClassifyValueList=['TagClassifyMap','ClassifyValue','FatherTagName']
                        ResultRegisterClassifyValueList[0]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyMap']
                        ResultRegisterClassifyValueList[1]=FourthlyFloorKey
                        ResultRegisterClassifyValueList[2]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyName']

                        if ResultRegisterClassifyValueList not in ExistClassifyValueInfoList:
                            # 准备插入此条 ClassifyValue记录···
                            TagClassifyComboName=SecondFloorKey.split('_')
                            if len(TagClassifyComboName) != 3:  # 检验标签类型名称，命名是否符合规范要求···
                                print("标签种类命名不符合规范：（例如：\"华为_Phone_Equal\"）")
                                return
                            ClassifyValueDict = {"TagGradeFlag": '',"ClassifyValueFlag": '', "ValueMin": '', "ValueMax": ''}
                            ClassifyValueDict["TagGradeFlag"]=2
                            if TagClassifyComboName[2]=='':
                                ClassifyValueDict["ClassifyValueFlag"] = 'Equal'
                            else:
                                ClassifyValueDict["ClassifyValueFlag"] = TagClassifyComboName[2]

                            if ClassifyValueDict["ClassifyValueFlag"]=='Equal':
                                InsertClassifyValueCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,FatherTagName,TagGradeFlag,ClassifyValueFlag)  " \
                                                           "values (%d,'%s','%s','%d','%s');" % (MysqlObject._UseDatabase,ResultRegisterClassifyValueList[0],ResultRegisterClassifyValueList[1],
                                                                                                 ResultRegisterClassifyValueList[2],ClassifyValueDict['TagGradeFlag'],ClassifyValueDict['ClassifyValueFlag'])
                                MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                MysqlObject._MysqlDatabase.commit()

                            if ClassifyValueDict["ClassifyValueFlag"]=='Range':
                                ClassifyValueComplex = FourthlyFloorKey.split('-')
                                if len(ClassifyValueComplex) == 2:  # 当范围型标签值可分出最大及最小值时···
                                    ClassifyValueDict['ValueMin'] = int(ClassifyValueComplex[0])
                                    ClassifyValueDict['ValueMax'] = int(ClassifyValueComplex[1])
                                else:
                                    if "以上" in ClassifyValueComplex[0]:
                                        ClassifyValueDict['ValueMin'] = int(ClassifyValueComplex[0].split("以上")[0])
                                        ClassifyValueDict['ValueMax'] = 99999999
                                    else:
                                        ClassifyValueDict['ValueMin'] = int(ClassifyValueComplex[0])
                                        ClassifyValueDict['ValueMax'] = int(ClassifyValueComplex[0])
                                InsertClassifyValueCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,FatherTagName,TagGradeFlag,ClassifyValueFlag,ValueMin,ValueMax)  " \
                                                           "values (%d,'%s','%s','%d','%s',%d,%d);" % (
                                                               MysqlObject._UseDatabase,
                                                               ResultRegisterClassifyValueList[1],
                                                               ResultRegisterClassifyValueList[2],
                                                               ResultRegisterClassifyValueList[3],
                                                               ClassifyValueDict["TagGradeFlag"],
                                                               ClassifyValueDict["ClassifyValueFlag"],
                                                               ClassifyValueDict["ValueMin"],
                                                               ClassifyValueDict["ValueMax"])
                                MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                MysqlObject._MysqlDatabase.commit()

                elif 'ChildClass' in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]:
                    for FourthlyFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ChildClass']:
                        for FifthFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ChildClass'][FourthlyFloorKey]:
                            if FifthFloorKey=='ChildClassTotal':
                                ResultRegisterClassifyValueList=['TagClassifyMap','ClassifyValue','FatherTagName']
                                ResultRegisterClassifyValueList[0]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyMap']
                                ResultRegisterClassifyValueList[1]=FourthlyFloorKey
                                ResultRegisterClassifyValueList[2]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyName']

                                if ResultRegisterClassifyValueList not in ExistClassifyValueInfoList:
                                    ClassifyValueDict = {"TagGradeFlag": '', "ClassifyValueFlag": '',"ValueMin": '', "ValueMax": ''}
                                    ClassifyValueDict["TagGradeFlag"]=2
                                    ClassifyValueDict["ClassifyValueFlag"] = 'Equal'
                                    InsertClassifyValueCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,FatherTagName,TagGradeFlag,ClassifyValueFlag)  " \
                                                                 "values (%d,'%s','%s','%d','%s');" % (
                                                                 MysqlObject._UseDatabase,
                                                                 ResultRegisterClassifyValueList[0],
                                                                 ResultRegisterClassifyValueList[1],
                                                                 ResultRegisterClassifyValueList[2],
                                                                 ClassifyValueDict['TagGradeFlag'],
                                                                 ClassifyValueDict['ClassifyValueFlag'])
                                    MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                    MysqlObject._MysqlDatabase.commit()

                            elif FifthFloorKey=='ClassifyValue':
                                for SixthFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['ChildClass'][FourthlyFloorKey][FifthFloorKey]:
                                    ResultRegisterClassifyValueList = ['TagClassifyMap', 'ClassifyValue','FatherTagName']
                                    ResultRegisterClassifyValueList[0]=GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyMap']
                                    ResultRegisterClassifyValueList[1] = SixthFloorKey
                                    ResultRegisterClassifyValueList[2] = FourthlyFloorKey
                                    if ResultRegisterClassifyValueList not in ExistClassifyValueInfoList:
                                        ClassifyValueDict = {"TagGradeFlag": '', "ClassifyValueFlag": '',"ValueMin": '', "ValueMax": ''}
                                        ClassifyValueDict["TagGradeFlag"] = 3
                                        ClassifyValueDict["ClassifyValueFlag"] = 'Equal'
                                        InsertClassifyValueCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,FatherTagName,TagGradeFlag,ClassifyValueFlag)  " \
                                                                     "values (%d,'%s','%s','%d','%s');" % (
                                                                         MysqlObject._UseDatabase,
                                                                         ResultRegisterClassifyValueList[0],
                                                                         ResultRegisterClassifyValueList[1],
                                                                         ResultRegisterClassifyValueList[2],
                                                                         ClassifyValueDict['TagGradeFlag'],
                                                                         ClassifyValueDict['ClassifyValueFlag'])
                                        MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                                        MysqlObject._MysqlDatabase.commit()

        elif FirstFloorKey=='MainClassTotal':
            for SecondFloorKey in GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey]:
                ResultRegisterClassifyValueList = ['TagClassifyMap', 'ClassifyValue', 'FatherTagName']
                ResultRegisterClassifyValueList[0] = GV.FinalResultRegisterDict["ResultRegisterDict"][FirstFloorKey][SecondFloorKey]['TagClassifyMap']
                ResultRegisterClassifyValueList[1] = '主标签汇总值'
                ResultRegisterClassifyValueList[2] = GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClassTotal'][SecondFloorKey]['TagClassifyName']
                if ResultRegisterClassifyValueList not in ExistClassifyValueInfoList:
                    ClassifyValueDict = {"TagGradeFlag": '', "ClassifyValueFlag": '', "ValueMin": '', "ValueMax": ''}
                    ClassifyValueDict["TagGradeFlag"] = 1
                    ClassifyValueDict["ClassifyValueFlag"] = 'Equal'
                    InsertClassifyValueCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,FatherTagName,TagGradeFlag,ClassifyValueFlag)  " \
                                                 "values (%d,'%s','%s','%d','%s');" % (
                                                     MysqlObject._UseDatabase,
                                                     ResultRegisterClassifyValueList[0],
                                                     ResultRegisterClassifyValueList[1],
                                                     ResultRegisterClassifyValueList[2],
                                                     ClassifyValueDict['TagGradeFlag'],
                                                     ClassifyValueDict['ClassifyValueFlag'])
                    MysqlObject._MysqlCursor.execute(InsertClassifyValueCommand)
                    MysqlObject._MysqlDatabase.commit()









