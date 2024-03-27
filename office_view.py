from tkinter import *
import time
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import tkinter as tk
import mysql.connector

logo = date = currenttime = bg = None


class Officeview:
    def __init__(self, master):
        self.master = master
        self.master.title('office view')
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)

        # clock method for date and time
        def clock():
            global date, currenttime
            date = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
            datetimeLabel.after(1000, clock)

        # Create a connection to the database
        # connetivity
        conn = mysql.connector.connect(host='localhost', user='user1', passwd='1234', database='dcms')
        mycursor = conn.cursor()

        def show_patient():

            query = 'select * from pvisit'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            ptable.delete(*ptable.get_children())
            for data in fetched_data:
                ptable.insert('', END, values=data)

        # exit button
        def exit_patient():
            result = messagebox.askyesno('Confirm', 'Do you want to exit?', parent=self.master)
            if result:
                self.master.destroy()
                import receptionist_home
            else:
                pass

        # add_patient
        def add_patient():
            def add_data():
                # if not timeEntry.get().isdigit():
                # messagebox.showerror("Error", "time number must be a number")
                # return

                if idEntry.get() == '' or p_nameEntry.get() == '' or dateEntry.get() == '' or timeEntry.get() == '' or \
                        fees_paidEntry.get() == '':
                    messagebox.showerror('Error', 'All Feilds are required',
                                         parent=add_window)  # if not given all entry

                else:
                    query = "INSERT INTO pvisit ( id,p_name, date, time,fees_paid) VALUES ( %s, %s, %s, %s,%s)"
                    values = (idEntry.get(), p_nameEntry.get(), dateEntry.get(), timeEntry.get(), fees_paidEntry.get())
                    mycursor.execute(query, values)
                    conn.commit()
                    result = messagebox.askyesno('confirm', 'Data added sucessfully!.\nDo you want to clear the form?',
                                                 parent=self.master)
                    # messagebox.showerror("","this is an error",parent=self.master)
                    print(result)
                    if result:  # If click yes
                        # idEntry.delete(0, END)
                        idEntry.delete(0, END)
                        p_nameEntry.delete(0, END)
                        dateEntry.delete(0, END)
                        timeEntry.delete(0, END)
                        fees_paidEntry.delete(0, END)
                        # statusEntry.delete(0, END)

                    else:
                        pass

                    query = 'select *from pvisit'
                    mycursor.execute(query)
                    fetched_data = mycursor.fetchall()
                    ptable.delete(*ptable.get_children())
                    for data in fetched_data:
                        ptable.insert('', END, values=data)

            add_window = Toplevel()
            add_window.configure(bg='#7868d5')
            add_window.grab_set()
            add_window.resizable(False, False)

            idLabel = Label(add_window, text='Id', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
            idEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, )
            idEntry.grid(row=0, column=1, pady=15, padx=10)

            p_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            p_nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
            p_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            p_nameEntry.grid(row=1, column=1, pady=15, padx=10)

            dateLabel = Label(add_window, text='date', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            dateLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
            dateEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            dateEntry.grid(row=2, column=1, pady=15, padx=10)

            timeLabel = Label(add_window, text='time', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            timeLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
            timeEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            timeEntry.grid(row=3, column=1, pady=15, padx=10)

            fees_paidLabel = Label(add_window, text='Fees paid', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                   fg='white')
            fees_paidLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
            fees_paidEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            fees_paidEntry.grid(row=4, column=1, pady=15, padx=10)

            p_button = ttk.Button(add_window, text='Add ', command=add_data)
            p_button.grid(row=6, columnspan=2, pady=15)

        # ------------------------------gui-----------------------------------------

        # define image
        global bg
        bg = PhotoImage(file="page.png")
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # leftframe
        leftFrame = Frame(self.master, bg="white")
        leftFrame.place(x=30, y=65, width=300, height=450)
        global logo
        logo = PhotoImage(file='officeview.png')
        logolable = Label(leftFrame, image=logo, bg='white')
        logolable.grid(row=0, column=0, padx=50)

        # lift the left frame to be on top of the image
        leftFrame.lift()

        # for date and time on window
        datetimeLabel = Label(self.master, font=('times new roman', 10, 'bold'), bg='white')
        datetimeLabel.place(x=25, y=30)
        clock()

        # Create a label widget
        label1 = Label(self.master, text='Office View', font=('Arial', 10, 'bold'), bg="white", fg='black')

        # Add the label to the window using pack method
        label1.pack(side=TOP, padx=10, pady=30)
        # button on frameleft
        addpButton = tk.Button(leftFrame, text='add patient visit', width=30, height=2,
                               command=add_patient)  # lambda :toplevel_patient('Add Patient', 'Add', add_data))
        addpButton.configure(bg='#7868d5', fg='white')
        addpButton.grid(row=1, column=0, pady=20)

        obtn = Button(leftFrame, width=30, height=2, text="view patient visit", bg="#7868d5", fg="white",
                      command=show_patient)
        obtn.grid(row=2, column=0, pady=20)

        obtn = Button(leftFrame, width=30, height=2, text="Exit", bg="#7868d5", fg="white", command=exit_patient)
        obtn.grid(row=3, column=0, pady=20)
        # right frame
        rightFrame = Frame(self.master)
        rightFrame.configure(bg="white")
        rightFrame.place(x=320, y=65, width=650, height=450)

        # treeview

        scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

        ptable = ttk.Treeview(rightFrame, columns=('id', 'p_name', 'date', 'time', 'fees_paid'),
                              xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

        scrollBarX.config(command=ptable.xview)
        scrollBarY.config(command=ptable.yview)

        scrollBarX.pack(side=BOTTOM, fill=X)
        scrollBarY.pack(side=RIGHT, fill=Y)

        ptable.pack(expand=1, fill=BOTH)

        ptable.heading("id", text='Id')
        ptable.heading("p_name", text='Patient Name')
        ptable.heading("date", text='Visit Date')
        ptable.heading("time", text='Visit Time')
        ptable.heading("fees_paid", text='Fees paid')

        ptable.column("id", width=200, anchor=CENTER)
        ptable.column("p_name", width=300, anchor=CENTER)
        ptable.column("date", width=100, anchor=CENTER)
        ptable.column("time", width=300, anchor=CENTER)
        ptable.column("fees_paid", width=200, anchor=CENTER)

        style = ttk.Style()

        style.configure('Treeview', rowheight=25, font=('arial', 10, 'bold'), fieldbackground='white',
                        background='white', )
        style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='#7868d5')

        ptable.config(show='headings')


if __name__ == "__main__":
    root = Tk()
    officeviewpage = Officeview(root)
    root.mainloop()

'''from tkinter import *
import time
from tkinter import messagebox,ttk
from tkinter.ttk import Combobox
import tkinter as tk
import mysql.connector
global logo
logo =None

#clock method for date and time
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)
# Create a connection to the database
#connetivity
conn=mysql.connector.connect(host='localhost',user='user1',passwd='1234',database='dcms')
mycursor = conn.cursor()
def show_patient():

    query = 'select * from pvisit'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    ptable.delete(*ptable.get_children())
    for data in fetched_data:
        ptable.insert('', END, values=data)

#exit button
def exit_patient():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        office_view_window.destroy()
        import receptionist_home
    else:
        pass

#add_patient
def add_patient():
    def add_data():
        #if not timeEntry.get().isdigit():
           # messagebox.showerror("Error", "time number must be a number")
           # return

        if idEntry.get()=='' or p_nameEntry.get() == '' or dateEntry.get() == '' or timeEntry.get() == '' or 
        fees_paidEntry.get() == '' : messagebox.showerror('Error', 'All Feilds are required', parent=add_window)  # 
        if not given all entry

        else:
            query = "INSERT INTO pvisit ( id,p_name, date, time,fees_paid) VALUES ( %s, %s, %s, %s,%s)"
            values = (idEntry.get(), p_nameEntry.get(), dateEntry.get(), timeEntry.get(), fees_paidEntry.get())
            mycursor.execute(query,(values))
            conn.commit()
            result = messagebox.askyesno('confirm', 'Data added sucessfully!.\nDo you want to clear the form?')
            print(result)
            if result:  # If click yes
                # idEntry.delete(0, END)
                idEntry.delete(0, END)
                p_nameEntry.delete(0, END)
                dateEntry.delete(0, END)
                timeEntry.delete(0, END)
                fees_paidEntry.delete(0, END)
                # statusEntry.delete(0, END)

            else:
                pass


            query = 'select *from pvisit'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            ptable.delete(*ptable.get_children())
            for data in fetched_data:
                ptable.insert('', END, values=data)

    add_window=Toplevel()
    add_window.grab_set()
    add_window.resizable(False,False)

    idLabel = Label(add_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, ) 
    idEntry.grid(row=0, column=1, pady=15, padx=10)
    
    p_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    p_nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    p_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    p_nameEntry.grid(row=1, column=1, pady=15, padx=10)

    dateLabel = Label(add_window, text='date', font=('times new roman', 20, 'bold'))
    dateLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    dateEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    dateEntry.grid(row=2, column=1, pady=15, padx=10)

    timeLabel = Label(add_window, text='time', font=('times new roman', 20, 'bold'))
    timeLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    timeEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    timeEntry.grid(row=3, column=1, pady=15, padx=10)

    fees_paidLabel = Label(add_window, text='Fees paid', font=('times new roman', 20, 'bold'))
    fees_paidLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    fees_paidEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    fees_paidEntry.grid(row=4, column=1, pady=15, padx=10)

    

    p_button = ttk.Button(add_window, text='Add ', command=add_data)
    p_button.grid(row=6, columnspan=2, pady=15)




#------------------------------gui-----------------------------------------

office_view_window = Tk()
office_view_window.title("office_view")
office_view_window.geometry("1000x563+10+10")
office_view_window.resizable(0, 0)  # for fixed sized window



# define image

bg = PhotoImage(file="page.png")
my_label = Label(office_view_window, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

#leftframe
leftFrame=Frame(office_view_window, bg="white")
leftFrame.place(x=30, y=65, width=300, height=450)

logo=PhotoImage(file='officeview.png')
logolable=Label(leftFrame,image=logo,bg='white')
logolable.grid(row=0,column=0,padx=50)

#lift the left frame to be on top of the image
leftFrame.lift()

#for date and time on window
datetimeLabel=Label(office_view_window,font=('times new roman',10,'bold'),bg='white')
datetimeLabel.place(x=25,y=30)
clock()

# Create a label widget
label1 = Label(office_view_window, text='Office View', font=('Arial', 10, 'bold'),bg="white", fg='black')

# Add the label to the window using pack method label1.pack(side=TOP, padx=10, pady=30) #button on frameleft 
addpButton=tk.Button(leftFrame, text='add patient visit', width=30,height=2,command =add_patient)#lambda 
:toplevel_patient('Add Patient', 'Add', add_data)) addpButton.configure(bg='#7868d5',fg='white') addpButton.grid(
row=1,column=0,pady=20)

obtn= Button(leftFrame, width=30, height=2, text="view patient visit", bg="#7868d5", fg="white",command=show_patient)
obtn.grid(row=2,column=0,pady=20)

obtn= Button(leftFrame, width=30, height=2, text="Exit", bg="#7868d5", fg="white",command=exit_patient)
obtn.grid(row=3,column=0,pady=20)
#right frame
rightFrame=Frame(office_view_window)
rightFrame.configure(bg="white")
rightFrame.place(x=320,y=65,width=650,height=450)

#treeview

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

ptable=ttk.Treeview(rightFrame, columns=('id','p_name', 'date','time','fees_paid'),
                                xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=ptable.xview)
scrollBarY.config(command=ptable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

ptable.pack(expand=1, fill=BOTH)

ptable.heading("id", text='Id')
ptable.heading("p_name", text='Patient Name')
ptable.heading("date", text='Visit Date')
ptable.heading("time", text='Visit Time')
ptable.heading("fees_paid", text='Fees paid')


ptable.column("id", width=200, anchor=CENTER)
ptable.column("p_name", width=300, anchor=CENTER)
ptable.column("date", width=100, anchor=CENTER)
ptable.column("time", width=300, anchor=CENTER)
ptable.column("fees_paid", width=200, anchor=CENTER)



style=ttk.Style()

style.configure('Treeview', rowheight=25,font=('arial', 10, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='#7868d5')

ptable.config(show='headings')
office_view_window.mainloop()
'''
