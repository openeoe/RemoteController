from apiController import kubernetesController,dockerController
import commonUtil


def createExoModule():
    inputLang = input("input language 1(C++) or 2(JAVA) : ")
    inputImage = input("input image name : ")
    inputTag = input("input Tag : ")

#    commonutil = commonUtil.commonUtil()
#    availablePortGRPC = commonutil.randomPort()
#    availablePortSSH = commonutil.randomPort()

    dockerapi = dockerController.dockerController()
    dockerapi.setInput(inputLang,inputImage, inputTag)
#    dockerapi.buildImage()
    dockerapi.pushImage()
#    kubernetesapi = kubernetesController.kubernetesController()
#    kubernetesapi.getInit(inputLang, inputImage, inputTag)
#    kubernetesapi.createDeployment()
#    kubernetesapi.createService(availablePortGRPC,availablePortSSH)

