from sqlalchemy.sql.coercions import TruncatedLabelImpl
import pandas as pd 
from dbms import mysql_connection
import sqlalchemy as sa

df = pd.DataFrame()

def read_orders_data():
    engine = mysql_connection()
    df = pd.read_sql("select * from orders", engine)
    print(df)

def clear():
    for x in range(3):
        print()

def orders_analysis_menu():
    engine = mysql_connection()
    df = pd.read_sql("select * from orders", engine)
    while True:
        clear()
        print("ORDERS ANALYSIS MENU")
        print("*" * 90)
        print()
        print("1.Show all orders data.")
        print("2.Display available data categories.")
        print("3.Display N records from Top.")
        print("4.Display N records from Bottom.")
        print("5.Show details of specific order by Order_Id.")
        print("6.Show details of specific order by Customer_Id.")
        print("7.Show details of specific order by Car_Id.")
        print("8.Show details of specific order by Employee_Id.")
        print("9.Add order data.")
        print("10.Add data category.")
        print("11.Delete order data.")
        print("12.Delete data category.")
        print("13.Update the detail of specific order.")
        print("14.Data summary.")
        print("15.Exit")
        ch = int(input("Enter your choice="))
        if ch == 1:
            print(df)
            wait = input("Press Enter to continue....")
        
        elif ch == 2:
            print(list(df.columns))
            wait = input("Press Enter to continue....")
            
        elif ch == 3:
            n = int(input("Details of how many orders do you want from Top? "))
            print(df.head(n))
            wait = input("Press Enter to continue....")
            
        elif ch == 4:
            n = int(input("Details of how many orders do you want from Bottom? "))
            print(df.tail(n))
            wait = input("Press Enter to continue....")
        
        elif ch == 5:
            oid = int(input("Enter the Order_Id="))
            df1 = df.loc[df.Order_Id == oid, :]
            print(df1)
            wait = input("Press Enter to continue....")
        
        elif ch == 6:
            cuid = int(input("Enter the Customer_Id="))
            df1 = df.loc[df.Customer_Id == cuid, :]
            print(df1)
            wait = input("Press Enter to continue....")

        elif ch == 7:
            cid = int(input("Enter the Car_Id="))
            df1 = df.loc[df.Car_Id == cid, :]
            print(df1)
            wait = input("Press Enter to continue....")

        elif ch == 8:
            eid = int(input("Enter the Employee_Id="))
            df1 = df.loc[df.Employee_Id == eid, :]
            print(df1)
            wait = input("Press Enter to continue....")

        elif ch == 9:
            new_data = {}
            for i in df.columns:
                new_val = eval(input(f"Enter the data of {i} (enter string value in quotes, numbers in number only)="))
                new_data[i] = new_val
            df.loc[len(df)] = new_data
            print(df)
            engine = mysql_connection()
            new_row = pd.DataFrame([new_data])
            new_row.to_sql(name='orders', con=engine, index=False, if_exists='append')
            wait = input("Press Enter to continue....")

        elif ch == 10:
            coln = input("Enter the name of column=")
            colv = eval(input("Enter default column value (enter string value in quotes, numbers in number only)="))
            df[coln] = colv
            print(df)
            engine = mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE orders ADD COLUMN `{coln}` VARCHAR(255) DEFAULT '{colv}'"))
                conn.commit()
            wait = input("Press Enter to continue....")

        elif ch == 11:
            oid = int(input("Enter order id="))
            n = df[df['Order_Id'] == oid].index.item()
            df.drop(n, inplace=True)
            print(df)
            engine = mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text("DELETE FROM orders WHERE Order_Id = :oid"), {"oid": oid})
                conn.commit()
            wait = input("Press Enter to continue....")

        elif ch == 12:
            print(list(df.columns))
            coln = input("Enter the name of column you want to delete=")
            del df[coln]
            print(df)
            engine = mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE orders DROP COLUMN `{coln}`"))
                conn.commit()
            wait = input("Press Enter to continue....")

        elif ch == 13:
            oid = int(input("Enter the Order_Id="))
            c = list(df.columns[1:])
            print(c)
            cn = input("Which data category do you want to update?")
            if cn in c:
                nv = eval(input("Enter the new value (enter string value in quotes, numbers in number only)="))
                df.loc[df['Order_Id'] == oid, cn] = nv
                engine = mysql_connection()
                with engine.connect() as conn:
                    conn.execute(sa.text(f"UPDATE orders SET `{cn}`=:nv WHERE Order_Id = :oid"), {"nv": nv, "oid": oid})
                    conn.commit()
                print("Updated Successfully...")
            else:
                print("Invalid column name")
            wait = input("Press Enter to continue....")

        elif ch == 14:
            print(df.describe())
            wait = input("Press Enter to continue....")

        elif ch == 15:
            break
        
        else:
            print("Invalid choice")

def orders_menu():
    while True:
        clear()
        print("ORDERS MENU")
        print("*" * 90)
        print()
        print("1.Show orders Information.")
        print("2.Data Analysis Menu.")
        print("3.Exit")
        choice = int(input("Enter your Choice="))
        if choice == 1:
            read_orders_data()
            wait = input("Press Enter to continue....")

        elif choice == 2:
            orders_analysis_menu()
            wait = input("Press Enter to continue....")

        elif choice == 3:
            break
        
        else:
            print("Invalid choice")

