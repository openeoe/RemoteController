
# -*- coding: utf-8 -*-
from importlib import reload
from combine import combineUtil

# developer 모듈
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/dev')
from exofunction import listExoModule
from apiController import kubernetesController,dockerController
import config as cp
import commonUtil

#reload(sys)
#sys.setdefaultencoding("utf-8")

if __name__ == "__main__":

    print('=== 컨테이너 구동 정보 ===')
    listExoModule.listExoModule('dev')

    argv = input("\n조합할 언어 모듈 이름을 순서대로 입력해주세요. [ex:qanal psfaq] : ")
    inputTail = input("생성하실 식별자를 입력해주세요.[ex:law] : ")
    inputTag = input("생성하실 버전명을 입력해주세요.[ex:1.0] : ")


    print("\n\n# 1. Setting Module ")
    inputImage = 'combine-' + inputTail # TODO Config 로 빼내야 한다.
    inputContainerName = inputImage

    commonutil = commonUtil.commonUtil()
    availablePortGRPC = commonutil.randomPort()
    availablePortSSH = commonutil.randomPort()

    print("\n\n# 2. Make CombineCode ")
    combineUtil = combineUtil.combineUtil()
    codepath = combineUtil.createCombineCode(argv)



    print("\n\n# 3. Make Image... ")
    dockerapi = dockerController.dockerController()
    dockerapi.setInput(inputImage, inputTag)

    buildRes = dockerapi.buildImageForOperator()
    if buildRes.ok != True:
        print('image build 실패 ! 이미지명과 태그를 확인해 주세요')
    pushRes = dockerapi.pushImage()
    if pushRes.ok != True:
        print('image push 실패 ! 이미지명과 태그를 확인해 주세요')




    print("\n\n# 4. Start Image... ")

    ### random port
    containerCreateSuccess = True;
    kubernetesapi = kubernetesController.kubernetesController()
    kubernetesapi.getInit(inputContainerName, inputTag)
    kubernetesapi.setRunType('ops')

    createRes = kubernetesapi.createDeployment()
    if createRes.ok != True:
        containerCreateSuccess = False;
        print('컨테이너 생성 실패 ')
        if createRes.status_code == 409:
            print('이미 서비스가 실행 중입니다.')
        elif createRes.status_code == 422:
            print('생성된 코드에 오류가 있습니다. 관리자에게 문의해주세요.')

    createRes2 = kubernetesapi.createService(availablePortGRPC,availablePortSSH)
    if createRes2.ok != True:
        containerCreateSuccess = False;
        print('서비스 생성 실패 ')
        if createRes.status_code == 409:
            print('이미 서비스가 실행 중입니다.')
        elif createRes.status_code == 422:
            print('생성된 코드에 오류가 있습니다. 관리자에게 문의해주세요.')



    print("\n\n\n# Operator 생성 결과 ===")
    if containerCreateSuccess != True:
        print('이미 동일한 이름의 Operator 가 실행 중입니다.')
    else :
        print("* 생성된 Operator 이름 : " + inputContainerName)
        print("* 생성된 SSH 접속 포트 : " + availablePortSSH)
        print("* 생성된 Operator 이미지 이름 : " + cp.repositoryHost + ":" + cp.repositoryPort + "/" + inputImage + ":" + inputTag)
