class Unit:
    def __init__(self, name, image, pick, win, totalScore):
        self.name = name
        self.image = image
        self.pick = int(pick)
        self.win = int(win)
        self.totalScore = int(totalScore)
        self.pickRate = 0.0
        self.winRate = 0.0
        self.average = 0.0

    def calculateStats(self, nbrGames):
        if self.pick == 0:
            return
        self.pickRate = round(self.pick / nbrGames * 100, 1)
        self.winRate = round(self.win / self.pick * 100, 1)
        self.average = round(self.totalScore / self.pick, 1)

    def addScore(self, score):
        if score == 1:
            self.win += 1
        self.pick += 1
        self.totalScore += score
