import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *

async def Scores():
    cost1 = get_cell_value("Units Stats!B:I")
    cost1 = cost1[2:]
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
        print("Test :" ,value)
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
        for user in users:
            if i % 8 == 0:
                task.append(printLastGameInfos_Loic(user, users, session, api_key, limiter))
            i += 1
        await asyncio.gather(*task)
    for user in users:
        user.calculateTotalScore()
    users.sort(key=lambda x: x.totalScore, reverse=True)
    for user in users:
        print("This is what I want" + user.username + "#" + user.tag, user.totalScore)
    printScores(users)


if __name__ == "__main__":
    asyncio.run(Scores())

