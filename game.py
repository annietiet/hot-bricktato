import bricktato

class Game:
    players = set()

    def __init__(self):
        self.players = set()

    def add_player(self, username):
        self.players.add(username)
        bricktato.update_num_players_label(len(self.players))

    def remove_player(self, username):
        if username in self.players:
            self.players.remove(username)
            bricktato.update_num_players_label(len(self.players))

