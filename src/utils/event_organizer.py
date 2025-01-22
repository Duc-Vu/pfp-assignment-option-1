import json
from tabulate import tabulate

class EventOrganizer():
    def isEventValid(self, event):
        data = self.tryOpenDataFile()
        if event.lower() in data["Events"]:
            self.event = event
            return True
        else:
            return False
        
    
    def addAttendees(self, name, role):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        #Thêm người tham dự vào event nếu người tham dự chưa tham gia
        with open("data.json", "w") as f:
            try:
                if self.event.lower() in data["Events"]:
                    if name.lower() not in data["Events"][self.event.lower()]["attendes"]:
                        if len(data["Events"][self.event.lower()]["attendes"]) < int(data["Events"][self.event.lower()]["max_attendes"]):
                            data["Events"][self.event.lower()]["attendes"][name.lower()] = role.lower()
                            json.dump(data, f, indent=4)
                            print(f"Add attendee {name.title()} successfully")
                        else:
                            json.dump(data, f, indent=4)
                            print(f"Over capacity for attendees {len(data["Events"][self.event.lower()]["attendes"])}/{int(data["Events"][self.event.lower()]["max_attendes"])}")
                    else:
                        print(f"{name.title()} is alrealy attendee")
                        json.dump(data, f, indent=4)
                else:
                    print("Event is not exist")
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(e)
                    
                    
    def deleteAttendees(self, name):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        with open("data.json", "w") as f:
            try:
                if self.event.lower() in data["Events"]:
                    if name.lower() in data["Events"][self.event.lower()]["attendes"]:
                        del data["Events"][self.event.lower()]["attendes"][name.lower()]
                        json.dump(data, f, indent=4)
                        print(f"Delete attendee {name.title()} successfully")
                    else:
                        json.dump(data, f, indent=4)
                        print(f"{name.title()} is not attendee of event {self.event.title()}")
                else:
                    print("Event is not exist")
                    json.dump(data, f, indent=4)
            except Exception as e:
                pass
            
    def showEventDetails(self):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        row = []
        if self.event.lower() in data["Events"]:
            event_data = data["Events"][self.event.lower()]
            keys = list(event_data["attendes"])
            for key, value in event_data["attendes"].items():
                row.append([keys.index(key)+1, key.title(), value.title()])
            headers = ["STT", "Attendees", "Role"]
            
            print(f"Event name: {self.event.title()}\nAttended: {len(event_data["attendes"])}\nMax Attendees: {event_data["max_attendes"]}\nDetail: {event_data["detail"]}\n{tabulate(row, headers=headers, tablefmt="pretty")}")
        else:
            print("Event is not exist")
    
    def tryOpenDataFile(self):
        #Kiểm tra file data.json có hợp lệ không
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                return data
        # Nếu file data.json bị lỗi hoặc chưa khởi tạo sẽ khởi tạo hoặc reset dữ liệu           
        except Exception as e:
            with open("data.json", "w") as f:
                json.dump({"Events": {}}, f, indent=4)
                return {"Events": {}}
        
                    
                    
# eo = EventOrganizer("")
# eo.event = "Fly"
# eo.addAttendees("vod", "Vistor")
# eo.deleteAttendees("god")
# eo.showEventDetails()
                    