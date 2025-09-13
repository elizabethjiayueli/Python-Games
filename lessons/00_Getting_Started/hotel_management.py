"""
Hotel Management System
1. Functions needed:
    1a. Be able to check in or check out
    1b. recieve price
    1c. choose room
    1d. how many guests
5. Should use lists, tuples, dictionaries
6. All functionality in functions
"""
from tkinter import messagebox, simpledialog,Tk
window = Tk()
window.withdraw()
db = {}

def in_or_out(db):
    
    rooms = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    while True:
        print(db)
        ask = simpledialog.askstring("HOTEL MANAGEMENT", "What is your name?")
        check = simpledialog.askstring("HOTEL MANAGEMENT", "Would you like to check in or check out?")
        if check == "check in" or check == "in":
            selected_rooms = []
            peeps_num = simpledialog.askinteger("HOTEL MANAGEMENT", "How many people are you traveling with?")
            if int(peeps_num) <= 6:
                selected_rooms.append(room_func(rooms))
                days = simpledialog.askinteger("HOTEL MANAGEMENT", "How many days are you going to stay?")
                price = 200*days + peeps_num
            elif int(peeps_num) >= 7:
                num_rooms = (simpledialog.askinteger("HOTEL MANAGEMENT", "Please choose 2 or more rooms. Enter the number of rooms you would like."))
                for i in range(num_rooms):
                    selected_rooms.append(room_func(rooms))
                days = simpledialog.askinteger("HOTEL MANAGEMENT", "How many days are you going to stay?")
                price = 200*days + peeps_num * num_rooms
            db[ask] = selected_rooms
            messagebox.showinfo("HOTEL MANAGEMENT",f"Your price is $ {price}")
        elif check == "check out" or check == "out":
            if ask in db:
                db.pop(ask) 
                messagebox.showinfo("HOTEL MANAGEMENT", "I hope you enjoyed your stay!")
            else:
                messagebox.showerror("error")
        else:
            messagebox.showwarning("invalid response", "please try again")
        messagebox.showinfo("HOTEL MANAGEMENT", db)
        continue_ = simpledialog.askstring("HOTEL MANAGEMENT", "Would you like to continue checking in?")
        if continue_ == "yes":
            pass
        elif continue_ == "no":
            break
        else:
            messagebox.showwarning("invalid response", "please try again")

def room_func(rooms):
    room = simpledialog.askinteger("Which room would you like?", rooms)
    if room in rooms:
        rooms.remove(room)
    else:
        messagebox.showerror("HOTEL MANAGEMENT", "This room is not available. Please try again.")
        room = simpledialog.askinteger("Which room would you like?", rooms)
    return room
in_or_out(db)