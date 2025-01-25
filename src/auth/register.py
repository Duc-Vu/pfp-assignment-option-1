from src.utils.users.users import Users
from typing import Callable
import os

class Register(Users):
    def __init__(self):
        super().__init__()
    
    def newUser(self) -> None:
        os.system("cls")
        name = self.getInput("Enter Full Name: ")
        username = self.isUniqueInfo(self.isUserNameExist, "Username")
        password = self.getInput("Create Password: ")
        email = self.isUniqueInfo(self.isEmailExist, "Email")
        phone_number = self.isUniqueInfo(self.isPhoneNumberExist, "Phone Number")
        while True:
            gender = self.getInput("Enter gender[Male/Female]: ")
            match gender:
                case "Male":
                    break
                case "Female":
                    break
                case _:
                    print("Answer should Male or Female")
        self.addUser(name=name, user_name=username, password=password, email_address=email, phone_number=phone_number, gender=gender, role=self.userRole[1])
        print(f"Register successful as a {self.userRole[1]}")
        
    def getInput(self, prompt: str) -> str:
        return input(prompt)
        
    def isUniqueInfo(self, func: Callable[[str], bool], prompt: str) -> str:
        while True:
            info = input(f"Enter {prompt}: ")
            if not func(info):
                return info
            print(f"The {prompt} already exists. Please enter a different one.")
            
    
            

    
    
    

    
    
    
    