from sqlalchemy.sql.coercions import TruncatedLabelImpl
import pandas as pd 
from dbms import mysql_connection
import sqlalchemy as sa

df=pd.DataFrame()

def read_employees_data():
    engine=mysql_connection()
    df=pd.read_sql("select * from employees",engine)
    print(df)

def clear():
    for x in range(3):
        print()

def employees_analysis_menu():
    engine=mysql_connection()
    df=pd.read_sql("select * from employees",engine)
    while True:
        clear()
        print("EMPLOYEES ANALYSIS MENU")
        print("*"*90)
        print()
        print("1.Show all employees data.")
        print("2.Display available data categories.")
        print("3.Display N records from Top.")
        print("4.Display N records from Bottom.")
        print("5.Show details of specific employee by employee_id.")
        print("6.Show details of specifoc employee by employee_name.")
        print("7.Add employee data.")
        print("8.Add data category.")
        print("9.Delete employee data.")
        print("10.Delete data category.")
        print("11.Update the detail of specific employee")
        print("12.Display phone number of specific employee.")
        print("13.Display detail of employee via phone number.")
        print("14.Data summary.")
        print("15.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            print(df)
            wait=input("Press enter to continue...")
        
        elif ch==2 :
            print(list(df.columns))
            wait=input("Press Enter to continue....")
            
        elif ch==3:
            n=int(input("Details of how many Employees details do you want from Top?"))
            print(df.head(n))
            wait=input("Press Enter to continue....")
            
        elif ch==4:
            n=int(input("Details of how many Employees details do you want from Bottom?"))
            print(df.tail(n))
            wait=input("Press Enter to continue....")
        
        elif ch==5:
            ci=int(input("Enter the Employee_Id="))
            df1=df.loc[df.Employee_Id==ci,:]
            print(df1)
            wait=input("Press Enter to continue....")

        elif ch==6:
            cn=input("Enter the Emloyee_Name=")
            df2=df.loc[df.Employee_Name==cn,:]
            print(df2)
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
            new_row.to_sql(name='employees',con=engine,index=False,if_exists='append')
            wait=input("Press Enter to continue....")

        elif ch==8:
            coln=input("Enter the name of column=")
            colv=eval(input("Enther default column value(enter string value in quotes,numbers in number only)="))
            df[coln]=colv
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE employees ADD COLUMN `{coln}` VARCHAR(255) DEFAULT '{colv}'"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==9:
            eid=int(input("Enter employee id="))
            n=df[df['Employee_Id']==eid].index.item()
            df.drop(n,inplace=True)
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text("DELETE FROM employees WHERE Employee_Id = :eid"),{"eid":eid})
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==10:
            print(list(df.columns))
            coln=input("Enter the name of column you want to delete=")
            del df[coln]
            print(df)
            engine=mysql_connection()
            with engine.connect() as conn:
                conn.execute(sa.text(f"ALTER TABLE employees DROP COLUMN `{coln}`"))
                conn.commit()
            wait=input("Press Enter to continue....")

        elif ch==11:
            eid=int(input("Enter the Employee_Id="))
            c=list(df.columns[1:])
            print(c)
            cn=input("Which data category you want to update?")
            if cn in c:
                nv=eval(input("Enter the new value(enter string value in quotes,numbers in number only)="))
                df.loc[df['Employee_Id']==eid,cn]=nv
                engine=mysql_connection()
                with engine.connect() as conn:
                    conn.execute(sa.text(f"UPDATE employees SET `{cn}`= :nv WHERE Employee_Id = :eid"),{"nv":nv,"eid":eid})
                    conn.commit()
                print("Updated Succesfully...")
            else :
                print("Invalid column name")
            wait=input("Press Enter to continue....")
        
        elif ch==12:
            nm=input("Enter the Name of Employee whose Phone number you want to display=")
            print(df.loc[df['Employee_Name']==nm,['Employee_Name',"Phone_Number"]])
            wait=input("Press Enter to continue....")

        elif ch==13:
            ph=input("Enter the phone number of employee whose details you want to display=")
            print(df.loc[df['Phone_Number']==ph])
            wait=input("Press Enter to continue....")

        elif ch==14:
            print(df.describe())
            wait=input("Press Enter to continue....")

        elif ch==15:
            break
        
        else:
            print("Invalid choice")

def employee_menu():
    while True:
        clear()
        print("EMPLOYEES MENU")
        print("*"*90)
        print()
        print("1.Show employee Information.")
        print("2.Data Analysis Menu.")
        print("3.Exit")
        choice=int(input("Enter your Choice="))
        if choice==1:
            read_employees_data()
            wait=input("Press Enter to continue....")

        elif choice==2:
            employees_analysis_menu()
            wait=input("Press Enter to continue....")

        elif choice==3:
            break
        
        else:
            print("Invalid choice")

