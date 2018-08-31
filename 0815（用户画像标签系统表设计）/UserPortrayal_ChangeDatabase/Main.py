import GlobalVariable as GV
import MySQLOperation as MSQLO
import OperateClassifyValue as OCV
import OperateCooperationCompany as OCC
import OperateDataExtractBatch as ODEB
import OperateTagClassify as OTC
#import QJC_Single.OriginDataStatistics as ODS
import QJC0831.QJCMain as QJCM
import InitFinalResultRegisterDict as IFRRD
import FillTagClassifyMap as FTCM
import FillClassifyValueMap as FCVM
import FillDataExtractBatch as FDEB
import InsertResultPersonNumber as IRPN
import ExtractPublicTaskInfo as EPTI
import copy
import gc


def main1():
    #MysqlObject=MSQLO.Mysql('192.168.7.31',3306,'ngoss_dim','ngoss_dim')
    MysqlObject = MSQLO.Mysql('127.0.0.1', 3306, 'root', 'mysql')
    #print(MysqlObject._UseDatabase)
    OriginDataPath=r'./QJC_Single/test10000.txt'
    GV.ReceiveStandardDataList=copy.deepcopy(ODS.OriginDataStatistics(OriginDataPath))
    #print(GV.ReceiveStandardDataList)
    IFRRD.InitFinalResultRegisterDict()
    #print(GV.FinalResultRegisterDict)
    #插入公司映射记录···
    CompanyName=('广发银行信用卡')
    OCC.InsertCooperationCompanyRegister(MysqlObject,CompanyName)
    CompanyName1=('PPmoney')
    OCC.InsertCooperationCompanyRegister(MysqlObject,CompanyName1)

    BatchTuple=('广发银行信用卡','2018-08-27 08:23:45')
    ODEB.InsertBatchRegister(MysqlObject,BatchTuple)
    OTC.InsertTagClassifyRegister(MysqlObject)
    FTCM.FillTagClassifyMap(MysqlObject)
    OCV.InsertClassifyValueRegister(MysqlObject)
    FCVM.FillClassifyValueMap(MysqlObject)
    FDEB.FillDataExtractBatch(MysqlObject,'广发银行信用卡','2018-08-27 08:23:45')
    #print(GV.FinalResultRegisterDict)
    IRPN.InsertResultPersonNumber(MysqlObject)
    EPTI.ExtractPublicTaskInfo(MysqlObject)
    print(GV.ExtractPublicTaskInfoDict)

def main():
    # MysqlObject=MSQLO.Mysql('192.168.7.31',3306,'ngoss_dim','ngoss_dim')
    MysqlObject = MSQLO.Mysql('127.0.0.1', 3306, 'root', 'mysql')
    # print(MysqlObject._UseDatabase)
    #OriginDataPath = r'./QJC_Single/test10000.txt'
    GV.ReceiveStandardDataList = copy.deepcopy(QJCM.QJC0831_Main())
    # print(GV.ReceiveStandardDataList)
    if GV.ReceiveStandardDataList:
        for SingleReceiveStandardDataList in GV.ReceiveStandardDataList:
            IFRRD.InitFinalResultRegisterDict(SingleReceiveStandardDataList)
            EPTI.ExtractPublicTaskInfo(MysqlObject)
            print(GV.ExtractPublicTaskInfoDict)
            # print(GV.FinalResultRegisterDict)
            # 插入公司映射记录···
            CompanyName = ('广发银行信用卡')
            OCC.InsertCooperationCompanyRegister(MysqlObject, CompanyName)
            # CompanyName1 = ('PPmoney')
            # OCC.InsertCooperationCompanyRegister(MysqlObject, CompanyName1)

            BatchTuple = ('广发银行信用卡', '2018-08-27 08:23:45')
            ODEB.InsertBatchRegister(MysqlObject, BatchTuple)
            OTC.InsertTagClassifyRegister(MysqlObject)
            FTCM.FillTagClassifyMap(MysqlObject)
            OCV.InsertClassifyValueRegister(MysqlObject)
            FCVM.FillClassifyValueMap(MysqlObject)
            FDEB.FillDataExtractBatch(MysqlObject, '广发银行信用卡', '2018-08-27 08:23:45')
            # print(GV.FinalResultRegisterDict)
            IRPN.InsertResultPersonNumber(MysqlObject)
    else:
        print('没有新的数据统计分析任务···')


if __name__ == '__main__':
    main()
    gc.collect()
    #print(GV.FinalResultRegisterDict)
    print("over program!")
