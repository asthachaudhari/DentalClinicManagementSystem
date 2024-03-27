# -----------------------------functionality-----------------------------
# import tkinter as tk
from tkinter import *
import time
from office_view import Officeview
from dentist import Dentist
from patient_details import Patient
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

logo = date = currenttime = None


class Receptionist:
    def __init__(self, master):
        self.master = master
        self.master.title('Receptionist home page')
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)

        # self.master = Tk()
        # self.master.title("Receptionist_homepage")
        # self.master.geometry("1000x563+10+10")
        # self.master.resizable(0, 0)  # for fixed sized window
        # define image
        bg = PhotoImage(file="dms project bg.png")
        # connetivity
        conn = mysql.connector.connect(host='localhost', user='user1', passwd='1234', database='dcms')
        con = conn.cursor()

        def office_view():
            # self.master.destroy()
            self.new_window = Toplevel(self.master)
            self.app = Officeview(self.new_window)
            # self.master.destroy()
            # import office_view

        # patient details
        def dentist():
            self.new_window = Toplevel(self.master)
            self.app = Dentist(self.new_window)
            # self.master.destroy()
            # import dentist

        def patient_details():
            self.new_window = Toplevel(self.master)
            self.app = Patient(self.new_window)
            # self.master.destroy()
            # import patient_details

        def logout():
            result = messagebox.askyesno('Confirm', 'Do you want to logout?', parent=self.master)
            if result:
                self.master.destroy()
            else:
                pass

        # clock method for date and time
        def clock():
            global date, currenttime
            date = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
            datetimeLabel.after(1000, clock)

        # ------------------------------gui-----------------------------------------

        # create a label for bg
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)
        label1 = Label(self.master, text="---Welcome To Sweet Tooth Dental Clinic---", font=("Arial", 16), bg="white",
                       fg="#7868d5")
        label1.place(x=290, y=30)
        # for date and time on window
        datetimeLabel = Label(self.master, font=('times new roman', 10, 'bold'), bg='white')
        datetimeLabel.place(x=25, y=30)
        clock()
        global logo
        logo = PhotoImage(file='recep.png')
        logolable = Label(self.master, image=logo, bg='white')
        logolable.grid(row=0, column=0, padx=100, pady=90)
        lbtn = Button(self.master, width=30, height=3, text="<-- Logout", bg="#EE82EE", fg="white",
                      command=logout)  # command=connect_database)
        lbtn.place(x=60, y=250)
        obtn = Button(self.master, width=30, height=3, text="Office View", bg="#7868d5", fg="white",
                      command=office_view)  # command=connect_database)
        obtn.place(x=60, y=320)
        pbtn = Button(self.master, width=30, height=3, text="Patient Details", bg="#7868d5", fg="white",
                      command=patient_details)  # command=connect_database)
        pbtn.place(x=60, y=390)
        dbtn = Button(self.master, width=30, height=3, text="Dentist details", bg="#7868d5", fg="white",
                      command=dentist)
        dbtn.place(x=60, y=460)

        self.master.mainloop()


if __name__ == "__main__":
    root = Tk()
    receptionistpage = Receptionist(root)
    root.mainloop()

'''
self.master = Tk()
self.master.title("Receptionist_homepage")
self.master.geometry("1000x563+10+10")
self.master.resizable(0, 0)  # for fixed sized window
# define image
bg = PhotoImage(file="dms project bg.png")
#connetivity
conn=mysql.connector.connect(host='localhost',user='user1',passwd='1234',database='dcms')
con = conn.cursor()

def office_view():
    self.new_window = Toplevel(self.master)
    self.app=Officeview(self.new_window)
    #self.master.destroy()
    #import office_view
#patient details
def dentist():
    self.master.destroy()
    import dentist
def patient_details():
        self.master.destroy()
        import patient_details
def logout():
    result = messagebox.askyesno('Confirm', 'Do you want to logout?')
    if result:
        self.master.destroy()
    else:
        pass




#clock method for date and time
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)

#------------------------------gui-----------------------------------------

# create a label for bg my_label = Label(self.master, image=bg) my_label.place(x=0, y=0, relwidth=1, relheight=1) 
label1 = Label(self.master, text="---Welcome To Sweet Tooth Dental Clinic---", font=("Arial", 16), bg="white", 
fg="#7868d5") label1.place(x=290, y=30) #for date and time on window datetimeLabel=Label(self.master,font=('times new 
roman',10,'bold'),bg='white') datetimeLabel.place(x=25,y=30) clock()

logo=PhotoImage(file='recep.png') logolable=Label(self.master,image=logo,bg='white') logolable.grid(row=0,column=0,
padx=100,pady=90) lbtn= Button(self.master, width=30, height=3, text="<-- Logout", bg="#EE82EE", fg="white",
command = logout)#command=connect_database) lbtn.place(x=60, y=250) obtn= Button(self.master, width=30, height=3, 
text="Office View", bg="#7868d5", fg="white", command=office_view)#command=connect_database) obtn.place(x=60, 
y=320) pbtn= Button(self.master, width=30, height=3, text="Patient Details", bg="#7868d5", fg="white",
command=patient_details)#command=connect_database) pbtn.place(x=60, y=390) dbtn= Button(self.master, width=30, 
height=3, text="Dentist details", bg="#7868d5", fg="white",command=dentist) dbtn.place(x=60, y=460)


self.master.mainloop()
'''
