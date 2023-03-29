from tkinter import *
from tkinter import messagebox, PhotoImage, ttk
from PIL import ImageTk, Image
import datetime
import mysql.connector as con
from tkcalendar import *
import math
import random
import smtplib
import pickle
import os
import datetime
from fpdf import FPDF
import qrcode
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from pdf_mail import sendpdf
from threading import *
from tkthread import *
ROW = 1
passdata = []


def check(entry01, entry02, entry03, entry04, entry05, otp, mainframe):
    global email, name, address, age, phone
    email = entry01.get()
    name = entry02.get()
    address = entry03.get()
    age = entry04.get()
    phone = entry05.get()
    flag = 0
    cursor.execute("use railways;")
    cursor.execute("select count(*) from user;")
    count = cursor.fetchone()
    count = count[0]
    cursor.execute("select * from user")
    logindata = cursor.fetchall()
    for i in range(0, count):
        if (logindata[i][0] == email):
            flag = 1
    if email == '' or name == '' or address == '' or age == '' or phone == '':
        messagebox.showinfo('', 'Please Fill all the Fields!!')
    elif (flag == 1):
        messagebox.showinfo('', 'Email ALready Registered!!')
    else:
        otpverify(email, mainframe, otp)


def mysqldata(userentry, passentry, root):
    global mysqluser, mysqlpass
    mysqluser = userentry.get()
    mysqlpass = passentry.get()
    try:
        connection = con.connect(host='localhost', user=mysqluser, password=mysqlpass)
    except con.errors.ProgrammingError:
        messagebox.showinfo('', 'Incorrect User or Password, Please Re-Check!!')
        getmysql(root)

    mysqldata = [mysqluser, mysqlpass]
    with open('login.txt', 'wb') as f:
        pickle.dump(mysqldata, f)
    root.destroy()
    return


def getmysql(root):
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    label1 = Label(mainframe, text="Enter Your MySql Username", bg='white', font=('Arila', 10))
    label1.place(x=10, y=10)
    userentry = Entry(mainframe, font=('Arial', 10), bg='white')
    userentry.place(x=10, y=30)
    label2 = Label(mainframe, text="Enter Your MySql Password", bg='white', font=('Arila', 10))
    label2.place(x=10, y=60)
    passentry = Entry(mainframe, font=('Arial', 10), bg='white')
    passentry.place(x=10, y=80)
    root.geometry('400x300')
    submitbut = Button(mainframe, text='Submit', bd=3, bg='white',
                       command=lambda: mysqldata(userentry, passentry, root))
    submitbut.place(x=10, y=110)
    root.mainloop()
    return


def pnr():
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTYUVWXYZ"
    length = len(chars)
    PNR = ""
    for i in range(7):
        PNR += chars[math.floor(random.random() * length)]
    PNR = 'PNR' + PNR
    return PNR


def seatno():
    digits = '0123456789'
    seat = ''
    for i in range(3):
        seat += digits[math.floor(random.random() * 10)]
    return seat


def ticketno():
    digits = '0123456789ABCDEFGHIJKLMNOPQRSTUV'
    length = len(digits)
    ticket = ''
    for i in range(5):
        ticket += digits[math.floor(random.random() * length)]
    return ticket


def otpverify(email, mainframe, otp):
    try:
        otp.destroy()
        email = entry01.get()
        digits = "0123456789"
        global OTP
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        otp = OTP + " is your OTP to Register for Railways Login Application"
        msg = otp
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('railwayslogin@gmail.com', 'kijhzjdxvyuxapfi')
        s.sendmail('railwayslogin@gmail.com', email, msg)
        global entry001
        label0 = Label(mainframe, text="Enter OTP Recieved on Email")
        label0.place(x=500, y=600)
        entry001 = Entry(mainframe, show='*', bd=3)
        entry001.place(x=500, y=650)
        verify = Button(mainframe, bd=3, text="VERIFY", command=lambda: verifyotp())
        verify.place(x=500, y=680)
        resendotp = Button(mainframe, bd=3, text="Resend OTP", command=lambda: otpverify(email, mainframe, otp))
        resendotp.place(x=600, y=680)
        root.mainloop()
    except smtplib.SMTPRecipientsRefused:
        messagebox.showinfo('', "Incorret Email, Please Re-Check!!")
        register1()
    except smtplib.socket.gaierror:
        messagebox.showinfo('', "Please Check Your Internet Connection and try again!!")
        register1()


