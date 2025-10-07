def romanianConverter(romanNumber):
    match romanNumber:
        case "I":
            rank = 1
        case "II":
            rank = 2
        case "III":
            rank = 3
        case "IV":
            rank = 4
        case _ :
            rank = 0
    return rank

class User:
    def __init__(self, username, tag, tactician=None, puuid=None, scores=[]):
        self.username = username
        self.tag = tag
        self.puuid = puuid
        self.lastMatchId = None
        self.tier = None
        self.rank = None
        self.lps = 0
        self.adjustedLps = 0
        self.tactician = tactician
        self.scores = scores
        self.totalScore = sum(self.scores)

    def calculateTotalScore(self):
        self.totalScore = sum(self.scores)
        top4 = 0
        top3 = 0
        top2 = 0
        top1 = 0
        for score in self.scores:
            top4 += 1
            match score:
                case 1:
                    top1 += 1
                case 2:
                    top2 += 1
                case 3:
                    top3 += 1
                case 4:
                    pass
                case _:
                    top4 -= 1
        self.totalScore += top4*0.1 + top1*0.01 + top2*0.001 + top3*0.0001
                
        print("Loïc Test :" + self.username, self.totalScore , self.scores)

    def calculateAdjustedLps(self):
        rank = romanianConverter(self.rank)
        match self.tier:
            case "MASTER" | "GRANDMASTER" | "CHALLENGER":
                self.adjustedLps = self.lps
                self.rank = ''
            case "DIAMOND":
                self.adjustedLps = 100 -(100 - self.lps) - 100 * rank
            case "EMERALD":
                self.adjustedLps = -300 - (100 - self.lps) - 100 * rank
            case "PLATINUM":
                self.adjustedLps = -700 - (100 - self.lps) - 100 * rank
            case "GOLD":
                self.adjustedLps = -1100 - (100 - self.lps) - 100 * rank
            case "SILVER":
                self.adjustedLps = -1500 - (100 - self.lps) - 100 * rank
            case "BRONZE":
                self.adjustedLps = -1900 - (100 - self.lps) - 100 * rank
            case "IRON":
                self.adjustedLps = -2300 - (100 - self.lps) - 100 * rank
            case _:
                self.adjustedLps = -2801
                self.rank = ''
