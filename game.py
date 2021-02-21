
class Game:
    players = set()

    def __init__(self):
        self.players = set()

    def add_player(self, username):
        self.players.add(username)

    def remove_player(self, username):
        if username in self.players:
            self.players.remove(username)
