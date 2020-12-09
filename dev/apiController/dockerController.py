import requests
import json
import config as cp
from apiController import kubernetesController
import tarfile
import shutil
import os

class dockerController:
    '''
    docker API 컨트롤러
    '''
    def __init__(self):
        self.namespace = cp.namespace
        self.nodeName =""
        self.imageName = ""
        self.imageVersion = ""
        self.container = ""
        self.lang = "java"
        # self.nodeName, self.imageName, self.tag, self.containerId = self.getKubernetesApi()

    def setInput(self,inputImage,inputVersion):
        '''
        operator 의 조합기에서 사용.
        '''
        self.inputImage=inputImage
        self.inputVersion=inputVersion

    def setLang(self,inputLang):
        '''
        developer 언어모듈 에서 사용 -  build 시 필요.
        '''
        self.inputLang=inputLang
        if self.inputLang.lower() == "c".lower():
            shutil.copy('DockerfileC', 'Dockerfile')
        elif self.inputLang.lower() == "java".lower():
            shutil.copy('DockerfileJ', 'Dockerfile')
        else :
            print('> 선택된 이미지가 없습니다. C 로 자동선택됩니다.')
            shutil.copy('DockerfileC', 'Dockerfile')

    def getContainerInfo(self,inputImage):
        kubernetescontroller = kubernetesController.kubernetesController()
        nodeIp, registryImageName, imageVersion, containerId = kubernetescontroller.getKubernetesInfo(inputImage)
        self.nodeName=nodeIp
        self.imageName=registryImageName
        self.imageVersion=imageVersion
        self.containerId=containerId


    def getCommitUrl(self,inputVersion):
        '''
        get CommitUrl
        :param inputVersion:
        :return:
        '''
        commitUrl="http://" + cp.dockerHost + ":" + cp.dockerPort + "/commit?container=" + self.containerId + "&repo=" + self.imageName + "&tag=" + inputVersion
        return commitUrl


    def commitImage(self, inputVersion):
        '''
        쿠버네티스 컨테이너 이미지로 commit
        :param inputVersion:
        :return:commitRes
        '''

        commitUrl = self.getCommitUrl(inputVersion)
        print('\n=== [REQUEST] Commit Image ===')
        print('> Url : ' + commitUrl)
        print('> Header : ' + str(cp.commitHeader))
        commitRes = requests.post(commitUrl, headers=cp.commitHeader)

        print('=== [RESPONSE] Commit Image ===')
        if commitRes.ok == True:
            print('> Image Commit Success')
            print('### Success Info ###')
            print(commitRes)
            print('##################')
        else:
            print('> Image Commit Failed')
            print('### Error Info ###')
            print(commitRes)
            print('##################')

        return commitRes

    def getPushUrl(self):
        '''
        get pushUrl
        :return:
        '''
        pushUrl = "http://" + cp.dockerHost + ":" + cp.dockerPort + "/images/" + cp.repositoryHost + ":" + cp.repositoryPort + "/" + self.inputImage + "/push"
        return pushUrl

    def pushImage(self):
        '''
        도커이미지 레지스트리 등록
        :return:
        '''
        pushbody = {'tag': self.inputVersion}
        pushUrl = self.getPushUrl()
        print('\n=== [REQUEST] Push Image ===')
        print('> Url : ' + pushUrl)
        print('> Body : ' + str(pushbody))
        print('> Header : ' + str(cp.pushHeader))
        pushRes = requests.post(pushUrl, data=json.dumps(pushbody), headers=cp.pushHeader)
