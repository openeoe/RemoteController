import requests
import io
import yaml
# developer 모듈
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))) + '/dev')
import config as cp

class combineUtil:

    def createCombineCode(self, argv):
        '''
        조합 코드를 생성하는 코드 './pysource/test_client.py' 코드가 생성된다.
        :return: ./pysource/test_client.py
        '''
        argvList = argv.split(' ')
        argvLength = len(argvList)

        code = '';
        isFirst = True;
        for i in range(0,argvLength):
            #여기서 포트번호 찾고 코드 만들어주기
            #포트번호가져오기
            name = argvList[i]

            getUrl = 'http://'+cp.kubernetesHost+':'+cp.kubernetesPort+'/api/v1/namespaces/default/services/'+name
            print('\n=== [REQUEST] Get Service Info ===')
            print('> Url : ' + getUrl)
            response = requests.get(url=getUrl)

            #print('\n=== Make Code===')
            #print(doc)
            print('=== [RESPONSE] Get Service Info ===')
            if response.ok == True:
                print('> Get Service Info Success')
            else:
                print('> Get Service Info Failed')
                print('### Error Info ###')
                print(response)
                print('##################')

            doc = yaml.load(response.text, Loader=yaml.FullLoader)

            port = doc['spec']['ports'][0]['nodePort']
            port = str(port)

            print('\n=== Make port===')
            print(port)

            code = code + "    with grpc.insecure_channel('"+cp.kubernetesHost+":"+port+"') as channel:" + '\n'
            code = code + "        stub = module_pb2_grpc.ModuleStub(channel)" + '\n'

            input = '';
            if isFirst == True:
                input = 'inputText'
                isFirst = False
            else:
                input = 'response.str'

            code = code + "        response = stub.runModule(module_pb2.Request(str="+input+"))" + '\n'
            code = code + "        print('"+ name +" Done')" + '\n'

        #print('\n=== Make Code===')

        r = io.open('./pysource/test_client.py_bak', mode='rt', encoding='utf-8')
        clientCode = r.read()
        #print(clientCode)
        newClientCode = clientCode.replace('codeLocation', code)
        print('=== Make Code===')
        print(newClientCode)
        r.close()

        f = io.open('./pysource/test_client.py', mode='wt', encoding='utf-8')
        f.write(newClientCode)
        f.close()

        return newClientCode