def verifyotp():
    a = entry001.get()
    if a == OTP:
        bg = ImageTk.PhotoImage(Image.open("005.jpg"))
        mainframe = Frame(root, bg='white')
        mainframe.place(x=0, y=0)
        label1 = Label(mainframe, image=bg)
        label1.pack()
        label0 = Label(mainframe, text='Create password', font=('Arial', 15))
        label0.place(x=60, y=150)
        entry0 = Entry(mainframe, show='*', bd=3)
        entry0.place(x=270, y=150)
        label01 = Label(mainframe, text='Confirm Password', font=('Arial', 15))
        label01.place(x=60, y=200)
        entry01 = Entry(root, show='*', bd=3)
        entry01.place(x=270, y=200)
        nex = Button(mainframe, text="Next->", command=lambda: next1(entry0, entry01), bd=3)
        nex.place(x=150, y=350)
        root.mainloop()
    else:
        messagebox.showinfo('', 'Incorrect OTP,Please Re-enter!!')


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

    filedata = os.listdir('Tickets')
    for x in filedata:
        os.remove("Tickets\{}".format(x))


def next1(entry0, entry01):
    p1 = entry0.get()
    p2 = entry01.get()
    if p1 == p2 and len(p1) >= 8:
        root.title("Railways Reservations")
        root.geometry('1200x700')

        bg = ImageTk.PhotoImage(Image.open("005.jpg"))
        label1 = Label(root, image=bg)
        label1.place(x=0, y=0)
        label03 = Label(root, text="Registration Completed Successfully, Please Login To Proceed", font=('Arial', 15))
        label03.place(x=300, y=300)
        loingbutton = Button(root, text='Login', bd=3, font=('Arial', 15), command=login)
        loingbutton.place(x=500, y=400)
        global password
        password = p1
        userdatasave()
        root.mainloop()

    else:
        messagebox.showinfo('', 'Please Check Your Password!!')


def createdatabase():
    cursor.execute("show databases;")
    databases = cursor.fetchall()
    flag = False
    for i in databases:
        if i[0] == 'railways':
            flag = True
    if (flag == False):
        cursor.execute("create database railways;")
        cursor.execute("use railways;")
        cursor.execute(
            "create table user(email varchar(100) primary key,password varchar(100),name varchar(100),age int,address varchar(200),phone varchar(12));")
        cursor.execute(
            " create table passenger(pnr varchar(20) primary key,name varchar(100),age int,phone varchar(12),gender varchar(8), aadhar varchar(20),email varchar(100),foreign key(email) references user(email));")
        cursor.execute(
            "create table reserves(ticketno varchar(20) primary key,j_date date,seatno int,status varchar(20),source varchar(20),destination varchar(20),traintype varchar(10),trainname varchar(100),pnr varchar(20),foreign key(pnr) references passenger(pnr))")
        cursor.execute(
            "create table cancles(cid varchar(20) primary key,pnr varchar(20),foreign key(pnr) references passenger(pnr),ticketno varchar(20),foreign key(ticketno) references reserves(ticketno));")
        cursor.execute(
            "create table train(tid int,tname varchar(100),ttype varchar(30),tsource varchar(20),tdestination varchar(30),jdate date,jtime timestamp,price int);")
        cursor.execute(
            "insert into train values(101,'Nanda Devi AC Express','A/C','HYDERABAD','BANGLORE','2023-4-21','2023-4-21 18:00:00',1200),(102,'Nagpur-Amritsar AC Superfast Express','A\C-Chair','NAGPUR','AMRITSAR','2023-4-20','2023-4-20 20:30:00',1200),(102,'Nagpur-Amritsar AC Superfast Express','A\C-First Class','NAGPUR','AMRITSAR','2023-3-29','2023-3-29 12:10:00',1200),(103,'Gujarat express','Non-A/C','GUJRAT','HYDERABAD','2023-2-26','2023-2-26 22:00:00',800),(105,'Gujarat express','A/C','GUJRAT','HYDERABAD','2023-1-17','2023-1-17 12:20:00',1300),(104,'Flying Ranee Express','Non-A/C-Chair','HYDERABAD','CHENNAI','2023-1-20','2023-1-20 12:00:00',1000),(106,'Rajdhani Express','A/C','DELHI','HYDERABAD','2023-2-20','2023-2-20 16:50:00',1700),(107,'Rajdhani Express','A/C-Chair','DELHI','HYDERABAD','2023-2-20','2023-2-20 20:00:00',1400),(101,'Nanda Devi AC Express','A/C','HYDERABAD','BANGLORE','2023-2-15','2023-2-15 19:40:00',1900),(108,'Nagpur-Amritsar AC Superfast Express','A\C-Chair','NAGPUR','AMRITSAR','2023-2-10','2023-2-10 17:50:00',1500),(102,'Nagpur-Amritsar AC Superfast Express','A\C-First Class','NAGPUR','AMRITSAR','2023-2-20','2023-2-20 20:15:00',1900),(103,'Gujarat express','Non-A/C','GUJRAT','HYDERABAD','2023-2-20','2023-2-20 21:10:00',1000),(105,'Gujarat express','A/C','GUJRAT','HYDERABAD','2023-2-20','2023-2-20 3:40:00',1800),(104,'Flying Ranee Express','Non-A/C-Chair','HYDERABAD','CHENNAI','2023-2-18','2023-2-18 3:10:00',1200),(106,'Rajdhani Express','A/C','DELHI','HYDERABAD','2023-2-18','2023-2-18 10:20:00',2000),(107,'Rajdhani Express','A/C-Chair','DELHI','HYDERABAD','2023-2-18','2023-2-18 12:50:00',1300);")
        cursor.execute('commit;')


