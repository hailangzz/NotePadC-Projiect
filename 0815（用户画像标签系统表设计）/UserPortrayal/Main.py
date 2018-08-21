
import MySQLOperation as MSQLO
import ReadTagInformation as RTI
import GlobalVariable as GV
import gc

def main():
    TagFilePath = r"./数据库map表初始化源文件.xlsx"
    RTI.ReadTagInformation(TagFilePath)
    #print(GV.UserTagClassifyDict)
    DMPUserTagDatabase=MSQLO.Mysql('127.0.0.1',3306,'root','mysql')
    DMPUserTagDatabase.CheckDatabase()
    DMPUserTagDatabase.InitAllMapTable()

if __name__ == '__main__':
    main()
    gc.collect()
    print("over program!")
