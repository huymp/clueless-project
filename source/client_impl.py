import grpc
import logging
import threading
import proto.clueless_pb2_grpc as pb2_grpc
import proto.clueless_pb2 as pb2

from source.data import EventData

logger = logging.getLogger(__name__)



def event_listener(stream, handler):
  try:
    for event_proto in stream:
      handler(event_proto)
  except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.CANCELLED:
      logger.debug("session stream closed")
    else:
      logger.exception("session stream error")

class CluelessClient(object):
  """
  Client for gRPC functionality
  """

  def __init__(self, host='localhost', port=56789):
    self.host = host
    self.server_port = port

    # instantiate a channel
    self.channel = grpc.insecure_channel(
        '{}:{}'.format(self.host, self.server_port))

    # bind the client and the server
    self.stub = pb2_grpc.CluelessStub(self.channel)

  def greetings(self, client_name):
    """
    Client function to call the rpc for ServerGreetings
    """
    request = pb2.Greetings(client_name=client_name)
    return self.stub.ServerGreetings(request)
  
  def events(self, handler):
    request = pb2.EventsRequest(request=True)
    stream = self.stub.Events(request)
    thread = threading.Thread(
      target=event_listener, args=(stream, handler), daemon=True
    )
    thread.start()
    return stream
