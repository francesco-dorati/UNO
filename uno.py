'''
 make difficulty: 
  easy: chooses always a number
  medium/random: chooses randomly
  hard: chooses always specials
'''

import random
import os
import sys
import time
from termcolor import colored


colors = ('red', 'yellow', 'green', 'blue')

class Game:
  def __init__(self, players: int):
    self.deck = Deck()
    self.deck.shuffle()
    self.players = []
    for _ in range(players):
      self.players.append(Player())
    self.turn = 0
    self.inversed = False

  def start(self) -> None:
    for player in self.players:
      player.draw(7)
    self.piletop = self.deck.draw()[0]
    self.piletop.active = False

  def won(self) -> bool:
    for player in self.players:
      if len(player.hand) == 0:
        return True
    return False
  
  def nextplayer(self) -> None:
    self.turn += 1 if not self.inversed else -1
    if self.turn == len(self.players):
      self.turn = 0
    elif self.turn == -1:
      self.turn = len(self.players) - 1
  
  def print_player_stats(self):
    # TODO add comments on the side of player
    for i, player in enumerate(self.players):
      if i == 0:
        message = colored(f"You: {len(player.hand)} cards", "white", attrs=["bold" if self.turn == 0 else "dark"])
      else:
        message = colored(f"Player {i}: {len(player.hand)} card","white", attrs=["bold" if self.turn == i else "dark"])
      print(message)

  def print_piletop(self):
    print('Pile top:')
    print(colored(self.piletop.value, self.piletop.color, attrs=['bold']))
    
# TODO add No playable cards before draw


class Player:
  def __init__(self):
    self.hand = []

  def draw(self, n: int = 1) -> list:
    drawed = game.deck.draw(n)
    self.hand += drawed
    return drawed

  def playable(self) -> list:
    playable = []
    if game.piletop.color == 'white' and not game.piletop.active:
      return self.hand
    for card in self.hand:
      if card.value == game.piletop.value or card.color == game.piletop.color or card.value  in ['+4', 'WILD']:
        playable.append(card)
    return playable 
  
  def play(self, index: int) -> 'Card':
    card = self.playable()[index]
    game.piletop = card
    self.hand.remove(card)
    return card

  def choose(self) -> None:
    played_card = None
    if self.playable():
      played_card = self.play(0)
    else:
      self.draw()
      if self.playable():
        played_card = self.play(0)
    if played_card and played_card.color == 'white':
      colors_count = [0, 0, 0, 0]
      for card in self.hand:
        colors_count[colors.index(card.color)] += 1
      game.piletop.color = colors[colors_count.index(max(colors_count))]

  def print_playable(self) -> list:
    print('Playable cards:')
    if game.turn == 0:
      if self.playable():
        for index, card in enumerate(self.playable()):
          sys.stdout.write(f'{colored(f"{index + 1})", "white", attrs=["dark"])} {colored(card.value, card.color, attrs=["bold"])}     ')
        line()
      else:
        print(colored('No playable cards', 'white', attrs=['dark']))
    else:
      print(colored('Wait for yotur turn', 'white', attrs=['dark']))
    return self.playable()

  def print_hand(self) -> None:
    print('All your cards:')
    for card in self.hand:
      sys.stdout.write(f'{colored(card.value, card.color, attrs=["bold"])}  ')
    line()
    


class Deck:
  def __init__(self):
    self.cards = []
    for color in colors:
      self.cards.append(Card('0', color))
      for _ in range(2):
        for number in range(1, 10):
          self.cards.append(Card(str(number), color))
        self.cards.append(Card('SKIP', color, True))
        self.cards.append(Card('REVERSE', color, True))
        self.cards.append(Card('+2', color, True))
      self.cards.append(Card('+4', 'white', True))
      self.cards.append(Card('WILD', 'white'))

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
  def __init__(self, value: str, color: str, active: bool = False):
    self.value = value
    self.color = color
    self.active = active

  def __str__(self) -> str:
    return f'Value: {self.value}  Color: {self.color}'



# VISUAL FUNCTIONS

def clear() -> None:
  _=os.system('cls')
  _=os.system('clear')


def line(n: int = 1) -> None:
  for _ in range(n):
    print()



# GAME START
game = Game(2)

game.start()


while not game.won():
  clear()

  if game.piletop.value == '+4' and game.piletop.active:
    game.piletop.active = False
    game.players[game.turn].draw(4)
    game.nextplayer()

  if game.piletop.value == '+2' and game.piletop.active:
    game.piletop.active = False
    game.players[game.turn].draw(2)
    game.nextplayer()

  if game.piletop.value == 'SKIP' and game.piletop.active:
    game.piletop.active = False
    game.nextplayer()

  if game.piletop.value == 'REVERSE' and game.piletop.active:
    game.piletop.active = False
    game.inversed = not game.inversed
    game.nextplayer()
    game.nextplayer()

  game.print_player_stats()
  line(3)

  game.print_piletop()
  line(3)

  playable = game.players[0].print_playable()
  line()

  game.players[0].print_hand()
  line(3)

  played_card = None

  if game.turn == 0:

    if playable:
      played_card_index = input('Insert the card index: ')
      while not played_card_index.isdigit() or int(played_card_index) not in range(1, len(playable) + 1):
        played_card_index = input('Insert the card index: ')
      
      played_card_index = int(played_card_index) -1

      played_card = game.players[0].play(played_card_index)
  
    else:
      input(f'{colored("No playable cards", "red")}, draw a card (enter): ')

      drawed = game.players[0].draw()[0]

      clear()

      game.print_player_stats()
      line(3)

      game.print_piletop()
      line(3)

      print('You drawed: ')
      print(colored(drawed.value, drawed.color, attrs=["bold"]))
      line()

      game.players[0].print_hand()
      line(3)

      if game.players[0].playable():
        decision = input(f'This card is {colored("playable", "green", attrs=["bold"])}. Do you want to play it (Y/n)? ')
        while decision not in ['Y', 'y', 'yes', 'N', 'n', 'no']:
          decision = input('Do you want to play it (Y/n)? ')
        if decision in ['Y', 'y', 'yes']:
          played_card = game.players[0].play(0)
      else:
        input(f'This card is {colored("unplayable", "red", attrs=["bold"])}, skip the turn (enter): ')
    
    if played_card and played_card.color == 'white':
      clear()

      game.print_player_stats()
      line(3)

      game.print_piletop()
      line(3)

      print('Choose a color:')
      for index, color in enumerate(colors):
        sys.stdout.write(f'{colored(f"{index + 1})", "white", attrs=["dark"])} {colored(color.upper(), color, attrs=["bold"])}     ')
      line(2)

      game.players[0].print_hand()
      line(3)

      chosen_color_index = input('Insert the color index: ')
      while not chosen_color_index.isdigit() or int(chosen_color_index) not in range(1, 5):
        chosen_color_index = input('Insert the color index: ')
      chosen_color_index = int(chosen_color_index) - 1
      game.piletop.color = colors[chosen_color_index]
    
  else:
    player = game.players[game.turn]
    print('Wait for your turn to come.')
    player.choose()

  game.nextplayer()

print('WON')