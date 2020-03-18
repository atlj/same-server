from network import network
from game import game
from models import player

class client:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.network = network()
        self.game = game()
        self.player = player
        self.player.name = name

    def get_input(self, prompt = ""):#ONLY CLI INPUT FOR NOW WILL CHAN WHEN GUI ARRIVES
        return input(f"{prompt} >> ")

    def output(self, data):#ONLY CLI OUTPUT FOR NOW WILL CHAN WHEN GUI ARRIVES
        print(data)

    def convert_card(self, card):
        if card == "00":
            return "?"
        card_name = ""
        patterns = {"H": "Kupa", "T": "Karo", "C": "Sinek", "P": "Maça"}
        numbers = {"1": "10", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "A": "As", "K": "Papaz", "Q": "Kız", "J": "Vale"}
        pattern = patterns[card[0]]
        number = numbers[card[1]]
        card_name = f"{pattern} {number}"
        return card_name

    def choose_card(self): #CLI FOR NOW WILL RETURN A CARDS NAME AS A STRING
        print("-" * 2 + "MASA KARTLARI" + "-"*2)
        if len(self.game.table_deck) == 0:
            print("-masa boş-")

        else:
            print("SAYISI KÜÇÜK OLAN DAHA ALTTA")
            index = 1
            for card in self.game.table_deck:
                text = f"{index} - {self.convert_card(card)}"
                print(text)
                index +=1
        print("\n")

        print("Bir Kart Seçin\n")
        index = 1
        for card in self.player.deck:
            text = f"{index} - {self.convert_card(card)}"
            print(text)
            index += 1

        print("\n" + "-"*10 + "\n")

        while True:
            chosen = input(">>")
            try:
                chosen = int(chosen)

            except ValueError:
                print("Lütfen Geçerli Bir Kart Girin\n")
                continue

            try:
                chosen = self.player.deck[chosen - 1]

            except IndexError:
                print("Lütfen Geçerli Bir Kart Girin\n")
                continue

            break

        return chosen

    def connect_server(self):
        self.network.connect(self.ip, self.port)

    def client_loop(self):
        while True:
            received = self.network.receive_client()
            rtype = received["type"]
            rdata = received["data"]

            if rtype == "table_deck":
                self.game.table_deck = rdata

            elif rtype == "player_deck":
                self.player.deck = rdata

            elif rtype == "player_inventory":
                self.player.inventory = rdata

            elif rtype == "game_state":
                if rdata == "your_turn":
                    self.network.send_client({"type": "select_card", "data": self.choose_card()})
                elif rdata == "end":
                    print("\n\n"+"-"*10 + "\nEl Bitti\n" + "-"*10 +"\n")

            elif rtype == "player_score":
                print(f"Skorun: {rdata}")
                print("Kartların: ")
                for card in self.player.inventory:
                    print(self.convert_card(card))
                print("")

            elif rtype == "game_info":
                if rdata == "same":
                    print("PİŞTİ")
            

    def init_connection(self):
        self.connect_server()
        self.network.send_client({"type":"create_player", "data": self.player.name})
        received = self.network.receive_client()
        if received["data"] == "start":
            self.client_loop()

        else:
            print("error") #TODO: remove here

