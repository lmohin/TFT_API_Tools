import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *

async def main():
    load_dotenv()
    limiter = AsyncLimiter(10, 1)
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    users = []
    for i in range(1):
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
        task = []
        for user in users:
            task.append(getLastMatchId(user, session, api_key, limiter))
        await asyncio.gather(*task)
        task = []
        for user in users:
            task.append(printLastGameInfos(user, session, api_key, limiter))
        await asyncio.gather(*task)
    users.sort(key=lambda x: x.adjustedLps, reverse=True)
    for user in users:
        print("This is what I want" + user.username + "#" + user.tag, user.adjustedLps)
    return users

if __name__ == "__main__":
    users = asyncio.run(main())
    print(users)
    ListtoGsheet(users)