def userdatasave():
    cursor.execute("use railways;")
    q = "insert into user(email,password,name,age,address,phone) values(%s,%s,%s,%s,%s,%s);"
    s = (email, password, name, age, address, phone)
    cursor.execute(q, s)
    cursor.execute("commit;")


def kill():
    root.destroy()


def register1():
    global entry01
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    root.title("Railways Reservations")
    root.geometry("1200x700")

    label1 = Label(mainframe, image=bg)
    label1.pack()
    label0 = Label(mainframe, text='Please Enter Your Details', bg='white', font=("Arial", 25))
    label0.place(x=400, y=50)
    label01 = Label(mainframe, text='Email Address', bg='white', font=('Arial', 15))
    label01.place(x=60, y=200)
    entry01 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry01.place(x=270, y=200)
    label02 = Label(mainframe, text='Full Name', bg='white', font=('Arial', 15))
    label02.place(x=60, y=250)
    entry02 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry02.place(x=270, y=250)
    label03 = Label(mainframe, text='Address', bg='white', font=('Arial', 15))
    label03.place(x=60, y=300)
    entry03 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry03.place(x=270, y=300)
    label04 = Label(mainframe, text='Age', bg='white', font=('Arial', 15))
    label04.place(x=60, y=350)
    entry04 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry04.place(x=270, y=350)
    label05 = Label(mainframe, text='Phone number', bg='white', font=('Arial', 15))
    label05.place(x=60, y=400)
    entry05 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry05.place(x=270, y=400)
    otp = Button(root, text='Register', bg='white',
                 command=lambda: check(entry01, entry02, entry03, entry04, entry05, otp, mainframe), height=2, width=11,
                 bd=2, font=('Arial', 15))
    otp.place(x=500, y=500)
    backbut = Button(text='Back', bd=3, bg='white', command=mainscreen)
    backbut.place(x=850, y=600)

    root.mainloop()


def login():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    label01 = Label(mainframe, text="Email-ID", bg='white', font=('Arial', 15))
    label01.place(x=60, y=200)
    entry01 = Entry(mainframe, bd=2, font=('Arial', 15))
    entry01.place(x=170, y=200)
    label02 = Label(mainframe, text="Password", bg='white', font=('Arial', 15))
    label02.place(x=60, y=300)
    entry02 = Entry(mainframe, bd=2, font=('Arial', 15), show="*")
    entry02.place(x=170, y=300)
    loginbut = Button(text="LOGIN", bd=3, font=('Arial', 15), command=lambda: logincheck(entry01, entry02))
    loginbut.place(x=300, y=500)
    backbut = Button(mainframe, text="Back", command=mainscreen)
    backbut.place(x=850, y=600)
    root.mainloop()


def logout(text):
    global uemail
    if text == 'LOGOUT':
        logout = messagebox.askyesno("", "Are you sure You want to LOGOUT ??")
        if (logout):
            mainscreen()
            uemail = ''
            global passdata
            passdata = []


def back(text):
    backbut = Button(text=text, bd=3, bg='white', command=lambda: logout(text))
    backbut.place(x=900, y=600)


def logincheck(entry01, entry02):
    global uemail
    flag = 0
    uemail = entry01.get()
    upassword = entry02.get()
    cursor.execute("use railways;")
    cursor.execute("select count(*) from user;")
    count = cursor.fetchone()
    count = count[0]
    cursor.execute("select * from user")
    logindata = cursor.fetchall()
    for i in range(0, count):
        if (logindata[i][0] == uemail and logindata[i][1] == upassword):
            flag = 1
    if (flag == 1):
        afterlogin()
    else:
        messagebox.showinfo('', 'Please Check Your Email or Password!!')


def afterlogin():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=150, y=100, relheight=0.5, relwidth=0.3)
    label0 = Label(framebg, image=img)
    label0.pack(padx=90, pady=100)
    newbookingbut = Button(framebg, text="New Booking", bg='white', command=newbooking, font=("Arial", 15), height=2,
                           width=20, bd=3)
    newbookingbut.place(x=70, y=30)
    canclebut = Button(framebg, text="Cancel Your Ticket", bg='white', command=cancle, font=("Arial", 15), height=2,
                       width=20, bd=3)
    canclebut.place(x=70, y=150)
    checkbut = Button(framebg, text="Check Your Booking Status", bg='white', font=("Arial", 15), height=2, width=23,
                      bd=3, command=checkstauts)
    checkbut.place(x=70, y=270)
    back("LOGOUT")
    userlabel=Label(mainframe,text="Logged in:-"+uemail,bg="white",font=("Arial",10))
    userlabel.place(x=700,y=20)
    root.mainloop()


