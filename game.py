import random
class game: 
    def __init__(self):
        self.table_deck = []
        self.patterns = ["H", "T", "C", "P"]
        self.numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "K", "Q", "J"] #1 means 10

    def generate_deck(self):
        self.host_deck = []
        for pattern in self.patterns:
            for number in self.numbers:
                card = pattern + number
                self.host_deck.append(card)

    def pick_card(self, amount):
        picked = []
        for times in range(amount):
            chosen_card = random.choice(self.host_deck)
            self.host_deck.remove(chosen_card)
            picked.append(chosen_card)
        return picked
