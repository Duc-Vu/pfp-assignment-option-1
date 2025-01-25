from src.auth import *
from typing import List
from src.utils.roles import *
import os

login_menu = ("Login", "Register", "Exit")

roles = {
    "Admin": Admin,
    "EventOrganizer": EventOrganizer,
    "Visitor": Visitor
    }

def showMenu(menu: List) -> str:
    index_menu = [f"{index+1}. {value}" for index, value in enumerate(menu)]
    option = input(f'{"\n".join(index_menu)}\nChoose the number: ')
    return option if option in list(map(str, list(range(1, len(menu)+1)))) else None

if __name__ == "__main__":
    while True:
        option = showMenu(login_menu)
        match option:
            case "1":
                os.system("cls")
                login = Login()
                status, role, user_id = login.verify()
                if status:
                    func = roles[role](user_id)
                    while func.flag:
                        option = showMenu(menu=func.menu)
                        func.handleMenu(option=option) 
            case "2":
                os.system("cls")
                reg = Register()
                reg.newUser()
            case "3":
                break
            case _:
                os.system("cls")
                print("Invalid option. Please choose a valid number.")