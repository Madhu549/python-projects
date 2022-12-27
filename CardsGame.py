#project cards
#global Variables declaration 
import random
suits=('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':11,'Queen':12,'King':13,'Ace':14}



#Desing the card class
class Card():
  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]

#for printing the card rank and suit of the card   
  def __str__(self):
    return self.rank+" of "+self.suit

#Deck Class
class Deck():
  def __init__(self):
    self.all_cards = []
    for suit in suits:
      for rank in ranks:
        created_card = Card(suit,rank)
    
        self.all_cards.append(created_card)
# For shuffling of cards in a deck 
  def shuffle(self):
    random.shuffle(self.all_cards)

#For drawing out a single card from the deck of cards
  def draw_one_card(self):
    return self.all_cards.pop()


#for inserting a single or a list of cards and removing of card from top of the deck 
#player class
class Player:
  def __init__(self,name):
    self.name = name
    self.all_cards = []

#For removing a card from the top of the deck
  def remove_card(self):
    return self.all_cards.pop(0)

#for adding a single card or a list of cards
  def add_cards(self,new_card):
    #checking whether new cards is a list or single card
    if type(new_card) == type([]):
      return self.all_cards.extend(new_card)
    else:
      return self.all_cards.append(new_card)

#for printing no of cards does the player have.
  def __str__(self):
    return f'{self.name} has {len(self.all_cards)} cards'



    
#main LOgic of the the Cards Game
#creating 2 objects for two players
player_1 = Player("player 1")
player_2 = Player("player 2")

#creating object for deck class
new_deck = Deck()
new_deck.shuffle()
new_deck.shuffle()

#Distribution of cards to the players equally
for i in range(26):
  player_1.add_cards(new_deck.draw_one_card())
  player_2.add_cards(new_deck.draw_one_card())

rounds = 0
game_on = True

while game_on:
  rounds += 1
  print(f'Round {rounds}')
  #player 1 has no cards
  if len(player_1.all_cards) == 0:
    print(f"player 1 has no cards left!\n{player_2.name} won the game.")
    game_on = False
    break
  #player 2 has no cards
  if len(player_2.all_cards) == 0:
    print(f"player 2 has no cards left!\n{player_1.name} won the game.")
    game_on = False
    break


  player_one_new_cards = []
  player_one_new_cards.append(player_1.remove_card())
  
  player_two_new_cards = []        
  player_two_new_cards.append(player_2.remove_card())   

  #war
  at_war = True
  while at_war:
    if player_one_new_cards[-1].value > player_two_new_cards[-1].value:
      player_1.add_cards(player_one_new_cards)
      player_1.add_cards(player_two_new_cards)
      at_war = False
    
    elif player_one_new_cards[-1].value < player_two_new_cards[-1].value:
      player_2.add_cards(player_one_new_cards)
      player_2.add_cards(player_two_new_cards)
      at_war = False
      
      
    else:
      print('At War!')
      if len(player_1.all_cards)<5:
        print(f"{player_1.name} unable to declare War\n{player_2.name} WINS!!!")
        game_on = False
        break
      elif len(player_2.all_cards)<5:
        print(f"{player_2.name} unable to declare War\n{player_1.name} WINS!!!")
        game_on = False
        break
      else:
        for i in range(5):
          player_one_new_cards.append(player_1.remove_card())
          player_two_new_cards.append(player_2.remove_card())
    