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

async def manageRankException(user):
    if user.username == "RCS Xperion":
        user.tier = "Pro Circuit"
        user.adjustedLps = 4000
        user.lps = '/'
        return True
    if user.username == "MIH TarteMan":
        user.tier = "Pro Circuit"
        user.adjustedLps = 3900
        user.lps = '/'
        return True
    if user.username == "M8 Jedusor":
        user.tier = "Pro Circuit"
        user.adjustedLps = 3950
        user.lps = '/'
        return True
    return False

async def getRank(user, session, api_key, limiter, retries=0):
    if user.puuid == None:
        user.calculateAdjustedLps()
        user.tier = "unranked"
        return
    if await manageRankException(user):
        return
    headers = {
        "X-Riot-Token": api_key
    }
    api_uri = f"https://euw1.api.riotgames.com/tft/league/v1/by-puuid/{user.puuid}"
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status == 429:
        print(f"Error: {response.status} ({user.username}#{user.tag})")
        await asyncio.sleep(2 ** retries + random.random())
        return await getRank(user, session, api_key, limiter, retries + 1)
    elif status != 200:
        print("ERROR GETRANK")
        return
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

async def getLastMatchId(user, session, api_key, limiter, retries=0):
    headers = {
        "X-Riot-Token": api_key
    }
    if user.puuid == None:
        return
    api_uri = f"https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/{user.puuid}/ids?count=1"
    async with limiter, session.get(api_uri, headers=headers) as response:
        if response.status == 200:
            datas = await response.json()
        status = response.status
    if status == 429:
        print("error, retrying lastmatchid")
        await asyncio.sleep(2 ** retries + random.random())
        return await getLastMatchId(user, session, api_key, limiter, retries + 1)
    elif status != 200:
        print("error lastmatchid", status, api_uri)
        return
    if len(datas) == 0:
        print(user.username + "#" + user.tag, "no game found")
        user.lastMatchId = None
    else:
        user.lastMatchId = datas[0]

async def printLastGameInfos_Loic(user, users, session, api_key, limiter, games, retries=0):
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
    games.append(game)
    for i in range(len(game)):
        playerInfo = game[i]
        player = next((potPlayer for potPlayer in users if playerInfo["riotIdGameName"].lower() == potPlayer.username.lower()), None)
        if player != None:
            print("Player  found : ", player.username)
        if player:
            player.scores.append(9 - playerInfo["placement"])

async def printLastGameInfos(user, users, session, api_key, limiter, retries=0):
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
        player = next((potPlayer for potPlayer in users if playerInfo["riotIdGameName"] == potPlayer.username), None)
        if player:
            pos = next(i for i, x in enumerate(player.scores) if not x)
            player.scores[pos] = 9 - playerInfo["placement"]

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
        return await printTactician(user, session, api_key, limiter, retries + 1)
    game = datas["info"]["participants"]
    for i in range(len(game)):
        playerInfo = game[i]
        if playerInfo["riotIdGameName"].lower() == user.username.lower() and playerInfo["riotIdTagline"].lower() == user.tag.lower():
            user.tactician = playerInfo["companion"]["content_ID"]