def traindetails(sourcecombo, destinationcombo, classcombo):
    source = sourcecombo.get()
    destination = destinationcombo.get()
    coachclass = classcombo.get()
    if source != 'Select Source' and destination != 'Select Destination' and coachclass != 'Select Class':
        if source != destination:
            cursor = connection.cursor(buffered=True)
            bg = ImageTk.PhotoImage(Image.open("005.jpg"))
            mainframe = Frame(root, bg='white')
            mainframe.place(x=0, y=0)
            label1 = Label(mainframe, image=bg)
            label1.pack()
            framebg = Frame(mainframe, bg='white')
            framebg.place(x=0, y=100)
            cursor.execute("use railways;")
            cursor.execute("select count(*) from train;")
            count = cursor.fetchone()
            count = count[0]
            q = 'select tname,ttype,tsource,tdestination,jtime,price from train where tsource=%s and tdestination=%s and ttype=%s and jdate=%s'
            data = [source, destination, coachclass, date3]
            cursor.execute(q, data)
            data = cursor.fetchall()
            list(data)
            count = len(data)
            column = 0
            namelabel = Label(framebg, text="Train Name   ", font=('Arial', 20), bg='white')
            namelabel.grid(row=1, column=0, sticky='W')
            classlabel = Label(framebg, text="Class   ", font=('Arial', 20), bg='white')
            classlabel.grid(row=1, column=1, sticky='W')
            sourcelabel = Label(framebg, text="Source   ", font=('Arial', 20), bg='white')
            sourcelabel.grid(row=1, column=2, sticky='W')
            destinationlabel = Label(framebg, text="Destination   ", font=('Arial', 20), bg='white')
            destinationlabel.grid(row=1, column=3, sticky='W')
            datelabel = Label(framebg, text="Date-Time   ", font=('Arial', 20), bg='white')
            datelabel.grid(row=1, column=4, sticky='W')
            pricelabel = Label(framebg, text="Cost   ", font=('Arial', 20), bg='white')
            pricelabel.grid(row=1, column=5, sticky='W')
            for i in range(count):
                label = "label" + str(i)
                for z in data[i]:
                    label = Label(framebg, text=str(z) + "    ", font=('Arial', 15), bg='white')
                    label.grid(row=i + 2, column=column, sticky='W')
                    column += 1
                bookbutton = Button(framebg, text="BOOK", font=('Arial', 8), bd=3, command=lambda a=data[i]: booknow(a))
                bookbutton.grid(row=i + 2, column=column + 1)
                column = 0
            backbut = Button(mainframe, text="Back", command=warning)
            backbut.place(x=850, y=600)
            back("LOGOUT")
        else:
            messagebox.showinfo('', "Source and destination cannot be same, Please Re-chekc!!")
    else:
        messagebox.showinfo('', "Please Fill all Fields!!")
    root.mainloop()


def booknow(data):
    global traindata
    traindata = data
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=0, y=100, relwidth=1)
    detaillabel = Label(framebg, text="                          Passenger Details", font=('Arial', 30), bg='white')
    detaillabel.grid(columnspan=3)
    add(framebg)
    global cost
    cost = data[-1]
    backbut = Button(mainframe, text="Back", command=warning)
    backbut.place(x=850, y=600)
    root.mainloop()


def warning():
    ans = messagebox.askyesno('', "You will have to re-enter you data again, Are you sure you want to go back ?")
    if (ans):
        newbooking()


def add(frame):
    global ROW
    global passdata
    labelname = ['Name', 'Age', 'Aadhar No', 'Phone No             ', 'Gender']
    for i, j in zip(labelname, range(len(labelname))):
        passlabel = Label(frame, text=i, bg='white', font=('Arial', 15))
        passlabel.grid(row=ROW, column=j)
    ROW += 1
    gender = ["Select Gender", "Male", "Female", "Other"]
    nameentry = Entry(frame, bg='white', bd=3)
    nameentry.grid(row=ROW, column=0)
    ageentry = Entry(frame, bg='white', bd=3)
    ageentry.grid(row=ROW, column=1)
    aadharentry = Entry(frame, bg='white', bd=3)
    aadharentry.grid(row=ROW, column=2)
    phentry = Entry(frame, bg='white', bd=3)
    phentry.grid(row=ROW, column=3)
    gendercombo = ttk.Combobox(frame, font=('Arial', 12), state='readonly', values=gender)
    gendercombo.current(0)
    gendercombo.grid(row=ROW, column=4)
    addpas = Button(frame, text="Add Passenger", font=('Arial', 10), bd=3, bg='white',
                    command=lambda: getdata(frame, 'addbut', nameentry, ageentry, aadharentry, phentry, gendercombo))
    addpas.grid(row=30, column=0)
    confirm = Button(frame, text="Confirm Booking", font=('Arial', 10), bd=3, bg='white',
                     command=lambda: getdata(frame, 'confirmbut', nameentry, ageentry, aadharentry, phentry,
                                             gendercombo))
    confirm.grid(row=30, column=2)
    ROW += 1


