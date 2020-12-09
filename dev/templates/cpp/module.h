#pragma execution_character_set("utf-8")

#ifndef MODULE_H_
#define MODULE_H_

#include <iostream>

#include <unistd.h>
#include <string>
//모듈헤더include 작성
/*
#include "QAnalHeader/QAnalyzer.h"
#include "QStruct.h"
#include "QAnalHeader/QAnalRSCMng.h"
#include "QAJsonHeader/QAnalJsonRW.h"
#include "QAnalHeader/QAnalQF.h"
#include "QAnalHeader/QAnalSAT.h"
#include "QAnalHeader/QAnalSAT_ML.h"
#include "QAnalHeader/QAnalLAT.h"
#include "QAnalHeader/QAnalLAT_ML.h"
#include "EvalHeader/EvalMeasure.h"
*/
using namespace std;
namespace grpc_nanum {

class module{
private:
//객체변수작성
/*
        CQAnalRSCMng qRscMngr;
        CQAnalyzer qAnalyzer;
        QAnal_Result qAnalResult, qAnalResult2;
        string strQuestion,strPrint, strJson, strJson2;
        LMInterface *pGLmi;
*/
public:
        string QA(string strQuestion);
        //생성자에서 init
        module();

};

} /* namespace grpc_nanum */

#endif /* MODULE_H_ */

