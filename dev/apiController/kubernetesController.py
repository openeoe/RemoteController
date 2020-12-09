import requests
import config as cp
import json
class kubernetesController:
    '''
    쿠버네티스 API 컨트롤러
    '''

    def __init__(self):
        self.inputLang = ""
        self.inputImage = ""
        self.inputVersion = ""
        self.nameSpace=cp.namespace
        self.runCommand = "service ssh start; cd /root/grpc_nanum;./run.sh; while true; do sleep 3600; done"
        self.runType = "dev"

    def getInit(self,inputImage,inputVersion):
        '''
        operator 조합기에서 사용.
        '''
        self.inputImage = inputImage
        self.inputVersion = inputVersion

    def getLang(self,inputLang):
        '''
        developer 언어모듈 에서 사용 - 아직 동일함.
        '''
        self.inputLang = inputLang
        if self.inputLang.lower() == "c".lower():
            self.runCommand = "service ssh start; cd /root/grpc_nanum;./run.sh; while true; do sleep 3600; done"


    #def setRunCommand(self, runCommand):
    #    self.runCommand = runCommand
    def setRunType(self, runType): # develoer, operator 존재.
        self.runType = runType
        if self.runType == "ops":
            self.runCommand = "python3 test_client.py"


    def getKubernetesInfo(self,inputImage):
        if inputImage == "":
            inputImage=self.inputImage

        url= "http://" + cp.kubernetesHost + ":" + cp.kubernetesPort + "/api/v1/namespaces/" + self.nameSpace + "/pods?labelSelector=app=" + inputImage
        r = requests.get(url)
        jsonData = r.json()
        data = jsonData.get('items')
        nodeIp = data[0].get('status').get('hostIP')
        # podName=data[0].get('metadata').get('name')
        registryImageName = data[0].get('spec').get('containers')[0].get('image')
        containerId = data[0].get('status').get('containerStatuses')[0].get('containerID')[9:]
        imageVersion = registryImageName.split(':')[-1]
        imageName = registryImageName[:-(imageVersion.__len__() + 1)]

        return nodeIp, registryImageName, imageVersion, containerId

    def __createDeploymentYaml(self):
        '''
        create deployment yaml
        :return:
        '''
        baseDeployment=\
        "apiVersion: apps/v1 \n"\
        "kind: Deployment \n"\
        "metadata:\n"\
        "    name: "+self.inputImage+"\n"\
        "    labels:\n"\
        "      app: "+self.inputImage+"\n"\
        "      type: "+self.runType+"\n"\
        "spec:\n"\
        "    replicas: 1\n"\
        "    selector: \n"\
        "      matchLabels: \n"\
        "        app: "+self.inputImage+"\n"\
        "    template:\n"\
        "      metadata:\n"\
        "        labels:\n"\
        "          app: "+self.inputImage+"\n"\
        "      spec:\n"\
        "        containers:\n"\
        "        - env:\n"\
        "          - name: " + self.inputImage +"\n"\
        "            value: development\n"\
        "          image: " + cp.repositoryHost + ":" + cp.repositoryPort + "/" + self.inputImage + ":" + self.inputVersion + "\n"\
        "          imagePullPolicy: Always\n"\
        "          command: ['/bin/sh', '-c']\n"\
        "          args:\n"\
        "            - " + self.runCommand + "\n"\
        "          name: " + self.inputImage + "\n"\
        "          ports:\n"\
        "            - containerPort: " + cp.defaultGrpcPort +"\n"\
        "        imagePullSecrets:\n"\
        "          - name: docker-registry-login \n"
        return baseDeployment

    def __createServiceYaml(self,portGRPC,portSSH):
        '''
        create service yaml
        :param port:
        :return:
        '''
        baseService=\
        "kind: Service\n"\
        "apiVersion: v1\n"\
        "metadata:\n"\
        "  name: "+self.inputImage+"\n"\
        "  labels:\n"\
        "    app: "+self.inputImage+"\n"\
        "    type: "+self.runType+"\n"\
        "spec:\n"\
        "  type: NodePort\n"\
        "  ports:\n"\
        "    - name: grpc\n"\
        "      port: " + cp.defaultGrpcPort +"\n"\
        "      targetPort: " + cp.defaultGrpcPort +"\n"\
        "      nodePort: "+portGRPC+"\n"\
        "    - name: ssh\n"\
        "      port: 22\n"\
        "      targetPort: 22\n"\
        "      nodePort: "+portSSH+"\n"\
        "  selector:\n"\
        "    app: "+self.inputImage+"\n"

        return baseService

    def getCreateUrl(self,kind):
        '''
        get createUrl
        :param kind:
        :return:
        '''
        if kind=="deployment":
            createUrl = "http://" + cp.kubernetesHost + ":" + cp.kubernetesPort + "/apis/apps/v1/namespaces/" + cp.namespace + "/deployments"
        elif kind=="service":
            createUrl = "http://" + cp.kubernetesHost + ":" + cp.kubernetesPort + "/api/v1/namespaces/" + cp.namespace + "/services"
        else:
            createUrl = ""

        if self.runType == "dev":
            createUrl = createUrl + "?labelSelector=type%3Ddev"
        elif self.runType == "ops":
            createUrl = createUrl + "?labelSelector=type%3Dops"
        return createUrl

    def createDeployment(self):
        '''
        create deployment
        :return:
        '''
        createBody = self.__createDeploymentYaml()
        createUrl = self.getCreateUrl("deployment")

        print('\n=== [REQUEST] Create Deploymnet ===')
        print('> Url : ' + createUrl)
        print('> Body : ' + str(createBody))
        print('> Header : ' + str(cp.createHeader))
        createRes = requests.post(createUrl, data=createBody, headers=cp.createHeader)

        print('=== [RESPONSE] Create Deploymnet ===')
        if createRes.ok == True:
            print('> Create Deployment Success')
        else:
            print('> Create Deployment Failed')
            print('### Error Info ###')
            print(createRes)
            print('##################')

        return createRes

    def createService(self, portGRPC, portSSH):
        '''
        create service
        :param port:
        :return:
        '''
        createBody = self.__createServiceYaml(portGRPC,portSSH)
        createUrl = self.getCreateUrl("service")

        print('\n=== [REQUEST] Create Service ===')
        print('> Url : ' + createUrl)
        print('> Body : ' + str(createBody))
        print('> Header : ' + str(cp.createHeader))
        createRes = requests.post(createUrl, data=createBody, headers=cp.createHeader)

        print('=== [RESPONSE] Create Service ===')
        if createRes.ok == True:
            print('> Create Service Success')
        else:
            print('> Create Service Failed')
            print('### Error Info ###')
            print(createRes)
            print('##################')

        return createRes

    def getList(self):
        createUrl = self.getCreateUrl("service")
        r = requests.get(createUrl)
        a = r.json()
        a = str(a)