def getdata(frame, text, nameentry, ageentry, aadharentry, phentry, gendercombo):
    if nameentry.get() != '' and ageentry.get() != '' and ageentry.get() != '' and aadharentry.get() != '' and phentry.get() != '' and gendercombo.get() != 'Select Gender':
        data = (
            pnr(), nameentry.get(), phentry.get(), ageentry.get(), gendercombo.get(), aadharentry.get(), uemail,
            seatno())
        passdata.append(data)
        if text == 'addbut':
            add(frame)
        if text == 'confirmbut':
            payment()
    else:
        messagebox.showinfo('', "Incorrect Info, Please Re-check")
        return


def payment():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=0, y=100, relwidth=0.8)
    price = str(cost * len(passdata))
    pricelabel = Label(framebg, text='Total Payable Amount :-' + price, bg='white', font=('Arial', 15))
    pricelabel.grid(row=1, column=4)
    methods = ['Select a Payment Method', 'NET BANKING', 'UPI', 'CASH']
    methodcombo = ttk.Combobox(framebg, font=('Arial', 15), state='readonly', values=methods)
    methodcombo.current(0)
    methodcombo.grid(row=2, column=4)
    backbut = Button(mainframe, text="Back", bd=3, bg='white', command=warning)
    backbut.place(x=850, y=600)
    back('LOGOUT')
    confirmbut = Button(framebg, text="Confirm Booking", bd=3, bg='white', command=lambda: call_nosync(sendmail(methodcombo)))
    confirmbut.grid(row=3, column=4)
    root.mainloop()


def sendmail(methodcombo):
    global passdata
    if methodcombo.get() != 'Select a Payment Method':
        try:
            savepasdata(passdata)
        except con.errors.DatabaseError:
            messagebox.showinfo('', "Incorrect Passenger Data, Please Re-check!!")
            newbooking()
        try:
            msg1 = ''
            msg = "IRCTC\n\n\nYour Ticket is Confirmed\nBooking date:-{}\n".format(
                datetime.date.today().strftime("%d-%m-%y"))
            pdf = FPDF()
            for data in passdata:
                msg1 = msg1 + "\nPassenger Details:-\nPNR:-{}\nPassenger Name:-{}\nPhone:-{}\nAge:-{}\nGender:-{}\nAadhar:-{}\nSeat No:-{}\n\nPayment Method:-{}\n".format(
                    data[0],
                    data[1], data[
                        2], data[3],
                    data[4],
                    data[5], data[7], methodcombo.get())

                msg1 = msg1 + "\nTrain Details:-\nTrain Name:-{}\nClass:-{}\nSource:-{}\nDestination:-{}\nDate-Time:-{}\nCost:-Rs{}".format(
                    traindata[0], traindata[1],
                    traindata[
                        2], traindata[3],
                    traindata[4].strftime("%d-%m-%Y %H:%M:%S"), cost)

                qr = qrcode.QRCode(version=1,
                                   box_size=5,
                                   border=0)
                qr.add_data(data[0])
                qr.make(fit=True)
                img = qr.make_image(fill_color='blue',
                                    back_color='white')

                img.save('Tickets\{}.png'.format(data[1]))
                msg = msg + msg1
                pdf.add_page()
                pdf.set_font('Arial', size=15)
                pdf.multi_cell(w=200, h=10, txt=msg)
                msg1 = ''
                msg = "IRCTC\n\n\nYour Ticket is Confirmed\nBooking date:-{}\n".format(
                    datetime.date.today().strftime("%d-%m-%y"))
            pdf.output('Tickets\Tickets.pdf')

            page_number = 0
            output_file = PdfWriter()
            with open("Tickets\Tickets.pdf", "rb") as f1:
                input_file = PdfReader(f1)
                for data in passdata:
                    c = canvas.Canvas('Tickets\{}.pdf'.format(data[1]))
                    c.drawImage('090.png', x=30, y=725, width=100, height=98)
                    c.drawImage('Tickets\{}.png'.format(data[1]), x=397, y=640, width=200, height=160)
                    c.save()
                    with open("Tickets\{}.pdf".format(data[1]), "rb") as f2:
                        watermark = PdfReader(f2)
                        page_count = len(input_file.pages)
                        input_page = input_file.pages[page_number]
                        input_page.merge_page(watermark.pages[0])
                        output_file.add_page(input_page)
                        page_number += 1
                with open("Tickets\QRTickets.pdf", "wb") as outputStream:
                    output_file.write(outputStream)

                send = sendpdf('railwayslogin@gmail.com', uemail, 'kijhzjdxvyuxapfi', 'IRCTC TICKET BOOKING',
                               'TICKETS CONFIRMED', 'QRTickets', 'Tickets\.')
                send.email_send()
                reserve(passdata)
                passdata = []
                bg = ImageTk.PhotoImage(Image.open("005.jpg"))
                mainframe = Frame(root, bg='white')
                mainframe.place(x=0, y=0)
                label1 = Label(mainframe, image=bg)
                label1.pack()
                framebg = Frame(mainframe, bg='white')
                framebg.place(x=80, y=100, relheight=0.8, relwidth=0.8)
                label = Label(framebg, text='Tickets Confirmed! You will Recieve Tickets on Registerd Email Address',
                          font=('Arial', 20), bg='white')
                label.place(x=30, y=200)
                backbut = Button(mainframe, text="Back", bd=3, bg='white', command=afterlogin)
                backbut.place(x=850, y=600)
                back('LOGOUT')

            filedata = os.listdir('Tickets')
            for x in filedata:
                os.remove("Tickets\{}".format(x))
        except smtplib.socket.gaierror:
            messagebox.showinfo('', 'Please Check Your Internet Connection')
    
    else:
        messagebox.showinfo('', 'Select Payment Method!!')
    root.mainloop()

