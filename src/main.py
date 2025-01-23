from auth import *
import os
# from utils.roles import *

login_menu = ["1. Login", "2. Register", "3. Exit"]
# role = {
#     "Admin": Admin,
#     "EventOrganizer": EventOrganizer,
#     "Visitor": Visitor
# }

def chooseOption(menu):
    option = input(f'{"\n".join(menu)}\nChoose the number: ')
    return option if option in list(map(str, list(range(1, len(menu)+1)))) else None


while True:
    option = chooseOption(login_menu)
    match option:
        case "1":
            os.system("cls")
            login = Login()
            status = login.verify()
            if status:
                pass
        case "2":
            os.system("cls")
            reg = Register()
            reg.newUser()
        case "3":
            break
        case _:
            os.system("cls")
            print("Invalid option. Please choose a valid number.")