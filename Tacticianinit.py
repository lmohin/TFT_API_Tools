import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *

async def updateTactician(columns,page,case):
    
    values = get_cell_value(f"{page}!{columns}")
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
        if len(value) == 3:
            puuid = value[2]
        else:
            puuid = None
        if puuid == "None":
            puuid = None
        users.append(User(value[0], value[1], puuid = puuid))
    async with aiohttp.ClientSession() as session:
        for user in users:
            if user.puuid == None:
                task.append(getPuuid(user, session, api_key, limiter))
        await asyncio.gather(*task)
        task = []
        for user in users:
            task.append(getLastMatchId(user, session, api_key, limiter))
        await asyncio.gather(*task)
        task = []
        for user in users:
            task.append(printTactician(user, session, api_key, limiter))
        await asyncio.gather(*task)
    for user in users:
        print("This is what I want" + user.username + "#" + user.tag, user.adjustedLps)
    print(users)
    InitTacticianList(users, f"{page}!{case}3")


if __name__ == "__main__":
    asyncio.run(updateTactician("E:G", "Phase 1 : Rondes Suisse (Samedi)", "D"))

