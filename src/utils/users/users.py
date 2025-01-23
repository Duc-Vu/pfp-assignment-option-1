from typing import List, Dict
import json, os

file_path = "database/users.json"

class Users():
    def __init__(self):
        self.data = self.loadUsers()
    
    # Thêm user vào file users.json
    def addUser(self, name: str, user_name: str, password: str, email_address: str, phone_number: str, gender: str, role: str) -> None:
        # Đặt user_id của user theo số nguyên tăng dần
        user_id = int(list(self.data.keys())[-1])+1 if len(self.data) > 0 else 0
        # Lưu các thông tin của user
        self.data[user_id] = {
            "name": name,
            "username": user_name,
            "password": password,
            "email_address": email_address,
            "phone_number": phone_number,
            "gender": gender,
            "role": role
        }
        # Lưu self.data vào file JSON
        self.updateUsers(self.data)
    
    # Xóa user theo user_id 
    def deleteUser(self, user_id: str) -> None:
        del self.data[str(user_id)]
        self.updateUsers(self.data)
    
    # Load dữ liệu từ file users.json 
    def loadUsers(self) -> list:
        # Kiểm tra nếu file không tồn tại
        if not os.path.exists(file_path):
            data = {}
            self.updateUsers(data)
            return data
        
        try:
            # Đọc file json
            with open(file_path, "r") as f:
                data = json.load(f)
            return data
        
        except ValueError as e:
            # Tạo lại file JSON nếu bị lỗi
            self.updateUsers(data)
            return data
        
    # Cập nhật hoặc tạo mới file users.json
    def updateUsers(self, data: List[Dict]) -> None:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    # Kiểm tra user_name đã tồn tại hay chưa
    def isUserNameExist(self, username: str, current_username=None) -> bool:
        return any(self.data[d]["username"] == username for d in self.data) if current_username == None else any(self.data[d]["username"] == username and self.data[d]["username"] != current_username for d in self.data)

    # Kiểm tra email đã tồn tại hay chưa
    def isEmailExist(self, email: str, current_email=None) -> bool:
        return any(self.data[d]["email_address"] == email for d in self.data) if current_email == None else any(self.data[d]["email_address"] == email and self.data[d]["email_address"] != current_email for d in self.data)
    
    # Kiểm tra email đã tồn tại hay chưa
    def isPhoneNumberExist(self, phone_number: str, current_phone_number=None) -> bool:
        return any(self.data[d]["email_address"] == phone_number for d in self.data) if current_phone_number == None else any(self.data[d]["phone_number"] == phone_number and self.data[d]["phone_number"] != current_phone_number for d in self.data)
    
    # Cập nhật thông tin của user theo ID
    def updateUserInfo(self, user_id: str, type_info: str, new_info: str) -> None:
        self.data[user_id][type_info] = new_info
        self.updateUsers(self.data)
    
    # Tìm ID của User theo Username
    def getIdFromUsername(self, username: str) -> str:
        return next((d for d in self.data.keys() if self.data[d]["username"] == username), None)
    
    # Kiểm tra password
    def isPasswordCorrect(self, user_id: str, password: str) -> bool:
        return True if self.data[user_id]["password"] == password else False
    
    def getRole(self, user_id: str) -> str:
        return self.data[user_id]["role"]
    
