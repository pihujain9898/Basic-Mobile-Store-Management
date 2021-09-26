#importing statements
import mysql.connector as mc
import pandas as pd
pd.set_option('display.max_columns',50)         #For too many columns
pd.set_option('expand_frame_repr',False)        #For columns in singel row
import subprocess as s
import time as t
from fpdf import FPDF
import webbrowser

#Fuctions
#Function 1(Viewing mobile phones stock)
def mobile_stock():
    cursor.execute("select * from stock")
    stock_data = cursor.fetchall()
    stock = pd.DataFrame(stock_data,columns = ['Item_ID','BRAND_NAME','MODEL_NAME','RAM','ROM','CAMERA','BATTERY','COLOUR','ACCESSORIES','PRICE','AVILABELITY'])
    print("Mobile phones and there details in stock :-\n")
    print(stock)    

#Function 2(Viewing customers and there details)
def customer_details():
    cursor.execute("select * from customer")
    customer_data = cursor.fetchall()
    customer = pd.DataFrame(customer_data,columns = ['SNo','Customer_Name','Item_ID','Mobile_No','Email','Date','Amount'])
    print("Customers and there details :-\n")
    print(customer)
    
#Function 3(To add new mobiles in stock)
def new_mobile():
    cursor.execute("select * from stock")
    stock_data = cursor.fetchall()
    Item_ID = len(stock_data)+1
    MODEL_NAME = input("Enter mobile model name: ")
    BRAND_NAME = input("Enter mobile brand name: ")
    RAM = input("Enter mobile RAM capacity: ")
    ROM = input("Enter mobile ROM capacity: ")
    CAMERA = input("Enter mobile camera quality: ")
    BATTERY = input("Enter mobile battery capacity : ")
    COLOUR = input("Enter mobile colur: ")
    ACCESSORIES = input("Enter the accesories: ")
    PRICE = int(input("Enter cost price of mobile: "))
    AVILABILITY = 'Yes'
    string1 = "insert into stock values({},'{}','{}','{}','{}','{}','{}','{}','{}',{},'{}')".format(Item_ID,MODEL_NAME,BRAND_NAME,RAM,ROM,CAMERA,BATTERY,COLOUR,ACCESSORIES,PRICE,AVILABILITY)
    cursor.execute(string1)
    obj.commit()

#Function 4(To sell mobile phones from stock)
def transaction():
    print("1. Select mobile directly through item ID\n2. Search mobile though features")
    print("3. Search mobile by price\n")
    choice2 = int(input("Enter your choice: "))
    if choice2 == 1:
        s.call('cls',shell=True)
        cursor.execute("select * from customer")
        customer_data = cursor.fetchall()
        SNo = len(customer_data)+1
        Customer_Name = input("Enter customer name: ")
        Item_ID =  int(input("Enter choosed item id: "))  
        cursor.execute("update stock set AVILABILITY = 'No' where Item_ID = {} and AVILABILITY = 'Yes';".format(Item_ID))
        obj.commit()
        cursor.execute("select * from stock where Item_ID = {}".format(Item_ID))
        bill_data = cursor.fetchall()
        Mobile_No = input("Enter customer mobile number: ")  
        Email = input("Enter customer email: ")
        current_time = t.localtime()
        Date = t.strftime("20%y-%m-%d",current_time)
        Amount = int(input("Enter selling price of phone: "))
        cursor.execute("insert into customer values({},'{}',{},'{}','{}','{}',{});".format(SNo,Customer_Name,Item_ID,Mobile_No,Email,Date,Amount))
        obj.commit()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(0,25,"MOBILE STORE CUSTOMER TRANSACTION BILL", ln=1, align="C")
        pdf.cell(0,0,"Name : "+Customer_Name,ln=1,align="L") 
        pdf.cell(0,0,"Date : "+Date,ln=1,align="R")
        pdf.cell(0,4,"           ",ln=1,align="C")
        pdf.cell(0,4,"-----------------------------------------------------------------------------------------------",ln=1,align="L")
        pdf.cell(0,6,"    MODEL NAME                       COLOUR                              COST ",ln=1,align="L")
        pdf.cell(0,6,"-----------------------------------------------------------------------------------------------",0,1,align="L")
        L=[]
        for i in bill_data:
               L.append(i)
               pdf.cell(6,8," ",0,0, align="C")
               pdf.cell(62,8,str(i[1])+' '+str(i[2]),0,0, align="L")
               pdf.cell(68,8,str(i[7]),0,0, align="C")
               pdf.cell(48,8,str(Amount),0,1, align="C")
        pdf.cell(0,8,"-----------------------------------------------------------------------------------------------",ln=1,align="L")
        pdf.cell(160,20,"GRAND TOTAL IS Rs "+ str(Amount),ln=1,align="L")
        pdf_name="Customer_Bill.pdf"
        pdf.output(pdf_name)
        webbrowser.open(pdf_name)           
    elif choice2 == 2:
        BRAND_NAME = '%'
        RAM = '%'
        ROM = '%'
        CAMERA = '%'
        BATTERY = '%'
        COLOUR = '%'
        choice3 = input("Features you want to sort: ")
        if 'brand name' in choice3.lower():
            BRAND_NAME = input("Enter required mobile brand name: ")
        if 'ram' in choice3.lower():
            RAM = input("Enter required mobile RAM capacity: ")
        if 'rom' in choice3.lower():
            ROM = input("Enter required mobile ROM capacity: ")
        if 'camera' in choice3.lower():
            CAMERA = input("Enter required mobile camera quality: ")
        if 'battery' in choice3.lower():
            BATTERY = input("Enter required mobile battery capacity : ")
        if 'colour' in choice3.lower():
            COLOUR = input("Enter required mobile colur: ")
        cursor.execute("select * from stock where BRAND_NAME = '{}' or RAM = '{}' or ROM = '{}' or CAMERA = '{}' or BATTERY = '{}' or COLOUR = '{}';".format(BRAND_NAME,RAM,ROM,CAMERA,BATTERY,COLOUR))
        selected_data = cursor.fetchall()
        selected_table = pd.DataFrame(selected_data,columns = ['Item_ID','BRAND_NAME','MODEL_NAME','RAM','ROM','CAMERA','BATTERY','COLOUR','ACCESSORIES','PRICE','AVILABELITY'])
        print("Mobile phones and there details in stock :-\n")
        print(selected_table)
    elif choice2 == 3:
        PRICE = int(input("Enter price under which you want to buy mobile: "))
        cursor.execute("select * from stock where price<={} ;".format(PRICE))
        selected_data = cursor.fetchall()
        selected_table = pd.DataFrame(selected_data,columns = ['Item_ID','BRAND_NAME','MODEL_NAME','RAM','ROM','CAMERA','BATTERY','COLOUR','ACCESSORIES','PRICE','AVILABELITY'])
        print("Mobile phones and there details in stock :-\n")
        print(selected_table)
    else:
        print("Check your choice.")
        
