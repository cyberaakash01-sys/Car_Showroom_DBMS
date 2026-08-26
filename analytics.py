import payments
import orders
import pandas as pd 
import matplotlib.pyplot as plt 
from dbms import mysql_connection

def load_data():
    engine =mysql_connection()
    cars=pd.read_sql("select * from cars",engine)
    customers=pd.read_sql("select * from customers",engine)
    employees=pd.read_sql("select * from employees",engine)
    orders=pd.read_sql("select * from orders",engine)
    payments=pd.read_sql("select * from payments",engine)

    return cars,customers,employees,orders,payments

def clear():
    for x in range(3):
        print()

#ANALYSIS SECTION
#SHOWROOM SUMMARY
def showroom_summary():
    cars,customers,employees,orders,payments=load_data()
    clear()
    print("SHOWROOM_SUMMARY")
    print("*"*90)
    print()
    print("1.Total cars :",len(cars))
    print("2.Total customers :",len(customers))
    print("3.Total employees :",len(employees))
    print("4.Total orders :",len(orders))
    print("5.Total payments :",len(payments))
    wait=input("Press Enter to continue....")

#CAR ANALYSIS
def company_analysis():
    cars,customers,employees,orders,payments=load_data()
    clear()
    print("1.COMPANY WISE CAR COUNT")
    print("*"*90)
    print()
    cc=cars["Company"].value_counts()
    for company,count in cc.items():
        print(company,":",count)

    clear()
    print("2.COMPANY WISE AVERAGE PRICE")
    print("*"*90)
    print()
    cp=cars.groupby("Company")["Price($)"].mean()
    for company,avgprice in cp.items():
        print(company,":",avgprice)
    print()

    clear()
    print("3.MOST EXPENSIVE company.")
    print("*"*90)
    print()
    exp=cars.loc[cars["Price($)"].idxmax(),["Company","Car_Name","Price($)"]]
    print("Expensive company=",exp["Company"])
    print("Expensive car=",exp["Car_Name"])
    print("Price=",exp["Price($)"],"$")
    print()
    
    clear()
    print("4.CHEAPEST company.")
    print("*"*90)
    print()
    ch=cars.loc[cars["Price($)"].idxmin(),["Company","Car_Name","Price($)"]]
    print("Cheapest company=",ch["Company"])
    print("Cheapest car=",ch["Car_Name"])
    print("Price=",ch["Price($)"],"$")
    print()
    wait=input("Press Enter to continue....")
        
def fuel_analysis():
    cars,customers,employees,orders,payments=load_data()
    clear()
    print("1.FUEL TYPE COUNT")
    print("*"*90)
    print()
    c=cars["Fuel_Type"].value_counts()
    for fuel_type,count in c.items():
        print(fuel_type,":",count)
    print()

    clear()
    print("2.FUEL WISE AVERAGE PRICE")
    print("*"*90)
    print()
    cp=cars.groupby("Fuel_Type")["Price($)"].mean()
    for fuel_type,avgprice in cp.items():
        print(fuel_type,":",avgprice)
    print()

    clear()
    print("3.OVERALL Most Expensive CAR (FUEL CATEGORY WISE).")
    print("*"*90)
    print()
    exp=cars.loc[cars["Price($)"].idxmax(),["Fuel_Type","Car_Name","Price($)"]]
    print("Expensive Fuel Type=",exp["Fuel_Type"])
    print("Car=",exp["Car_Name"])
    print("Price=",exp["Price($)"],"$")
    print()

    clear()
    print("4.OVERALL Cheapest CAR.")
    print("*"*90)
    print()
    ch=cars.loc[cars["Price($)"].idxmin(),["Fuel_Type","Car_Name","Price($)"]]
    print("Cheapest Fuel Type=",ch["Fuel_Type"])
    print("Car=",ch["Car_Name"])
    print("Price=",ch["Price($)"],"$")
    print()

    clear()
    print("5.EXPENSIVE CAR FROM EACH FUEL TYPE CATEGORY.")
    print("*"*90)
    print()
    for fuel in cars["Fuel_Type"].unique():
        fuel_data=cars[cars["Fuel_Type"]==fuel]
        c=fuel_data.loc[fuel_data["Price($)"].idxmax(),["Company","Car_Name","Price($)"]]
        print(fuel)
        print("Expensive Company=",c["Company"])
        print("Car=",c["Car_Name"])
        print("Price=",c["Price($)"],"$")
        print()
    print()

    clear()
    print("6.CHEAPEST CAR FROM EACH FUEL TYPE CATEGORY.")
    print("*"*90)
    print()
    for fuel in cars["Fuel_Type"].unique():
        fuel_data=cars[cars["Fuel_Type"]==fuel]
        c=fuel_data.loc[fuel_data["Price($)"].idxmin(),["Company","Car_Name","Price($)"]]
        print(fuel)
        print("Cheapest Company=",c["Company"])
        print("Car=",c["Car_Name"])
        print("Price=",c["Price($)"],"$")
        print()
    print()
    wait=input("Press Enter to continue....")

