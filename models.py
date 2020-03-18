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
        self.same_count = 0

    def count_score(self):
        score_cards = {"HA": 1,
                       "TA": 1,
                       "CA": 1,
                       "PA": 1,
                       "HJ": 1,
                       "TJ": 1,
                       "CJ": 1,
                       "PJ": 1,
                       "C2": 2,
                       "T1": 3}

        for card in self.inventory:#KART PUANLARI
            if card in score_cards:
                self.score += score_cards[card]
        if len(self.inventory) > 26:
            self.score += 3#KART FAZLALIĞI

        self.score += self.same_count * 10#PİŞTİ SAYISI
