from Admin import Admin
from Event_Organizer import EventOrganizer
from Student import Student

def AdminRole():
    ad = Admin()
    print("\nAdmin Access")
    while True:
        print("\n1. Create Event\n2. Delete Event\n3. Update Event\n4. View All Events Details\n5. Exit")
        option = str(input("Choose the number: "))
        if option == "1":
            print("\nCreate new event")
            event_name = str(input("Enter event name: "))
            max_attendees = str(input("Enter max attendees: "))
            event_date = str(input("Enter event date: "))
            details = str(input("Enter event detail: "))
            ad.createEvents(event_name, max_attendees, event_date, details)
        elif option == "2":
            print("\nDelete event")
            event_name = str(input("Enter event name: "))
            ad.deleteEvents(event_name)
        elif option == "3":
            print("\nUpdate event\n")
            while True:
                print("\n1. Update Max Attendees Event\n2. Update Details Event\n3. Update Date Event\n4. Exit\n")
                option = str(input("Choose the number: "))
                if option == "1":
                    print("\nUpdate Max Attendees Event")
                    event_name = str(input("Enter event name: "))
                    max_attendees = str(input("Enter max attendees: "))
                    ad.updateEvents(event=event_name, act=1, max_attendes=max_attendees)
                elif option == "2":
                    print("\nUpdate Details Event")
                    event_name = str(input("Enter event name: "))
                    details = str(input("Enter event detail: "))
                    ad.updateEvents(event=event_name, act=2, detail=details)
                elif option == "3":
                    print("\nUpdate Date Event")
                    event_name = str(input("Enter event name: "))
                    event_date = str(input("Enter event date: "))
                    ad.updateEvents(event=event_name, act=3, date=event_date)
                elif option == "4":
                    break
        elif option == "4":
            ad.allEvents()
        elif option == "5":
            break
        else:
            print("Error format")
            
def EventOrganizerRole():
    eo = EventOrganizer()
    print("\nEvent Organizer Access")
    flag = True
    while flag:
        event = str(input("Enter event name: ")).lower()
        if eo.isEventValid(event):
            while True:
                print(f"\nAccess Event {event.title()}")
                print("1. Add Attendee\n2. Delete Attendee\n3. Show Event Details\n4. Exit")
                option = str(input("Choose the number: "))
                if option == "1":
                    print("\nAdd Attendee")
                    att_name = str(input("Ender attendee name: "))
                    role = str(input("Ender attendee role: "))
                    eo.addAttendees(name=att_name, role=role)
                elif option == "2":
                    print("\nDelete Attendee")
                    att_name = str(input("Ender attendee name: "))
                    eo.deleteAttendees(name=att_name)
                elif option == "3":
                    print("\nShow Event Details")
                    eo.showEventDetails()
                elif option == "4":
                    flag = False
                    break
        else:
            print("Event is not exist")
            break

def StudentVistor():
    st = Student()
    print("\nStudent/Visitor Access")
    while True:
        print("\n1. View List Events\n2. Attend Event\n3. View Attended Events\n4. Exit")
        option = str(input("Choose the number: "))
        if option == "1":
            print("View List Events")
            st.searchEvents()
        elif option == "2":
            print("Attend Event")
            event_name = str(input("Enter event name: "))
            name = str(input("Enter your name: "))
            st.attendEvent(event_name, name)
        elif option == "3":
            print("View Attended Events")
            name = str(input("Enter your name: "))
            st.viewEventsAttended(name)
        elif option == "4":
            break
        
while True:
    print("\nCampus Event Management System")
    print("\n1. Admin\n2. Event Organizer\n3. Student/Visitor\n4. Exit\n")
    option = str(input("Choose the number: "))
    if option == "1":
        AdminRole()
    elif option == "2":
        EventOrganizerRole()
    elif option == "3":
        StudentVistor()
    elif option == "4":
        break
    else:
        print("Invalid choice. Please enter a valid number from the menu.")
        

        
    