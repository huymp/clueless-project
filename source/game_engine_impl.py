from source.data import Player

class GameEngine:
  def __init__(self):
    self.name = "Clueless"
    self.players = []
    self.event_handlers = []
  
  def broadcast_event(self, event_data):
    for handler in self.event_handlers:
      handler(event_data)
  
  def add_player(self, player_name):
    player_data = Player()
    player_data.set_name(player_name)
    self.players.append(player_data)
    return
  def get_players(self):
    return self.players