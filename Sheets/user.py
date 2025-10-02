class User:
    def __init__(self, username, tag, puuid=None):
        self.username = username
        self.tag = tag
        self.puuid = puuid
        self.lastMatchId = None
        self.tier = None
        self.rank = 0
        self.lps = 0
        self.adjustedLps = 0

    def calculateAdjustedLps(self):
        match self.tier:
            case "MASTER" | "GRANDMASTER" | "CHALLENGER":
                self.adjustedLps = self.lps
            case "DIAMOND":
                self.adjustedLps = 100 -(100 - self.lps) - 100 * self.rank
            case "EMERALD":
                self.adjustedLps = -300 - (100 - self.lps) - 100 * self.rank
            case "PLATINUM":
                self.adjustedLps = -700 - (100 - self.lps) - 100 * self.rank
            case "GOLD":
                self.adjustedLps = -1100 - (100 - self.lps) - 100 * self.rank
            case "SILVER":
                self.adjustedLps = -1500 - (100 - self.lps) - 100 * self.rank
            case "BRONZE":
                self.adjustedLps = -1900 - (100 - self.lps) - 100 * self.rank
            case "IRON":
                self.adjustedLps = -2300 - (100 - self.lps) - 100 * self.rank
            case _:
                self.adjustedLps = -2801
