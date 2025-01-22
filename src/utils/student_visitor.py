import json
from tabulate import tabulate

class Student():
    def __init__(self):
        pass
    
    def searchEvents(self):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        row = []
        event_data = data["Events"]
        
        for event in event_data:
            row.append([event.title(), f"{len(event_data[event]["attendes"])}/{event_data[event]["max_attendes"]}", event_data[event]["date"], event_data[event]["detail"]])
    
        headers = ["Events", "Attendance", "Date", "Details"]
        print(tabulate(row, headers=headers, tablefmt="pretty"))
        
    def attendEvent(self, event, name):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        event_data = data["Events"]
        with open("data.json", "w") as f:
            if event.lower() in event_data:
                if name.lower() not in event_data[event.lower()]["attendes"]:
                    if len(event_data[event.lower()]["attendes"]) < int(event_data[event.lower()]["max_attendes"]):
                        event_data[event.lower()]["attendes"][name.lower()] = "Student/Visitor"
                        json.dump(data, f, indent=4)
                        print(f"Attend event {event.title()} successfully")
                    else:
                        json.dump(data, f, indent=4)
                        print(f"Over capacity for attendees {len(event_data[event.lower()]["attendes"])}/{int(event_data[event.lower()]["max_attendes"])}")
                else:
                    json.dump(data, f, indent=4)
                    print(f"{name.title()} is alrealy attend {event.title()}")
            else:
                json.dump(data, f, indent=4)
                print("Event is not exist")
                
    def viewEventsAttended(self, name):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        event_data = data["Events"]
        row = []
        for event in event_data:
            if name.lower() in event_data[event.lower()]["attendes"]:
                row.append([event.title(), event_data[event]["date"], "Attended"])
        
        headers = ["Events", "Date", "Status"]
        print(f"Events that {name.title()} attended")
        print(tabulate(row, headers=headers, tablefmt="pretty"))
        
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
            
