from src.auth import *
from src.utils.roles import *
from typing import List
import os

login_menu = ("Login", "Register", "Exit")

roles = {
    "Admin": Admin,
    "EventOrganizer": EventOrganizer,
    "Visitor": Visitor
    }

def showMenu(menu: List) -> str:
    index_menu = "\n".join([f"{index+1}. {value}" for index, value in enumerate(menu)])
    option = input(f'{index_menu}\nChoose the number: ')
    return option if option in list(map(str, list(range(1, len(menu)+1)))) else None

if __name__ == "__main__":
    while True:
        option = showMenu(login_menu)
        match option:
            case "1":
                os.system("cls")
                status, role, user_id = Login().verify()
                if status:
                    func = roles[role](user_id)
                    while func.flag:
                        func.handleMenu(option=showMenu(menu=func.menu)) 
            case "2":
                os.system("cls")
                Register().newUser()
            case "3":
                break
            case _:
                os.system("cls")
                print("Invalid option. Please choose a valid number.")