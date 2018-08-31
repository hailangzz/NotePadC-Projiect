import QJC0831.GetNewFilePath as GetNewFilePath
import paramiko
import os
path = r'F:\data_resource\file_xzt\filenames\app_filename.txt'
severse_path = '/home/appSys/RIOpenApi4UMC/xzt1/app'
new_path=(GetNewFilePath.new_filenamepath(path, severse_path))
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport(GetNewFilePath.conf['host_ip'], GetNewFilePath.conf['port'])
        t.connect(username=GetNewFilePath.conf['username'], password=GetNewFilePath.conf['password'])
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print (e)
def getfilename(path):
    for (path, path_, filename) in os.walk(path):
        return filename
data_path=[]
if len(new_path)==0:
    print('服务器还没有上传新app文件！')
else:
    print("发现新app文件")
    for name in new_path:
        paths=name
        localfilename=name.split('/')[-1]
        sftp_down_file(paths, r"F:\data_resource\file_xzt\app\%s"%(localfilename))
        data_path.append(r"F:\data_resource\file_xzt\app\%s" % (localfilename))





