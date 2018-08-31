# 说明：将每一个批次的所有插入操作集合到一个函数中进行···
import GlobalVariable as GV

def InitEachBatchGlobalVariable():
    GV.FinalResultRegisterDict = {"CompanyName": '', "BatchDate": '', "BatchMap": '',"ResultRegisterDict": {"MainClass": {}, "MainClassTotal": {}}}
    GV.ClassifyMapDict = {"TagClassifyName": '', "TagClassifyMap": 0, "ClassifyValueDict": {}}
    GV.InsertResultRegisterDict = {'InsertBatchAndValueMapList': [], 'TotalPopulationList': []}

def EachBatchGroupOperation(MysqlObject):
    for ExtractTask in GV.ExtractPublicTaskInfoDict['ExtractTaskID']:
        InitEachBatchGlobalVariable()
        OCC.InsertCooperationCompanyRegister(MysqlObject, GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTask]['labelname'])
        ODEB.InsertBatchRegister(MysqlObject, (GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTask]['labelname'],GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTask]['createtime']))
        OTC.InsertTagClassifyRegister(MysqlObject)
        FTCM.FillTagClassifyMap(MysqlObject)
        OCV.InsertClassifyValueRegister(MysqlObject)
        FCVM.FillClassifyValueMap(MysqlObject)
        FDEB.FillDataExtractBatch(MysqlObject, GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTask]['labelname'], GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTask]['createtime'])
        IRPN.InsertResultPersonNumber(MysqlObject)



