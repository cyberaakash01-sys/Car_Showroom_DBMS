import sys
import os
from cars_information import car_menu
from customers import customers_menu
from employees import employee_menu
from orders import orders_menu
from payments import payment_menu
from analytics import analytics_menu

# Add GUI directory to sys.path
gui_path = os.path.join(os.path.dirname(__file__), 'GUI')
if gui_path not in sys.path:
    sys.path.append(gui_path)

def clear():
    for x in range(3):
        print()

def launch_gui():
    try:
        from GUI import CarShowroomGUI
        print("Launching Car Showroom Tkinter Desktop Application...")
        app = CarShowroomGUI()
        app.mainloop()
    except Exception as e:
        print("Error launching GUI:", e)

def login():
    un=input("Enter Login Name=")
    p=input("Enter Login password=")
    if un=="ADMIN" and p=="cars":
        main_menu()
    else :
        print("Login Name or Password must be incorrect.. check and enter again")

def main_menu():
    while True:
        clear()
        print("MAIN MENU")
        print("*"*90)
        print()
        print("1.Cars Information")
        print("2.Customers information.")
        print("3.Employees Information.")
        print("4.Orders Information.")
        print("5.Payments Information")
        print("6.Analytics")
        print("7.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            car_menu()
        
        elif ch==2:
            customers_menu()

        elif ch==3:
            employee_menu()

        elif ch==4:
            orders_menu()

        elif ch==5:
            payment_menu()

        elif ch==6:
            analytics_menu()

        elif ch==7:
            break

        else :
            print("Invalid choice...")

if __name__ == "__main__":
    print("=" * 60)
    print("       WELCOME TO CAR SHOWROOM DBMS MANAGEMENT SYSTEM      ")
    print("=" * 60)
    print("1. Launch Tkinter Desktop Application (GUI)")
    print("2. Launch Command Line Interface (CLI)")
    print("3. Exit")
    try:
        mode = input("Select Mode (1 for GUI / 2 for CLI): ").strip()
        if mode == "1":
            launch_gui()
        elif mode == "2":
            login()
        else:
            print("Exiting application...")
    except KeyboardInterrupt:
        print("\nExiting...")