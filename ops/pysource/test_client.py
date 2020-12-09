# -*- coding: utf-8 -*-
from __future__ import print_function

from concurrent import futures
import logging

import grpc

import module_pb2
import module_pb2_grpc

class ModuleService(module_pb2_grpc.ModuleServicer):

    def runModule(self, request, context):
        answer = run(request.str)
        return module_pb2.Reply(str=answer)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    module_pb2_grpc.add_ModuleServicer_to_server(ModuleService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("working.....................")
    server.wait_for_termination()

def run(inputText):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('129.254.165.43:32623') as channel:
        stub = module_pb2_grpc.ModuleStub(channel)
        response = stub.runModule(module_pb2.Request(str=inputText))
        print('qanallaw Done')


    print("received: " + response.str)
    return response.str

if __name__ == '__main__':
    logging.basicConfig()
    serve()
