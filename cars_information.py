from sqlalchemy.sql.coercions import TruncatedLabelImpl
import pandas as pd 
from dbms import mysql_connection
import sqlalchemy as sa

df=pd.DataFrame()

def read_cars_data():
    engine =mysql_connection()
    df=pd.read_sql("select * from cars",engine)
    print(df)

def clear():
    for x in range(3):
        print()

def cars_analysis_menu():
    engine=mysql_connection()
    df=pd.read_sql("select * from cars",engine)
    while True:
        clear()
        print("CARS_ANALYSIS_MENU")
        print("*"*90)
        print("1.Display record of all cars.")
        print("2.Display available data categories.")
        print("3.Display N records from Top.")
        print("4.Display N records from Bottom.")
        print("5.Show details of specific cars.")
        print("6.Show details of specific categories")
        print("7.Add details of new cars.")
        print("8.Add a data category.")
        print("9.Delete the data category.")
        print("10.Delete the specific record of car.")
        print("11.Display power of specific car.")
        print("12.Update th detail of specific car.")
        print("13.Fuel wise category.")
        print("14.Display price of specific car.")
        print("15.Data Summary.")
        print("16.Exit(back to main_menu).")
        ch=int(input("Enter your choice="))
        if ch==1:
            print(df)
            wait=input("Press Enter to continue....")
            
        elif ch==2 :
            print(list(df.columns))
            wait=input("Press Enter to continue....")
            
        elif ch==3:
            n=int(input("Details of how many cars do you want from Top?"))
            print(df.head(n))
            wait=input("Press Enter to continue....")
            
        elif ch==4:
            n=int(input("Details of how many cars do you want from Bottom?"))
            print(df.tail(n))
            wait=input("Press Enter to continue....")
            
        elif ch==5:
            cn=input("Enter the Name of Car=")
            df1=df.loc[df.Car_Name==cn,:]
            print(df1)
            wait=input("Press Enter to continue....")
            
        elif ch==6:
            print(list(df.columns))
            coln=input("Enter the Column name you want to print=")
            print(df[coln])
            wait=input("Press Enter to continue....")
            
        elif ch==7:
            cid=int(input("Enter the car id="))
            c=input("Enter the Name of Car=")
            com=input("Enter the Company of "+c+"=")
            ct=input("Enter the type of "+c+"=")
            ft=input("Enter the Fuel type of "+c+"=")
            p=int(input("Enter the price of "+c+" in $="))
            et=input("What is the Engine type of "+c+"=")
            pw=int(input("Enter the Power of "+c+"="))
            df.loc[len(df)]=[cid,c,com,ct,ft,p,et,pw]
            print(df)
            engine=mysql_connection()
            new_row=pd.DataFrame([[cid,c,com,ct,ft,p,et,pw]],columns=df.columns[:8])
            new_row.to_sql(name='cars',con=engine,index=False,if_exists='append')
            wait=input("Press Enter to continue....")
            
        elif ch==8:
            coln=input("Name of column=")
            colv=eval(input("Enter default column value="))
            df[coln]=colv
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE cars ADD COLUMN `{coln}` VARCHAR(255) DEFAULT '{colv}'"))
                conn.commit()
            wait=input("Press Enter to continue....")
            
        elif ch==9:
            print(list(df.columns))
            coln=input("Enter the Name of column you want to delete=")
            del df[coln]
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE cars drop COLUMN `{coln}`"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==10:
            nm=input("Enter the Name of Car you want to delete=")
            n=df[df['Car_Name']==nm].index.item()
            df.drop(n,inplace=True)
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"DELETE FROM cars WHERE car_Name = {nm}"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==11:
            nm=input("Enter the Name of car whose Power you want to display=")
            print(df.loc[df['Car_Name']==nm,['Car_Name',"Power(HP)"]])
            wait=input("Press Enter to continue....")

        elif ch==12:
            cid=int(input("Enter the Car_Id="))
            c=list(df.columns)
            print(c[1:])
            cn=input("Which data category you want to update?")
            nv=eval(input("Enter the new value="))
            df.loc[df['Car_Id']==cid,cn]=nv
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"UPDATE cars SET `{cn}`={nv} WHERE Car_Id = {cid}"))
                conn.commit()
            print("Updated Succesfully...")
            wait=input("Press Enter to continue....")

        elif ch==13:
            print("Available Fuel Type are Petrol and Hybrid")
            ft=input("Enter your Fuel Type from Petrol and Hybrid=")
            if ft=='Petrol':
                print(df.loc[df['Fuel_Type']==ft])
            elif ft=='Hybrid':
                print(df.loc[df['Fuel_Type']==ft])
            wait=input("Press Enter to continue....")

        elif ch==14:
            nm=input("Enter the Name of car whose Price you want to display=")
            print(df.loc[df['Car_Name']==nm,['Car_Name',"Price($)"]])
            wait=input("Press Enter to continue....")

        elif ch==15:
            print(df.describe())
            wait=input("Press Enter to continue....")
            
        elif ch==16:
            break

        else:
            print("Invalid choice.")

def car_menu():
    while True:
        clear()
        print("Car_MENU")
        print("*"*90)
        print()
        print("1.Show cars Information.")
        print("2.Data Analysis Menu.")
        print("3.Exit")
        choice=int(input("Enter your Choice="))
        if choice==1:
            read_cars_data()
            wait=input("Press Enter to continue....")

        elif choice==2:
            cars_analysis_menu()
            wait=input("Press Enter to continue....")

        elif choice==3:
            break
        
        else:
            print("Invalid choice.")
    
