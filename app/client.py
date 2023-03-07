from source.client_impl import CluelessClient
from source.data import EventData
import time

def process_event(event):
  """
  Process event

  :param EventData event
  """
  game_status = event.status
  players = event.players[:]
  print("Broadcast event from Server: \nGame status: ", game_status, "Players: ", players)

if __name__ == '__main__':
  client = CluelessClient()
  handling_events = client.events(process_event)
  result = client.greetings(client_name="Computer 1")
  #handling_events = client.events(process_event)
  while True:
    time.sleep(1)
  