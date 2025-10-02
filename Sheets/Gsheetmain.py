from quickstart import *
from user import User

def ListtoGsheet(users):
    users_list = []
    for user in users:
        user_car = []
        user_car.append(str(user.username))
        user_car.append(str(user.lps))
        users_list.append(user_car)
    print(users_list)
    print(users)

    write_cells("F1", users_list)