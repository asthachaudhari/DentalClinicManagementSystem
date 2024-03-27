from tkinter import *
import time
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import tkinter as tk
import mysql.connector

logo = date = currenttime = bg = None


class Dentist:
    def __init__(self, master):
        self.master = master
        self.master.title('Dentist details')
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

        def show_dentist():
            query = 'select * from ddetail'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            dtable.delete(*dtable.get_children())
            for data in fetched_data:
                dtable.insert('', END, values=data)

        # exit button
        def exit_dentist():
            result = messagebox.askyesno('Confirm', 'Do you want to exit?', parent=self.master)
            if result:
                self.master.destroy()
                import receptionist_home
            else:
                pass

        # add_dentist
        def add_dentist():
            def add_data():
                # if not phoneEntry.get().isdigit():
                # messagebox.showerror("Error", "time number must be a number")
                # return

                if d_nameEntry.get() == '' or designationEntry.get() == '' or phoneEntry.get() == '' or \
                        sheduleEntry.get() == '':
                    messagebox.showerror('Error', 'All Feilds are required',
                                         parent=add_window)  # if not given all entry

                    if d_nameEntry.get() == "":
                        d_nameLabel.config(text='Name *', fg='red')
                    else:
                        d_nameLabel.config(text='Name ', fg='white')

                    if designationEntry.get() == '':
                        designationLabel.config(text='Designation *', fg='red')
                    else:
                        designationLabel.config(text='Designation ', fg='white')

                    if phoneEntry.get() == '':
                        phoneLabel.config(text='phone *', fg='red')
                    else:
                        phoneLabel.config(text='phone', fg='white')

                    if sheduleEntry.get() == '':
                        sheduleLabel.config(text='schedule *', fg='red')
                    else:
                        sheduleLabel.config(text='schedule ', fg='white')

                    return

                if not phoneEntry.get().isdigit() or len(phoneEntry.get()) != 10:
                    messagebox.showerror("Error", "Phone number must be 10 digits and must be integer",
                                         parent=add_window)
                    phoneLabel.config(text='phone *', fg='red')
                    return

                    # if the phone number is valid, set the phoneLabel color to white
                phoneLabel.config(text='phone', fg='white')

                query = "INSERT INTO ddetail (d_name, designation, phone,shedule) VALUES (  %s, %s, %s,%s)"
                values = (d_nameEntry.get(), designationEntry.get(), phoneEntry.get(), sheduleEntry.get())
                mycursor.execute(query, values)
                conn.commit()
                d_nameLabel.config(text='Name ', fg='white')
                designationLabel.config(text='Designation', fg='white')
                phoneLabel.config(text='Phone', fg='white')
                sheduleLabel.config(text='Schedule', fg='white')

                result = messagebox.askyesno('confirm', 'Data added successfully!.\nDo you want to clear the form?',
                                             parent=add_window)
                print(result)
                if result:  # If click yes
                    # idEntry.delete(0, END)
                    d_nameEntry.delete(0, END)
                    designationEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    sheduleEntry.delete(0, END)
                else:
                    pass

                query = 'select *from ddetail'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                dtable.delete(*dtable.get_children())
                for data in fetched_data:
                    dtable.insert('', END, values=data)

            add_window = Toplevel()
            add_window.configure(bg='#7868d5')
            add_window.grab_set()
            add_window.resizable(False, False)

            # idLabel = Label(add_window, text='Id', font=('times new roman', 20, 'bold'))
            # idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
            # idEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, )
            # idEntry.grid(row=0, column=1, pady=15, padx=10)

            d_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            d_nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
            d_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            d_nameEntry.grid(row=0, column=1, pady=15, padx=10)

            designationLabel = Label(add_window, text='designation', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                     fg='white')
            designationLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
            designationEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            designationEntry.grid(row=2, column=1, pady=15, padx=10)

            phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            phoneLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
            phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            phoneEntry.grid(row=3, column=1, pady=15, padx=10)

            sheduleLabel = Label(add_window, text='Dentist Schedule', font=('times new roman', 20, 'bold'),
                                 bg='#7868d5', fg='white')
            sheduleLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
            sheduleEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            sheduleEntry.grid(row=4, column=1, pady=15, padx=10)

            d_button = ttk.Button(add_window, text='Add ', command=add_data)
            d_button.grid(row=6, columnspan=2, pady=15)

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
        logo = PhotoImage(file='dentistpic.png')
        logolable = Label(leftFrame, image=logo, bg='white')
        logolable.grid(row=0, column=0, padx=50)

        # lift the left frame to be on top of the image
        leftFrame.lift()

        # for designation and time on window
        datetimeLabel = Label(self.master, font=('times new roman', 10, 'bold'), bg='white')
        datetimeLabel.place(x=25, y=30)
        clock()

        # Create a label widget
        label1 = Label(self.master, text='Dentist Detials', font=('Arial', 10, 'bold'), bg="white", fg='#7868d5')

        # Add the label to the window using pack method
        label1.pack(side=TOP, padx=10, pady=30)
        # button on frameleft
        adddButton = tk.Button(leftFrame, text='add dentist', width=30, height=2, command=add_dentist)
        adddButton.configure(bg='#7868d5', fg='white')
        adddButton.grid(row=1, column=0, pady=20)

        sbtn = Button(leftFrame, width=30, height=2, text="show dentist", bg="#7868d5", fg="white",
                      command=show_dentist)
        sbtn.grid(row=2, column=0, pady=20)

        ebtn = Button(leftFrame, width=30, height=2, text="Exit", bg="#7868d5", fg="white", command=exit_dentist)
        ebtn.grid(row=3, column=0, pady=20)
        # right frame
        rightFrame = Frame(self.master)
        rightFrame.configure(bg="white")
        rightFrame.place(x=320, y=65, width=650, height=450)

        # treeview

        scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

        dtable = ttk.Treeview(rightFrame, columns=('id', 'd_name', 'designation', 'phone', 'shedule'),
                              xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

        scrollBarX.config(command=dtable.xview)
        scrollBarY.config(command=dtable.yview)

        scrollBarX.pack(side=BOTTOM, fill=X)
        scrollBarY.pack(side=RIGHT, fill=Y)

        dtable.pack(expand=1, fill=BOTH)

        dtable.heading("id", text='Id')
        dtable.heading("d_name", text='Dentist Name')
        dtable.heading("designation", text='Designation')
        dtable.heading("phone", text='Phone no.')
        dtable.heading("shedule", text='Dentist Schedule')

        dtable.column("id", width=200, anchor=CENTER)
        dtable.column("d_name", width=300, anchor=CENTER)
        dtable.column("designation", width=100, anchor=CENTER)
        dtable.column("phone", width=300, anchor=CENTER)
        dtable.column("shedule", width=200, anchor=CENTER)

        style = ttk.Style()

        style.configure('Treeview', rowheight=25, font=('arial', 10, 'bold'), fieldbackground='white',
                        background='white', )
        style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='#7868d5')

        dtable.config(show='headings')
        self.master.mainloop()


