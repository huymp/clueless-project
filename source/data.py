from dataclasses import dataclass, field
from typing import List

@dataclass
class EventData:
  name: str = None
  players: List[str] = None

class Player:
  def __init__(self):
    self.name = None
  def set_name(self, name):
    self.name = name
