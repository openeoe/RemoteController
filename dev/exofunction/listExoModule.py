from apiController import kubernetesController,dockerController
import commonUtil


def listExoModule(runType):
    kubernetesapi = kubernetesController.kubernetesController()
    kubernetesapi.setRunType(runType)
    kubernetesapi.getList()

#def listExoModule():
#    kubernetesapi = kubernetesController.kubernetesController()
#    kubernetesapi.getList()
