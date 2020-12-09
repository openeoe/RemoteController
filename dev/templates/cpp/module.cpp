#pragma execution_character_set("utf-8")

#ifndef WIN32
#include <iostream>
#include <boost/filesystem.hpp>
using namespace boost::filesystem;
#endif

#include <unistd.h>

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


#include "module.h"

namespace grpc_nanum {

module::module() {
//로딩 작성
/*
  pGLmi = new LMInterface;

  qRscMngr.Open_Resource(pGLmi, string("./module/rsc"), string(""), string(""));

  qAnalyzer.SetRscMng(&qRscMngr, pGLmi);

  strQuestion = "";
  strPrint = "";
  strJson = "";
  strJson2 = "";

  printf("<Resource Open Complete!!!>\n");
*/

}

std::string module::QA(string strQuestion){
//입출력 작성
/*
        CQAnalJsonRW qJsonRW;
        qAnalResult = qAnalyzer.QAnalysis4WikiQA(strQuestion);
        strJson = qJsonRW.GetJsonFromQAnalStruct(qAnalResult);

        qAnalResult2 = qJsonRW.GetQAnalStructFromJson(strJson);
        strJson2 = qJsonRW.GetJsonFromQAnalStruct(qAnalResult2);

        cout<<strJson2.data()<<endl;

        qRscMngr.Free_QAnalResult(qAnalResult);

        return strJson2.data();
*/
}
} /* namespace nanum_grpc */
