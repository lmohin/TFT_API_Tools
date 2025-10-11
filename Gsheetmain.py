from quickstart import *
from user import User

def InitGsheetPlayerList(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.username))
        user_car.append(str(user.tag))
        user_car.append(str(user.puuid))
        user_car.append(str(user.tier).capitalize() + " " + (str(user.rank) if user.rank != None else ''))
        if user.tier == "Pro Circuit":
            user_car.append("=IMAGE(\"https://liquipedia.net/commons/images/thumb/7/77/TFT_Regional_Finals_icon_darkmode.png/42px-TFT_Regional_Finals_icon_darkmode.png\")")
        else:
            user_car.append("=IMAGE(\"https://cdn.dak.gg/tft/images2/tft/tiers/"+ str(user.tier).lower() + ".png?set=10\")")
        user_car.append(str(user.lps))
        users_list.append(user_car)

    write_cells("D3", users_list)
    return

def InitGsheetPlayerList2(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.username))
        user_car.append(str(user.tag))
        user_car.append(str(user.puuid))
        users_list.append(user_car)
    write_cells("Phase 1 : Rondes Suisse (Samedi)!E3", users_list)
    return

def InitTacticianList(users,case):
    users_list = []
    for user in users:
        user_car = []
        user_car.append("https://ddragon.dakgg.net/tactician/"+ str(user.tactician) + ".jpg")
        users_list.append(user_car)
    write_cells(case, users_list)

def printScores(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.tactician))
        user_car.append(str(user.username))
        user_car.append(str(user.tag))
        user_car.append(str(user.puuid))
        scores = user.scores
        for score in scores:
            user_car.append(str(score) if score else '')
        users_list.append(user_car)
    write_cells("Phase 1 : Rondes Suisse (Samedi)!D3", users_list)

def printUnits(units, page):
    units_list = []
    for unit in units:
        unit_car = []
        unit_car.append(str(unit.image))
        unit_car.append(str(unit.name))
        unit_car.append(str(unit.pickRate) + "%")
        unit_car.append(str(unit.pick))
        unit_car.append(str(unit.winRate) + "%")
        unit_car.append(str(unit.win))
        unit_car.append(str(unit.average))
        unit_car.append(str(unit.totalScore))
        units_list.append(unit_car)
    write_cells(page, units_list)
