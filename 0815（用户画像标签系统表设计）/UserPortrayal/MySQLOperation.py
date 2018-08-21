import pymysql
import datetime
import GlobalVariable as GV
import copy

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
        #self.CheckDatabase(self._UseDatabase)


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

    def CreateTable(self,DatabaseName="usertag"):
        #self.CreateDatabase(DatabaseName)
        try:
            MysqlCommand="use %s;" % DatabaseName
            CreateCooperationCompany="create table if not exists CooperationCompany(ID int auto_increment unique,CompanyName Varchar(50)  not null unique, CompanyMap  Char(20),PRIMARY KEY(CompanyMap ));"
            CreateDataExtractBatch="create table if not exists DataExtractBatch (CompanyMap  Char(20) not null, BatchDate date not null , BatchMap int auto_increment,PRIMARY KEY(BatchMap),unique KEY complex_unique(CompanyMap  , BatchDate),FOREIGN KEY (CompanyMap) REFERENCES CooperationCompany (CompanyMap));"
            CreateTagClassify="create table if not exists TagClassify ( TagClassifyName Varchar(50)  not null unique,TagClassifyFlag char(20)  not null default 'mainclass', TagClassifyMap  int auto_increment,PRIMARY KEY(TagClassifyMap ));"
            CreateClassifyValue="create table if not exists ClassifyValue (TagClassifyMap int, ClassifyValue Varchar(50) not null ,ClassifyValueFlag char(20) not null default 'Equal',ValueMin int ,ValueMax int, ClassifyValueMap  int auto_increment,PRIMARY KEY(ClassifyValueMap),unique KEY complex_unique(TagClassifyMap ,ClassifyValue),FOREIGN KEY (TagClassifyMap) REFERENCES TagClassify (TagClassifyMap));"
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
        self.CreateTable(DatabaseName)
        '''
        for Table in RequisiteTableList:
            if Table.lower() not in DatabaseTableList:
                self.CreateTable(DatabaseName)
        '''
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

    def InsertBatchAction(self,BatchDataDict):
        try:
            #BatchTuple=list(BatchTuple)
            CompanyMap='NULL'
            # 查询公司名称映射值···
            SelectCompanyMapCommand = "select CompanyMap from %s.CooperationCompany where CompanyName='%s';" % (self._UseDatabase, BatchDataDict['CompanyName'])
            self._MysqlCursor.execute(SelectCompanyMapCommand)
            CompanyMapTuple = self._MysqlCursor.fetchone()
            CompanyMap = CompanyMapTuple[0]
            BatchDataDict['CompanyMap'] = CompanyMapTuple[0]

            # 检索批次信息表，防止插入非法批次记录信息···
            BatchTuple = (BatchDataDict['CompanyMap'],BatchDataDict['BatchDateString'])
            BatchDateList = []
            MysqlCommand = "select CompanyMap,DATE_FORMAT(BatchDate,'%%Y-%%m-%%d') from %s.DataExtractBatch;" % self._UseDatabase
            # print(MysqlCommand)
            self._MysqlCursor.execute(MysqlCommand)
            BatchRegisterTupleList = self._MysqlCursor.fetchall()
            for RegisterTuple in BatchRegisterTupleList:
                BatchDateList.append(tuple([RegisterTuple[0], RegisterTuple[1]]))

            # print(BatchDateList)
            # print(BatchTuple)
            # 当新插入的二元彼此信息数据不存在重复（合法）时，进行插入操作，否则返回“无法插入说明···”
            if BatchTuple not in BatchDateList:
                #print(CompanyMapTuple)
                MysqlCommand = "insert into %s.DataExtractBatch (CompanyMap,BatchDate) Values('%s','%s')" % (
                self._UseDatabase, CompanyMap, BatchTuple[1])
                self._MysqlCursor.execute(MysqlCommand)
                self._MysqlDatabase.commit()
            else:
                print("无法插入批次记录，批次重复···")


        except Exception as result:
            print("插入数据批次记录错误！ %s" % result)

    def InsertBatchRegister(self,BatchTuple):
        try:
            if len(BatchTuple)==2: # 当录入完整批次信息时···
                BatchTuple = list(BatchTuple)
                CompanyMap = 'NULL'
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

                # print(BatchDateList)
                # print(BatchTuple)
                # 当新插入的二元彼此信息数据不存在重复（合法）时，进行插入操作，否则返回“无法插入说明···”
                if BatchTuple not in BatchDateList:
                    print(CompanyMapTuple)
                    MysqlCommand = "insert into %s.DataExtractBatch (CompanyMap,BatchDate) Values('%s','%s')" % (self._UseDatabase, CompanyMap, BatchTuple[1])
                    self._MysqlCursor.execute(MysqlCommand)
                    self._MysqlDatabase.commit()
                else:
                    print("无法插入批次记录，批次重复···")

            else:  # 当用户没有输入日期字段信息时，默认读取当前的日期信息插入记录···
                #nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在，获取当前时间的字符串信息
                nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
                #print(nowTime)
                #print(BatchTuple,type(BatchTuple))
                BatchDataDict={'CompanyName':'','BatchDateString':'','CompanyMap':''}
                BatchDataDict['CompanyName']=BatchTuple
                BatchDataDict['BatchDateString'] = nowTime
                self.InsertBatchAction(BatchDataDict)
                #print(BatchDataDict)
        except Exception as result:
            print("插入数据批次记录错误！ %s" % result)


     #此时，用户画像标签种类命名的协议规范为，是子标签类的类名称为："子类名称_父类名称（Flag）_此类的运算形式（相等运算、范围比较运算）"例如：sex__equal,
    def InsertTagClassifyRegister(self,TagClassify):
        #插入用户画像标签种类映射记录···
        try:
            #自动拆分检索标签种类名称（查看是否包含子标签的Flag标志信息，并存储到TagClassifyDict数据结构中）
            TagClassifyDict={"TagClassifyName":'',"TagClassifyFlag":'',"ClassifyValueAlgorithm":''}
            TagClassifyCombo=TagClassify.split('_')
            if len(TagClassifyCombo)!=3:      #检验标签类型名称，命名是否符合规范要求···
                print("标签种类命名不符合规范：（例如：\"华为_Phone_Equal\"）")
                return
            TagClassifyDict["TagClassifyName"]=TagClassifyCombo[0]
            TagClassifyDict["TagClassifyFlag"] = TagClassifyCombo[1]

            # 首先，检索标签种类映射表，看标签种类名称是否已经存在···
            ExistTagClassifyList=[]
            SelectTagClassifyCommand = "select TagClassifyName  from %s.TagClassify;" % (self._UseDatabase)
            self._MysqlCursor.execute(SelectTagClassifyCommand)
            ExistTagClassifyTupleList = self._MysqlCursor.fetchall()
            for TagClassifyTuple in ExistTagClassifyTupleList:
                ExistTagClassifyList.append(TagClassifyTuple[0])

            # 判断，当将要插入的新标签种类不存在于标签映射表中时，执行在新增标签的插入操作···
            if TagClassifyDict["TagClassifyName"] not in ExistTagClassifyList:
                if TagClassifyDict["TagClassifyFlag"] =='':
                    InsertTagClassifyCommand = "insert into %s.TagClassify (TagClassifyName)  values ('%s');" % (self._UseDatabase,TagClassifyDict["TagClassifyName"])
                    self._MysqlCursor.execute(InsertTagClassifyCommand)
                    self._MysqlDatabase.commit()
                else:
                    InsertTagClassifyCommand = "insert into %s.TagClassify (TagClassifyName,TagClassifyFlag)  values ('%s','%s');" % (self._UseDatabase,TagClassifyDict["TagClassifyName"],TagClassifyDict["TagClassifyFlag"])
                    self._MysqlCursor.execute(InsertTagClassifyCommand)
                    self._MysqlDatabase.commit()
            else:
                print("标签种类插入失败，标签种类重复···")

        except Exception as result:
            print("插入标签种类记录错误！ %s" % result)

    def InsertClassifyValueRegister(self,TagClassify,TagClassifyValueList):
        # 插入用户画像标签种类对应值的映射记录···
        try:
            ClassifyValueList=[]
            if type(TagClassifyValueList) is str:
                ClassifyValueList.append(TagClassifyValueList)
            else:
                ClassifyValueList=list(TagClassifyValueList)

            if type(ClassifyValueList) is not list or len(ClassifyValueList)==0:
                print("输入的标签种类值不是列表类型···")
                return
            # 自动拆分检索标签种类名称（查看是否包含子标签的Flag标志信息，并存储到TagClassifyDict数据结构中）
            #TagClassifyDict = {"TagClassifyName": '', "TagClassifyFlag": '', "ClassifyValueAlgorithm": ''}
            TagClassifyCombo = TagClassify.split('_')
            if len(TagClassifyCombo) != 3:  # 检验标签类型名称，命名是否符合规范要求···
                print("标签种类命名不符合规范：（例如：\"华为_Phone_Equal\"）")
                return
            # TagClassifyDict["TagClassifyName"] = TagClassifyCombo[0]
            # TagClassifyDict["TagClassifyFlag"] = TagClassifyCombo[1]
            # TagClassifyDict["ClassifyValueAlgorithm"] = TagClassifyCombo[2]

            ClassifyValueDict={"TagClassifyName":'',"TagClassifyMap":'',"ClassifyValue":'',"ClassifyValueFlag":'',"ValueMin":'',"ValueMax":''}
            ClassifyValueDict["TagClassifyName"]=TagClassifyCombo[0]
            if TagClassifyCombo[2]=='':
                ClassifyValueDict["ClassifyValueFlag"]='Equal'
            else:
                ClassifyValueDict["ClassifyValueFlag"] = TagClassifyCombo[2]

            # 首先，检索标签种类映射表，检索出标签种类名称对应的映射值（TagClassifyMap）,将用到标签种类值映射表的记录插入中···
            ExistTagClassifyList = []
            SelectTagClassifyCommand = "select TagClassifyMap  from %s.TagClassify where TagClassifyName='%s';" % (self._UseDatabase,ClassifyValueDict["TagClassifyName"])
            self._MysqlCursor.execute(SelectTagClassifyCommand)
            ExistTagClassifyTupleList = self._MysqlCursor.fetchall()
            #print(ExistTagClassifyTupleList)
            if len(ExistTagClassifyTupleList)==0:  #此时表示此标签种类名称（TagClassify），并没有插入到标签种类映射表中( 则：立即插入)···
                self.InsertTagClassifyRegister(TagClassify)
            else:
                ClassifyValueDict["TagClassifyMap"]=ExistTagClassifyTupleList[0][0]
                #print(ExistTagClassifyTupleList,len(ExistTagClassifyTupleList))


            # 先将所有的ClassifyValue表中存在的，标签名称映射和标签值名称统一存储到内存数组中，一遍做插入前的校验···（防止插入非法记录）
            ExistClassifyValueComplexAll = []
            ClassifyValueComplexSingle = [0, 0]
            SelectTagClassifyCommand = "select TagClassifyMap,ClassifyValue from %s.ClassifyValue;" % (self._UseDatabase)
            self._MysqlCursor.execute(SelectTagClassifyCommand)
            ExistTagClassifyTupleList = self._MysqlCursor.fetchall()

            for TagClassifyTuple in ExistTagClassifyTupleList:

                #print(TagClassifyTuple)
                #print(ClassifyValueComplexSingle)
                #print(TagClassifyTuple[0],TagClassifyTuple[1])
                ClassifyValueComplexSingle[0] = TagClassifyTuple[0]
                ClassifyValueComplexSingle[1] = TagClassifyTuple[1]
                #print(ClassifyValueComplexSingle)
                ExistClassifyValueComplexAll.append(ClassifyValueComplexSingle)
            #print(ExistClassifyValueComplexAll)

            #将每一个标签种类值列表（ClassifyValueList），中的标签种类值，计入标签种类值字典结构中（ClassifyValueDict）···
            for ClassifyValue in ClassifyValueList:
                if type(ClassifyValue) is not str:
                    print("标签种类的值列表中，有标签值类型不符（%s）···" % ClassifyValue)
                    return

                ClassifyValueDict['ClassifyValue']=ClassifyValue
                if ClassifyValueDict["ClassifyValueFlag"]=='Range':        #当标签值的运算标志为，区间运算时·····
                    ClassifyValueComplex=ClassifyValue.split('-')
                    if len(ClassifyValueComplex)==2:     #当范围型标签值可分出最大及最小值时···
                        ClassifyValueDict['ValueMin'] = int(ClassifyValueComplex[0])
                        ClassifyValueDict['ValueMax'] = int(ClassifyValueComplex[1])
                    else:
                        if "以上" in ClassifyValueComplex[0]:
                            ClassifyValueDict['ValueMin']=int(ClassifyValueComplex[0].split("以上")[0])
                            ClassifyValueDict['ValueMax']=99999999
                        else:
                            ClassifyValueDict['ValueMin'] = int(ClassifyValueComplex[0])
                            ClassifyValueDict['ValueMax'] = int(ClassifyValueComplex[0])
                    # 此时将准备好的标签字段值字典数据结构写入到，标签值映射表中（ClassifyValue）···
                    # 1.检索ClassifyValue表中记录，防止插入重复的，标签映射和标签映射值组合的情况发生···
                    CheckClassifyValueComplex = [ClassifyValueDict["TagClassifyMap"],
                                                 ClassifyValueDict["ClassifyValue"]]
                    if CheckClassifyValueComplex in ExistClassifyValueComplexAll:
                        print("%s,记录已经存在，在标签值映射表中···") % str(CheckClassifyValueComplex)
                        continue  # 当标签映射及标签值组合已经存在时，跳过并继续循环···

                    # 此时执行插入操作,(插入标签值字典结构字段记录)···
                    else:
                        InsertTagClassifyCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,ClassifyValueFlag,ValueMin,ValueMax)  " \
                                                   "values (%d,'%s','%s',%d,%d);" % (
                                                   self._UseDatabase, ClassifyValueDict["TagClassifyMap"],
                                                   ClassifyValueDict["ClassifyValue"],
                                                   ClassifyValueDict["ClassifyValueFlag"],
                                                   ClassifyValueDict["ValueMin"], ClassifyValueDict["ValueMax"])
                        self._MysqlCursor.execute(InsertTagClassifyCommand)
                        self._MysqlDatabase.commit()

                else:   #当 ClassifyValueDict["ClassifyValueFlag"]='Equal'时;

                    #此时将准备好的标签字段值字典数据结构写入到，标签值映射表中（ClassifyValue）···
                    # 1.检索ClassifyValue表中记录，防止插入重复的，标签映射和标签映射值组合的情况发生···
                    CheckClassifyValueComplex=[ClassifyValueDict["TagClassifyMap"],ClassifyValueDict["ClassifyValue"]]
                    if CheckClassifyValueComplex in ExistClassifyValueComplexAll:
                        print("%s,记录已经存在，在标签值映射表中···") % str(CheckClassifyValueComplex)
                        continue                   #当标签映射及标签值组合已经存在时，跳过并继续循环···

                    #此时执行插入操作,(插入标签值字典结构字段记录)···
                    else:
                        InsertTagClassifyCommand = "insert into %s.ClassifyValue (TagClassifyMap,ClassifyValue,ClassifyValueFlag)  " \
                                                   "values (%d,'%s','%s');" % (self._UseDatabase, ClassifyValueDict["TagClassifyMap"],ClassifyValueDict["ClassifyValue"],
                                                                                     ClassifyValueDict["ClassifyValueFlag"])
                        self._MysqlCursor.execute(InsertTagClassifyCommand)
                        self._MysqlDatabase.commit()
        except Exception as result:
            print("插入标签种类记录错误！ %s" % result)

    def SelectBatchMap(self):
        try:
            SelectTagClassifyCommand = "select CompanyMap  from %s.CooperationCompany Where CompanyName='%s';" % (self._UseDatabase,GV.FinalResultRegisterDict["CompanyName"])
            self._MysqlCursor.execute(SelectTagClassifyCommand)
            ExistCompanyTupleList = self._MysqlCursor.fetchone()
            #print(ExistTagClassifyTupleList)
            if not ExistCompanyTupleList:
                print('插入数据的公司名称不存在···')
                return
            else:
                GV.FinalResultRegisterDict["CompanyMap"]=int(ExistCompanyTupleList[0])

                # 紧接着，查询批次的映射值信息（BatchMap）
                SelectTagClassifyCommand = "select BatchMap  from %s.DataExtractBatch Where CompanyMap=%d and BatchDate='%s';" % (
                self._UseDatabase, GV.FinalResultRegisterDict["CompanyMap"],GV.FinalResultRegisterDict["BatchDate"])
                #print(SelectTagClassifyCommand)
                self._MysqlCursor.execute(SelectTagClassifyCommand)
                ExistExtractBatchTupleList = self._MysqlCursor.fetchone()
                #print(ExistTagClassifyTupleList)
                if  not ExistExtractBatchTupleList:
                    print('插入批次映射不存在···')
                    return
                else:
                    GV.FinalResultRegisterDict["BatchMap"] = int(ExistExtractBatchTupleList[0])
        except Exception as result:
            print("插入数据批次映射查询错误！ %s" % result)

    def SelectClassifyValueMap(self):
        try:
            SelectTagClassifyCommand = "select TagClassifyName,TagClassifyMap  from %s.TagClassify;" % (self._UseDatabase)
            self._MysqlCursor.execute(SelectTagClassifyCommand)
            ExistTagClassifyTupleList = self._MysqlCursor.fetchall()
            #print(ExistTagClassifyTupleList)
            if not ExistTagClassifyTupleList:
                print('用户画像标签种类映射表为空···')
                return

            else:
                for EachClassifyMapTuple in ExistTagClassifyTupleList:
                    #print(EachClassifyMapTuple)
                    if EachClassifyMapTuple[0] not in GV.FinalResultRegisterDict["ResultRegisterDict"]:
                        GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]=copy.deepcopy(GV.ClassifyMapDict)
                        GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]["TagClassifyMap"]=EachClassifyMapTuple[1]

                        # 查询标签种类映射值及对应标签值的，标签值映射信息····
                        SelectTagClassifyCommand = "select ClassifyValue,ClassifyValueMap  from %s.ClassifyValue Where TagClassifyMap=%d ;" % (
                            self._UseDatabase, GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]["TagClassifyMap"])
                        #print(SelectTagClassifyCommand)
                        self._MysqlCursor.execute(SelectTagClassifyCommand)
                        ExistClassifyValueTupleList = self._MysqlCursor.fetchall()
                        #print(ExistTagClassifyTupleList)
                        if not ExistClassifyValueTupleList:
                            print('插入标签值的映射不存在:%s···' % EachClassifyMapTuple)
                            return
                        else:
                            for ClassifyValueTuple in ExistClassifyValueTupleList:
                                if ClassifyValueTuple[0] not in GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]["ClassifyValueDict"]:
                                    GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]["ClassifyValueDict"][ClassifyValueTuple[0]] = {"ClassifyValueMap":int(ClassifyValueTuple[1]),"PersonNumber":0}

        except Exception as result:
            print("插入数据前映射信息检索错误！ %s" % result)



    def InsertResultRegister(self,CommpanyName,BatchDate):  #插入最终的结果数据之前，首先将合作公司映射表、批次映射、标签映射表、标签值映射表、等信息加载到内存中，以便最终的结果插入···
        GV.FinalResultRegisterDict["CompanyName"]=CommpanyName
        GV.FinalResultRegisterDict["BatchDate"] = BatchDate
        #print(GV.FinalResultRegisterDict)
        self.SelectBatchMap()
        #print(GV.FinalResultRegisterDict)
        self.SelectClassifyValueMap()
        #print(GV.FinalResultRegisterDict)
        #print(GV.FinalResultRegisterDict["ResultRegisterDict"].keys())
        #print( GV.FinalResultRegisterDict["ResultRegisterDict"][EachClassifyMapTuple[0]]["ClassifyValueDict"].keys())

    def InitAllMapTable(self):
        for TagClassify in GV.UserTagClassifyDict:
            self.InsertTagClassifyRegister(TagClassify)
            self.InsertClassifyValueRegister(TagClassify, GV.UserTagClassifyDict[TagClassify])

    def DatabaseClose(self):
        self._MysqlDatabase.close()


testa=Mysql('127.0.0.1',3306,'root','mysql')
#testa.InsertTagClassifyRegister('手机品牌_mainclass_')
#testa.InsertClassifyValueRegister('手机品牌_mainclass_',['汇总值'])
testa.InsertCompanyRegister(('PPmoney',2312))
testa.InsertBatchRegister(('PPmoney'))

testa.InsertResultRegister('PPmoney','2018-8-20')
#testa.InsertCompanyRegister(('PPmoney',2312))
#testa.InsertBatchRegister(('PPmoney'))
#testa.InsertTagClassifyRegister('性别__')
#testa.InsertClassifyValueRegister('性别__Range',['12-15'])
#testa.InsertResultRegister('PPmoney','2018-8-20')
#testa.CreateDatabase('Usertag')
#testa.CreateTable('Usertag')
