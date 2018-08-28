
UserTagClassifyDict={}  # 例如:UserTagClassifyDict={"华为":['P10','P20','F1'],"性别":['男','女']}

#最终的结果数据存储字典结果···
FinalResultRegisterDict={"CompanyName":'',"BatchDate":'',"BatchMap":'',"ResultRegisterDict":{"MainClass":{},"MainClassTotal":{}}}
ClassifyMapDict={"TagClassifyName":'',"TagClassifyMap":0,"ClassifyValueDict":{}}
WriteLogFilePoint=""
InsertResultRegisterDict={'InsertBatchAndValueMapList':[],'TotalPopulationList':[]}
#批次插入标签种类及对应值，列表字典···
BatchInsertClassifyDict={}  # 例如:UserTagClassifyDict={"华为":['P10','P20','F1'],"性别":['男','女']}
ReceiveStandardDataList=[]  # 例如:[{'MainClass': {'性别_MainClass_Equal': {'ClassifyValue': {'男': 3499, '女': 2954}}}, 'MainClassTotal': {'性别汇总': 6453}}]