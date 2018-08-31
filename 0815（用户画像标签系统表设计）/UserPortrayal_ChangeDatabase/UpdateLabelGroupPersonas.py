# 说明：操作完成后，更新公用数据查询批次表的状态码信息····
import GlobalVariable as GV

def UpdateLabelGroupPersonas(MysqlObject):
    try:
        for ExtractTaskID in GV.ExtractPublicTaskInfoDict['ExtractTaskID']:
            MysqlCommand = "update %s.label_group_personas set  status=%d,endtime=%s where filename=%s;" % (MysqlObject._UseDatabase,GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTaskID]['status'],
                                                                                                            GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTaskID]['endtime'],
                                                                                                            GV.ExtractPublicTaskInfoDict['ExtractTaskID'][ExtractTaskID]['filename']
                                                                                                            )
            MysqlObject._MysqlCursor.execute(MysqlCommand)
            MysqlObject._MysqlCursor.commit()
    except Exception as result:
        print("更新公用数据查询批次表信息失败！ %s" % result)