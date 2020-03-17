#no class for a card
#every card has a unique id
#every card goes as AB
#A : cards pattern
#B : cards number or sign
#H : Hearts, T : Tiles, C : Clovers, P : Pikes
#An example card goes as: T5, meaning Tiles 5
# Ace is A, Queen is Q, King is K and Joker is J
# if a card is unknown o player ie: at the start of the game the data is 00
# 1 means 10

class player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.deck = [] #this list contains card id's
        self.inventory = []

