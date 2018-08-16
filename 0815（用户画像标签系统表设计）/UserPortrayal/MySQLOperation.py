import pymysql

class Mysql:
    _MysqlHost = {"host": '', "port": 0, "user": '', "password": ''}
    _MysqlDatabase=''
    _MysqlCursor=''
    _UseDatabase=''

    def __init__(self, host, port, user, password,DatabaseName='usertag'):
        self._MysqlHost["host"]=host
        self._MysqlHost["port"]=port
        self._MysqlHost["user"]=user
        self._MysqlHost["password"]=password
        self._UseDatabase=DatabaseName.lower()
        self.ConnectMysql()
        self.CheckDatabase(self._UseDatabase)


    def ConnectMysql(self):
        try:
            self._MysqlDatabase = pymysql.connect(host=self._MysqlHost["host"],port=self._MysqlHost["port"],user=self._MysqlHost["user"], passwd=self._MysqlHost["password"])
            self._MysqlCursor=self._MysqlDatabase.cursor()
        except Exception as result:
            print("连接数据库错误！ %s" % result)

    def  CreateDatabase(self,DatabaseName):
        try:
            MysqlCommand="create database if not exists %s;" % DatabaseName
            self._MysqlCursor.execute(MysqlCommand)
        except Exception as result:
            print("新建数据库错误！ %s" % result)

    def CreateTable(self,DatabaseName):
        self.CreateDatabase(DatabaseName)
        try:
            MysqlCommand="use %s;" % DatabaseName
            CreateCooperationCompany="create table if not exists CooperationCompany(ID int auto_increment unique,CompanyName Varchar(50)  not null unique, CompanyMap  Char(20),PRIMARY KEY(CompanyMap ));"
            CreateDataExtractBatch="create table if not exists DataExtractBatch (CompanyMap  Char(20) not null, BatchDate date not null , BatchMap int auto_increment,PRIMARY KEY(BatchMap),unique KEY complex_unique(CompanyMap  , BatchDate),FOREIGN KEY (CompanyMap) REFERENCES CooperationCompany (CompanyMap));"
            CreateTagClassify="create table if not exists TagClassify ( TagClassifyName Varchar(50)  not null unique, TagClassifyMap  int auto_increment,PRIMARY KEY(TagClassifyMap ));"
            CreateClassifyValue="create table if not exists ClassifyValue (TagClassifyMap int, ClassifyValue Varchar(50) not null , ClassifyValueMap  int auto_increment,PRIMARY KEY(ClassifyValueMap),unique KEY complex_unique(TagClassifyMap  , ClassifyValue),FOREIGN KEY (TagClassifyMap) REFERENCES TagClassify (TagClassifyMap));"
            CreateResultPersonNumber="create table ResultPersonNumber (ID bigint primary key auto_increment, BatchMap int  not null, ClassifyValueMap int not null , TotalPopulation  bigint not null,unique KEY complex_unique(BatchMap  , ClassifyValueMap),FOREIGN KEY (BatchMap) REFERENCES DataExtractBatch (BatchMap),FOREIGN KEY (ClassifyValueMap) REFERENCES ClassifyValue (ClassifyValueMap));"
            self._MysqlCursor.execute(MysqlCommand)
            self._MysqlCursor.execute(CreateCooperationCompany)
            self._MysqlCursor.execute(CreateDataExtractBatch)
            self._MysqlCursor.execute(CreateTagClassify)
            self._MysqlCursor.execute(CreateClassifyValue)
            self._MysqlCursor.execute(CreateResultPersonNumber)
        except Exception as result:
            print("新建数据表错误！ %s" % result)

    def CheckDatabase(self,DatabaseName = 'usertag'):
        DatabaseName = DatabaseName
        DatabaseTuple=()
        DatabaseList = []
        MysqlCommand="show databases;"
        self._MysqlCursor.execute(MysqlCommand)
        DatabaseTuple=self._MysqlCursor.fetchall()
        for TupleList in DatabaseTuple:
            DatabaseList.append(TupleList[0])
        #print(DatabaseList)
        if  DatabaseName.lower() not in DatabaseList:
            self.CreateDatabase(DatabaseName)
        self.CheckUserTagTable(DatabaseName)

    def CheckUserTagTable(self,DatabaseName):
        RequisiteTableList=['CooperationCompany','DataExtractBatch','TagClassify','ClassifyValue','ResultPersonNumber']
        DatabaseTableTuple=()
        DatabaseTableList=[]
        MysqlCommand = "use %s;" % DatabaseName
        self._MysqlCursor.execute(MysqlCommand)
        MysqlCommand = "show tables;"
        self._MysqlCursor.execute(MysqlCommand)
        DatabaseTableTuple=self._MysqlCursor.fetchall()
        #print(DatabaseTableTuple)
        for TupleList in DatabaseTableTuple:
            DatabaseTableList.append(TupleList[0])
        #print(DatabaseTableList)
        for Table in RequisiteTableList:
            if Table.lower() not in DatabaseTableList:
                self.CreateTable(DatabaseName)

    def InsertCompanyRegister(self,CompanyTuple):
        try:
            CompanyList=[]
            CompanyMapList=[]
            MysqlCommand="select CompanyName,CompanyMap from %s.CooperationCompany;" % self._UseDatabase
            self._MysqlCursor.execute(MysqlCommand)
            CompanyRegisterTupleList = self._MysqlCursor.fetchall()
            for RegisterTuple in CompanyRegisterTupleList:
                CompanyList.append(RegisterTuple[0])
                CompanyMapList.append(RegisterTuple[1])

            if CompanyTuple[0] not in CompanyList and CompanyTuple[1] not in CompanyMapList:
                MysqlCommand="insert into %s.CooperationCompany (CompanyName,CompanyMap) Values('%s','%s')" % (self._UseDatabase,CompanyTuple[0],CompanyTuple[1])
                #print(MysqlCommand)
                self._MysqlCursor.execute(MysqlCommand)
                self._MysqlDatabase.commit()
            else:
                print("无法插入公司记录，公司名称及映射值重复···")
        except Exception as result:
            print("插入公司名称记录错误！ %s" % result)

    def InsertBatchRegister(self,BatchTuple):
        try:
            BatchTuple=list(BatchTuple)
            CompanyMap='NULL'
            if len(BatchTuple)==2: # 当录入完整批次信息时···

                #查询公司名称映射值···
                SelectCompanyMapCommand="select CompanyMap from %s.CooperationCompany where CompanyName='%s';" %(self._UseDatabase,BatchTuple[0])
                self._MysqlCursor.execute(SelectCompanyMapCommand)
                CompanyMapTuple = self._MysqlCursor.fetchone()
                CompanyMap=CompanyMapTuple[0]
                BatchTuple[0]=CompanyMapTuple[0]

                # 检索批次信息表，防止插入非法批次记录信息···
                BatchTuple = tuple(BatchTuple)
                BatchDateList = []
                MysqlCommand = "select CompanyMap,DATE_FORMAT(BatchDate,'%%Y-%%m-%%d') from %s.DataExtractBatch;" % self._UseDatabase
                # print(MysqlCommand)
                self._MysqlCursor.execute(MysqlCommand)
                BatchRegisterTupleList = self._MysqlCursor.fetchall()
                for RegisterTuple in BatchRegisterTupleList:
                    BatchDateList.append(tuple([RegisterTuple[0], RegisterTuple[1]]))
                #print(BatchDateList)
                #print(BatchTuple)

                if BatchTuple not in BatchDateList:
                    print(CompanyMapTuple)
                    MysqlCommand = "insert into %s.DataExtractBatch (CompanyMap,BatchDate) Values('%s','%s')" % (self._UseDatabase, CompanyMap, BatchTuple[1])
                    self._MysqlCursor.execute(MysqlCommand)
                    self._MysqlDatabase.commit()
                else:
                    print("无法插入批次记录，批次重复···")

            else:  # 当用户没有输入日期字段信息时，默认读取当前的日期信息插入记录···
                print("haha")


        except Exception as result:
            print("插入数据批次记录错误！ %s" % result)


testa=Mysql('127.0.0.1',3306,'root','mysql')

testa.InsertCompanyRegister(('PPmoney',2312))
testa.InsertBatchRegister(('广发银行信用卡','2018-08-11'))
#testa.CreateDatabase('Usertag')
#testa.CreateTable('Usertag')
