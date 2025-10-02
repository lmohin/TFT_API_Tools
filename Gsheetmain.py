from quickstart import *
from user import User

def InitGsheetPlayerList(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.username))
        user_car.append(str(user.tag))
        user_car.append(str(user.puuid))
        user_car.append(str(user.tier).capitalize() + " " + str(user.rank))
        user_car.append("=IMAGE(\"https://cdn.dak.gg/tft/images2/tft/tiers/"+ str(user.tier).lower() + ".png?set=10\")")
#user_car.append("=IMAGE(\"https://ddragon.dakgg.net/tactician/"+ str(user.tactician) + ".jpg\")")
        user_car.append(str(user.lps))
        user_car.append(str(user.adjustedLps))
        users_list.append(user_car)
    print(users_list)
    print(users)

    write_cells("F3", users_list)
    return

def InitTacticianList(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append("=IMAGE(\"https://ddragon.dakgg.net/tactician/"+ str(user.tactician) + ".jpg\")")
        users_list.append(user_car)
    write_cells("D3", users_list)


