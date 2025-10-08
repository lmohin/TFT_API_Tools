import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *
from unit import Unit

async def Scores():
    cost1 = get_cell_value("Units Stats!B:I")
    cost1 = cost1[2:]
    units1 = []
    for unit1 in cost1:
        units1.append(Unit(unit1[1], unit1[0], unit1[3], unit1[5], unit1[7]))
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
    for value in values:
        if value[0] == "":
            continue
        scores = []
        for i in range(len(value)-4):
             scores.append(int(value[i+4]))
        users.append(User(value[1], value[2], tactician = value[0], puuid = value[3], scores=scores))
    for user in users:
        print(user.username, user.totalScore)
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
                print(user.username, "coucou")
                task.append(printLastGameInfos_Loic(user, users, session, api_key, limiter, games))
            i += 1
        await asyncio.gather(*task)
    for user in users:
        user.calculateTotalScore()
    users.sort(key=lambda x: x.totalScore, reverse=True)
    for game in games:
        for player in game:
            if player["puuid"] == "BOT":
                break
            for playedUnit in player["units"]:
                for unit1 in units1:
                    if "TFT15_" + unit1.name == playedUnit["character_id"]:
                        unit1.addScore(int(player["placement"]))
    for unit1 in units1:
        unit1.calculateStats(3)
    printUnits(units1)
    printScores(users)


if __name__ == "__main__":
    asyncio.run(Scores())

