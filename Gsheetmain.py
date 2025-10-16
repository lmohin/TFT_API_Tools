from quickstart import *
from user import User
from Interface_Validation_PyQT import *

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
    PreviewQt("Liste Joueurs!D3", users_list)
    #write_cells("Liste Joueurs!D3", users_list)
    return

def InitGsheetPlayerList2(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.username))
        user_car.append(str(user.tag))
        user_car.append(str(user.puuid))
        users_list.append(user_car)
    PreviewQt("Phase 1 : Rondes Suisse (Samedi)!E3", users_list)
    return

def InitTacticianList(users,case):
    users_list = []
    for user in users:
        user_car = []
        user_car.append("https://ddragon.dakgg.net/tactician/"+ str(user.tactician) + ".jpg")
        print(user.puuid)
        users_list.append(user_car)
    PreviewQt(case, users_list)

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
    PreviewQt("Phase 2 : Finale (Dimanche)!D3", users_list)

def printUnits(units, page):
    units_list = []
    for unit in units:
        unit_car = []
        unit_car.append(str(unit.image))
        unit_car.append(str(unit.name))
        unit_car.append(str(unit.pickRate))
        unit_car.append(str(unit.pick))
        unit_car.append(str(unit.winRate) + "%")
        unit_car.append(str(unit.win))
        unit_car.append(str(unit.average))
        unit_car.append(str(unit.totalScore))
        units_list.append(unit_car)
    PreviewQt(page, units_list)
