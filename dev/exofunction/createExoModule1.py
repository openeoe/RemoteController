from apiController import kubernetesController,dockerController
import commonUtil


def createExoModule():
    inputImage = input("input image name : ")
    inputTag = input("input Tag : ")

    commonutil = commonUtil.commonUtil()
    availablePort = commonutil.randomPort()

    dockerapi = dockerController.dockerController()
    dockerapi.setInput(inputImage, inputTag)
    kubernetesapi = kubernetesController.kubernetesController()
    kubernetesapi.getInit(inputImage, inputTag)
    kubernetesapi.createDeployment()
    kubernetesapi.createService(availablePort)

