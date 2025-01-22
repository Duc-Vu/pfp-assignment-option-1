
import json
from tabulate import tabulate

class Admin():
    def createEvents(self, event_name=None, max_attendes=None,date=None, detail=None):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        #Thêm event vào file json nếu event chưa tồn tại
        with open("data.json", "w") as f:
            try:
                if event_name is not None or max_attendes is None or max_attendes > 0:
                    if event_name.lower() not in data["Events"]:
                        data["Events"][event_name.lower()] = {
                            'attendes': {},
                            'max_attendes': int(max_attendes) if max_attendes is not None else None,
                            'date': date,
                            'detail': detail
                        }
                        json.dump(data, f, indent=4)
                        print(f"Create event {event_name.title()} success")
                    else:
                        json.dump(data, f, indent=4)
                        print("Event existed")
                else:
                    print("Event name is not valid")
                    json.dump(data, f, indent=4)
            except Exception as e :
                print("Max attendes is not valid")
                json.dump(data, f, indent=4)
            
        
    def updateEvents(self, event, act, max_attendes=None,date=None, detail=None):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        #Nếu event có tồn tại thì update event
        with open("data.json", "w") as f:
            if event.lower() in data['Events']:
                
                    #Cập nhật số lượng attendes tối đa
                    if act == 1:
                        try:
                            #Kiểm tra tính hợp lệ của max_attendes
                            if max_attendes is None or int(max_attendes) > 0:
                                data['Events'][event.lower()]["max_attendes"] = int(max_attendes) if max_attendes is not None else None
                                json.dump(data, f, indent=4)
                                print(f"Update max attendes event {event.title()} successfully")
                        except Exception as e:
                            print("Max attendes is not valid")
                            json.dump(data, f, indent=4)
                            
                    #Cập nhật chi tiết của event
                    elif act == 2:
                        try:
                                data['Events'][event.lower()]["detail"] = str(detail)
                                json.dump(data, f, indent=4)
                                print(f"Update detail event {event.title()} successfully")

                        except Exception as e:
                            print("Detail is not valid")
                            json.dump(data, f, indent=4)
                            
                    #Cập nhật ngày của event
                    elif act == 3:
                        try:
                            data['Events'][event.lower()]["date"] = str(date)
                            json.dump(data, f, indent=4)
                            print(f"Update date event {event.title()} successfully")
                        except Exception as e:
                            print("Date is not valid")
                            json.dump(data, f, indent=4)
                    else:
                        print("Action is not exist")
                        json.dump(data, f, indent=4)
            else:
                print("Event is not exist")
                json.dump(data, f, indent=4)



    def deleteEvents(self, event):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
        
        with open("data.json", "w") as f:
            if event.lower() in data['Events']:
                del data['Events'][event.lower()]
                json.dump(data, f, indent=4)
                print(f"Delete event {event.title()} successfully")
            else:
                print("Event is not exist")
                json.dump(data, f, indent=4)
                    
    def allEvents(self):
        #Kiểm tra file data.json có hợp lệ không
        data = self.tryOpenDataFile()
                
        row = []
        max_per_line = 5  # Số người mỗi dòng
        #In dữ liệu của các sự kiện dưới dạng bảng
        for event in data["Events"]:
            attendes_list = data["Events"][event]["attendes"]
            attendee_names = [f"{name.title()} ({attendes_list[name]})" for name in attendes_list.keys()]
            attendees_str = "\n".join(", ".join(attendee_names[i:i+max_per_line]) for i in range(0, len(attendee_names), max_per_line))
            row.append([event.title(), attendees_str, data["Events"][event]["max_attendes"], f"{len(data["Events"][event]["attendes"])}/{data["Events"][event]["max_attendes"]}", data["Events"][event]["date"], data["Events"][event]["detail"]])
            
            
        headers = ["Event", "Attendees", "Max Attendees", "Attended Number", "Date", "Detail"]
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
            
        
    

# admin = Admin()
# admin.createEvents("Swim", 3, "10/7/2007", "You can swim in the space")
# admin.updateEvents("Hello", 2,  detail="Hello in English") 
# admin.deleteEvents("hello")
# admin.allEvents()
