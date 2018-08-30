import copy
#说明：操作公司信息映射表的模块
def GetExistCooperationCompanyInfoDict(MysqlObject):
    CompanyInfoDict={}
    MysqlCommand = "select CompanyName,CompanyMap from %s.CooperationCompany;" % MysqlObject._UseDatabase
    MysqlObject._MysqlCursor.execute(MysqlCommand)
    CompanyRegisterTupleList = MysqlObject._MysqlCursor.fetchall()
    for RegisterTuple in CompanyRegisterTupleList:
        if RegisterTuple[0] not in CompanyInfoDict:
            CompanyInfoDict[RegisterTuple[0]]=RegisterTuple[1]

    return CompanyInfoDict

def InsertCooperationCompanyRegister(MysqlObject,CompanyTuple):
    try:
        CompanyInfoDict=copy.deepcopy(GetExistCooperationCompanyInfoDict(MysqlObject))
        if CompanyTuple[0] not in CompanyInfoDict:
            MysqlCommand = "insert into %s.CooperationCompany (CompanyName,CompanyMap) Values('%s','%s')" % (MysqlObject._UseDatabase, CompanyTuple[0], CompanyTuple[1])
            # print(MysqlCommand)
            MysqlObject._MysqlCursor.execute(MysqlCommand)
            MysqlObject._MysqlDatabase.commit()
    except Exception as result:
        print("插入公司名称记录失败！ %s" % result)


