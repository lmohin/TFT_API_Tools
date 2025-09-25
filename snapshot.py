import requests
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

async def printUserInfos(user, tag, api_key):
    """'user' (string) must designs a valid riot ID"""
    api_uri = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + user + "/" + tag
    headers = {
            "X-Riot-Token": api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(api_uri, headers=headers) as response:
            if response.status != 200:
                print(f"Error: {response.status} ({user}#{tag})")
                if response.status == 404:
                    return
                await asyncio.sleep(1)
                return await printUserInfos(user, tag)
            datas = await response.json()
            puuid = datas["puuid"]
            api_uri = "https://euw1.api.riotgames.com/tft/league/v1/by-puuid/"
            api_uri += puuid
        async with session.get(api_uri, headers=headers) as response:
            if response.status != 200:
                print(f"Error: {response.status} ({user}#{tag})")
                #await asyncio.sleep(1)
                return
                #return await printUserInfos(user, tag)
            datas = (await response.json())
            if len(datas) == 0:
                return
            datas = datas[0]
            print(user, tag, datas['tier'], datas['rank'], datas['leaguePoints'])
        api_uri  = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
        async with session.get(api_uri, headers=headers) as response:
            if response.status != 200:
                print(f"Error: {response.status} ({user}#{tag})")
                return
            datas = (await response.json())
            matchId = datas[0]
        api_uri = f"https://europe.api.riotgames.com/tft/match/v1/matches/{matchId}"
        async with session.get(api_uri, headers=headers) as response:
            if response.status != 200:
                print(f"Error match: {response.status} ({user}#{tag})")
                return
            datas = await response.json()
            print(datas["info"]["participants"])


async def main():
    api_key = os.environ.get('RIOT_API_KEY')
    if api_key == None:
        print("Error: no riot api key detected")
        return
    task = []
    for i in range(1): 
        #task.append(printUserInfos("Toonutv", "EUW", api_key))
        task.append(printUserInfos("Falkor", "Genti", api_key))
        #task.append(printUserInfos("Megata", "0000", api_key))
        #task.append(printUserInfos("Essrog", "TFT", api_key))
        #task.append(printUserInfos("Arestidios", "AAA", api_key))
        #task.append(printUserInfos("Azzo", "009", api_key))
        #task.append(printUserInfos("Yottah", "0000", api_key))
        #task.append(printUserInfos("brozilla", "brz", api_key))
        #task.append(printUserInfos("etre infame", "EUW", api_key))
    results = await asyncio.gather(*task)

if __name__ == "__main__":
      asyncio.run(main())
