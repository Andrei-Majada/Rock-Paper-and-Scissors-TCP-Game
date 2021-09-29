class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.start = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.start

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):

        p1 = self.moves[0].upper()
        p2 = self.moves[1].upper()

        winner = -1
        if p1 == "PEDRA" and p2 == "TESOURA":
            winner = 0
        elif p1 == "TESOURA" and p2 == "PEDRA":
            winner = 1
        elif p1 == "PAPEL" and p2 == "PEDRA":
            winner = 0
        elif p1 == "PEDRA" and p2 == "PAPEL":
            winner = 1
        elif p1 == "TESOURA" and p2 == "PAPEL":
            winner = 0
        elif p1 == "PAPEL" and p2 == "TESOURA":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False