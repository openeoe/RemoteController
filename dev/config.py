#config 데이타
repositoryHost= "129.254.165.43"
repositoryPort= "5000"
repositoryUsr="rnd"
repositoryPw="nanumrltnf"
dockerHost="129.254.165.43"
dockerPort="2375"
kubernetesHost="129.254.165.43"
kubernetesPort="8001"
namespace = "default"
defaultGrpcPort = "50051"

authHeader = {
    "Accept": "application/vnd.docker.distribution.manifest.v2+json"
}

buildHeader = {
    'Content-type': 'application/tar'
}
postHeader = {
    "Content-Type: application/yaml"
}
commitHeader = {
    'Content-Type': 'application/json'
}
pushHeader={
    "X-Registry-Auth": "ewogICJ1c2VybmFtZSI6ICJybmQiLAogICJwYXNzd29yZCI6ICJuYW51bXJsdG5mIiwKICAiZW1haWwiOiAiZGV2QG5hbnVtLmNvLmtyIiwKICAic2VydmVyYWRkcmVzcyI6ICIxMjkuMjU0LjE2NS40Mzo1MDAwIgp9"
}
createHeader={
    "Content-Type": "application/yaml"
}
patchHeader={
    'Content-Type': 'application/strategic-merge-patch+json'
}
