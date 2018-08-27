import GlobalVariable as GV
import copy
# 说明：用于初始化，最终的覆盖人数记录插入，所需要的存储数据结果：

def InitFinalResultRegisterDict():
    if len(GV.ReceiveStandardDataList)==0:
        print("标准化结果数据列表为空")
        return
    else:
        for ReceiveStandardData in GV.ReceiveStandardDataList:
            for FirstFloorKey in ReceiveStandardData.keys():
                if FirstFloorKey=='MainClass':
                    for SecondFloorKey in ReceiveStandardData[FirstFloorKey].keys():
                        if SecondFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass']:
                            GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]=copy.deepcopy(GV.ClassifyMapDict)
                            GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["TagClassifyName"]=SecondFloorKey.split('_')[0]
                        for ThirdlyFloorKey in ReceiveStandardData[FirstFloorKey][SecondFloorKey].keys():
                            if ThirdlyFloorKey=='ClassifyValue':
                                if ThirdlyFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"]:
                                    GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]={}
                                for FourthlyFloorKey in ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey].keys():
                                    if FourthlyFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]:
                                        PersonNumber=ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey][FourthlyFloorKey]
                                        GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]={"ClassifyValueMap":'',"PersonNumber":PersonNumber}

                            elif ThirdlyFloorKey=='ChildClass':
                                if ThirdlyFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"]:
                                    GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]={}
                                for FourthlyFloorKey in ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey].keys():
                                    if FourthlyFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey]:
                                        GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]={}
                                    for FifthFloorKey in ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey][FourthlyFloorKey]:
                                        if FifthFloorKey == 'ClassifyValue':
                                            if FifthFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]:
                                                GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]={}
                                            for SixthFloorKey in ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]:
                                                if SixthFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]:
                                                    PersonNumber=ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey][SixthFloorKey]
                                                    GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey][SixthFloorKey]={"ClassifyValueMap":'',"PersonNumber":PersonNumber}
                                        elif FifthFloorKey == 'ChildClassTotal':
                                            if FifthFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey]:
                                                ChildClassTotalPersonNumber=ReceiveStandardData[FirstFloorKey][SecondFloorKey][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]
                                                GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey] = {"ClassifyValueMap": '', "PersonNumber": ChildClassTotalPersonNumber}
                                                #GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClass'][SecondFloorKey]["ClassifyValueDict"][ThirdlyFloorKey][FourthlyFloorKey][FifthFloorKey]={"ChildClassTotalName":FourthlyFloorKey+'汇总',"ClassifyValueMap":'',"PersonNumber":ChildClassTotalPersonNumber}


                elif FirstFloorKey=='MainClassTotal':
                    for SecondFloorKey in ReceiveStandardData[FirstFloorKey].keys():
                        if SecondFloorKey not in GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClassTotal']:
                            SecondFloorKey=SecondFloorKey.split('汇总')[0] #应客户端开发人员要求，去掉结尾的“汇总”字段···
                            SecondFloorKey=SecondFloorKey+'_Total_Equal'
                            PersonNumber=ReceiveStandardData[FirstFloorKey][SecondFloorKey]
                            GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClassTotal'][SecondFloorKey]=copy.deepcopy(GV.ClassifyMapDict)
                            GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClassTotal'][SecondFloorKey]['TagClassifyName']=SecondFloorKey.split('_')[0]
                            GV.FinalResultRegisterDict["ResultRegisterDict"]['MainClassTotal'][SecondFloorKey]['ClassifyValueDict'] = {"主标签汇总值":{"ClassifyValueMap":'',"PersonNumber":PersonNumber}}


