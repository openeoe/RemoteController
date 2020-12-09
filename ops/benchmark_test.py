# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import requests
import logging
import json

from importlib import reload
from flask import Flask, render_template, redirect, request, url_for

import grpc
# protobuf
sys.path.append('./pysource')
import module_pb2
import module_pb2_grpc


# developer 모듈
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + '/dev')
import config as cp
from apiController import kubernetesController


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
@app.route('/johab', methods=['GET'])
def dropdown():
    #colours = ['Red', 'Blue', 'Black', 'Orange']
    items = getOpsListCore()
    return render_template('main00.html', opsList=items)

@app.route('/getList', methods=['GET'])
def getPodList():
    return getOpsListCore()

@app.route('/combine', methods=['GET'])
def combine():
    #colours = ['Red', 'Blue', 'Black', 'Orange']
    items = getOpsListCore()
    return items

@app.route('/result',methods=['POST','GET'])
def getText(num=None):
    if request.method == 'POST':
        text = request.form['text']
        port = '30559'
        result = getTextCore(text, port)
    elif request.method == 'GET':
        text = request.args.get("text")
        port = '30559' 
    else:
        port = None
        result = '유효하지 않은 port 번호입니다.'


    return "{\"result\": " + result + "}"


# deployment list 가져오는 함수 구현
def getOpsListCore():
    kubernetesapi = kubernetesController.kubernetesController()
    kubernetesapi.setRunType('ops')
    items = kubernetesapi.getListDict()
    result = json.dumps(items)
    return "{\"opsList\": " + result + "}"


# text 리턴받는 함수 구현
def getTextCore(inputText, port):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel(cp.kubernetesHost + ':' + port) as channel:
        stub = module_pb2_grpc.ModuleStub(channel)
        response = stub.runModule(module_pb2.Request(str=inputText))
        print('test Done')

    #print("received: " + response.str)
    return response.str



if __name__ == '__main__':
    app.logger.info('Processing default request')
    app.run(host='0.0.0.0', port=8000)
