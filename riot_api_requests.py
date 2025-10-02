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
    if status == 429:
        print(f"Error here: {response.status} ({user.username}#{user.tag})")
        await asyncio.sleep(2 ** retries + random.random())
        return await getPuuid(user, session, api_key, limiter, retries + 1)
    elif status != 200:
        print(f"Error here: {response.status} ({user.username}#{user.tag})")
        user.puuid = None
        return
    user.puuid = datas["puuid"]


async def getRank(user, session, api_key, limiter, retries=0):
    if user.puuid == None:
        user.calculateAdjustedLps()
        user.tier = "unranked"
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
        user.tier = "UNRANKED"
        return
    rankedDatas = None
    for tempDatas in datas:
        if tempDatas['queueType'] == 'RANKED_TFT':
            rankedDatas = tempDatas
            break
    datas = rankedDatas
    if datas == None:
        print(user.username, 'no lp')
        user.calculateAdjustedLps()
        user.tier = "UNRANKED"
        return
    user.tier = datas['tier']
    user.rank = datas['rank']
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

async def printTactician(user, session, api_key, limiter, retries=0):
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
        if playerInfo["riotIdGameName"].lower() == user.username.lower() and playerInfo["riotIdTagline"].lower() == user.tag.lower():
            user.tactician = playerInfo["companion"]["content_ID"]
            print(playerInfo["riotIdGameName"], playerInfo["riotIdTagline"], playerInfo["placement"], 9 - playerInfo["placement"], playerInfo["companion"]["content_ID"])
