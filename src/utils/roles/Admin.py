default_menu = (
    "Create Event",
    "Update Event",
    "Delete Event",
    "Delete All Events",
    "View All Events",
    "Manage Users",
    "Logout"
)
update_event_menu = (
    "Add Event Organizer",
    "Remove Event Organizer",
    "Change Event Name",
    "Change Event Description",
    "Change Max Attendees",
    "Change Start Date",
    "Change End Date",
    "Change Address",
    "Change Status",
    "Exit"
)
manage_users_menu = (
    "View All Users",
    "Change Info Users",
    "Delete User",
    "Delete All Users",
    "Exit"
)
change_info_users_menu = (
    "Change Name",
    "Change Username",
    "Change User Password",
    "Change Email Address",
    "Change Phone Number",
    "Change Gender",
    "Change Role",
    "Exit"
)
change_role_menu = (
    "Admin",
    "Visitor",
    "Exit"
)
change_gender_menu = ("Male", "Female", "Unknow", "Exit")
view_all_events_menu = ("View Event Details", "Exit")
event_status_menu = ("SCHEDULED", "ONGOING", "COMPLETED", "Exit")
from src.utils.events.events import Events
from src.utils.users.users import Users

class Admin(Events, Users):
    def __init__(self, account_user_id):
        super().__init__()
        self.menu = default_menu
        self.flag = True
        self.event_id = None
        self.user_id = None
    
    def handleMenu(self, option: str) -> None:
        menu_handlers = {
            default_menu: self.defaultMenu,
            update_event_menu: self.updateEventsMenu,
            view_all_events_menu: self.viewAllEventsMenu,
            event_status_menu: self.eventStatusMenu,
            manage_users_menu: self.manageUsersMenu,
            change_info_users_menu: self.changeInfoUsersMenu,
            change_role_menu: self.changeRoleMenu,
            change_gender_menu: self.genderMenu
        }
        handler = menu_handlers.get(self.menu)
        if handler:
            handler(option=option)
        
    def defaultMenu(self, option: str) -> None:
        match option:
            case "1":
                event_name = input("Enter event name: ")
                if self.isEventNameExist(event_name=event_name):
                    print("Event name is exist")
                    return
                try:
                    max_attendees = int(input("Enter maximum number of attendees: "))
                    if max_attendees < 0:
                        print("The maximum number of attendees cannot be negative.")
                        return
                except Exception:
                    print("Max attendees does not valid")
                    return
                description = input("Enter description: ")
                start_date = input("Enter start date: ")
                end_date = input("Enter end date: ")
                address = input("Enter event address: ")
                status = event_status_menu[0]
                self.createEvent(event_name, description, max_attendees, start_date, end_date, address, status)
                print(f"Create event {event_name.title()} successful")
    
            case "2":
                self.menu = update_event_menu
                self.event_id = None
            case "3":
                event_id = input("Enter the id of the event you want to delete: ")
                if self.isEventIdExist(event_id=event_id):
                    users_in_event_organizer = self.events_data[event_id]["organizer"]
                    self.deleteEvent(event_id=event_id)
                    for user_id in users_in_event_organizer:
                        if not self.isUserIdOrganizer(user_id):
                            self.updateUserInfo(user_id=user_id, type_info="role", new_info=self.userRole[1])
                    return
                print("Event does not exist")
            case "4":
                confirm = input("Are you sure to delete all events [y/n]: ")
                if confirm == "y":
                    self.deleteAllEvents()
                    self.resetEventOrganizersToVisitor()
                    print("Delete all events successful")
                elif confirm != "n":
                    print("Invalid option. Please choose a valid option.")
            case "5":
                self.showEvents()
                self.menu = view_all_events_menu
            case "6":
                self.menu = manage_users_menu
                self.user_id = None
            case "7":
                self.flag = False
            case _:
                print("Invalid option. Please choose a valid number.")
                
    def updateEventsMenu(self, option: str) -> None:
        if option in list(map(str, list(range(1, 10)))) and self.event_id == None:
            self.event_id = input("Enter event id: ")
            if not self.isEventIdExist(event_id=self.event_id):
                print("EventID does not exist")
                return
        match option:
            case "1":
                user_id = input("Enter user id: ")
                if self.isUserIdExist(user_id=user_id):
                    if not self.isUserIdOrganizer(user_id=user_id, in_event_id=self.event_id):
                        self.deleteUserIdFromAllEvents(user_id=user_id, organizer=False)
                        self.addEventOrganizer(event_id=self.event_id, user_id=user_id)
                        self.updateUserInfo(user_id=user_id, type_info="role", new_info=self.userRole[2])
                        print(f"Promote {self.getNameFromId(user_id=user_id)} to Event Organizer for the event {self.getEventNameFromID(event_id=self.event_id).title()}.")
                        return
                    print(f"{self.getNameFromId(user_id=user_id)} was a Event Organizer in {self.getEventNameFromID(event_id=self.event_id).title()}")
                print("UserID does not exist")
            case "2":
                user_id = input("Enter user id: ")
                if self.isUserIdExist(user_id=user_id):
                    if self.isUserIdOrganizer(user_id=user_id, in_event_id=self.event_id):
                        self.deleteEventOrganizer(event_id=self.event_id, user_id=user_id)
                        if not self.isUserIdOrganizer(user_id):
                            self.updateUserInfo(user_id=user_id, type_info="role", new_info=self.userRole[1])
                        print("Delete Event Organizer successful")
                print("UserID does not exist")
            case "3":
                new_event_name = input("Enter new event name: ").lower()
                if self.isEventNameExist(event_name=new_event_name):
                    print("Event name is exist")
                    return
                self.updateEventInfo(event_id=self.event_id, type_info="event_name", new_info=new_event_name)
                print(f"Update event name to {new_event_name.title()} successful")
            case "4":
                new_description = input("Enter new description: ")
                self.updateEventInfo(event_id=self.event_id, type_info="description", new_info=new_description)
                print("Update description successful")
            case "5":
                try:
                    new_max_attendees = int(input("Enter new maximum number of attendees: "))
                    if new_max_attendees < 0:
                        print("Maximun attendees cannot be negative")
                        return
                    self.updateEventInfo(event_id=self.event_id, type_info="max_attendees", new_info=new_max_attendees)
                    print("Update maximun attendees successful")
                except Exception as e:
                    print("The number of new maximum number is not valid")
            case "6":
                new_start_date = input("Enter new start date: ")
                self.updateEventInfo(event_id=self.event_id, type_info="start_date", new_info=new_start_date)
                print("Update start date successful")
            case "7":
                new_end_date = input("Enter new end date: ")
                self.updateEventInfo(event_id=self.event_id, type_info="end_date", new_info=new_end_date)
                print("Update end_date successful")
            case "8":
                new_address = input("Enter new address: ")
                self.updateEventInfo(event_id=self.event_id, type_info="address", new_info=new_address)
                print("Update address successful")
            case "9":
                self.menu = event_status_menu
            case "10":
                self.menu = default_menu
            case _:
                print("Invalid option. Please choose a valid number.")
            
    
    def viewAllEventsMenu(self, option: str) -> None:
        match option:
            case "1":
                event_id = input("Enter event id: ")
                if not self.isEventIdExist(event_id=event_id):
                    print("Event does not exit")
                    return
                self.showEventDetails(event_id=event_id)
            case "2":
                self.menu = default_menu
            case _:
                print("Invalid option. Please choose a valid number.")
                
    def eventStatusMenu(self, option: str) -> None:
        match option:
            case "1":
                self.updateEventInfo(event_id=self.event_id, type_info="status", new_info=event_status_menu[int(option)-1])
                print("Update status successful")
                self.menu = update_event_menu
            case "2":
                self.updateEventInfo(event_id=self.event_id, type_info="status", new_info=event_status_menu[int(option)-1])
                print("Update status successful")
                self.menu = update_event_menu
            case "3":
                self.updateEventInfo(event_id=self.event_id, type_info="status", new_info=event_status_menu[int(option)-1])
                print("Update status successful")
                self.menu = update_event_menu
            case "4":
                self.menu = update_event_menu
            case _:
                 print("Invalid option. Please choose a valid number.")
                 
    def manageUsersMenu(self, option: str) -> None:
        if option in list(map(str, list(range(2, 4)))) and self.user_id == None:
            self.user_id = input("Enter event id: ")
            if not self.isUserIdExist(user_id=self.user_id):
                print("UserID does not exist")
                return
        match option:
            case "1":
                self.showAllUsers()
            case "2":
                self.menu = change_info_users_menu
            case "3":
                self.deleteUserIdFromAllEvents(user_id=self.user_id)
                self.deleteUser(user_id=self.user_id)
                print(f"Delete user successful")
            case "4":
                confirm = input("Are you sure to delete all users [y/n]: ")
                if confirm == "y":
                    self.deleteAllUsersExceptAdmin()
                    self.resetAllUsersInEvent()
                    print("Delete all users successful")
                elif confirm != "n":
                    print("Invalid option. Please choose a valid option.")
            case "5":
                self.menu = default_menu
            case _:
                print("Invalid option. Please choose a valid number.")
    
    def changeInfoUsersMenu(self, option: str) -> None:
        match option:
            case "1":
                new_name = input("Enter new name: ")
                self.updateUserInfo(user_id=self.user_id, type_info="name", new_info=new_name)
                print("Update name successful")
            case "2":
                new_user_name = input("Enter new username: ")
                if not self.isUserNameExist(username=new_user_name):
                    self.updateUserInfo(user_id=self.user_id, type_info="username", new_info=new_user_name)
                    print("Update username successful")
                    return
                print("Username existed")
            case "3":
                new_password = input("Enter new password: ")
                self.updateUserInfo(user_id=self.user_id, type_info="password", new_info=new_password)
                print("Update password successful")
            case "4":
                new_email = input("Enter new email: ")
                if not self.isEmailExist(email=new_email):
                    self.updateUserInfo(user_id=self.user_id, type_info="email_address", new_info=new_email)
                    print("Update email address successful")
                    return
                print("Email address existed")
            case "5":
                new_phone_number = input("Enter new phone number: ")
                if not self.isPhoneNumberExist(phone_number=new_phone_number):
                    self.updateUserInfo(user_id=self.user_id, type_info="phone_number", new_info=new_phone_number)
                    print("Update phone number successful")
                    return
                print("Phone number address existed")
            case "6":
                self.menu = change_gender_menu
            case "7":
                self.menu = change_role_menu
            case "8":
                self.menu = manage_users_menu
            case _:
                print("Invalid option. Please choose a valid number.")
    
    def changeRoleMenu(self, option: str) -> None:
        match option:
            case "1":
                self.deleteUserIdFromAllEvents(user_id=self.user_id)
                self.updateUserInfo(user_id=self.user_id, type_info="role", new_info=self.userRole[0])
                print(f"Change role to {self.userRole[0]} successful")
            case "2":
                self.deleteUserIdFromAllEvents(user_id=self.user_id)
                self.updateUserInfo(user_id=self.user_id, type_info="role", new_info=self.userRole[1])
                print(f"Change role to {self.userRole[1]} successful")
            case "3":
                self.menu = change_info_users_menu  
            case _:
                print("Invalid option. Please choose a valid number.")
    
    def genderMenu(self, option: str) -> None:
        match option:
            case "1":
                self.updateUserInfo(user_id=self.user_id, type_info="gender", new_info="Male")
                print("Change gender to Male successful")
            case "2":
                self.updateUserInfo(user_id=self.user_id, type_info="gender", new_info="Female")
                print("Change gender to Female successful")
            case "3":
                self.updateUserInfo(user_id=self.user_id, type_info="gender", new_info="Unknow")
                print("Change gender to Unknow successful")
            case "4":
                self.menu = change_info_users_menu
            case _:
                print("Invalid option. Please choose a valid number.")
            