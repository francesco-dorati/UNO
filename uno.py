import random


colors = ('red', 'yellow', 'green', 'blue')


class Deck:
  def __init__(self):
    self.cards = []
    for color in colors:
      self.cards.append(Card('0', color))
      for _ in range(2):
        for number in range(1, 10):
          self.cards.append(Card(str(number), color))
        self.cards.append(Card('SKIP', color))
        self.cards.append(Card('REVERSE', color))
        self.cards.append(Card('+2', color))
      self.cards.append(Card('+4', None))
      self.cards.append(Card('WILD', None))

  def __iter__(self):
    for card in self.cards:
      yield card

  def __call__(self) -> list:
    return self.cards

  def shuffle(self) -> None:
    random.shuffle(self.cards)

  def draw(self, n: int=1) -> list:
    drawed = []
    drawed = self.cards[-n:]
    self.cards = self.cards[:-n]
    return drawed


class Card:
  def __init__(self, value: str, color: str):
    self.value = value
    self.color = color

  def __str__(self) -> str:
    return f'Value: {self.value}  Color: {self.color}'


class Player:
  def __init__(self):
    self.hand = []
    self.hand += deck.draw(7)




deck = Deck()


# EXEC

deck.shuffle()

players_number = 3

players = []

for _ in range(players_number):
  players.append(Player())




# TMP
i = 0
for player in players:
  print(f'\nplayer {i}: ')
  i += 1
  for card in player.hand:
    print(card.value)
