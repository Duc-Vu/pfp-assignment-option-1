default_menu = (
                "Search Events", 
                "Registration Event",
                "Cancel Registration",
                "View Registered Events",
                "View account details",
                "Update Infomation",
                "Logout"
)
change_infomation_menu = (
    "Update username",
    "Update Password",
    "Exit"
)
from ...utils.events.events import Events
from ...utils.users.users import Users
class Visitor(Events, Users):
    def __init__(self, account_user_id):
        super().__init__()
        self.account_id = account_user_id
        self.menu = default_menu
        self.flag = True

    def handleMenu(self, option: str):
        menu_handlers = {
            default_menu: self.defaultMenu,
            change_infomation_menu: self.changeInfoMenu
        }
        handler = menu_handlers.get(self.menu)
        if handler:
            handler(option=option)
    
    def defaultMenu(self, option: str):
        match option:
            case "1":
                self.showEvents()
            case "2":
                event_id = input("Enter event id to attend: ")
                if not self.isEventIdExist(event_id=event_id):
                    print("Event does not exist")
                    return
                if self.isEventOverAttendees(event_id=event_id):
                    print("Event is over capacity")
                    return
                if self.isUserAttendedEvent(user_id=self.account_id, event_id=event_id):
                    print("You already attend this event")
                    return
                self.addUserToEvents(user_id=self.account_id, event_id=event_id)
                print("Attend event successful")
            case "3":
                event_id = input("Enter event id to cancle registration: ")
                if not self.isEventIdExist(event_id=event_id):
                    print("Event does not exist")
                    return
                if not self.isUserAttendedEvent(user_id=self.account_id, event_id=event_id):
                    print("You not attend this event")
                    return
                self.deleteUserFromEvents(user_id=self.account_id, event_id=event_id)
                print("Cancle registration from event successful")
            case "4":
                self.showEventAttended(user_id=self.account_id)
            case "5":
                self.showUserDetails(user_id=self.account_id)
            case "6":
                self.menu = change_infomation_menu
            case "7":
                self.flag = False
            case _:
                print("Invalid option. Please choose a valid number.")
                
    def changeInfoMenu(self, option: str):
        match option:
            case "1":
                new_username = input("Enter new usernam: ")
                if self.isUserNameExist(username=new_username):
                    print("Username existed")
                    return
                self.updateUserInfo(user_id=self.account_id, type_info="username", new_info=new_username)
                print("Update username successful")
            case "2":
                password = input("Enter your old password: ")
                if not self.isPasswordCorrect(user_id=self.account_id, password=password):
                    print("Your password is not correct. Please try again")
                    return
                new_password = input("Enter new password: ")
                self.updateUserInfo(user_id=self.account_id, type_info="password", new_info=new_password)
                print("Update password successful")
            case "3":
                self.menu = default_menu
            case _:
                print("Invalid option. Please choose a valid number.")
            
                
        
        