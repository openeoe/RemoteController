import requests
import sys
import json
import config as cp


class exoUtil:
    '''
    엑소브레인 컨테이너화 프로젝트 유틸 클래스
    '''
    def __init__(self,namespace,inputImage):
        self.namespace = namespace
        self.apiurl="http://" + cp.kubernetesHost + ":" + cp.kubernetesPort + "/api/v1/namespaces/"+self.namespace+"/pods?labelSelector=app="+inputImage
        self.nodeName, self.imageName, self.tag, self.containerId = self.getKubernetesApi()

    def getKubernetesApi(self):
        '''
        쿠버네티스에 배포된 컨테이너 정보 수집
        '''
        r = requests.get(self.apiurl)
        jsonData=r.json()
        data = jsonData.get('items')
        nodeName=data[0].get('status').get('hostIP')
        # podName=data[0].get('metadata').get('name')
        image=data[0].get('spec').get('containers')[0].get('image')
        containerId=data[0].get('status').get('containerStatuses')[0].get('containerID')[9:]
        tag = image.split(':')[-1]
        imageName = image[:-(tag.__len__()+1)]

        return nodeName,imageName,tag,containerId


    def patchDeployment(self,inputTag):
        '''
        이미지 변경시 쿠버네티스 컨테이너 apply
        :param inputTag:
        :return:patchRes
        '''

        dpname=self.imageName.split('/')[-1]
        patchUrl = "http://" + cp.kubernetesHost + ":" + cp.kubernetesPort + "/apis/apps/v1/namespaces/" + self.namespace + "/deployments/" + dpname + "-dp"
        data = {"spec":{"template":{"spec":{"containers":[{"name":dpname,"image":self.imageName+":"+inputTag}]}}}}

        patchRes=requests.patch(patchUrl,json.dumps(data),headers=cp.patchHeader,verify=False)

        if patchRes.ok == True:
            print('Deployment 패치 완료')
        else:
            print('Deployment 패치 실패!')

        return patchRes

    def commitImage(self,inputTag):
        '''
        쿠버네티스 컨테이너 이미지로 commit
        :param inputTag:
        :return:commitRes
        '''

        commitUrl = "http://" + cp.repositoryHost + ":" + cp.repositoryPort + "/commit?container=" + self.containerId + "&repo=" + self.imageName + "&tag=" + inputTag
        commitRes = requests.post(commitUrl, headers=cp.commitHeader)

        if commitRes.ok == True:
            print('이미지 커밋 완료')
        else:
            print('이미지 커밋 실패!')

        return commitRes

    # def buildImage(self,inputTag):
    #     buildHeader={
    #         'Content-Type: application/tar'
    #     }
    #     curl - v - X POST - H "Content-Type:application/tar" --data-binary '@Dockerfile.tar.gz'
    #     http: // 10.0.0.147: 4323 / build?t = 1.0

    def pushImageFromContainer(self,inputTag):
        '''
        컨테이너 -> 이미지 도커 레지스트리 등록
        :param inputTag:
        :return:pushRes
        '''
        pushbody = {'tag': inputTag}
        pushUrl = "http://" + cp.repositoryHost + ":" + cp.repositoryPort + "/images/" + self.imageName + "/push"
        pushRes = requests.post(pushUrl, data=json.dumps(pushbody), headers=cp.pushHeader)

        return pushRes

    def deleteImage(self,repoName,inputTag):
        res = requests.head('http://nanum:nanumrltnf@10.0.0.147:5000/v2/'+repoName+'/manifests/'+inputTag,
                            headers={"Accept": "application/vnd.docker.distribution.manifest.v2+json"})

        digest = res.headers.get('Docker-Content-Digest')
        authorization = res.request.headers.get('Authorization')
        delHeader={
            "Authorization": authorization,
            "Accept": "application/vnd.docker.distribution.manifest.v2+json"
        }
        delRes = requests.delete("http://"+cp.repositoryHost+":"+cp.repositoryPort+"/v2/"+repoName+"/manifests/" + digest,
                                 headers=delHeader)
        if delRes.ok==True:
            print('이미지 삭제 완료')
        else :
            print('이미지 삭제 실패! 이미지명과 태그를 확인해 주세요')

# if __name__=="__main__":
#     inputImage = sys.argv[1]
#     inputTag = sys.argv[2]
#
#     exoutil = exoUtil("demo-service", inputImage)
#     exoutil.commitImage(inputTag)
#     print('컨테이너 커밋 완료')
#     exoutil.pushImage(inputTag)
#     print('이미지 레지스트리 등록 완료')
#     exoutil.patchDeployment(inputTag)
#     print('컨테이너 패치 완료')

    # 이미지 삭제 기능 
    # 테스트 완료
    # 현재 사용하지 않는 기능이라 주석처리
    # exoutil.deleteImage(inputImage,inputTag)

# if __name__=="__main__":
#
#     inputImage = sys.argv[1]
#     inputTag = sys.argv[2]
#
#     exoutil=exoUtil("demo-service",inputImage)
#
#     commitHeaders = {'Content-Type': 'application/json'}
#     commitUrl = "http://"+nodeName+":2376/commit?container="+containerId+"&repo="+imageName+"&tag="+inputTag
#     commitRes=requests.post(commitUrl,headers=commitHeaders)
#     print('컨테이너 커밋 완료')
#
#     pushHeaders = {
#         'X-Registry-Auth': 'ewogICJ1c2VybmFtZSI6ICJuYW51bSIsCiAgInBhc3N3b3JkIjogIm5hbnVtcmx0bmYiLAogICJlbWFpbCI6ICJkZXZAbmFudW0uY28ua3IiLAogICJzZXJ2ZXJhZGRyZXNzIjogIjEwLjAuMC4yMjQ6NTAwMCIKfQ=='}
#     pushbody = {'tag': inputTag}
#     pushUrl = "http://"+nodeName+":2376/images/"+imageName+"/push"
#     pushRes = requests.post(pushUrl,data=json.dumps(pushbody), headers=pushHeaders)
#     print('이미지 레지스트리 등록 완료')
#
#     patchDeployment(namespace, imageName, inputTag)
#     exoutil.patchDeployment(inputTag)
#     print('컨테이너 패치 완료')

