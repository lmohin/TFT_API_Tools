import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *

async def main():
    values = get_cell_value("D:E")
    values.pop(0)
    values.pop(0)
#     print(values)
#     return values
    
    tactician = get_cell_value("B:C")
    tactician.pop(0)
    tactician.pop(0)
    load_dotenv()
    limiter = AsyncLimiter(10, 1)
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    users = []
    for i in range(len(values)):
        value = values[i]
        print(values[i])
        print(tactician[i])
        users.append(User(value[0], value[1], tactician[i]))
#     async with aiohttp.ClientSession() as session:
#         for user in users:
#             if user.puuid == None:
#                 task.append(getPuuid(user, session, api_key, limiter))
#         await asyncio.gather(*task)
        task = []
        for user in users:
            task.append(getRank(user, session, api_key, limiter))
        await asyncio.gather(*task)
#         task = []
#         for user in users:
#             task.append(getLastMatchId(user, session, api_key, limiter))
#         await asyncio.gather(*task)
#         task = []
#         for user in users:
#             task.append(printLastGameInfos(user, session, api_key, limiter))
#         await asyncio.gather(*task)
#     users.sort(key=lambda x: x.adjustedLps, reverse=True)
#     for user in users:
#         print("This is what I want" + user.username + "#" + user.tag, user.adjustedLps)
    print(users)
    InitTacticianList(users)


if __name__ == "__main__":
    asyncio.run(main())

