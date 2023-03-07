import grpc
from concurrent import futures
import time
import proto.clueless_pb2_grpc as pb2_grpc
import proto.clueless_pb2 as pb2
from source.game_engine_impl import GameEngine
from source.events import EventStreamer
from source.data import EventData
import logging

logger = logging.getLogger(__name__)

class CluelessService(pb2_grpc.CluelessServicer):
  def __init__(self, game_engine):
    self.game_engine = game_engine
    self.running = True

  def _is_running(self, context):
    return self.running and context.is_active()

  def ServerGreetings(self, request, context):
    client_name = request.client_name
    message = f'Hi "{client_name}". Welcome to Clueless!'
    response = {'message': message, 'status': "connected"}
    # update game state and broadcast new state
    self.game_engine.add_player(client_name)
    data = EventData()
    data.name = "clueless"
    data.players = [player.name for player in self.game_engine.get_players()]
    self.game_engine.broadcast_event(data)
    return pb2.GreetingsResponse(**response)
  
  def Events(self, request, context):
    logger.info("Received EventsRequest from client")
    request_events = request.request
    streamer = EventStreamer(self.game_engine)
    while self._is_running(context):
      event = streamer.process()
      if event:
        yield event
    streamer.remove_handlers()
    self._cancel_stream(context)