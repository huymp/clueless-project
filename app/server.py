import grpc
from concurrent import futures
import time

import proto.clueless_pb2_grpc as pb2_grpc
import proto.clueless_pb2 as pb2

from source.server_impl import CluelessService
from source.game_engine_impl import GameEngine

def serve():
  game_engine = GameEngine()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pb2_grpc.add_CluelessServicer_to_server(CluelessService(game_engine), server)
  server.add_insecure_port('[::]:56789')
  server.start()
  print("gRPC server started, listening on [::]:56789")
  server.wait_for_termination()

if __name__ == '__main__':
    serve()