def reserve(passdata):
    reservedata = []
    cursor.execute("use railways;")
    for data in passdata:
        data = list(data)
        data.append('Confirmed')
        reservedata = [ticketno(), data[0], data[-2], data[-1], traindata[0], traindata[1], traindata[2], traindata[3],
                       traindata[4]]
        q = 'insert into reserves(ticketno,pnr,seatno,status,trainname,traintype,source,destination,j_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(q, reservedata)
        cursor.execute('commit;')
    reservedata = []


def savepasdata(passdata):
    cursor.execute("use railways;")
    for data in passdata:
        q = 'insert into passenger(pnr,name,phone,age,gender,aadhar,email) values(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(q, data[:7])
        cursor.execute('commit;')


def cancle():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    img = ImageTk.PhotoImage(Image.open("01.png"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=150, y=100, relheight=0.5, relwidth=0.3)
    label0 = Label(framebg, image=img)
    label0.pack(padx=90, pady=100)
    labelcancle = Label(framebg, text='Enter PNR for Cancelation', bg='white', font=('Arial', 20))
    labelcancle.place(x=10, y=40)
    cancleentry = Entry(framebg, bd=3, bg='white', font=('Arial', 15))
    cancleentry.place(x=10, y=100)
    proceedbut = Button(framebg, text='Proceed', font=('Arial', 10), bd=3, bg='white',
                        command=lambda: confirmcancle(cancleentry))
    proceedbut.place(x=10, y=130)
    backbut = Button(mainframe, text="Back", bg='white', command=afterlogin)
    backbut.place(x=850, y=600)
    back("LOGOUT")
    root.mainloop()


def confirmcancle(cancleentry):
    flag = 0
    lemail = [uemail]
    cursor.execute("use railways;")
    q1 = "select r.pnr from reserves r,passenger p where r.pnr=p.pnr and p.email=%s"
    pnr = [cancleentry.get()]
    global canpnr
    canpnr = pnr[0]
    cursor.execute(q1, lemail)
    candata = cursor.fetchall()
    count = len(candata)
    for data in candata:
        for i in data:
            if pnr[0] == i:
                flag = 1
    if (flag == 1):
        ans = messagebox.askyesno('', 'Are You sure you want to cancle your Ticket ??')
    else:
        messagebox.showinfo("", "Incorrect PNR,Please Re-Check")
    if(ans):
        q = "update reserves set status='Cancled' where pnr=%s"
        cursor.execute(q, pnr)
        cursor.execute("commit;")
        q = 'insert into cancles(cid,pnr) values(%s,%s)'
        data = [ticketno(), pnr[0]]
        cursor.execute(q, data)
        cursor.execute("commit;")
        bg = ImageTk.PhotoImage(Image.open("005.jpg"))
        mainframe = Frame(root, bg='white')
        mainframe.place(x=0, y=0)
        label1 = Label(mainframe, image=bg)
        label1.pack()
        framebg = Frame(mainframe, bg='white')
        framebg.place(x=80, y=100, relheight=0.8, relwidth=0.8)
        label = Label(framebg, text='Tickets Cancled !! You will Recieve Messeage on your Email Address',
                      font=('Arial', 20), bg='white')
        label.place(x=30, y=200)
        cancleemail()
        backbut = Button(mainframe, text="Back", bd=3, bg='white', command=afterlogin)
        backbut.place(x=850, y=600)
        back('LOGOUT')
        root.mainloop()
    else:
        return


def checkstauts():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    img = ImageTk.PhotoImage(Image.open("01.png"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=150, y=100, relheight=0.5, relwidth=0.3)
    label0 = Label(framebg, image=img)
    label0.pack(padx=90, pady=100)
    labelstat = Label(framebg, text='Enter PNR for Status', bg='white', font=('Arial', 20))
    labelstat.place(x=10, y=40)
    statentry = Entry(framebg, bd=3, bg='white', font=('Arial', 15))
    statentry.place(x=10, y=100)
    proceedbut = Button(framebg, text='Proceed', font=('Arial', 10), bd=3, bg='white',
                        command=lambda: checkproceed(statentry))
    proceedbut.place(x=10, y=130)
    backbut = Button(mainframe, text="Back", bg='white', command=afterlogin)
    backbut.place(x=850, y=600)
    back("LOGOUT")
    root.mainloop()


def checkproceed(statentry):
    flag = 0
    lemail = [uemail]
    cursor.execute("use railways;")
    q1 = "select r.pnr from reserves r,passenger p where r.pnr=p.pnr and p.email=%s"
    pnr = statentry.get()
    cursor.execute(q1, lemail)
    statdata = cursor.fetchall()
    count = len(statdata)
    for data in statdata:
        for i in data:
            if pnr == i:
                flag = 1
    if (flag == 1):
        q2 = "select pnr,status,trainname,traintype,source,destination,j_date from reserves where pnr='{}'".format(pnr)
        cursor.execute(q2)
        statdata1 = cursor.fetchall()
        countstat = len(statdata1)
        bg = ImageTk.PhotoImage(Image.open("005.jpg"))
        mainframe = Frame(root, bg='white')
        mainframe.place(x=0, y=0)
        label1 = Label(mainframe, image=bg)
        label1.pack()
        framebg = Frame(mainframe, bg='white')
        framebg.place(x=80, y=100)
        statlabel = Label(framebg, text="PNR", font=('Arial', 20), bg='white')
        statlabel.grid(row=1, column=0, sticky='W')
        statlabel = Label(framebg, text="Stauts", font=('Arial', 20), bg='white')
        statlabel.grid(row=1, column=1, sticky='W')
        namelabel = Label(framebg, text="Train Name   ", font=('Arial', 20), bg='white')
        namelabel.grid(row=1, column=2, sticky='W')
        classlabel = Label(framebg, text="Class   ", font=('Arial', 20), bg='white')
        classlabel.grid(row=1, column=3, sticky='W')
        sourcelabel = Label(framebg, text="Source   ", font=('Arial', 20), bg='white')
        sourcelabel.grid(row=1, column=4, sticky='W')
        destinationlabel = Label(framebg, text="Destination   ", font=('Arial', 20), bg='white')
        destinationlabel.grid(row=1, column=5, sticky='W')
        datelabel = Label(framebg, text="Date-Time   ", font=('Arial', 20), bg='white')
        datelabel.grid(row=1, column=6, sticky='W')
        column = 0
        for i in range(countstat):
            for z in statdata1[i]:
                label = Label(framebg, text=str(z) + "    ", font=('Arial', 15), bg='white')
                label.grid(row=i + 2, column=column, sticky='W')
                column += 1
        backbut = Button(mainframe, text="Back", bd=3, bg='white', command=checkstauts)
        backbut.place(x=850, y=600)
        back('LOGOUT')
        root.mainloop()
    else:
        messagebox.showinfo("", "Incorrect PNR,Please Re-Check")


def cancleemail():
    msg = "Your Ticket With PNR No {} is Cancled Successfully".format(canpnr)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('railwayslogin@gmail.com', 'kijhzjdxvyuxapfi')
    s.sendmail('railwayslogin@gmail.com', uemail, msg)
    backbut = Button(mainframe, text="Back", bd=3, bg='white', command=warning)
    backbut.place(x=850, y=600)
    back('LOGOUT')


def newbooking():
    global passdata
    passdata = []
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    img = ImageTk.PhotoImage(Image.open('irctc.png'))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=150, y=100, relheight=0.8, relwidth=0.4)
    label1 = Label(framebg, text="Source", font=('Arial', 15), bg='white')
    label1.place(x=100, y=50)
    label2 = Label(framebg, text="Destination", font=('Arial', 15), bg='white')
    label2.place(x=100, y=150)
    label3 = Label(framebg, text="Class", font=('Arial', 15), bg='white')
    label3.place(x=100, y=350)
    destinations = ["Select Destination", "HYDERABAD", "BANGLORE", "CHENNAI", "NAGPUR", "DELHI", "GUJRAT", "AMRITSAR"]
    destinationcombo = ttk.Combobox(framebg, font=('Arial', 15), state='readonly', values=destinations)
    destinationcombo.current(0)
    destinationcombo.place(x=100, y=200)
    sources = ["Select Source", "HYDERABAD", "BANGLORE", "CHENNAI", "KERELA", "NAGPUR", "DELHI", "GUJRAT", "AMRITSAR"]
    sourcecombo = ttk.Combobox(framebg, font=('Arial', 15), state='readonly', values=sources)
    sourcecombo.current(0)
    sourcecombo.place(x=100, y=100)
    backbut = Button(mainframe, text="Back", command=afterlogin)
    backbut.place(x=850, y=600)
    coachclass = ["Select Class", "Sleeper", "A/C", 'Non-A/C', "Semi-Sleeper", "A/C-Chair", "Non-A/C-Chair",
                  "A/C-First Class"]
    classcombo = ttk.Combobox(framebg, font=('Arial', 15), state='readonly', values=coachclass)
    classcombo.current(0)
    classcombo.place(x=100, y=400)
    train = Button(framebg, text='Search', command=lambda: traindetails(sourcecombo, destinationcombo, classcombo))
    train.place(x=100, y=450)
    date(framebg)
    back("LOGOUT")
    root.mainloop()


def date(framebg):
    framebg = framebg
    today = datetime.date.today()
    today = today.strftime("%d/%m/%y")
    today = today.split('/')
    today[2] = '20' + today[2]
    cal = Calendar(framebg, selectmode="day", year=int(today[2]), month=int(today[1]), day=int(today[0]))
    cal.place(x=100, y=250)
    calbutton = Button(framebg, text='Select Date', font=('Arial', 8), bg='white',
                       command=lambda: calsave(framebg, calbutton, cal))
    calbutton.place(x=300, y=450)


def calsave(framebg, calbutton, cal):
    global date3
    framebg = framebg
    date1 = cal.selection_get()
    date3 = date1.strftime("20%y-%m-%d")
    date2 = date1.strftime("%d/%m/%y")
    if date1 >= datetime.date.today():
        calbutton.destroy()
        cal.destroy()
        label1 = Label(framebg, text=date2, font=('Arial', 15), bg='white')
        label1.place(x=100, y=300)
        calbutton = Button(framebg, text='Select Date', command=lambda: date(framebg), font=('Arial', 15), bg='white')
        calbutton.place(x=100, y=250)
    else:
        messagebox.showinfo("", "Please select valid DATE!!")


def mainscreen():
    bg = ImageTk.PhotoImage(Image.open("005.jpg"))
    img = ImageTk.PhotoImage(Image.open("01.png"))
    mainframe = Frame(root, bg='white')
    mainframe.place(x=0, y=0)
    label1 = Label(mainframe, image=bg)
    label1.pack()
    framebg = Frame(mainframe, bg='white')
    framebg.place(x=150, y=100, relheight=0.5, relwidth=0.3)
    label0 = Label(framebg, image=img)
    label0.pack(padx=90, pady=100)
    label2 = Label(root, text='Online Railways Ticket Booking Application', bg='white', font=("Arial", 25))
    label2.place(x=320, y=0)
    root.title("Railways Reservations")

    root.geometry("1200x700")
    register = Button(framebg, text="Register", command=register1, bg='white', font=("Arial", 15), height=2, width=20,
                      bd=3)
    register.place(x=70, y=60)
    loginbut = Button(framebg, text="Login", command=login, bg='white', font=("Arial", 15), height=2, width=20, bd=3)
    loginbut.place(x=70, y=200)
    root.mainloop()


def checkmysql():
    try:
        with open('login.txt', 'rb') as f:
            d = pickle.load(f)
        connection = con.connect(host='localhost', user=d[0], password=d[1])
        global mysqluser, mysqlpass
        mysqluser = d[0]
        mysqlpass = d[1]
    except (FileNotFoundError, con.InterfaceError, pickle.UnpicklingError):
        root = Tk()
        getmysql(root)
    except con.errors.DatabaseError:
        messagebox.showinfo('', "PLEASE INSTALL MYSQL SERVER TO RUN THIS APPLICATION !!!")
        root = Tk()
        getmysql(root)


checkmysql()
root = Tk()
bg = ImageTk.PhotoImage(Image.open("005.jpg"))
img = ImageTk.PhotoImage(Image.open("01.png"))
img1 = ImageTk.PhotoImage(Image.open("irctc.png"))
connection = con.connect(host='localhost', user=mysqluser, password=mysqlpass)
cursor = connection.cursor()
createdatabase()
mainframe = Frame(root, bg='white')
mainframe.place(x=0, y=0)
label1 = Label(mainframe, image=bg)
label1.pack()
framebg = Frame(mainframe, bg='white')
framebg.place(x=150, y=100, relheight=0.5, relwidth=0.3)
label0 = Label(framebg, image=img)
label0.pack(padx=90, pady=100)
label2 = Label(root, text='Online Railways Ticket Booking Application', bg='white', font=("Arial", 25))
label2.place(x=320, y=0)
root.title("Railways Reservations")

root.geometry("1200x700")
register = Button(framebg, text="Register", command=register1, bg='white', font=("Arial", 15), height=2, width=20,
                  bd=3).place(x=70, y=60)
loginbut = Button(framebg, text="Login", command=login, bg='white', font=("Arial", 15), height=2, width=20, bd=3).place(
    x=70, y=200)
root.iconphoto(True, img1)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
