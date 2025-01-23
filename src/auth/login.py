from utils.users.users import Users
import os

class Login(Users):
    def __init__(self):
        super().__init__()
    
    def verify(self) -> bool:
        if self.isUsernameValid():
            if self.isPasswordValid(self.username):
                print(f"You have logged in as {self.username}")
                return True
            else:
                print("Incorrect password. Please reach out to the Admin to reset your password")
                return False
        else:
            print("Username does not exist. Please register")
            return False
            
    def isUsernameValid(self) -> bool:
        self.username = input("Enter username: ")
        return self.isUserNameExist(username=self.username)
    
    def isPasswordValid(self, username: str) -> bool:
        password = input("Enter password: ")
        self.user_id = self.getIdFromUsername(username=username)
        return self.isPasswordCorrect(user_id=self.user_id, password=password)
            
    
    