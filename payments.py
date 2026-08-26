from sqlalchemy.sql.coercions import TruncatedLabelImpl
import pandas as pd 
from dbms import mysql_connection
import sqlalchemy as sa

df = pd.DataFrame()

def read_payments_data():
    engine = mysql_connection()
    df = pd.read_sql("select * from payments", engine)
    print(df)

def clear():
    for x in range(3):
        print()

def payments_analysis_menu():
    engine = mysql_connection()
    df = pd.read_sql("select * from payments", engine)
    while True:
        clear()
        print("PAYMENTS ANALYSIS MENU")
        print("*" * 90)
        print()
        print("1.Show payments data.")
        print("2.Display available Data categories.")
        print("3.Display N records from Top.")
        print("4.Display N receords from Bottom.")
        print("5.Display details of specific payment by payment_id")
        print("6.Display details of specific payment by order_id")
        print("7.Add payment data.")
        print("8.Add data category.")
        print("9.Delete payment data.")
        print("10.Delete data category.")
        print("11.Update payment status.")
        print("12.Display Paid payments.")
        print("13.Display Pending payments.")
        print("14.Display EMI payments.")
        print("15.Data summary")
        print("16.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            print(df)
            wait = input("Press Enter to continue....")
        
        elif ch==2:
            print(list(df.columns))
            wait = input("Press Enter to continue....")
        
        elif ch==3:
            n=int(input("Details of how many Payments details do you want from Top?"))
            print(df.head(n))
            wait=input("Press Enter to continue....")
            
        elif ch==4:
            n=int(input("Details of how many Payments details do you want from Bottom?"))
            print(df.tail(n))
            wait=input("Press Enter to continue....")
        
        elif ch==5:
            op=int(input("Enter the Payment_Id="))
            df1=df.loc[df.Payment_Id==op,:]
            print(df1)
            wait=input("Press Enter to continue....")
        
        elif ch==6:
            oid=int(input("Enter the Order_Id="))
            df1=df.loc[df.Order_Id==oid,:]
            print(df1)
            wait=input("Press Enter to continue....")
        
        elif ch==7:
            new_data={}
            for i in df.columns:
                new_val=eval(input(f"Enter the data of {i} (enter string value in quotes,numbers in number only)="))
                new_data[i]=new_val
            df.loc[len(df)]=new_data
            print(df)
            engine=mysql_connection()
            new_row = pd.DataFrame([new_data])
            new_row.to_sql(name='payments',con=engine,index=False,if_exists='append')
            wait=input("Press Enter to continue....")
        
        elif ch==8:
            coln=input("Enter the name of column=")
            colv=eval(input("Enther default column value(enter string value in quotes,numbers in number only)="))
            df[coln]=colv
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE payments ADD COLUMN `{coln}` VARCHAR(255) DEFAULT '{colv}'"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==9:
            op=int(input("Enter the Payment_Id you want to delete="))
            n=df[df['Payment_Id']==op].index.item()
            df.drop(n,inplace=True)
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text("DELETE FROM payments WHERE Payment_Id = :op"),{"op":op})
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==10:
            print(list(df.columns))
            coln=input("Enter the name of column you want to delete=")
            del df[coln]
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE payments DROP COLUMN `{coln}`"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==11:
            op=int(input("Enter the payment id whose status u want to update="))
            ns=input("Enter the New Status=")
            df.loc[df.Payment_Id==op,"Status"]=ns
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text("UPDATE payments SET Status=:ns WHERE Payment_Id=:op"),{"ns":ns,"op":op})
                conn.commit()
            print("Updated succesfully...")
            wait=input("Press Enter to continue....")

        elif ch==12:
            print(df.loc[df.Status=="Paid"])
            wait=input("Press Enter to continue....")
        
        elif ch==13:
            print(df.loc[df.Status=="Pending"])
            wait=input("Press Enter to continue....")
        
        elif ch==14:
            print(df.loc[df.Status=="EMI"])
            wait=input("Press Enter to continue....")
        
        elif ch==15:
            print(df.describe())
            wait=input("Press Enter to continue....")
        
        elif ch==16:
            break

        else:
            print("Invalid choice")

def payment_menu():
    while True:
        clear()
        print("PAYMENTS MENU")
        print("*" * 90)
        print()
        print("1.Show payments Information.")
        print("2.Data Analysis Menu.")
        print("3.Exit")
        choice = int(input("Enter your Choice="))
        if choice == 1:
            read_payments_data()
            wait = input("Press Enter to continue....")

        elif choice == 2:
            payments_analysis_menu()
            wait = input("Press Enter to continue....")

        elif choice == 3:
            break
        
        else:
            print("Invalid choice")

