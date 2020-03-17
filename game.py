import random
class game: 
    def __init__(self):
        self.table_deck = []

    def generate_deck(self):
        self.host_deck = []
        patterns = ["H", "T", "C", "P"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "K", "Q", "J"] #1 means 10
        
        for pattern in patterns:
            for number in numbers:
                card = pattern + number
                self.host_deck.append(card)

    def pick_card(self, amount):
        picked = []
        for times in range(amount):
            chosen_card = random.choice(self.host_deck)
            self.host_deck.remove(chosen_card)
            picked.append(chosen_card)
        return picked
