from apiController import dockerController
from exofunction import listExoModule

def commitExoModule():
    print('=== 컨테이너 구동 정보 ===')
    listExoModule.listExoModule('dev')   #리스트 목록 출력

    inputImage = input("저장하실 모듈 이름을 입력해주세요. ")
    inputTag = input("저장하실 버전(Tag)을 입력해주세요. ")
    dockerapi = dockerController.dockerController()
    dockerapi.setInput(inputImage, inputTag)
    dockerapi.getContainerInfo(inputImage)
    buildRes = dockerapi.commitImage(inputTag)
    if buildRes.ok != True:
        print('image commit 실패 ! 이미지명과 태그를 확인해 주세요')