def price_analysis():
    cars,customers,employees,orders,payments=load_data()
    clear()
    print("1.AVERAGE CAR PRICE")
    print("*"*90)
    print()
    avg=cars["Price($)"].mean()
    print("Average Car Price =",avg,"$")
    print()

    clear()
    print("2.MOST EXPENSIVE CAR")
    print("*"*90)
    exp=cars.loc[cars["Price($)"].idxmax(),["Company","Car_Name","Price($)"]]
    print("Company=",exp["Company"])
    print("Car=",exp["Car_Name"])
    print("Price=",exp["Price($)"],"$")
    print()

    clear()
    print("3.CHEAPEST CAR")
    print()
    ch=cars.loc[cars["Price($)"].idxmin(),["Company","Car_Name","Price($)"]]
    print("Company=",ch["Company"])
    print("Car=",ch["Car_Name"])
    print("Price=",ch["Price($)"],"$")
    print()

    clear()
    print("4.PRICE SEGMENT ANALYSIS")
    print("*"*90)
    print()
    budget=[]
    mid_range=[]
    luxury=[]
    for i,j in cars.iterrows():
        price=j["Price($)"]
        ci={"Car":j['Car_Name'],
            "Company":j['Company'],
            "Price":price}
        if price<50000:
            budget.append(ci)
        elif 50000<=price<=200000:
            mid_range.append(ci)
        else :
            luxury.append(ci)

    print(">> 1.Budget")
    for c in budget:
        print("    Car:",c["Car"])
        print("    Company:",c["Company"])
        print("    Price:",c['Price'])
        print()
    print()

    print(">> 2.Mid Range")
    for c in mid_range:
        print("    Car:",c["Car"])
        print("    Company:",c["Company"])
        print("    Price:",c['Price']) 
        print()
    print()

    print(">> 3.Luxury")
    for c in luxury:
        print("    Car:",c["Car"])
        print("    Company:",c["Company"])
        print("    Price:",c['Price'])
        print()
    print()

    clear()
    print("5.COMPANY WISE HIGHEST PRICED CAR")
    print("*"*90)
    print()
    for company in cars["Company"].unique():
        company_data=cars[cars["Company"]==company]
        c=company_data.loc[company_data["Price($)"].idxmax(),["Company","Car_Name","Price($)"]]
        print(company)
        print("Highest Priced Car=",c["Car_Name"])
        print("Price=",c["Price($)"],"$")
        print()
    print()

    clear()
    print("6.TOP 5 MOST EXPENSIVE CAR")
    print("*"*90)
    print()
    sorted_cars=cars.sort_values(by="Price($)",ascending=False)
    for i,j in sorted_cars.head(5).iterrows():
        print("Company:",j["Company"])
        print("Car:",j["Car_Name"])
        print("Price:",j["Price($)"],"$")
        print()
    print()
    wait=input("Press Enter to continue....")

