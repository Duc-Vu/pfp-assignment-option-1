default_menu = (
    "Add Attendee",
    "Remove Attendee",
    "View Events",
    "Logout"
)

view_events_menu = ("View Event Details", "Exit")
from src.utils.events.events import Events
from src.utils.users.users import Users
class EventOrganizer(Events, Users):
    def __init__(self, account_user_id):
        super().__init__()
        self.flag = True
        self.account_id = account_user_id
        self.events_organizer = self.getEventsOrganizer(user_id=self.account_id)
        self.showEventsOrganizer(user_id=self.account_id)
        self.menu = default_menu
        
    def handleMenu(self, option: str) -> None:
        menu_handlers = {
            default_menu: self.defaultMenu,
            view_events_menu: self.viewEventsMenu
        }
        handler = menu_handlers.get(self.menu)
        if handler:
            handler(option=option)
            
    def defaultMenu(self, option: str) -> None:
        match option:
            case "1":
                event_id = input("Enter event id: ")
                if not self.isEventIdExist(event_id=event_id):
                    print("EventID does not exist")
                    return
                if event_id not in self.getEventsOrganizer(user_id=self.account_id):
                    print("You not have access to add user in this event")
                    return
                user_id = input("Enter user id: ")
                if self.isUserIdExist(user_id=user_id):
                    if not self.isUserStaff(user_id=user_id):
                        if not self.isUserAttendedEvent(user_id=user_id, event_id=event_id):
                            if not self.isEventOverAttendees(event_id=event_id):
                                self.addUserToEvents(user_id=user_id, event_id=event_id)
                                print("Add user to event successful")
                                return
                            print("Event was over capacity")
                            return
                        print("User is alrealy attend this event")
                        return
                    print("Cannot add staff to any events")
                    return
                print("UserID does not exist")
            case "2":
                event_id = input("Enter event id: ")
                if not self.isEventIdExist(event_id=event_id):
                    print("EventID does not exist")
                    return
                if event_id not in self.getEventsOrganizer(user_id=self.account_id):
                    print("You not have access to detlete user in this event")
                    return
                user_id = input("Enter user id: ")
                if self.isUserIdExist(user_id=user_id):
                    if self.isUserAttendedEvent(user_id=user_id, event_id=event_id):
                        self.deleteUserFromEvents(user_id=user_id, event_id=event_id)
                        print("Delete user from event successful")
                        return
                    print("User is not attend this event")
                    return
                print("User does not exist")
            case "3":
                self.showEventsOrganizer(user_id=self.account_id)
                self.menu = view_events_menu
            case "4":
                self.flag = False
            case _:
                print("Invalid option. Please choose a valid number.")
            
    def viewEventsMenu(self, option: str) -> None:
        match option:
            case "1":
                event_id = input("Enter event id: ")
                if self.isEventIdExist(event_id=event_id):
                    if event_id in self.getEventsOrganizer(user_id=self.account_id):
                        self.showEventDetails(event_id=event_id)
                        return
                    print("You not have access to view this event details")
                print("EventID does not exist")
            case "2":
                self.menu = default_menu
            case _:
                print("Invalid option. Please choose a valid number.")
                