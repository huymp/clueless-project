import logging
from queue import Empty, Queue
from source.data import EventData

import proto.clueless_pb2_grpc as pb2_grpc
import proto.clueless_pb2 as pb2

logger = logging.getLogger(__name__)

def handle_game_event(data):
  # build the event message
  event = pb2.Event()
  event.status = "Running"
  event.players[:] = data.players
  return event

class EventStreamer:
  def __init__(self, game_engine):
    self.game_engine = game_engine
    self.queue = Queue()
    self.add_handlers()
  
  def add_handlers(self):
    self.game_engine.event_handlers.append(self.queue.put)

  def process(self):
    event = None
    try:
      data = self.queue.get(timeout=1)
      if isinstance(data, EventData):
        event = handle_game_event(data)
      else:
        logger.error("unknown event: %s", data)
    except Empty:
      pass
    return event

  def remove_handlers(self):
    self.game_engine.event_handlers.remove(self.queue.put)
        