#Main Function
def mobilstore_management():
    choice1 = 1
    while choice1 != 0:
        print('\nX-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X-----X')
        print("1. Mobile phones and there details in stock\n2. Customer and there details")
        print('3. Add new mobiles in stock\n4. To sell mobile phones from stock')
        print("0. Quit\n")
        choice1 = int(input("Enter your choice: "))
        if choice1 == 1:
            s.call('cls',shell=True)
            mobile_stock()
        elif choice1 == 2:
            s.call('cls',shell=True)
            customer_details()
        elif choice1 == 3:
            s.call('cls',shell=True)
            new_mobile()
        elif choice1 == 4:
            s.call('cls',shell=True)
            transaction()            
        elif choice1 == 0:
            exit()
        else:
            print("Check your choice.")

#python-mysql connection and starting of program
try:
    mysql_password = input("Enter password of your mysql: ")
    print("Welcome To Mobile Store Management\n")
    try:
        obj = mc.connect(host = "localhost",
                      user = "root",
                      passwd = mysql_password,
                      database = "mobilstore_management")
        cursor = obj.cursor()
        mobilstore_management()
    except:
        obj = mc.connect(host = "localhost",
                            user = "root",
                            passwd = mysql_password,
                            database = "mysql")
        cursor = obj.cursor()
        cursor.execute("create database mobilstore_management;")
        cursor.execute("use mobilstore_management;")
        cursor.execute("create table stock(Item_ID int,MODEL_NAME varchar(60),BRAND_NAME varchar(40),RAM varchar(10),ROM int,CAMERA varchar(10),BATTERY varchar(10),COLOUR varchar(60),ACCESSORIES varchar(20),PRICE int,AVILABILITY varchar(5));")
        cursor.execute("insert into stock values(1,'Redmi','Y2','4','64','20','3000','Cavier Black','Charger',10000,'No');")
        cursor.execute("insert into stock values(2,'Redmi','Y2','2','64','20','3000','Cavier Black','Charger',10000,'Yes');")
        cursor.execute("insert into stock values(3,'Redmi','Y2','4','32','20','3000','Cavier Black','Charger',10000,'Yes');")
        cursor.execute("insert into stock values(4,'Redmi','Y2','2','32','20','3000','Cavier Black','Charger',10000,'Yes');")        
        cursor.execute("insert into stock values(5,'Samsung','Galaxy M30S','3','64','8','6000','Sapphire Blue','Charger',13000,'No');")
        cursor.execute("insert into stock values(6,'Samsung','Galaxy M30S','2','64','8','6000','Sapphire Blue','Charger',13000,'Yes');")
        cursor.execute("insert into stock values(7,'Samsung','Galaxy M30S','3','32','8','6000','Sapphire Blue','Charger',13000,'Yes');")
        cursor.execute("insert into stock values(8,'Samsung','Galaxy M30S','2','32','8','6000','Sapphire Blue','Charger',13000,'Yes');")        
        cursor.execute("insert into stock values(9,'Vivo','U10','4','64','12','4500','Purple','Charger',11000,'No');")
        cursor.execute("insert into stock values(10,'Vivo','U10','2','64','12','4500','Purple','Charger',11000,'Yes');")
        cursor.execute("insert into stock values(11,'Vivo','U10','4','32','12','4500','Purple','Charger',11000,'Yes');")
        cursor.execute("insert into stock values(12,'Vivo','U10','2','32','12','4500','Purple','Charger',11000,'Yes');")
        cursor.execute("create table customer(SNo int, Customer_Name varchar(40), Item_ID varchar(60), Mobile_No varchar(15), Email varchar(40),Date date,Amount int(6));")
        cursor.execute("insert into customer values(1,'Aman',1,'9929507402','aman12@gmail.com','2019-11-09',11000);")
        cursor.execute("insert into customer values(2,'Raman',5,'9929512530','raman001@gmail.com','2019-11-11',14000);")
        cursor.execute("insert into customer values(3,'Piyush',9,'6367898902','piyush11@yahoo.com','2019-11-14',12000);")
        obj.commit()
        mobilstore_management()
except:
    s.call('cls',shell=True)
    print("Something went wrong!")
    mobilstore_management()
