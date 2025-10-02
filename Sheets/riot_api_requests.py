import random
import asyncio

async def getPuuid(user, session, api_key, limiter, retries=0):
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

async def getRank(user, session, api_key, limiter, retries=0):
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
        user.calculateAdjustedLps()
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

async def getLastMatchId(user, session, api_key, limiter, retries=0):
    headers = {
        "X-Riot-Token": api_key
    }
    if user.puuid == None:
        return
    api_uri = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{user.puuid}/ids"
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status != 200:
        print("error, retrying")
        await asyncio.sleep(2 ** retries + random.random())
        return await getLastMatchId(user, session, api_key, limiter, retries + 1)
    if len(datas) == 0:
        print(user.username + "#" + user.tag, "no game found")
        user.lastMatchId = None
    else:
        user.lastMatchId = datas[0]

async def printLastGameInfos(user, session, api_key, limiter, retries=0):
    headers = {
        "X-Riot-Token": api_key
    }
    if user.lastMatchId == None:
        return
    api_uri = f"https://europe.api.riotgames.com/tft/match/v1/matches/{user.lastMatchId}"
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status != 200:
        print(f"Error match: {response.status} ({user.username}#{user.tag})")
        await asyncio.sleep(2 ** retries + random.random())
        return await printLastGameInfos(user, session, api_key, limiter, retries + 1)
    game = datas["info"]["participants"]
    for i in range(len(game)):
        playerInfo = game[i]
        print(playerInfo["riotIdGameName"], playerInfo["riotIdTagline"], playerInfo["placement"], 9 - playerInfo["placement"])
