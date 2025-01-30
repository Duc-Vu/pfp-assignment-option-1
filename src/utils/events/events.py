from typing import List, Dict
from tabulate import tabulate
import json, os

file_path = "database/events.json"

from ...utils.users.users import Users

class Events():
    def __init__(self):
        super().__init__()
        self.events_data = self.loadEvents()
        self.users = Users()
    
    # Tạo event mới
    def createEvent(self, event_name: str, description: str, max_attendees: str, start_date: str, end_date: str, address: str, status: str) -> None:
        event_id = int(list(self.events_data.keys())[-1])+1 if len(self.events_data) > 0 else 0
        # Lưu các thông tin của user
        self.events_data[event_id] = {
            "event_name": event_name.lower(),
            "description": description,
            "attendees": [],
            "organizer": [],
            "max_attendees": max_attendees,
            "start_date": start_date,
            "end_date": end_date,
            "address": address,
            "status": status
        }
        # Lưu self.events_data vào file JSON
        self.updateEventsToJson(self.events_data)
    
    # Xóa user theo event id
    def deleteEvent(self, event_id: str) -> None:
        del self.events_data[event_id]
        self.updateEventsToJson(self.events_data)
    
    # Load dữ liệu từ file users.json 
    def loadEvents(self) -> Dict:
        # Kiểm tra nếu file không tồn tại
        if not os.path.exists(file_path):
            events_data = {}
            self.updateEventsToJson(events_data)
            return events_data
        
        try:
            # Đọc file json
            with open(file_path, "r") as f:
                events_data = json.load(f)
            return events_data
        
        except ValueError as e:
            # Tạo lại file JSON nếu bị lỗi
            self.updateEventsToJson(events_data)
            return events_data
        
    # Cập nhật hoặc tạo mới file events.json
    def updateEventsToJson(self, events_data: List[Dict]) -> None:
        with open(file_path, "w") as f:
            json.dump(events_data, f, indent=4)
            
    # Kiểm tra event name đã tồn tại hay chưa
    def isEventNameExist(self, event_name: str, current_event_name=None) -> bool:
        return any(self.events_data[d]["event_name"] == event_name for d in self.events_data) if current_event_name == None else any(self.events_data[d]["event_name"] == event_name and self.events_data[d]["event_name"] != current_event_name for d in self.events_data)
    
    # Cập nhật thông tin của Event theo event id
    def updateEventInfo(self, event_id: str, type_info: str, new_info: str) -> None:
        self.events_data[event_id][type_info] = new_info
        self.updateEventsToJson(self.events_data)
    
    # Thêm Event Organizer vào event
    def addEventOrganizer(self, event_id: str, user_id: str) -> None:
        self.events_data[event_id]["organizer"].append(user_id)
        self.updateEventsToJson(self.events_data)
    
    # Xóa Event Organizer khỏi event
    def deleteEventOrganizer(self, event_id: str, user_id: str) -> None:
        self.events_data[event_id]["organizer"].remove(user_id)
        self.updateEventsToJson(self.events_data)
        
    # Kiểm tra số lượng event đã tối đa chứ
    def isEventOverAttendees(self, event_id) -> bool:
        return len(self.events_data[event_id]["attendees"]) > int(self.events_data[event_id]["max_attendees"]) - 1
    # Kiểm tra envent id có tồn tại
    def isEventIdExist(self, event_id: str) -> bool:
        return event_id in self.events_data
    
    # Show danh sách các sự kiện
    def showEvents(self) -> None:
        row = [[events_data, self.events_data[events_data]["event_name"].title(), self.events_data[events_data]["description"], len(self.events_data[events_data]["attendees"]), self.events_data[events_data]["max_attendees"], self.events_data[events_data]["start_date"], self.events_data[events_data]["end_date"], self.events_data[events_data]["address"], self.events_data[events_data]["status"]] for events_data in self.events_data]
        headers = ["Event ID", "Event Name", "Description", "Attendees", "Maximun Attendees", "Start Date", "End Date", "Address", "Status"]
        print(tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None))
    
    # Show chi tiết sự kiện
    def showEventDetails(self, event_id: str) -> None:
        events_data = self.events_data[event_id]
        user_data = self.users.users_data
        print(f"Event Name: {events_data["event_name"]}\nDescription: {events_data["description"]}\nMaximun Attendees: {events_data["max_attendees"]}\nStart Date: {events_data["start_date"]}\nEnd Date: {events_data["end_date"]}\nAddress: {events_data["address"]}\nStatus: {events_data["status"]}")
        row = [[user_id, user_data[user_id]["username"], user_data[user_id]["role"], user_data[user_id]["email_address"], user_data[user_id]["phone_number"], user_data[user_id]["gender"]] for user_id in events_data["attendees"]]
        headers = ["UserID", "Username", "Role", "Email Address", "Phone Number", "Gender"]
        print(f"Attendees:\n{tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None)}")
        row = [[user_id, user_data[user_id]["username"], user_data[user_id]["role"], user_data[user_id]["email_address"], user_data[user_id]["phone_number"], user_data[user_id]["gender"]] for user_id in events_data["organizer"]]
        headers = ["UserID", "Username", "Role", "Email Address", "Phone Number", "Gender"]
        print(f"Organizer:\n{tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None)}")

    # Kiểm tra user có phải là Event Organizer
    def isUserIdOrganizer(self, user_id: str, in_event_id = None) -> bool:
        return any(user_id in organizers for events_data in self.events_data for organizers in self.events_data[events_data]["organizer"]) if user_id == None else user_id in self.events_data[in_event_id]["organizer"]
    
    # Get eventname từ event id
    def getEventNameFromID(self, event_id: str) -> str:
        return next(self.events_data[events_data]["event_name"] for events_data in self.events_data if events_data == event_id)
    
    # Xóa tất cả các events
    def deleteAllEvents(self) -> None:
        self.updateEventsToJson({})
        
    # Xóa user khỏi danh sách tham dự và ban tổ chức của tất cả events
    def deleteUserIdFromAllEvents(self, user_id: str, attendees=True, organizer=True) -> None:
        keys = []
        if attendees:
            keys.append("attendees")
        if organizer:
            keys.append("organizer")
            
        for event_id in self.events_data:
            for key in keys:
                if user_id in self.events_data[event_id][key]:
                    self.events_data[event_id][key].remove(user_id)
        self.updateEventsToJson(self.events_data)
    
    # Đặt lại danh sách tham dự và ban tổ chức của tất cả events          
    def resetAllUsersInEvent(self):
        for event_id in self.events_data:
            for key in ["attendees", "organizer"]:
                self.events_data[event_id][key] = []
        self.updateEventsToJson(self.events_data)
    
    # Lấy danh sách của các event mà user_id làm ban tổ chức
    def getEventsOrganizer(self, user_id: str) -> List:
        event_id_organizer = []
        for event_id in self.events_data:
            if user_id in self.events_data[event_id]["organizer"]:
                event_id_organizer.append(event_id)
        return event_id_organizer
    
    def getEventsAttended(self, user_id: str) -> List:
        event_id_attended = []
        for event_id in self.events_data:
            if user_id in self.events_data[event_id]["attendees"]:
                event_id_attended.append(event_id)
        return event_id_attended
    
    # Show danh sách của tất cả event mà user_id làm ban tổ chức
    def showEventsOrganizer(self, user_id: str) -> None:
        headers = ["Event ID", "Event Name", "Description", "Attendees", "Maximun Attendees", "Start Date", "End Date", "Address", "Status"]
        row = [[events_data, self.events_data[events_data]["event_name"].title(), self.events_data[events_data]["description"], len(self.events_data[events_data]["attendees"]), self.events_data[events_data]["max_attendees"], self.events_data[events_data]["start_date"], self.events_data[events_data]["end_date"], self.events_data[events_data]["address"], self.events_data[events_data]["status"]] for events_data in self.getEventsOrganizer(user_id=user_id)]
        print(tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None))
        
    # Kiểm tra event có tham gia event chưa
    def isUserAttendedEvent(self, user_id: str, event_id: str) -> None:
        return user_id in self.events_data[event_id]["attendees"]
    
    # Thêm user vào event
    def addUserToEvents(self, user_id: str, event_id: str) -> None:
        self.events_data[event_id]["attendees"].append(user_id)
        self.updateEventsToJson(self.events_data)
    
    # Xóa user khỏi event  
    def deleteUserFromEvents(self, user_id: str, event_id: str) -> None:
        self.events_data[event_id]["attendees"].remove(user_id)
        self.updateEventsToJson(self.events_data)
        
    def showEventAttended(self, user_id: str) -> None:
        headers = ["Event ID", "Event Name", "Description", "Attendees", "Maximun Attendees", "Start Date", "End Date", "Address", "Status"]
        row = [[events_data, self.events_data[events_data]["event_name"].title(), self.events_data[events_data]["description"], len(self.events_data[events_data]["attendees"]), self.events_data[events_data]["max_attendees"], self.events_data[events_data]["start_date"], self.events_data[events_data]["end_date"], self.events_data[events_data]["address"], self.events_data[events_data]["status"]] for events_data in self.getEventsAttended(user_id=user_id)]
        print(tabulate(row, headers=headers, tablefmt="grid", colalign=["center"]*len(headers) if len(row) > 0 else None))