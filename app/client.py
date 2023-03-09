from source.client_impl import CluelessClient
from source.data import EventData
import time
import argparse

def process_event(event):
  """
  Process event

  :param EventData event
  """
  game_status = event.status
  players = event.players[:]
  print("Broadcast event from Server: \nGame status: ", game_status, "\nActive players: ", players)

if __name__ == '__main__':
  # parse user arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--server-address', dest="server_address", type=str, required=False, action='store', default="localhost")
  parser.add_argument('-p', '--server-port', dest="server_port", type=int, required=False, action='store', default=56789)
  parser.add_argument('-n', '--player-name', dest="player_name", type=str, required=False, action='store', default="Anonymous")
  args = parser.parse_args()

  client = CluelessClient(args.server_address, args.server_port)
  handling_events = client.events(process_event)
  time.sleep(1)
  result = client.greetings(client_name=args.player_name)
  #handling_events = client.events(process_event)
  while True:
    time.sleep(1)
  