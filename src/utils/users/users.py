from typing import List, Dict
import json, os
from tabulate import tabulate

file_path = "database/users.json"


class Users():
    def __init__(self):
        super().__init__()
        self.users_data = self.loadUsers()
        self.userRole = ["Admin", "Visitor", "EventOrganizer"]
    
    # Thêm user vào file users.json
    def addUser(self, name: str, user_name: str, password: str, email_address: str, phone_number: str, gender: str, role: str) -> None:
        # Đặt user_id của user theo số nguyên tăng dần
        user_id = int(list(self.users_data.keys())[-1])+1 if len(self.users_data) > 0 else 0
        # Lưu các thông tin của user
        self.users_data[user_id] = {
            "name": name,
            "username": user_name,
            "password": password,
            "email_address": email_address,
            "phone_number": phone_number,
            "gender": gender,
            "role": role
        }
        # Lưu self.users_data vào file JSON
        self.updateUsers(self.users_data)
    
    # Xóa user theo user_id 
    def deleteUser(self, user_id: str) -> None:
        del self.users_data[str(user_id)]
        self.updateUsers(self.users_data)
    
    # Load dữ liệu từ file users.json 
    def loadUsers(self) -> list:
        # Kiểm tra nếu file không tồn tại
        if not os.path.exists(file_path):
            users_data = {}
            self.updateUsers(users_data)
            return users_data
        
        try:
            # Đọc file json
            with open(file_path, "r") as f:
                users_data = json.load(f)
            return users_data
        
        except ValueError as e:
            # Tạo lại file JSON nếu bị lỗi
            self.updateUsers(users_data)
            return users_data
        
    # Cập nhật hoặc tạo mới file users.json
    def updateUsers(self, users_data: List[Dict]) -> None:
        with open(file_path, "w") as f:
            json.dump(users_data, f, indent=4)
            
    # Kiểm tra user_name đã tồn tại hay chưa
    def isUserNameExist(self, username: str, current_username=None) -> bool:
        return any(self.users_data[d]["username"] == username for d in self.users_data) if current_username == None else any(self.users_data[d]["username"] == username and self.users_data[d]["username"] != current_username for d in self.users_data)

    # Kiểm tra email đã tồn tại hay chưa
    def isEmailExist(self, email: str, current_email=None) -> bool:
        return any(self.users_data[d]["email_address"] == email for d in self.users_data) if current_email == None else any(self.users_data[d]["email_address"] == email and self.users_data[d]["email_address"] != current_email for d in self.users_data)
    
    # Kiểm tra email đã tồn tại hay chưa
    def isPhoneNumberExist(self, phone_number: str, current_phone_number=None) -> bool:
        return any(self.users_data[d]["email_address"] == phone_number for d in self.users_data) if current_phone_number == None else any(self.users_data[d]["phone_number"] == phone_number and self.users_data[d]["phone_number"] != current_phone_number for d in self.users_data)
    
    # Cập nhật thông tin của user theo ID
    def updateUserInfo(self, user_id: str, type_info: str, new_info: str) -> None:
        self.users_data[user_id][type_info] = new_info
        self.updateUsers(self.users_data)
    
    # Tìm ID của User theo Username
    def getIdFromUsername(self, username: str) -> str:
        return next((d for d in self.users_data.keys() if self.users_data[d]["username"] == username), None)
    
    # Tìm username theo id
    def getNameFromId(self, user_id: str) -> str:
        return next((self.users_data[users_data]["username"] for users_data in self.users_data if users_data==user_id), None)
    
    # Kiểm tra password
    def isPasswordCorrect(self, user_id: str, password: str) -> bool:
        return self.users_data[user_id]["password"] == password
    
    # Get role của user thông qua user_id
    def getRole(self, user_id: str) -> str:
        return self.users_data[user_id]["role"]
    
    # Kiểm tra UserID đã tồn tại chưa
    def isUserIdExist(self, user_id: str) -> bool:
        return user_id in self.users_data
    
    # Hiển thị toàn bộ users đã đăng ký
    def showAllUsers(self) -> None:
        headers = ["UserID", "Username", "Role", "Email Address", "Phone Number", "Gender", "Password"]
        row = [[user_id, self.users_data[user_id]["username"], self.users_data[user_id]["role"], self.users_data[user_id]["email_address"], self.users_data[user_id]["phone_number"], self.users_data[user_id]["gender"], self.users_data[user_id]["password"]] for user_id in self.users_data]
        print(tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None))
        
    def resetEventOrganizersToVisitor(self) -> None:
        for user_id in self.users_data:
            if self.users_data[user_id]["role"] == self.userRole[2]:
                self.users_data[user_id]["role"] = self.userRole[1]
        self.updateUsers(self.users_data)
        
    def deleteAllUsersExceptAdmin(self) -> None:
        users_data = self.users_data
        for user_id in list(users_data.keys()):
            if users_data[user_id]["role"] != self.userRole[0]:
                del users_data[user_id]
        self.updateUsers(users_data)
        
    def isUserStaff(self, user_id: str):
        return self.users_data[user_id]["role"] != self.userRole[1]
    
    def showUserDetails(self, user_id: str):
        print("UserID:",user_id)
        for user_data in self.users_data[user_id].keys():
            if user_data != "password":
                print(f"{user_data.title()}: {self.users_data[user_id][user_data]}")

        

    