def car_analysis_menu():
    while True:
        clear()
        print("CAR ANALYSIS MENU")
        print("*"*90)
        print()
        print("1.Company Analysis.")
        print("2.Fuel Analysis.")
        print("3.Price Analysis.")
        print("4.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            company_analysis()
        elif ch==2:
            fuel_analysis()
        elif ch==3:
            price_analysis()
        elif ch==4:
            break
        else:
            print("Invalid choice.")

#Sales ANALYSIS
def total_sales():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.TOATL SALES COUNT")
    print("*"*90)
    print()
    print("Total Sales Count=", len(orders))
    print()

    clear()
    print("TOTAL REVENUE GENERATED")
    print("*"*90)
    print()
    print("Total Revenue=", payments["Amount"].sum())
    print()

    clear()
    print("3.AVERAGE SALES VALUE")
    print("*"*90)
    print()
    print("Average Sales Value=", payments["Amount"].mean())
    print()

    clear()
    print("4.HIGHEST SALES VALUE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    highest=sales.loc[sales["Amount"].idxmax(),["Company","Car_Name","Amount"]]
    print("Highest sales >>>")
    print("Company=",highest["Company"])
    print("Car=",highest["Car_Name"])
    print("Amount=",highest["Amount"])
    print()

    clear()
    print("5.LOWEST SALES VALUE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    lowest=sales.loc[sales["Amount"].idxmin(),["Company","Car_Name","Amount"]]
    print("Lowest sales >>>")
    print("Company=",lowest["Company"])
    print("Car=",lowest["Car_Name"])
    print("Amount=",lowest["Amount"])
    print()

    clear()
    print("6.COMPANY WISE TOTAL SALES COUNT")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    cs=sales["Company"].value_counts()
    for company, count in cs.items():
        print(company, ":", count)
    print()
    wait=input("Press Enter to continue....")

def top_selling_cars():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.CAR WISE SALES COUNT")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    cs=sales["Car_Name"].value_counts()
    for company, count in cs.items():
        print(company, ":", count)
    print()

    clear()
    print("2.TOP 5 SELLING CARS")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    top5=sales[["Car_Name","Company"]].value_counts().head(5)
    for (car, company), count in top5.items():
        print("Car :", car)
        print("Company :", company)
        print("Sold :", count)
        print()
    print()

    clear()
    print("3.COMPANY WISE CARS SALES")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    cs=sales["Company"].value_counts()
    for company, count in cs.items():
        print(company, ":", count)
    print()

    clear()
    print("4.BEST SELLING COMPANY")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    company_sales = sales["Company"].value_counts()
    best_company = company_sales.idxmax()
    best_company_sales = company_sales.max()
    print("Best Selling Company :", best_company)
    print("Sales Count :", best_company_sales)
    print()

    clear()
    print("5.BEST SELLING CAR's REVENUE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(cars,on="Car_Id")
    car_sales=sales["Car_Name"].value_counts()
    best_car=car_sales.idxmax()
    sold_count=car_sales.max()
    best_car_data = sales[sales["Car_Name"] == best_car]
    revenue = best_car_data["Amount"].sum()
    company = best_car_data.iloc[0]["Company"]
    print("Best Selling Car =", best_car)
    print("Company =", company)
    print("Total Sold =", sold_count)
    print("Revenue Generated =", revenue, "$")
    print()
    wait=input("Press Enter to continue....")

def employee_sales():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.EMPLOYEE SALES COUNT")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(employees,on="Employee_Id")
    sales_count=sales["Employee_Name"].value_counts()
    for name,count in sales_count.items():
        print("Employee Name:",name)
        print("Sales Count:",count)
        print()

    clear()
    print("2.EMPLOYEE WISE REVENUE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(employees,on="Employee_Id")
    revenue=sales.groupby("Employee_Name")["Amount"].sum()
    for name,amount in revenue.items():
        print("Employee Name:",name)
        print("Revenue:",amount,"$")
        print()
    print()

    clear()
    print("3.TOP PERFORMING EMPLOYEE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(employees,on="Employee_Id")
    revenue=sales.groupby("Employee_Name")["Amount"].sum()
    best=revenue.idxmax()
    max_revenue=revenue.max()
    print("Employee Name=",best)
    print("Revenue Generated=",max_revenue,"$")
    print()

    clear()
    print("4.EMPLOYEE WISE CAR SALES")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(employees,on="Employee_Id")
    sales=sales.merge(cars,on="Car_Id")
    for employee in sales["Employee_Name"].unique():
        print(employee)
        print("-"*50)
        emp_data = sales[sales["Employee_Name"]==employee]
        car_count = emp_data["Car_Name"].value_counts()
        for car,count in car_count.items():
            print(car,":",count)
        print()
    print()

    clear()
    print("5.EMPLOYEE PERFORMANCE REPORT")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_ID")
    sales=sales.merge(employees,on="Employee_Id")
    sales=sales.merge(cars,on="Car_Id")
    group=sales.groupby("Employee_Name")
    c=group.size()
    revenue=group["Amount"].sum()
    avg=group["Amount"].mean()
    for name,count in c.items():
        print("Employee Name :",name)
        print("Total Sales :",count)
        print("Total Revenue :",revenue[name],"$")
        print("Average Sale :",avg[name],"$")
        print()
    print()
    wait=input("Press Enter to continue...")

def sales_analysis():
    while True:
        clear()
        print("SALES ANALYSIS MENU")
        print("*"*90)
        print()
        print("1.Total Sales")
        print("2.Top Selling Cars")
        print("3.Employee sales")
        print("4.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            total_sales()
        elif ch==2:
            top_selling_cars()
        elif ch==3:
            employee_sales()
        elif ch==4:
            break
        else:
            print("Invalid choice...")

#PAYMENT ANALYSIS
def revenue_analysis():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.TOTAL REVENUE GENERATED")
    print("*"*90)
    print()
    tr=payments["Amount"].sum()
    print("Total Revenue = ",tr,"$")
    print()

    clear()
    print("2.AVERAGE PAYMENT VALUE")
    print("*"*90)
    print()
    ap=payments["Amount"].mean()
    print("Average Payment =",ap,"$")
    print()

    clear()
    print("3.MAXIMUM PAYMENT RECEIVED")
    print("*"*90)
    print()
    max_payment=payments.loc[payments["Amount"].idxmax()]
    print("Order ID=",max_payment["Order_Id"])
    print("Amount=",max_payment["Amount"],"$")
    print("Mode of Payment=",max_payment["Payment_Mode"])
    print()

    clear()
    print("4.PAYMENT MODE COUNT")
    print("*"*90)
    print()
    pm=payments["Payment_Mode"].value_counts()
    for mode,count in pm.items():
        print(mode,":",count)
    print()
    
    clear()
    print("5.PAYMENT MODE REVENUE")
    print("*"*90)
    print()
    pm=payments.groupby("Payment_Mode")["Amount"].sum()
    for mode,amount in pm.items():
        print(mode,":",amount,"$")
    print()
    wait=input("Press Enter to continue...")

def paid_payments():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.TOTAL PAID TRANSACTIONS")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    tp=len(paid)
    print("Total Paid Transaction=",tp)
    print()

    clear()
    print("2.TOTAL PAID REVENUE")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    paid_revenue=paid["Amount"].sum()
    print("Total Paid Revenue = ",paid_revenue,"$")
    print()

    clear()
    print("3.AVERAGE PAID REVENUE")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    avg_paid_revenue=paid["Amount"].mean()
    print("Average Paid Revenue = ",avg_paid_revenue,"$")
    print()

    clear()
    print("4.PAID PAYMENT MODE")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    mode=paid["Payment_Mode"].value_counts()
    for m,count in mode.items():
        print(m,":",count)
    print()

    clear()
    print("5.TOTAL PAID REVENUE")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    highest_paid=paid.loc[paid["Amount"].idxmax()]
    print("Order ID =",highest_paid["Order_ID"])
    print("Amount =",highest_paid["Amount"],"$")
    print("Mode =",highest_paid["Payment_Mode"])
    print()

    clear()
    print("6.PAID REVENUE BY PAYMENT MODE")
    print("*"*90)
    print()
    paid=payments[payments["status"]=="Paid"]
    pr=paid.groupby("Payment_Mode")["Amount"].sum()
    for mode,amount in pr.items():
        print(mode,":",amount,"$")
    print()
    wait=input("Press Enter to continue...")

def pending_payments():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.TOTAL PENDING TRANSACTIONS")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    tp=len(pending)
    print("Total Pending Transaction=",tp)
    print()

    clear()
    print("2.TOTAL PENDING REVENUE")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    pending_revenue=pending["Amount"].sum()
    print("Total Pending Revenue = ",pending_revenue,"$")
    print()

    clear()
    print("3.AVERAGE PENDING REVENUE")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    avg_pending_revenue=pending["Amount"].mean()
    print("Average Pending Revenue = ",avg_pending_revenue,"$")
    print()

    clear()
    print("4.PENDING PAYMENT MODE")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    mode=pending["Payment_Mode"].value_counts()
    for m,count in mode.items():
        print(m,":",count)
    print()

    clear()
    print("5.HIGHEST PENDING REVENUE")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    if not pending.empty:
        pending_revenue=pending.loc[pending["Amount"].idxmax()]
        print("Order ID =",pending_revenue["Order_ID"])
        print("Amount =",pending_revenue["Amount"],"$")
        print("Mode =",pending_revenue["Payment_Mode"])
    else:
        print("No pending payments found.")
    print()

    clear()
    print("6.PENDING REVENUE PAYMENT MODE WISE")
    print("*"*90)
    print()
    pending=payments[payments["status"]=="Pending"]
    pr=pending.groupby("Payment_Mode")["Amount"].sum()
    for mode,amount in pr.items():
        print(mode,":",amount,"$")
    print()
    wait=input("Press Enter to continue...")

def payment_analysis():
    while True:
        clear()
        print("PAYMENT ANALYSIS MENU")
        print("*"*90)
        print()
        print("1.REVENUE ANALYSIS")
        print("2.PAID PAYMENT")
        print("3.PENDING PAYMENT")
        print("4.EXIT")
        ch=int(input("Enter your choice="))
        if ch==1:
            revenue_analysis()
        elif ch==2:
            paid_payments()
        elif ch==3:
            pending_payments()
        elif ch==4:
            break
        else:
            print("Invalid choice...")

#Customer Analysis
def customer_analysis():
    cars, customers, employees, orders, payments = load_data()
    clear()
    print("1.TOTAL CUSTOMERS SUMMARY")
    print("*"*90)
    print()
    tc=len(customers)
    print("Total Customers =",tc)
    print()

    clear()
    print("2.CUSTOMER WISE PURCHASE COUNT")
    print("*"*90)
    print()
    sales=orders.merge(customers,on="Customer_Id")
    sales=sales.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    cc=sales["Customer_Name"].value_counts()
    for cn,c in cc.items():
        print(cn,":",c)
    print()

    clear()
    print("3.CUSTOMER WISE REVENUE")
    print("*"*90)
    print()
    sales=orders.merge(customers,on="Customer_Id")
    sales=sales.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    cr=sales.groupby("Customer_Name")["Amount"].sum()
    for cn,amount in cr.items():
        print("Customer Name=",cn)
        print("Amount=",amount,"$")
    print()

    clear()
    print("4.TOP CUSTOMERS")
    print("*"*90)
    print()
    sales=orders.merge(customers,on="Customer_Id")
    sales=sales.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    cr=sales.groupby("Customer_Name")["Amount"].sum()
    tc=cr.loc[cr["Amount"].idxmax()]
    print("Customer Name=",tc["Customer_Name"])
    print("Amount=",tc["Amount"],"$")
    print()

    clear()
    print("5.CUSTOMER PURCHASE HISTORY")
    print("*"*90)
    print()
    sales=orders.merge(customers,on="Customer_Id")
    sales=sales.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    for customer in sales["Customer_name"].unique():
        data = sales[sales["Customer_name"] == customer]
        print(customer)
        print("-"*50)
        for i,j in data.iterrows():
            print("Car :",j["Car_Name"])
            print("Company :",j["Company"])
            print("Price :",j["Price($)"],"$")
        print()
    print()

    clear()
    print("6.CUSTOMERS PURCHASE BEHAVIOUR")
    print("*"*90)
    print()
    sales=orders.merge(customers,on="Customer_Id")
    sales=sales.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    pb=sales.groupby("Customer_Name")["Payment_Mode"].first()
    for name,mode in pb.items():
        print("Customer Name=",name)
        print("Payment Mode=",mode)
        print()
    print()
    wait=input("Press Enter to continue...")

#Employee Analysis
def employee_analysis():
    cars,customers,employees,orders,payments = load_data()
    clear()
    print("1.EMPLOYEE SUMMARY")
    print("*"*90)
    print()
    te=len(employees)
    tr=len(employees["Role"].unique())
    print("Total Employees=",te)
    print("Total Roles=",tr)
    print()

    clear()
    print("2.ROLE WISE EMPLOYEE COUNT")
    print("*"*90)
    print()
    rc=employees["Role"].value_counts()
    for role,count in rc.items():
        print(role,":",count)
    print()

    clear()
    print("3.MOST EXPERIENCED EMPLOYEE")
    print("*"*90)
    print()
    employees["Experienced_Year"]=(employees["Experience"].str.replace("yrs","").astype(int))
    me=employees.loc[employees["Experienced_Year"].idxmax()]
    print("Employee Name:",me["Employee_Name"])
    print("Role:",me["Role"])
    print("Experience:",me["Experience"])
    print()

    clear()
    print("4.EMPLOYEE's SALARY ANALYSIS")
    print("*"*90)
    print()
    print(">> 1.HIGHEST SALARY EMPLOYEE:")
    max_salary=employees.loc[employees["Salary"].idxmax()]
    print("    Employee Name:",max_salary["Employee_Name"])
    print("    Salary:",max_salary["Salary"])
    print("    Role:",max_salary["Role"])
    print()
    print(">> 2.AVERAGE SALARY:")
    avg_salary=employees["Salary"].mean()
    print("    Average Salary=",avg_salary)
    print()
    print(">> 3.LOWEST SALARY EMPLOYEE:")
    min_salary=employees.loc[employees["Salary"].idxmin()]
    print("    Employee Name:",min_salary["Employee_Name"])
    print("    Salary:",min_salary["Salary"])
    print("    Role:",min_salary["Role"])
    print()

    clear()
    print("5.EMPLOYEE SALES CONTRIBUTION")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(employees,on="Employee_Id")
    revenue=sales.groupby("Employee_Name")["Amount"].sum()
    for i,j in revenue.items():
        print(i,":",j)
    print()

    clear()
    print("6.TOP PERFORMING EMPLOYEE")
    print("*"*90)
    print()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(employees,on="Employee_Id")
    revenue=sales.groupby("Employee_Name")["Amount"].sum()
    top=revenue.idxmax()
    top_employee=employees[employees["Employee_Name"]==top]
    print("Employee Name=",top_employee.iloc[0]["Employee_Name"])
    print("Role=",top_employee.iloc[0]["Role"])
    print("Experience=",top_employee.iloc[0]["Experience"])
    print("Amount=",revenue[top],"$")
    print()
    wait=input("Press Enter to continue...")

def analysis_menu():
    while True:
        clear()
        print("ANALYSIS MENU")
        print("*"*90)
        print()
        print("1.Showroom Summary")
        print("2.Car Analysis")
        print("3.Sales Analysis")
        print("4.Payment Analysis")
        print("5.Customer Analysis")
        print("6.Employee Analysis")
        print("7.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            showroom_summary()

        elif ch==2:
            car_analysis_menu()

        elif ch==3:
            sales_analysis()

        elif ch==4:
            payment_analysis()

        elif ch==5:
            customer_analysis()

        elif ch==6:
            employee_analysis()

        elif ch==7:
            break

        else:
            print("Invalid choice...")

#VISUALIZATION SECTION
#BRAND VISUALIZATION
def company_car_count_graph():
    cars,customers,employees,orders,payments = load_data()
    x=cars['Company'].value_counts()
    y=cars['Company'].value_counts().index
    plt.bar(y,x)
    plt.title("COMPANY WISE CAR COUNT")
    plt.xlabel("Company>>>")
    plt.ylabel("Count>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def company_price_graph():
    cars,customers,employees,orders,payments = load_data()
    avg_price=cars.groupby("Company")["Price($)"].mean()
    x=avg_price.index
    y=avg_price.values
    plt.bar(x,y)
    plt.title("COMPANY WISE AVERAGE PRICE OF CARS")
    plt.xlabel("Company>>>")
    plt.ylabel("Price($)>>>")
    plt.xticks(rotation=45)
    plt.show()
    wait=input("Press Enter to continue...")

def brand_visualization():
    while True:
        clear()
        print("BRAND VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Company Car Count Graph")
        print("2.Company Price Graph")
        print("3.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            company_car_count_graph()

        elif ch==2:
            company_price_graph()

        elif ch==3:
            break

        else:
            print("Invalid choice...")

#FUEL VISUALIZATION
def fuel_distribution_graph():
    cars,customers,employees,orders,payments = load_data()
    x=cars['Fuel_Type'].value_counts()
    y=cars['Fuel_Type'].value_counts().index
    plt.pie(x,labels=y,autopct="%1.1f%%")
    plt.title("FUEL WISE DISTRIBUTION")
    plt.show()
    wait=input("Press Enter to continue...")

def fuel_wise_avg_price():
    cars,customers,employees,orders,payments = load_data()
    x=cars['Fuel_Type'].value_counts().index
    y=cars.groupby("Fuel_Type")["Price($)"].mean()
    plt.bar(x,y)
    plt.title("FUEL WISE AVERAGE PRICE OF CARS")
    plt.xlabel("Fuel Type>>>")
    plt.ylabel("Price($)>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def fuel_visualization():
    while True:
        clear()
        print("FUEL VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Fuel Distribution Graph")
        print("2.Fuel Wise Average Price")
        print("3.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            fuel_distribution_graph()

        elif ch==2:
            fuel_wise_avg_price()

        elif ch==3:
            break

        else:
            print("Invalid choice...")

#SALES VISUALIZATION
def monthly_sales_graph():
    cars,customers,employees,orders,payments = load_data()
    orders["Month"]=pd.to_datetime(orders["Order_Date"]).dt.month
    monthly_sales=orders.groupby("Month")["Quantity"].sum()
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    x=months[:len(monthly_sales)]
    y=monthly_sales.values
    plt.bar(x,y)
    plt.title("MONTHLY SALES TREND")
    plt.xlabel("Month>>>")
    plt.ylabel("Quantity of Cars Sold>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def top_selling_cars_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(cars,on="Car_Id")
    top=sales["Car_Name"].value_counts(0)
    plt.bar(top.index,top.values)
    plt.title("TOP SELLING CARS")
    plt.xlabel("Car Names>>>")
    plt.ylabel("Quantity Sold>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def sales_visualization():
    while True:
        clear()
        print("SALES VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Monthly Sales Graph")
        print("2.Top Selling Cars Graph")
        print("3.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            monthly_sales_graph()
        
        elif ch==2:
            top_selling_cars_graph()

        elif ch==3:
            break

        else :
            print("Invalid choice...")
 
#REVENUE VISUALIZATION
def brand_revenue_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(cars,on="Car_Id")
    revenue=sales.groupby("Company")["Amount"].sum()
    x=revenue.index
    y=revenue.values
    plt.bar(x,y)
    plt.title("COMPANY WISE REVENUE")
    plt.xlabel("Company>>>")
    plt.ylabel("Revenue($)>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def monthly_revenue_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales["Month"]=pd.to_datetime(sales["Order_Date"]).dt.month
    revenue=sales.groupby("Month")["Amount"].sum()
    months=["January","February","March","April","May","June","July","August","September","October","November","December"]
    x=months[:len(revenue)]
    y=revenue.values
    plt.bar(x,y)
    plt.title("MONTHLY REVENUE TREND")
    plt.xlabel("Month>>>")
    plt.ylabel("Revenue($)>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def status_revenue_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    revenue=sales.groupby("Status")["Amount"].sum()
    x=revenue.index
    y=revenue.values
    plt.pie(y,labels=x,autopct="%1.1f%%")
    plt.title("STATUS WISE REVENUE")
    plt.show()
    wait=input("Press Enter to continue...")

def revenue_visualization():
    while True :
        clear()
        print("REVENUE VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Brand Revenue Graph")
        print("2.Monthly Revenue Graph")
        print("3.Status Revenue Graph")
        print("4.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            brand_revenue_graph()
        
        elif ch==2:
            monthly_revenue_graph()

        elif ch==3:
            status_revenue_graph()

        elif ch==4:
            break

        else :
            print("Invalid choice...")

#PAYMENT VISUALIZATION
def payment_mode_distribution_graph():
    cars,customers,employees,orders,payments = load_data()
    x=payments["Payment_Mode"].value_counts()
    y=payments["Payment_Mode"].value_counts().index
    plt.pie(x,labels=y,autopct="%1.1f%%")
    plt.title("PAYMENT MODE DISTRIBUTION")
    plt.show()
    wait=input("Press Enter to continue...")

def payment_status_distribution_graph():
    cars,customers,employees,orders,payments = load_data()
    x=payments["Status"].value_counts()
    y=payments["Status"].value_counts().index
    plt.bar(y,x)
    plt.title("PAYMENT STATUS DISTRIBUTION")
    plt.xlabel("Status>>>")
    plt.ylabel("Count>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def payment_visualization():
    while True :
        clear()
        print("PAYMENT VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Payment Mode Distribution Graph")
        print("2.Payment Status Distribution Graph")
        print("3.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            payment_mode_distribution_graph()
        
        elif ch==2:
            payment_status_distribution_graph()

        elif ch==3:
            break

        else :
            print("Invalid choice...")

#EMPLOYEE VISUALIZATION
def employee_revenue_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(payments,left_on="Order_Id",right_on="Order_Id")
    sales=sales.merge(employees,on="Employee_Id")
    revenue=sales.groupby("Employee_Name")["Amount"].sum()
    x=revenue.index
    y=revenue.values
    plt.bar(x,y)
    plt.title("REVENUE GENERATED BY EMPLOYEES")
    plt.xlabel("Employee Name>>>")
    plt.ylabel("Revenue($)>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def employee_sales_count_graph():
    cars,customers,employees,orders,payments = load_data()
    sales=orders.merge(employees,on="Employee_Id")
    sales_count=sales.groupby("Employee_Name")["Car_Id"].count()
    x=sales_count.index
    y=sales_count.values
    plt.bar(x,y)
    plt.title("SALES COUNT BY EMPLOYEES")
    plt.xlabel("Employee Name>>>")
    plt.ylabel("Sales Count>>>")
    plt.show()
    wait=input("Press Enter to continue...")

def employee_role_distribution():
    cars,customers,employees,orders,payments = load_data()
    x=employees["Role"].value_counts()
    y=employees["Role"].value_counts().index
    plt.pie(x,labels=y,autopct="%1.1f%%")
    plt.title("EMPLOYEE ROLE DISTRIBUTION")
    plt.show()
    wait=input("Press Enter to continue...")

def employee_visualization():
    while True :
        clear()
        print("EMPLOYEE VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Employee Revenue Graph")
        print("2.Employee Sales Count Graph")
        print("3.Employee Role Distribution Graph")
        print("4.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            employee_revenue_graph()
        
        elif ch==2:
            employee_sales_count_graph()

        elif ch==3:
            employee_role_distribution()

        elif ch==4:
            break

        else :
            print("Invalid choice...")

def visualization_menu():
    while True:
        clear()
        print("VISUALIZATION MENU")
        print("*"*90)
        print()
        print("1.Brand Visualization")
        print("2.Fuel Visualization")
        print("3.Sales Visualization")
        print("4.Revenue Visualization")
        print("5.Payment Visualization")
        print("6.Employee Visualization")
        print("7.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            brand_visualization()
        
        elif ch==2:
            fuel_visualization()

        elif ch==3:
            sales_visualization()

        elif ch==4:
            revenue_visualization()

        elif ch==5:
            payment_visualization()

        elif ch==6:
            employee_visualization()

        elif ch==7:
            break

        else :
            print("Invalid choice...")

#MAIN ANALYTICS MENU
def analytics_menu():
    while True:
        clear()
        print("ANALYTICS MENU")
        print("*"*90)
        print()
        print("1.Analysis Menu")
        print("2.Visualization Menu")
        print("3.Exit")
        ch=int(input("Enter your choice="))
        if ch==1:
            analysis_menu()

        elif ch==2:
            visualization_menu()

        elif ch==3:
            break

        else :
            print("Invalid choice...")
