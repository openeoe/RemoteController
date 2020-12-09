from exofunction import commitExoModule, createExoModule, listExoModule

if __name__ == "__main__":

    while True:
        inputMode = input("\n사용하실 기능을 입력해주세요. [create / commit / list] : ")
        if inputMode.lower() == 'create'.lower():
            # 이미지 등록 & 쿠버네티스 배포
            createExoModule.createExoModule()

        elif inputMode.lower() == 'commit'.lower():
            # 쿠버네티스 컨테이너 커밋
            commitExoModule.commitExoModule()

        elif inputMode.lower() == 'list'.lower():
            # 서비스 리스트
            listExoModule.listExoModule('dev')

        else:
            break
