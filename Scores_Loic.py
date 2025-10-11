import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *
from unit import Unit


async def getUnitsValues(sheet):
    cost = get_cell_value(sheet)
    cost = cost[2:]
    units = []
    print(cost)
    for unit in cost:
        units.append(Unit(unit[1], unit[0], unit[3], unit[5], unit[7]))
    return units

async def Scores():
    units1 = await getUnitsValues("Units Stats!B:I")
    units2 = await getUnitsValues("Units Stats!K:R")
    units3 = await getUnitsValues("Units Stats!T:AA")
    units4 = await getUnitsValues("Units Stats!AC:AJ")
    units5 = await getUnitsValues("Units Stats!AL:AS")
    values = get_cell_value("Phase 1 : Rondes Suisse (Samedi)!D:M")
    values = values[2:]
    load_dotenv()
    limiter = AsyncLimiter(10, 1)
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    users = []
    nbr_rounds = 1
    for value in values:
        scores = []
        for i in range(len(value)-4):
             scores.append(int(value[i+4]))
             nbr_rounds += 1
        puuid = None
        if len(value) > 3 and value[3]:
            puuid = value[3]
        print(value)
        users.append(User(value[1], value[2], tactician = value[0], puuid = puuid, scores=scores))
    async with aiohttp.ClientSession() as session:
        for user in users:
            if user.puuid == None:
                task.append(getPuuid(user, session, api_key, limiter))
        await asyncio.gather(*task)
        task = []
        i = 0
        for user in users:
            if i % 8 == 0:
                task.append(getLastMatchId(user, session, api_key, limiter))
            i += 1
        await asyncio.gather(*task)
        task = []
        i = 0
        games = []
        for user in users:
            if i % 8 == 0:
                task.append(printLastGameInfos_Loic(user, users, session, api_key, limiter, games))
            i += 1
        await asyncio.gather(*task)
    for user in users:
        user.calculateTotalScore()
        print(user.totalScore)
    users.sort(key=lambda x: x.totalScore, reverse=True)
    for game in games:
        for player in game:
            print(player["units"])
            if player["puuid"] == "BOT":
                break
            for playedUnit in player["units"]:
                for unit1 in units1:
                    if ("TFT15_" + unit1.name).lower() == playedUnit["character_id"].lower():
                        unit1.addScore(int(player["placement"]))
                for unit2 in units2:
                    if ("TFT15_" + unit2.name).lower() == playedUnit["character_id"].lower():
                        unit2.addScore(int(player["placement"]))
                for unit3 in units3:
                    if ("TFT15_" + unit3.name).lower() == playedUnit["character_id"].lower():
                        unit3.addScore(int(player["placement"]))
                for unit4 in units4:
                    if ("TFT15_" + unit4.name).lower() == playedUnit["character_id"].lower():
                        unit4.addScore(int(player["placement"]))
                for unit5 in units5:
                    if ("TFT15_" + unit5.name).lower() == playedUnit["character_id"].lower():
                        unit5.addScore(int(player["placement"]))
    nbr_games = nbr_rounds * (len(users) // 8)
    for u1 in units1:
        u1.calculateStats(nbr_games)
    for u2 in units2:
        u2.calculateStats(nbr_games)
    for u3 in units3:
        u3.calculateStats(nbr_games)
    for u4 in units4:
        u4.calculateStats(nbr_games)
    for u5 in units5:
        u5.calculateStats(nbr_games)
    units1.sort(key=lambda x: x.pickRate, reverse=True)
    units2.sort(key=lambda x: x.pickRate, reverse=True)
    units3.sort(key=lambda x: x.pickRate, reverse=True)
    units4.sort(key=lambda x: x.pickRate, reverse=True)
    units5.sort(key=lambda x: x.pickRate, reverse=True)
    printUnits(units1, "Units Stats!B3")
    printUnits(units2, "Units Stats!K3")
    printUnits(units3, "Units Stats!T3")
    printUnits(units4, "Units Stats!AC3")
    printUnits(units5, "Units Stats!AL3")
    printScores(users)


if __name__ == "__main__":
    asyncio.run(Scores())