#        a = a.replace("'",'\"')
        a = a.replace('"','\\"')
        a = a.replace("'",'"')

        b = json.loads(a)
        items = b['items']

        i = 1
        for item in items:
            ports = item['spec']["ports"]
            portsCount = len(ports)
            if portsCount > 1:
                svcName = item['spec']["ports"][1]['name']
                if svcName == "ssh":
                    sshPort = item['spec']["ports"][1]['nodePort']
                    moduleName = item['spec']["selector"]["app"]
                    print(' 이름 : ' + moduleName + ' / 통신 포트 : '+str(sshPort))
                    i = i+1

    def getListDict(self):
        '''
        dict 형태로 리턴받는 pods 리스트를 출력하는 함수.
        name, grpcPort 가 필요
        '''
        result = []

        createUrl = self.getCreateUrl("service")
        r = requests.get(createUrl)
        a = r.json()
        a = str(a)
#        a = a.replace("'",'\"')
        a = a.replace('"','\\"')
        a = a.replace("'",'"')

        b = json.loads(a)
        items = b['items']

        print('dict')
        i = 1
        for item in items:
            ports = item['spec']["ports"]
            portsCount = len(ports)
            print(portsCount)
            if portsCount > 1:
                svcName = item['spec']["ports"][0]['name']
                print(svcName)
                if svcName == "grpc":
                    grpcPort = item['spec']["ports"][0]['nodePort']
                    moduleName = item['spec']["selector"]["app"]
                    print(' 이름 : ' + moduleName + ' / 통신 포트 : '+str(grpcPort))
                    result.append({
                        'opsname' : moduleName,
                        'port' : grpcPort
                    })
                    i = i+1

        return result
#
#        for i in a:
#            if str(i).find('ssh')!=-1:

 #               if str(i).find('"metadata"')!=-1:
  #                  jj = i.split(', "status"')
   #                 j = jj.split(', "metadata"')
    #            else:
     #               j = i.split(', "status"');
#
 #               k = json.loads(j[0])
  #              l = k['ports'][1]['name']
   #             if l=="ssh":
    #                b = k['ports'][1]['nodePort']
     #               c = k["selector"]["app"]
      #          print(c+str(b))