#        pushRes = requests.post(pushUrl, headers=cp.pushHeader)

        print('=== [RESPONSE] Push Image ===')
        if pushRes.ok == True:
            print('> Image Push Success')
            print('### Success Info ###')
            print(pushRes)
            print('##################')
        else:
            print('> Image Commit Failed')
            print('### Error Info ###')
            print(pushRes)
            print('##################')

        return pushRes

    def buildImageForOperator(self):
        os.remove('./Dockerfile.tar.gz')
        #tar = tarfile.open("Dockerfile.tar.gz", "w:gz")
        tar = tarfile.open("Dockerfile.tar.gz", "w")
        for name in ["Dockerfile", "requirements.txt", "pysource"]:
            tar.add(name)
        tar.close()
        buildUrl = "http://" + cp.dockerHost + ":" + cp.dockerPort + "/build?t=" + cp.repositoryHost + ":" + cp.repositoryPort + "/" + self.inputImage + ":" + self.inputVersion
        print('\n=== [REQUEST] Build Image ===')
        print('> Url : ' + buildUrl)
        print('> Header : ' + str(cp.buildHeader))
        # files = {'dockerfile': open('./Dockerfile.tar.gz', 'rb')}
        buildRes = requests.post(buildUrl, data=open('Dockerfile.tar.gz', 'rb').read(), headers=cp.buildHeader)

        print('=== [RESPONSE] Build Image ===')

        if buildRes.ok == True:
            print('> Build Image Success')
            print('### Success Info ###')
            print(buildRes)
            print('##################')
        else:
            print('> Build Image Failed')
            print('### Error Info ###')
            print(buildRes)
            print('##################')

        return buildRes

    def buildImage(self):
        os.remove('./Dockerfile.tar.gz')
        #tar = tarfile.open("Dockerfile.tar.gz", "w:gz")
        tar = tarfile.open("Dockerfile.tar.gz", "w")
        for name in ["Dockerfile","../module"]:
            tar.add(name)
        tar.close()
        buildUrl = "http://" + cp.dockerHost + ":" + cp.dockerPort + "/build?t=" + cp.repositoryHost + ":" + cp.repositoryPort + "/" + self.inputImage + ":" + self.inputVersion
        print('\n=== [REQUEST] Build Image ===')
        print('> Url : ' + buildUrl)
        print('> Header : ' + str(cp.buildHeader))
        # files = {'dockerfile': open('./Dockerfile.tar.gz', 'rb')}
        buildRes = requests.post(buildUrl, data=open('Dockerfile.tar.gz', 'rb').read(), headers=cp.buildHeader)

        print('=== [RESPONSE] Build Image ===')

        if buildRes.ok == True:
            print('> Build Image Success')
            print('### Success Info ###')
            print(buildRes)
            print('##################')
        else:
            print('> Build Image Failed')
            print('### Error Info ###')
            print(buildRes)
            print('##################')

        return buildRes

    def getDeleteUrl(self,repoName,imageVersion):
        '''
        get deleteUrl
        :param repoName:
        :param imageVersion:
        :return:
        '''
        res = requests.head(
            "http://" + cp.repositoryUsr + ":" + cp.repositoryPw + "@" + cp.repositoryHost + ":" + cp.repositoryPort + "/v2/" + repoName + '/manifests/' + imageVersion,
            headers=cp.authHeader)

        digest = res.headers.get('Docker-Content-Digest')
        authorization = res.request.headers.get('Authorization')
        delHeader = {
            "Authorization": authorization,
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        delUrl="http://"+cp.repositoryHost+":"+cp.repositoryPort+"/v2/"+repoName+"/manifests/" + digest
        return delUrl,delHeader

    def deleteImage(self,repoName,imageVersion):
        '''
        docker registry 이미지 삭제
        :param repoName:
        :param imageVersion:
        :return:
        '''
        delUrl, delHeader = self.getDeleteUrl(repoName,imageVersion)
        print('\n=== [REQUEST] Delete Image ===')
        print('> Url : ' + delUrl)
        print('> Header : ' + str(delHeader))
        delRes = requests.delete(delUrl,headers=delHeader)

        print('=== [RESPONSE] Delete Image ===')
        if delRes.ok==True:
            print('> Delete Image Success')
        else :
            print('> Delete Image Failed')
            print('### Error Info ###')
            print(delRes)
            print('##################')

        return delRes
