import time
import os
import datetime
from GlobalVariable import WriteLogFilePoint as WLFP

def CreateWriteLogFile():
    if not os.path.exists(r'./Logs'):
        os.makedirs(r'./Logs')
    while True:
        #ToDay = datetime.datetime.now().strftime('%Y-%m-%d')
        time.sleep(3)
        #ToDay = datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')
        ToDay = datetime.datetime.now().strftime('%Y-%m-%d')
        if not os.path.exists(r'./Logs/%s' % ToDay):
            WLFP = open(r'./Logs/%s.log' % ToDay, 'a+')
            #print(WLFP,WLFP.name)
# while True:
#
#     #ToDay = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     ToDay = datetime.datetime.now().strftime('%Y-%m-%d')
#     with open('./Logs/test.log', 'a+') as tf:
#         i = 0
#         while True:
#             i = i + 1
#             time.sleep(1)
#             print(i, file=tf, flush=True)

CreateWriteLogFile()