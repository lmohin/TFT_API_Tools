import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
import random

load_dotenv()

class User:
    def __init__(self, username, tag, puuid=None):
        self.username = username
        self.tag = tag
        self.puuid = puuid
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


async def getPuuid(user, session, api_key, limiter, retries=1):
    """'user is an instance of User"""
    api_uri = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user.username}/{user.tag}"
    headers = {
            "X-Riot-Token": api_key
    }
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status != 200:
        print(f"Error here: {response.status} ({user.username}#{user.tag})")
        await asyncio.sleep(2 ** retries + random.random())
        return await getPuuid(user, session, api_key, limiter, retries + 1)
    user.puuid = datas["puuid"]

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
    return rank

async def getRank(user, session, api_key, limiter, retries = 1):
    if user.puuid == None:
        return
    headers = {
        "X-Riot-Token": api_key
    }
    api_uri = f"https://euw1.api.riotgames.com/tft/league/v1/by-puuid/{user.puuid}"
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status != 200:
        print(f"Error: {response.status} ({user.username}#{user.tag})")
        await asyncio.sleep(2 ** retries + random.random())
        return await getRank(user, session, api_key, limiter, retries + 1)
    if len(datas) == 0:
        print(user.username, "no lp")
        return
    rankedDatas = None
    for tempDatas in datas:
        if tempDatas['queueType'] == 'RANKED_TFT':
            rankedDatas = tempDatas
            break
    datas = rankedDatas
    if datas == None:
        print(user.username, 'no lp')
        return
    user.tier = datas['tier']
    user.rank = romanianConverter(datas['rank'])
    user.lps = datas['leaguePoints']
    user.calculateAdjustedLps()       
    print(user.username + "#" + user.tag, datas['tier'], datas['rank'], datas['leaguePoints'], user.adjustedLps)

async def printUserInfos(user, session, api_key):
    headers = {
        "X-Riot-Token": api_key
    }
    if user.puuid == None:
        return
    await getRank(user, session, headers)
    api_uri  = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{user.puuid}/ids"
    async with session.get(api_uri, headers=headers) as response:
        if response.status != 200:
            print(f"Error: {response.status} ({user.username}#{user.tag})")
            return
        datas = (await response.json())
        matchId = datas[0]
    api_uri = f"https://europe.api.riotgames.com/tft/match/v1/matches/{matchId}"
    async with session.get(api_uri, headers=headers) as response:
        if response.status != 200:
            print(f"Error match: {response.status} ({user.username}#{user.tag})")
            return
        datas = await response.json()
        game = datas["info"]["participants"]
        for i in range(len(game)):
            playerInfo = game[i]
            print(playerInfo["riotIdGameName"], playerInfo["riotIdTagline"], playerInfo["placement"], 9 - playerInfo["placement"])

async def main():
    limiter = AsyncLimiter(10, 1)
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    users = []
    for i in range(40):
        users.append(User("Falkor", "Genti"))
    users.append(User("Megata", "0000"))
    users.append(User("Yottah", "0000"))
    users.append(User("Arestidios", "AAA"))
    users.append(User("Patrick", "888"))
    users.append(User("Lornyk", "888"))
    users.append(User("Higa", "gmgn"))
    users.append(User("xRynn", "EUW"))
    users.append(User("giselle", "purr"))
    users.append(User("grizzly", "4896"))
    users.append(User("Cysteine", "EUW"))
    users.append(User("La Viky", "EUW"))
    users.append(User("Nikulol", "EUW"))
    users.append(User("true86", "EUW"))
    users.append(User("cZxHSusie", "EUW"))
    users.append(User("RCS Xperion", "EUW11"))
    users.append(User("QAQ Hecaa", "EUW"))
    users.append(User("Bambilex", "EUW"))
    async with aiohttp.ClientSession() as session:
        for user in users:
            if user.puuid == None:
                task.append(getPuuid(user, session, api_key, limiter))
        await asyncio.gather(*task)
        task = []
        for user in users:
            task.append(getRank(user, session, api_key, limiter))
        await asyncio.gather(*task)

if __name__ == "__main__":
      asyncio.run(main())
