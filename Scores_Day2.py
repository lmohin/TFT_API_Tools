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

    values = get_cell_value("Phase 2 : Finale (Dimanche)!D3:M10")
    load_dotenv()
    limiter = AsyncLimiter(10, 1)
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    users = []
    for value in values:
        scores = []
        for i in range(len(value)-4):
             scores.append(int(value[i+4]))
        if len(value) > 3 and value[3]:
            puuid = value[3]
        print(value)
        users.append(User(value[1], value[2], tactician = value[0], puuid = puuid, scores=scores))

    
#     for value in values:
#         username1,tag1 = value[0].split('#')
#         users.append(User(username1, tag1))
#         username2,tag2 = value[1].split('#')
#         users.append(User(username2, tag2))
#     values = get_cell_value("Phase 2 - Lobbies!H16:I19")
#     for value in values:
#         username1,tag1 = value[0].split('#')
#         users.append(User(username1, tag1))
#         username2,tag2 = value[1].split('#')
#         users.append(User(username2, tag2))
# 
#     values = get_cell_value("Phase 2 : Finale (Dimanche)!D:M")
#     values = values[2:]
#     for value in values:
#         playername = value[1]
#         print(playername)
#         player = next((potPlayer for potPlayer in users if playername == potPlayer.username), None)
#         if player != None:
#             scores = []
#             for i in range(len(value)-4):
#                 scores.append(int(value[i+4]))
#             player.tactician = value[0]
#             player.puuid = value[3]
#             player.scores = scores

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
                task.append(printLastGameInfos_L(user, users, session, api_key, limiter, games))
            i += 1
        await asyncio.gather(*task)
    for user in users:
        user.calculateTotalScore()
        print(user.username, user.tag, user.tactician)
    #users.sort(key=lambda x: x.totalScore, reverse=True)
    printScores(users)


if __name__ == "__main__":
    asyncio.run(Scores())

        