if __name__ == "__main__":
    root = Tk()
    dentistdetailpage = Dentist(root)
    root.mainloop()

'''from tkinter import *
import time
from tkinter import messagebox, ttk
from tkinter.ttk import Combobox
import tkinter as tk
import mysql.connector

global logo
logo = None


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


def show_dentist():
    query = 'select * from ddetail'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    dtable.delete(*dtable.get_children())
    for data in fetched_data:
        dtable.insert('', END, values=data)


# exit button
def exit_dentist():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        dentist_window.destroy()
        import receptionist_home
    else:
        pass


# add_dentist
def add_dentist():
    def add_data():
        # if not phoneEntry.get().isdigit():
        # messagebox.showerror("Error", "time number must be a number")
        # return

        if d_nameEntry.get() == '' or designationEntry.get() == '' or phoneEntry.get() == ''or sheduleEntry.get()=='':
            messagebox.showerror('Error', 'All Feilds are required', parent=add_window)  # if not given all entry
            
            if d_nameEntry.get() == "":
                d_nameLabel.config(text='Name *', fg='red')


            else:
                d_nameLabel.config(text='Name ', fg='black')


            if designationEntry.get() == '':
                designationLabel.config(text='Designation *', fg='red')


            else:
                designationLabel.config(text='Designation ', fg='black')


            if phoneEntry.get() == '':
                phoneLabel.config(text='phone *', fg='red')


            else:
                phoneLabel.config(text='phone', fg='black')


            if sheduleEntry.get() == '':
                sheduleLabel.config(text='schedule *', fg='red')


            else:
                sheduleLabel.config(text='schedule ', fg='black')



            return

        if not phoneEntry.get().isdigit() or len(phoneEntry.get()) != 10:
            messagebox.showerror("Error", "Phone number must be 10 digits and must be integer")
            phoneLabel.config(text='phone *', fg='red')
            return

            # if the phone number is valid, set the phoneLabel color to black
        phoneLabel.config(text='phone', fg='black')





        query = "INSERT INTO ddetail (d_name, designation, phone,shedule) VALUES (  %s, %s, %s,%s)"
        values = (d_nameEntry.get(), designationEntry.get(), phoneEntry.get(), sheduleEntry.get())
        mycursor.execute(query, (values))
        conn.commit()
        d_nameLabel.config(text='Name ', fg='black')
        designationLabel.config(text='Designation', fg='black')
        phoneLabel.config(text='Phone', fg='black')
        sheduleLabel.config(text='Schedule', fg='black')

        result = messagebox.askyesno('confirm', 'Data added successfully!.\nDo you want to clear the form?')
        print(result)
        if result:  # If click yes
            # idEntry.delete(0, END)
            d_nameEntry.delete(0, END)
            designationEntry.delete(0, END)
            phoneEntry.delete(0, END)
            sheduleEntry.delete(0, END)
        else:
            pass


        query = 'select *from ddetail'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        dtable.delete(*dtable.get_children())
        for data in fetched_data:
            dtable.insert('', END, values=data)

    add_window = Toplevel()
    add_window.grab_set()
    add_window.resizable(False, False)

    #idLabel = Label(add_window, text='Id', font=('times new roman', 20, 'bold'))
    #idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    #idEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, )
    #idEntry.grid(row=0, column=1, pady=15, padx=10)

    d_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    d_nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    d_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    d_nameEntry.grid(row=0, column=1, pady=15, padx=10)

    designationLabel = Label(add_window, text='designation', font=('times new roman', 20, 'bold'))
    designationLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    designationEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    designationEntry.grid(row=2, column=1, pady=15, padx=10)

    phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=3, column=1, pady=15, padx=10)

    sheduleLabel = Label(add_window, text='Dentist Schedule', font=('times new roman', 20, 'bold'))
    sheduleLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    sheduleEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    sheduleEntry.grid(row=4, column=1, pady=15, padx=10)

    d_button = ttk.Button(add_window, text='Add ', command=add_data)
    d_button.grid(row=6, columnspan=2, pady=15)


# ------------------------------gui-----------------------------------------

dentist_window = Tk()
dentist_window.title("dentist details")
dentist_window.geometry("1000x563+10+10")
dentist_window.resizable(0, 0)  # for fixed sized window

# define image

bg = PhotoImage(file="page.png")
my_label = Label(dentist_window, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

# leftframe
leftFrame = Frame(dentist_window, bg="white")
leftFrame.place(x=30, y=65, width=300, height=450)

logo = PhotoImage(file='dentistpic.png')
logolable = Label(leftFrame, image=logo, bg='white')
logolable.grid(row=0, column=0, padx=50)

# lift the left frame to be on top of the image
leftFrame.lift()

# for designation and time on window
datetimeLabel = Label(dentist_window, font=('times new roman', 10, 'bold'), bg='white')
datetimeLabel.place(x=25, y=30)
clock()

# Create a label widget
label1 = Label(dentist_window, text='Office View', font=('Arial', 10, 'bold'), bg="white", fg='black')

# Add the label to the window using pack method
label1.pack(side=TOP, padx=10, pady=30)
# button on frameleft
adddButton = tk.Button(leftFrame, text='add dentist', width=30, height=2,command=add_dentist)
adddButton.configure(bg='#7868d5', fg='white')
adddButton.grid(row=1, column=0, pady=20)

sbtn = Button(leftFrame, width=30, height=2, text="show dentist", bg="#7868d5", fg="white", command=show_dentist)
sbtn.grid(row=2, column=0, pady=20)

ebtn = Button(leftFrame, width=30, height=2, text="Exit", bg="#7868d5", fg="white", command=exit_dentist)
ebtn.grid(row=3, column=0, pady=20)
# right frame
rightFrame = Frame(dentist_window)
rightFrame.configure(bg="white")
rightFrame.place(x=320, y=65, width=650, height=450)

# treeview

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

dtable = ttk.Treeview(rightFrame, columns=('id', 'd_name', 'designation', 'phone', 'shedule'),
                      xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=dtable.xview)
scrollBarY.config(command=dtable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

dtable.pack(expand=1, fill=BOTH)

dtable.heading("id", text='Id')
dtable.heading("d_name", text='Dentist Name')
dtable.heading("designation", text='Designation')
dtable.heading("phone", text='Phone no.')
dtable.heading("shedule", text='Dentist Schedule')

dtable.column("id", width=200, anchor=CENTER)
dtable.column("d_name", width=300, anchor=CENTER)
dtable.column("designation", width=100, anchor=CENTER)
dtable.column("phone", width=300, anchor=CENTER)
dtable.column("shedule", width=200, anchor=CENTER)

style = ttk.Style()

style.configure('Treeview', rowheight=25, font=('arial', 10, 'bold'), fieldbackground='white', background='white', )
style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='#7868d5')

dtable.config(show='headings')
dentist_window.mainloop()'''
