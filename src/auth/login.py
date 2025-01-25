from src.utils.users.users import Users

class Login(Users):
    def __init__(self):
        super().__init__()
    
    # Xác thực mật khẩu và user_name
    def verify(self) -> tuple:
        if self.isUsernameValid():
            if self.isPasswordValid(self.username):
                print(f"You have logged in as {self.username}")
                return True, self.getRole(self.user_id), self.user_id
            else:
                print("Incorrect password. Please reach out to the Admin to reset your password")
                return False, None, None
        else:
            print("Username does not exist. Please register")
            return False, None,  None
    
    # Kiểm tra user_name đã tồn tại hay không
    def isUsernameValid(self) -> bool:
        self.username = input("Enter username: ")
        return self.isUserNameExist(username=self.username)
    
    # Kiểm tra mật khẩu đã hợp lệ hay chưa
    def isPasswordValid(self, username: str) -> bool:
        password = input("Enter password: ")
        self.user_id = self.getIdFromUsername(username=username)
        return self.isPasswordCorrect(user_id=self.user_id, password=password)
            
    
    