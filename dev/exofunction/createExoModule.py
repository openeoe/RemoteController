from apiController import kubernetesController,dockerController
import commonUtil
import config as cp

def createExoModule():
    inputLang = input("개발 언어를 입력해주세요. [java / c]  : ")
    inputImage = input("생성하실 이미지 이름을 입력해주세요.  : ") #유니크한 이름이어야 합니다. 문구 추가?
    inputTag = input("생성하실 버전(Tag)을 입력해주세요. : ")

    print("\n\n# 1. Setting Module ")
    commonutil = commonUtil.commonUtil()
    availablePortGRPC = commonutil.randomPort()
    availablePortSSH = commonutil.randomPort()


    print("# 2. Make Image... ")
    dockerapi = dockerController.dockerController()
    dockerapi.setInput(inputImage, inputTag)
    dockerapi.setLang(inputLang)

    buildRes = dockerapi.buildImage()
    if buildRes.ok != True:
        print('image build 실패 ! 이미지명과 태그를 확인해 주세요')
    #pushRes = dockerapi.pushImage()
    #if pushRes.ok != True:
    #    print('image push 실패 ! 이미지명과 태그를 확인해 주세요')


    print("# 3. Start Image... ")
    containerCreateSuccess = True;
    kubernetesapi = kubernetesController.kubernetesController()
    kubernetesapi.getInit(inputImage, inputTag)
    kubernetesapi.setRunType('dev')

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



    print("\n\n\n# 언어모듈 생성 결과 ===")
    if containerCreateSuccess != True:
        print('이미 동일한 이름의 언어모듈이 실행 중입니다.')
    else :
        print("* 생성된 언어모듈 이름 : " + inputImage)
        print("* 생성된 SSH 접속 포트 : " + availablePortSSH)
        print("* 생성된 이미지 이름 : " + cp.repositoryHost + ":" + cp.repositoryPort + "/" + inputImage + ":" + inputTag)
