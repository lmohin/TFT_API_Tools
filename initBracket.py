import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from aiolimiter import AsyncLimiter
from user import User
from riot_api_requests import *
from Gsheetmain import *

def initBracket(lobbyNumber):
    values = get_cell_value("B:F")
    values.pop(0)
    values.pop(0)
    users = []
    for value in values:
        users.append(User(value[2], value[3], tactician = value[0], puuid = value[4]))
    i = 0
    ascend = -1
    for user in users:
        if ascend > 0:
            user.lobby = i % (lobbyNumber) + 1
        else:
            user.lobby = lobbyNumber - i % lobbyNumber
        if i % lobbyNumber == lobbyNumber - 1:
            ascend *= -1
        i += 1
    users.sort(key=lambda x: x.lobby, reverse=False)
    InitGsheetPlayerList2(users)

if __name__ == "__main__":
    initBracket(4)
