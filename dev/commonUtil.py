import random
import os

class commonUtil:

    def randomPort(self):
        '''
        비어있는 포트번호 체크
        :return: str(portNum)
        '''
        portNum = random.randint(30000, 32767)
        while 0 == 0:
            if os.system('netstat -ano | grep ' + str(portNum)) != 0:
                break
            elif portNum > 32767:
                portNum = random.randint(30000, 32767)
            else:
                portNum = portNum + 1
        return str(portNum)
