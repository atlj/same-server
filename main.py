from threading import Thread
from network import network
from game import game
from models import player
import random

class main:

    def __init__(self, ip, port):
        self.network = network()
        self.game = game()
        self.ip = ip
        self.port = port
        self.lastid = -1
        self.players = {}#playerid: [playerobj, clientobj]
        self.p1 = False
        self.p2 = False
    
    def runtime(self, player_count = 2):
        self.start_server()
        for times in range(player_count):
            Thread(target = self.client_enterance, args = ()).start()


    def start_server(self):
        self.network.bindserver(self.ip, self.port)

    def announce(self, message):#sends a message to all players
        for player in self.players:
            client = self.players[player][1]
            self.network.send(message, client)

    def announce_info(self, message):
        self.announce({"type": "game_info", "data": message})

    def inform_player(self, message,player_id):
        self.network.send(message, self.players[player_id][1])

    def listen_player(self, player_id):
        return self.network.receive(self.players[player_id][1])

    def start_game(self):
        if len(self.players) == 2:
            self.announce({"type" : "game_state", "data" : "start"})
            self.outer_game_loop()

    def game_logic(self, card, player):
        self.players[player][0].deck.remove(card)
        if len(self.game.table_deck) > 0:
            top_card = self.game.table_deck[-1]

        else: #MASADA KART YOK
            self.announce_info("different")
            self.game.table_deck.append(card) #TODO: VALE KOYAMAMA KURALINI İMPLEMENTE ET
            return 1

        if len(self.game.table_deck) > 1:#MASADA BİRDEN FAZLA KART VAR
            if top_card[1] == card[1]:
                self.announce_info("collect")
                self.game.table_deck.append(card) 
                self.players[player][0].inventory += self.game.table_deck
                self.game.table_deck = []
                self.last_hit = player

            elif card[1] == "J":
                self.announce_info("joker")
                self.game.table_deck.append(card) 
                self.players[player][0].inventory += self.game.table_deck
                self.game.table_deck = []
                self.last_hit = player
                
            elif top_card[1] != card[1]:
                self.announce_info("different")
                self.game.table_deck.append(card)
                
            return 1

        elif len(self.game.table_deck) == 1: #MASADA BİR KART VAR
            if top_card[1] == card[1]:
                self.announce_info("same")
                self.game.table_deck.append(card) 
                self.players[player][0].same_count += 1
                self.players[player][0].inventory += self.game.table_deck
                self.game.table_deck = []
                self.last_hit = player

            elif card[1] == "J":
                self.announce_info("joker")
                self.game.table_deck.append(card) 
                self.players[player][0].inventory += self.game.table_deck
                self.game.table_deck = []
                self.last_hit = player

            elif top_card[1] != card[1]:
                self.announce_info("different")
                self.game.table_deck.append(card)

            return 1

    def game_loop(self):
        self.game.generate_deck()
        self.game.table_deck = self.game.pick_card(4)
        if self.p1 == False:
            self.p1 = random.choice(list(self.players.keys()))
            for player in self.players:
                if player != self.p1:
                    self.p2 = player
        else:
            self.p1, self.p2 = self.p2, self.p1
        self.announce({"type": "table_deck", "data":["00", "00", "00", self.game.table_deck[3]]})
        self.players[self.p1][0].deck += self.game.pick_card(4)
        self.players[self.p2][0].deck += self.game.pick_card(4)
        print("p1 id: " + str(self.p1))
        print("p2 id: " + str(self.p2))
        print("p1 deck: " + str(self.players[self.p1][0].deck))
        print("p2 deck: " + str(self.players[self.p2][0].deck))
        pick = self.p1
        counter = 8
        while True: 
            p1_deck = self.players[self.p1][0].deck
            p2_deck = self.players[self.p2][0].deck
            p1_inventory = self.players[self.p1][0].inventory
            p2_inventory = self.players[self.p2][0].inventory
            self.inform_player({"type": "player_deck", "data": p1_deck }, self.p1)
            self.inform_player({"type": "player_deck", "data": p2_deck }, self.p2)
            self.inform_player({"type": "player_inventory", "data": p1_inventory}, self.p1)
            self.inform_player({"type": "player_inventory", "data": p2_inventory}, self.p2)
            self.inform_player({"type": "game_state", "data": "your_turn"}, pick)
            print("its the turn of the id: " + str(pick))
            card = self.network.receive(self.players[pick][1])["data"]
            self.game_logic(card, pick)
            self.announce({"type": "table_deck", "data": self.game.table_deck})
            
            counter -= 1

            if counter == 0:
                if len(self.game.host_deck) == 0:
                    self.players[self.last_hit][0].inventory += self.game.table_deck#CARDS GOES TO LAST HIT
                    self.game.table_deck = []
                    self.announce({"type": "game_state", "data": "end"})
                    self.players[self.p1][0].count_score()
                    self.players[self.p2][0].count_score()
                    print("p1 envanter: " + str(self.players[self.p1][0].inventory))
                    print("p2 envanter: " + str(self.players[self.p2][0].inventory))
                    self.inform_player({"type": "player_inventory", "data": p1_inventory}, self.p1)
                    self.inform_player({"type": "player_inventory", "data": p2_inventory}, self.p2)
                    self.inform_player({"type": "player_score", "data": self.players[self.p1][0].score}, self.p1)
                    self.inform_player({"type": "player_score", "data": self.players[self.p2][0].score}, self.p2)
                    break
                self.players[self.p1][0].deck += self.game.pick_card(4)
                self.players[self.p2][0].deck += self.game.pick_card(4)
                counter = 8
            if pick == self.p1:
                pick = self.p2

            else:
                pick = self.p1

    def outer_game_loop(self):
        while True:
            self.game_loop()

    def client_enterance(self):
        client, adress = self.network.accept()
        player_id = False
        received = self.network.receive(client)
        player_name = received["data"]
        player_id = self.lastid + 1
        self.lastid += 1
        self.players[player_id] = [player(player_name), client]
        print(received["data"]+"katıldı")
        self.start_game()
            
 
