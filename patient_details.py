# --------functionality----------
# import libraries
from tkinter import *
import time
import re
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

logo = idEntry = p_nameEntry = ageEntry = phoneEntry = ap_timeEntry = fees_paidEntry = statusEntry = screen = \
    bg = my_label1 = date = mycursor = con = currenttime = bg1 = my_label = None


class Patient:
    def __init__(self, master):
        self.master = master
        self.master.title('Patient details')
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)

        # top level method
        def toplevel_patient(title, button_text, command):
            global idEntry, p_nameEntry, ageEntry, phoneEntry, ap_timeEntry, fees_paidEntry, statusEntry, screen
            screen = Toplevel()
            screen.configure(bg="#7868d5")
            screen.title(title)
            screen.grab_set()
            screen.resizable(False, False)
            idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
            idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            idEntry.grid(row=0, column=1, pady=15, padx=10)

            p_nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            p_nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
            p_nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            p_nameEntry.grid(row=1, column=1, pady=15, padx=10)

            ageLabel = Label(screen, text='Age', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            ageLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
            ageEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            ageEntry.grid(row=3, column=1, pady=15, padx=10)

            phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
            phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            phoneEntry.grid(row=2, column=1, pady=15, padx=10)

            ap_timeLabel = Label(screen, text='Appointment time', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                 fg='white')
            ap_timeLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
            ap_timeEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            ap_timeEntry.grid(row=4, column=1, pady=15, padx=10)

            fees_paidLabel = Label(screen, text='Fees paid', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                   fg='white')
            fees_paidLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
            fees_paidEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
            fees_paidEntry.grid(row=5, column=1, pady=15, padx=10)

            statusLabel = Label(screen, text='Status', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            statusLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
            statusEntry = Entry(screen, font=('roman', 15, 'bold'), width=24, )
            statusEntry.insert(0, "pending")
            statusEntry.grid(row=6, column=1, pady=15, padx=10)

            p_button = ttk.Button(screen, text=button_text, command=command)
            p_button.grid(row=7, columnspan=2, pady=15)
            if title == 'Update patient':
                indexing = ptable.focus()

                content = ptable.item(indexing)
                listdata = content['values']
                idEntry.insert(0, listdata[0])
                p_nameEntry.insert(0, listdata[1])
                ageEntry.insert(0, listdata[2])
                phoneEntry.insert(0, listdata[3])
                ap_timeEntry.insert(0, listdata[4])
                fees_paidEntry.insert(0, listdata[5])
                statusEntry.insert(0, listdata[6])

        # exit button
        def iexit():
            result = messagebox.askyesno('Confirm', 'Do you want to exit?', parent=self.master)
            if result:
                self.master.destroy()
                import receptionist_home
            else:
                pass

        # show patiet
        def show_patient():
            query = 'select * from pdetail'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            ptable.delete(*ptable.get_children())
            for data in fetched_data:
                ptable.insert('', END, values=data)

        # delete the patient cha code modify
        # delete patient
        def delete_patient():
            selected_item = ptable.selection()
            if not selected_item:
                messagebox.showwarning("Warning!", "Please select a patient.", parent=self.master)
                return
            if selected_item:
                if messagebox.askyesno('confirm', 'are you sure you want to delete?', parent=self.master):
                    content = ptable.item(selected_item)
                    content_id = content['values'][0]
                    query = "SELECT * FROM pdetail WHERE id = %s"
                    mycursor.execute(query, (content_id,))
                    deleted_data = mycursor.fetchone()  # get the deleted data
                    if not deleted_data:
                        messagebox.showwarning("Warning!", "Selected patient not found.")
                        return
                    if deleted_data:
                        recycle_query = "INSERT INTO deleted_pdetail (id, p_name, age, phone, ap_time, fees_paid, " \
                                        "status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        mycursor.execute(recycle_query,
                                         deleted_data)  # move the deleted data into the deleted_pdetail table
                        query = "DELETE FROM pdetail WHERE id = %s"
                        mycursor.execute(query, (content_id,))
                        con.commit()
                        messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully', parent=self.master)
                        ptable.delete(selected_item)
                        if messagebox.askyesno('Select', 'Do you want to view deleted record?', parent=self.master):
                            recycle_data()
            else:
                return

        def recycle_data():
            # Create a new window to show deleted records
            recycle_window = Toplevel()
            recycle_window.title("Recycle Bin")
            recycle_window.geometry("1000x563+10+10")
            recycle_window.resizable(0, 0)  # for fixed sized window
            global bg, my_label1
            bg = PhotoImage(file="page.png")
            recycle_window.bg = bg  # assign to a persistent object
            my_label1 = Label(recycle_window, image=recycle_window.bg)
            my_label1.place(x=0, y=0, relwidth=1, relheight=1)

            # title
            label1 = Label(recycle_window, text="Recycle bin", font=("Arial", 14), bg="white", fg="#7868d5")
            label1.place(x=450, y=30)

            # leftframe
            leftFrame = Frame(recycle_window)
            leftFrame.configure(bg="white")
            leftFrame.place(x=30, y=65, width=300, height=450)
            leftFrame.lift()

            # right frame  deleted table recycle deleted_table treeview
            rightFrame = Frame(recycle_window)
            rightFrame.configure(bg="white")
            rightFrame.place(x=320, y=65, width=650, height=450)
            scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
            scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
            deleted_table = ttk.Treeview(rightFrame,
                                         columns=('id', 'p_name', 'age', 'phone', 'ap_time', 'fees_paid', 'status'),
                                         xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

            scrollBarX.config(command=deleted_table.xview)
            scrollBarY.config(command=deleted_table.yview)

            scrollBarX.pack(side=BOTTOM, fill=X)
            scrollBarY.pack(side=RIGHT, fill=Y)

            # Display a list of deleted records deleted_table = ttk.Treeview(recycle_window, columns=('id','p_name',
            # 'age', 'phone', 'ap_time', 'fees_paid', 'status'))
            deleted_table.heading('id', text='ID')
            deleted_table.heading('p_name', text='Name')
            deleted_table.heading('age', text='Age')
            deleted_table.heading('phone', text='Phone')
            deleted_table.heading('ap_time', text='Appointment Time')
            deleted_table.heading('fees_paid', text='Fees Paid')
            deleted_table.heading('status', text='Status')
            deleted_table['show'] = 'headings'
            deleted_table.pack(fill=BOTH, expand=1)

            query = "SELECT * FROM deleted_pdetail"
            mycursor.execute(query)
            deleted_data = mycursor.fetchall()
            for data in deleted_data:
                deleted_table.insert('', END, values=data)

            def restore_data():
                selected_item = deleted_table.selection()
                if not selected_item:
                    messagebox.showwarning("Warning!", "Please select a patient.", parent=recycle_window)
                    return
                if selected_item:
                    content = deleted_table.item(selected_item)
                    content_id = content['values'][0]
                    query = "INSERT INTO pdetail SELECT * FROM deleted_pdetail WHERE id = %s"
                    mycursor.execute(query, (content_id,))
                    con.commit()
                    messagebox.showinfo('Restored', f'Id {content_id} is restored successfully', parent=recycle_window)

                    # Delete the restored item from deleted_pdetail table
                    query = "DELETE FROM deleted_pdetail WHERE id = %s"
                    mycursor.execute(query, (content_id,))
                    con.commit()

                    # Remove the restored item from deleted_table widget
                    deleted_table.delete(selected_item)

                    # Fetch the data from the deleted_pdetail table
                    query = 'SELECT * FROM deleted_pdetail'
                    mycursor.execute(query)
                    fetched_data = mycursor.fetchall()

                    # Repopulate the deleted_table with the updated data
                    deleted_table.delete(*deleted_table.get_children())
                    for data in fetched_data:
                        deleted_table.insert('', END, values=data)
                    recycle_window.destroy()

                    # Fetch the data from the pdetail table and repopulate the main_table with the updated data
                    # load_data()

            def delete_permanently():
                selected_item = deleted_table.selection()
                if not selected_item:
                    messagebox.showwarning("Warning!", "Please select a patient.", parent=recycle_window)
                    return
                content = deleted_table.item(selected_item)
                content_id = content['values'][0]

                # Execute DELETE query to remove record permanently
                query = "DELETE FROM deleted_pdetail WHERE id = %s"
                mycursor.execute(query, (content_id,))
                con.commit()
                messagebox.showinfo('Deleted', f'Id {content_id} is deleted permanently', parent=recycle_window)

                # Fetch the deleted record from deleted_pdetail table
                query = "SELECT * FROM deleted_pdetail"
                mycursor.execute(query)
                deleted_record = mycursor.fetchall()
                print(deleted_record)
                if deleted_record is not None:
                    deleted_table.delete(*deleted_table.get_children())
                    for data in deleted_record:
                        deleted_table.insert('', END, values=data)
                if deleted_record is None:
                    messagebox.showerror('', 'no records in recycle bin', parent=self.master)

                # if deleted_record is not None:
                # Insert the record back into pdetail table
                '''query = "INSERT INTO pdetail (id, p_name, age, phone, ap_time, fees_paid, status) VALUES (%s, %s, 
                %s, %s, %s, %s, %s)" values = ( deleted_record[0], deleted_record[1], deleted_record[2], 
                deleted_record[3], deleted_record[4], deleted_record[5], deleted_record[6]) mycursor.execute(query, 
                values) con.commit() messagebox.showinfo('Recycled', f'Id {content_id} is recycled successfully')'''

                '''# Delete the record from deleted_pdetail table
                query = "DELETE FROM deleted_pdetail WHERE id = %s"
                mycursor.execute(query, (content_id,))
                con.commit()
                load_data()
                load_deleted_data()'''

                # else:
                # messagebox.showerror('Error', f'Id {content_id} not found in deleted_pdetail table')

            # Refresh the tables
            def load_data():
                query = 'SELECT * FROM pdetail'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                deleted_table.delete(*deleted_table.get_children())
                for data in fetched_data:
                    deleted_table.insert('', END, values=data)

            def load_deleted_data():
                query = 'SELECT * FROM deleted_patients'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                deleted_table.delete(*deleted_table.get_children())
                for data in fetched_data:
                    deleted_table.insert('', END, values=data)

            # Add buttons to permanently delete or restore records

            # button on frameleft
            global logo
            logo = PhotoImage(file='cloud-storage .png')
            logolable = Label(recycle_window, image=logo, bg='white')
            logolable.grid(row=0, column=0, padx=100, pady=40)
            restore_button = tk.Button(leftFrame, text='restore', width=25, command=restore_data)
            restore_button.configure(bg='#7868d5', fg='white', font='bold')
            restore_button.place(x=30, y=140)
            # restore_button.grid(row=1,column=0,pady=60)
            delete_button = tk.Button(leftFrame, text='delete permanent', width=25, command=delete_permanently)
            delete_button.configure(bg='#7868d5', fg='white', font='bold')
            delete_button.place(x=30, y=220)
            exit_button = Button(leftFrame, text="Exit", command=recycle_window.destroy, width=25)
            exit_button.configure(bg='#EE82EE', fg='white', font='bold')
            exit_button.place(x=30, y=300)

        # search patient
        def search_data():
            query = 'select * from pdetail where id=%s or p_name=%s or age=%s or phone=%s or ap_time=%s or ' \
                    'fees_paid=%s or status=%s'
            mycursor.execute(query, (
                idEntry.get(), p_nameEntry.get(), ageEntry.get(), phoneEntry.get(), ap_timeEntry.get(),
                fees_paidEntry.get(), statusEntry.get()))
            ptable.delete(*ptable.get_children())
            fetched_data = mycursor.fetchall()
            if not fetched_data:
                messagebox.showinfo('no records found!', 'no matching records were found!', parent=self.master)
            else:
                for data in fetched_data:
                    ptable.insert('', END, values=data)

        # update button
        def update_data():
            id = idEntry.get()
            # Check if the ID exists in the database
            mycursor.execute("SELECT * FROM pdetail WHERE id = %s", (id,))
            result = mycursor.fetchone()
            if not result:
                messagebox.showerror('Error', f'Id {id} does not exist .\nplease use valid id', parent=screen)
                return
            # If the ID exists, fetch the existing data
            existing_data = result[1:]  # ignore the first column 'id'
            # Get the new data entered by the user
            phone = phoneEntry.get()
            if phone and (len(phone) != 10 or not phone.isdigit()):
                messagebox.showerror("Error", "Phone number must be 10 digits and must be integer")
                return
            new_data = [p_nameEntry.get(), ageEntry.get(), phone, ap_timeEntry.get(), fees_paidEntry.get(),
                        statusEntry.get()]

            # Replace empty fields with existing data
            for i in range(len(new_data)):
                if new_data[i] == "":
                    new_data[i] = existing_data[i]
            # Execute the update query
            query = 'UPDATE pdetail SET p_name=%s, age=%s, phone=%s, ap_time=%s, fees_paid=%s, status=%s WHERE id=%s'
            val = (new_data[0], new_data[1], new_data[2], new_data[3], new_data[4], new_data[5], id)
            mycursor.execute(query, val)
            con.commit()
            messagebox.showinfo('Success', f'Id {id} is modified successfully', parent=screen)
            screen.destroy()
            show_patient()

        sticky = W  # for all label on left

        # add_patient
        def add_patient():
            def add_data():
                # if not phoneEntry.get().isdigit():
                # messagebox.showerror("Error", "Phone number must be a number")
                # return

                if p_nameEntry.get() == '' or ageEntry.get() == '' or phoneEntry.get() == '' or \
                        ap_timeEntry.get() == '' or fees_paidEntry.get() == '' or statusEntry.get() == '':
                    messagebox.showerror('Error', 'All Feilds are required',
                                         parent=add_window)  # if not given all entry

                    if p_nameEntry.get() == "":
                        p_nameLabel.config(text='Name *', fg='red')
                    else:
                        p_nameLabel.config(text='Name ', fg='white')

                    if ageEntry.get() == '':
                        ageLabel.config(text='Age *', fg='red')
                    else:
                        ageLabel.config(text='Age', fg='white')

                    if phoneEntry.get() == '':
                        phoneLabel.config(text='Phone *', fg='red')
                    else:
                        phoneLabel.config(text='Phone', fg='white')

                    if ap_timeEntry.get() == '':
                        ap_timeLabel.config(text='Appointment time *', fg='red')
                    else:
                        ap_timeLabel.config(text='Appointment time ', fg='white')

                    if fees_paidEntry.get() == '':
                        fees_paidLabel.config(text='Fees paid *', fg='red')
                    else:
                        fees_paidLabel.config(text='Fees paid ', fg='white')

                    if statusEntry.get() == '':
                        statusLabel.config(text='Status*', fg='red')
                    else:
                        statusLabel.config(text='Status ', fg='white')

                    return

                else:  # for entering values in table
                    if not phoneEntry.get().isdigit() or len(phoneEntry.get()) != 10:
                        messagebox.showerror("Error", "Phone number must be 10 digits and must be integer",
                                             parent=add_window)
                        phoneLabel.config(text='Phone *', fg='red')
                        return

                        # if the phone number is valid, set the phoneLabel color to black
                    phoneLabel.config(text='Phone', fg='white')

                    try:

                        query = "INSERT INTO pdetail ( p_name, age, phone, ap_time, fees_paid,status) VALUES " \
                                "( %s, %s, %s, %s, %s,%s)"
                        values = (p_nameEntry.get(), ageEntry.get(), phoneEntry.get(), ap_timeEntry.get(),
                                  fees_paidEntry.get(), statusEntry.get())
                        mycursor.execute(query, values)
                        con.commit()
                        p_nameLabel.config(text='Name', fg='white')
                        ageLabel.config(text='Age', fg='white')
                        phoneLabel.config(text='Phone', fg='white')
                        ap_timeLabel.config(text='Appointment time', fg='white')
                        fees_paidLabel.config(text='Fees paid', fg='white')
                        statusLabel.config(text='Status', fg='white')

                        result = messagebox.askyesno('condirm',
                                                     'Data added sucessfully!.\nDo you want to clear the form?',
                                                     parent=add_window)
                        print(result)
                        if result:  # If click yes
                            # idEntry.delete(0, END)
                            p_nameEntry.delete(0, END)
                            ageEntry.delete(0, END)
                            phoneEntry.delete(0, END)
                            ap_timeEntry.delete(0, END)
                            fees_paidEntry.delete(0, END)
                            # statusEntry.delete(0, END)

                        else:
                            pass
                    except:
                        messagebox.showerror('Error', 'Id cannot be repeated', parent=add_window)
                        return

                    query = 'select *from pdetail'
                    mycursor.execute(query)
                    fetched_data = mycursor.fetchall()
                    ptable.delete(*ptable.get_children())
                    for data in fetched_data:
                        ptable.insert('', END, values=data)

            add_window = Toplevel()
            add_window.configure(bg="#7868d5")
            add_window.grab_set()
            add_window.resizable(False, False)
            p_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            p_nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
            p_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            p_nameEntry.grid(row=0, column=1, pady=15, padx=10)

            ageLabel = Label(add_window, text='Age', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            ageLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
            ageEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            ageEntry.grid(row=1, column=1, pady=15, padx=10)

            phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'), bg='#7868d5', fg='white')
            phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
            phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            phoneEntry.grid(row=2, column=1, pady=15, padx=10)

            ap_timeLabel = Label(add_window, text='Appointment time', font=('times new roman', 20, 'bold'),
                                 bg='#7868d5', fg='white')
            ap_timeLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
            ap_timeEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            ap_timeEntry.grid(row=3, column=1, pady=15, padx=10)

            fees_paidLabel = Label(add_window, text='Fees paid', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                   fg='white')
            fees_paidLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
            fees_paidEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
            fees_paidEntry.grid(row=4, column=1, pady=15, padx=10)

            statusLabel = Label(add_window, text='Status', font=('times new roman', 20, 'bold'), bg='#7868d5',
                                fg='white')
            statusLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
            statusEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, )
            statusEntry.insert(0, "pending")
            statusEntry.grid(row=5, column=1, pady=15, padx=10)

            p_button = ttk.Button(add_window, text='Add data', command=add_data)
            p_button.grid(row=7, columnspan=2, pady=15)

        # connecting database
        def connect_database():
            def connect():
                global mycursor, con
                try:
                    con = mysql.connector.connect(host='localhost', user='user1',
                                                  passwd='1234')  # con is used to commit the changes
                    mycursor = con.cursor()
                    messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)
                except:
                    messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
                    return
                try:
                    # create new database as database is already created as database is alreadycreated so he
                    # except block code is executed
                    query = 'create database dcms'
                    mycursor.execute(query)
                    query = 'use dcms'
                    mycursor.execute(query)
                    query = 'create table pdetail(id int  AUTO_INCREMENT primary key , p_name varchar(30) not null ,' \
                            'age int not null,phone bigint not null,ap_time varchar(20) not null,fees_paid varchar(' \
                            '20) not null,status varchar(30) default "pending")'
                    mycursor.execute(query)
                except:
                    query = 'use dcms'
                    mycursor.execute(query)

                    # query = 'create table pdetail(id INT AUTO_INCREMENT primary key, p_name varchar(30) not null ,
                    # age int not null,phone bigint not null,ap_time varchar(20) not null,fees_paid varchar(20) not
                    # null,status varchar(30) default "pending")' mycursor.execute(query) query = 'create table
                    # pdetail(id varchar(30)  primary key, p_name varchar(30) not null ,age int not null,phone bigint
                    # not null,ap_time varchar(20) not null,fees_paid varchar(20) not null)' mycursor.execute(query)

                connectWindow.destroy()
                addpButton.config(state=NORMAL)
                searchpButton.config(state=NORMAL)
                updatepButton.config(state=NORMAL)
                showpButton.config(state=NORMAL)
                deletepButton.config(state=NORMAL)
                recypButton.config(state=NORMAL)

            connectWindow = Toplevel()
            connectWindow.grab_set()
            connectWindow.geometry('470x250+730+230')
            connectWindow.title('Database Connection')
            connectWindow.resizable(0, 0)

            hostnameLabel = Label(connectWindow, text='Host Name', font=('arial', 20, 'bold'))
            hostnameLabel.grid(row=0, column=0, padx=20)

            hostEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
            hostEntry.grid(row=0, column=1, padx=40, pady=20)

            usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
            usernameLabel.grid(row=1, column=0, padx=20)

            usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
            usernameEntry.grid(row=1, column=1, padx=40, pady=20)

            passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
            passwordLabel.grid(row=2, column=0, padx=20)

            passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
            passwordEntry.grid(row=2, column=1, padx=40, pady=20)

            connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
            connectButton.grid(row=3, columnspan=2)

        count = 0
        text = ''

        # clock method for date and time
        def clock():
            global date, currenttime
            date = time.strftime('%d/%m/%Y')
            currenttime = time.strftime('%H:%M:%S')
            datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
            datetimeLabel.after(1000, clock)

        # ------------gui part-------------------------------

        # define image
        global bg1, my_label
        bg1 = PhotoImage(file="page.png")
        my_label = Label(self.master, image=bg1)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # for date and time on window
        datetimeLabel = Label(self.master, font=('times new roman', 10, 'bold'), bg='white')
        datetimeLabel.place(x=25, y=30)
        clock()

        # title
        label1 = Label(self.master, text="patient details", font=("Arial", 14, 'bold'), bg='white', fg='#7868d5')
        label1.place(x=319, y=32, width=655)
        # connect button : connect to database when click
        connectButton = tk.Button(self.master, text='Connect database', command=connect_database)
        connectButton.configure(bg='white', fg='black')
        connectButton.place(x=850, y=35)

        # leftframe
        leftFrame = Frame(self.master)
        leftFrame.configure(bg="#7868d5")
        leftFrame.place(x=24, y=65, width=350, height=450)

        # button on frameleft
        addpButton = tk.Button(leftFrame, text='add data', width=25, state=DISABLED,
                               command=add_patient)  # lambda :toplevel_patient('Add Patient', 'Add', add_data))
        addpButton.configure(bg='white', fg='#7868d5')
        addpButton.grid(row=1, column=0, padx=45, pady=20)

        searchpButton = tk.Button(leftFrame, text='Search Patient', width=25, state=DISABLED,
                                  command=lambda: toplevel_patient('Search Patient', 'Search', search_data))
        searchpButton.configure(bg='white', fg='#7868d5')
        searchpButton.grid(row=2, column=0, padx=45, pady=20)

        deletepButton = tk.Button(leftFrame, text='Delete Patient', width=25, state=DISABLED, command=delete_patient)
        deletepButton.configure(bg='white', fg='#7868d5')
        deletepButton.grid(row=3, column=0, padx=45, pady=20)

        updatepButton = tk.Button(leftFrame, text='Update Patient', width=25, state=DISABLED,
                                  command=lambda: toplevel_patient('Update Patient', 'Update', update_data))
        updatepButton.configure(bg='white', fg='#7868d5')
        updatepButton.grid(row=4, column=0, padx=45, pady=20)

        showpButton = tk.Button(leftFrame, text='Show Patient', width=25, state=DISABLED, command=show_patient)
        showpButton.configure(bg='white', fg='#7868d5')
        showpButton.grid(row=5, column=0, padx=45, pady=20)

        recypButton = tk.Button(leftFrame, text='Recycle bin', width=25, state=DISABLED, command=recycle_data)
        recypButton.configure(bg='white', fg='#7868d5')
        recypButton.grid(row=6, column=0, padx=45, pady=20)

        exitButton = tk.Button(leftFrame, text='Exit', width=25, command=iexit)
        exitButton.configure(bg='white', fg='#7868d5')
        exitButton.grid(row=7, column=0, padx=45, pady=20)
        # right frame
        rightFrame = Frame(self.master)
        rightFrame.configure(bg='white')
        rightFrame.place(x=320, y=65, width=650, height=450)

        # treeview

        scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

        ptable = ttk.Treeview(rightFrame, columns=('id', 'p_name', 'age', 'phone', 'ap_time', 'fees_paid', 'status'),
                              xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

        scrollBarX.config(command=ptable.xview)
        scrollBarY.config(command=ptable.yview)

        scrollBarX.pack(side=BOTTOM, fill=X)
        scrollBarY.pack(side=RIGHT, fill=Y)

        ptable.pack(expand=1, fill=BOTH)

        ptable.heading("id", text='Id')
        ptable.heading("p_name", text='Patient Name')
        ptable.heading("age", text='Age')
        ptable.heading("phone", text='Mobile no')
        ptable.heading("ap_time", text='Appointment time')
        ptable.heading("fees_paid", text='Fees paid')
        ptable.heading("status", text='status')

        ptable.column("id", width=200, anchor=CENTER)
        ptable.column("p_name", width=300, anchor=CENTER)
        ptable.column("age", width=100, anchor=CENTER)
        ptable.column("phone", width=300, anchor=CENTER)
        ptable.column("ap_time", width=200, anchor=CENTER)
        ptable.column("fees_paid", width=300, anchor=CENTER)
        ptable.column("status", width=300, anchor=CENTER)

        style = ttk.Style()

        style.configure('Treeview', rowheight=25, font=('arial', 10, 'bold'), fieldbackground='white',
                        background='white', )
        style.configure('Treeview.Heading', font=('arial', 14, 'bold'), foreground='#7868d5')

        ptable.config(show='headings')

        self.master.mainloop()


if __name__ == "__main__":
    root = Tk()
    patientpage = Patient(root)
    root.mainloop()

'''#--------functionality----------
#import libraries
from tkinter import *
import time
import re
import tkinter as tk
from tkinter import ttk,messagebox
import mysql.connector
logo = None


#top level method
def toplevel_patient(title,button_text,command):
    global idEntry,p_nameEntry,ageEntry,phoneEntry,ap_timeEntry,fees_paidEntry,statusEntry,screen
    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    p_nameLabel = Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    p_nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    p_nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    p_nameEntry.grid(row=1, column=1, pady=15, padx=10)

    ageLabel = Label(screen, text='Age', font=('times new roman', 20, 'bold'))
    ageLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    ageEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    ageEntry.grid(row=3, column=1, pady=15, padx=10)

    phoneLabel = Label(screen, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    ap_timeLabel = Label(screen, text='Appointment time', font=('times new roman', 20, 'bold'))
    ap_timeLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    ap_timeEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    ap_timeEntry.grid(row=4, column=1, pady=15, padx=10)

    fees_paidLabel = Label(screen, text='Fees paid', font=('times new roman', 20, 'bold'))
    fees_paidLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    fees_paidEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    fees_paidEntry.grid(row=5, column=1, pady=15, padx=10)

    statusLabel = Label(screen, text='Status', font=('times new roman', 20, 'bold'))
    statusLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    statusEntry = Entry(screen, font=('roman', 15, 'bold'), width=24,)
    statusEntry.insert(0,"pending")
    statusEntry.grid(row=6, column=1, pady=15, padx=10)



    p_button = ttk.Button(screen, text=button_text, command=command)
    p_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update patient':
        indexing = ptable.focus()

        content = ptable.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        p_nameEntry.insert(0, listdata[1])
        ageEntry.insert(0, listdata[2])
        phoneEntry.insert(0, listdata[3])
        ap_timeEntry.insert(0, listdata[4])
        fees_paidEntry.insert(0, listdata[5])
        statusEntry.insert(0,listdata[6])

#exit button
def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        patient_details_window.destroy()
        import receptionist_home
    else:
        pass
#show patiet
def show_patient():
    query = 'select * from pdetail'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    ptable.delete(*ptable.get_children())
    for data in fetched_data:
        ptable.insert('', END, values=data)



#delete the patient cha code modify #delete patient def delete_patient(): selected_item = ptable.selection() if not 
selected_item: messagebox.showwarning("Warning!", "Please select a patient.") return if messagebox.askyesno(
'confirm','are you sure you want to delete?'): content = ptable.item(selected_item) content_id = content['values'][0] 
query = "SELECT * FROM pdetail WHERE id = %s" mycursor.execute(query, (content_id,)) deleted_data = 
mycursor.fetchone() # get the deleted data if not deleted_data: messagebox.showwarning("Warning!", "Selected patient 
not found.") return recycle_query = "INSERT INTO deleted_pdetail (id, p_name, age, phone, ap_time, fees_paid, 
status) VALUES (%s, %s, %s, %s, %s, %s, %s)" mycursor.execute(recycle_query, deleted_data) # move the deleted data 
into the deleted_pdetail table query = "DELETE FROM pdetail WHERE id = %s" mycursor.execute(query, (content_id,
)) con.commit() messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully') ptable.delete(
selected_item) if messagebox.askyesno('Select', 'Do you want to view deleted record?'): recycle_data() else: return


def recycle_data():
    # Create a new window to show deleted records
    recycle_window = Toplevel()
    recycle_window.title("Recycle Bin")
    recycle_window.geometry("1000x563+10+10")
    recycle_window.resizable(0, 0)  # for fixed sized window
    bg = PhotoImage(file="page.png")
    recycle_window.bg = bg  # assign to a persistent object
    my_label = Label(recycle_window, image=recycle_window.bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)

    # title
    label1 = Label(recycle_window, text="Recycle bin", font=("Arial", 14), bg="white", fg="#7868d5")
    label1.place(x=450, y=30)

    # leftframe
    leftFrame = Frame(recycle_window)
    leftFrame.configure(bg="white")
    leftFrame.place(x=30, y=65, width=300, height=450)
    leftFrame.lift()


    # right frame
    rightFrame = Frame(recycle_window)
    rightFrame.configure(bg="white")
    rightFrame.place(x=320, y=65, width=650, height=450)
    scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
    scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)
    deleted_table = ttk.Treeview(rightFrame, columns=('id', 'p_name', 'age', 'phone', 'ap_time', 'fees_paid', 'status'),
                                 xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

    scrollBarX.config(command=deleted_table.xview)
    scrollBarY.config(command=deleted_table.yview)

    scrollBarX.pack(side=BOTTOM, fill=X)
    scrollBarY.pack(side=RIGHT, fill=Y)



    # Display a list of deleted records #deleted_table = ttk.Treeview(recycle_window, columns=('id','p_name', 'age', 
    'phone', 'ap_time', 'fees_paid', 'status')) deleted_table.heading('id', text='ID') deleted_table.heading(
    'p_name', text='Name') deleted_table.heading('age', text='Age') deleted_table.heading('phone', text='Phone') 
    deleted_table.heading('ap_time', text='Appointment Time') deleted_table.heading('fees_paid', text='Fees Paid') 
    deleted_table.heading('status', text='Status') deleted_table['show'] = 'headings' deleted_table.pack(fill=BOTH, 
    expand=1)

    query = "SELECT * FROM deleted_pdetail"
    mycursor.execute(query)
    deleted_data = mycursor.fetchall()
    for data in deleted_data:
        deleted_table.insert('', END, values=data)

    def restore_data():
        selected_item = deleted_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning!", "Please select a patient.")
            return
        content = deleted_table.item(selected_item)
        content_id = content['values'][0]
        query = "INSERT INTO pdetail SELECT * FROM deleted_pdetail WHERE id = %s"
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Restored', f'Id {content_id} is restored successfully')

        # Delete the restored item from deleted_pdetail table
        query = "DELETE FROM deleted_pdetail WHERE id = %s"
        mycursor.execute(query, (content_id,))
        con.commit()

        # Remove the restored item from deleted_table widget
        deleted_table.delete(selected_item)

        # Fetch the data from the deleted_pdetail table
        query = 'SELECT * FROM deleted_pdetail'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()

        # Repopulate the deleted_table with the updated data
        deleted_table.delete(*deleted_table.get_children())
        for data in fetched_data:
            deleted_table.insert('', END, values=data)

        # Fetch the data from the pdetail table and repopulate the main_table with the updated data
        load_data()


    def delete_permanently():
        selected_item = deleted_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning!", "Please select a patient.")
            return
        content = deleted_table.item(selected_item)
        content_id = content['values'][0]

        # Execute DELETE query to remove record permanently
        query = "DELETE FROM deleted_pdetail WHERE id = %s"
        mycursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Id {content_id} is deleted permanently')

        # Fetch the deleted record from deleted_pdetail table
        query = "SELECT * FROM deleted_pdetail WHERE id = %s"
        mycursor.execute(query, (content_id,))
        deleted_record = mycursor.fetchone()

        if deleted_record is not None: # Insert the record back into pdetail table query = "INSERT INTO pdetail (id, 
        p_name, age, phone, ap_time, fees_paid, status) VALUES (%s, %s, %s, %s, %s, %s, %s)" values = (
        deleted_record[0], deleted_record[1], deleted_record[2], deleted_record[3], deleted_record[4], 
        deleted_record[5], deleted_record[6]) mycursor.execute(query, values) con.commit() messagebox.showinfo(
        'Recycled', f'Id {content_id} is recycled successfully')

            # Delete the record from deleted_pdetail table
            query = "DELETE FROM deleted_pdetail WHERE id = %s"
            mycursor.execute(query, (content_id,))
            con.commit()
            load_data()
            load_deleted_data()
        else:
            messagebox.showerror('Error', f'Id {content_id} not found in deleted_pdetail table')
    # Refresh the tables
    def load_data():
        query = 'SELECT * FROM pdetail'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        deleted_table.delete(*deleted_table.get_children())
        for data in fetched_data:
            deleted_table.insert('', END, values=data)


    def load_deleted_data():
        query = 'SELECT * FROM deleted_patients'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()
        deleted_table.delete(*deleted_table.get_children())
        for data in fetched_data:
            deleted_table.insert('', END, values=data)

    # Add buttons to permanently delete or restore records

    # button on frameleft
    global logo
    logo = PhotoImage(file='cloud-storage .png')
    logolable = Label(recycle_window, image=logo,bg='white')
    logolable.grid(row=0, column=0, padx=100,pady=40)
    restore_button = tk.Button(leftFrame, text='restore', width=25, command=restore_data)
    restore_button.configure(bg='#7868d5', fg='white',font='bold')
    restore_button.place(x=30,y=140)
    #restore_button.grid(row=1,column=0,pady=60)
    delete_button = tk.Button(leftFrame, text='delete permanent', width=25, command=delete_permanently)
    delete_button.configure(bg='#7868d5', fg='white',font='bold')
    delete_button.place(x=30,y=220)
    exit_button = Button(leftFrame, text="Exit", command=recycle_window.destroy,width=25)
    exit_button.configure(bg='#EE82EE',fg='white',font='bold')
    exit_button.place(x=30,y=300)




#search patient def search_data(): query = 'select * from pdetail where id=%s or p_name=%s or age=%s or phone=%s or 
ap_time=%s or fees_paid=%s or status=%s' mycursor.execute(query,(idEntry.get(),p_nameEntry.get(),ageEntry.get(),
phoneEntry.get(),ap_timeEntry.get(),fees_paidEntry.get(),statusEntry.get())) ptable.delete(*ptable.get_children()) 
fetched_data = mycursor.fetchall() if not fetched_data: messagebox.showinfo('no records found!', 'no matching records 
were found!') else: for data in fetched_data: ptable.insert('', END, values=data)

#update button
def update_data():
    id = idEntry.get()
    # Check if the ID exists in the database
    mycursor.execute("SELECT * FROM pdetail WHERE id = %s", (id,))
    result = mycursor.fetchone()
    if not result:
        messagebox.showerror('Error', f'Id {id} does not exist .\nplease use valid id', parent=screen)
        return
    # If the ID exists, fetch the existing data
    existing_data = result[1:]  # ignore the first column 'id'
    # Get the new data entered by the user
    phone = phoneEntry.get()
    if phone and (len(phone) != 10 or not phone.isdigit()):
        messagebox.showerror("Error", "Phone number must be 10 digits and must be integer")
        return
    new_data = [p_nameEntry.get(), ageEntry.get(), phone, ap_timeEntry.get(), fees_paidEntry.get(),statusEntry.get()]

    # Replace empty fields with existing data
    for i in range(len(new_data)):
        if new_data[i] == "":
            new_data[i] = existing_data[i]
    # Execute the update query
    query = 'UPDATE pdetail SET p_name=%s, age=%s, phone=%s, ap_time=%s, fees_paid=%s, status=%s WHERE id=%s'
    val = (new_data[0], new_data[1], new_data[2], new_data[3], new_data[4], new_data[5], id)
    mycursor.execute(query, val)
    con.commit()
    messagebox.showinfo('Success', f'Id {id} is modified successfully', parent=screen)
    screen.destroy()
    show_patient()



sticky=W #for all label on left

#add_patient
def add_patient():
    def add_data():
        #if not phoneEntry.get().isdigit():
           # messagebox.showerror("Error", "Phone number must be a number")
           # return

        if p_nameEntry.get() == '' or ageEntry.get() == '' or phoneEntry.get() == '' or ap_timeEntry.get() == '' or 
        fees_paidEntry.get() == '' or statusEntry.get() == '': messagebox.showerror('Error', 'All Feilds are 
        required', parent=add_window)# if not given all entry

            if p_nameEntry.get() == "":
                p_nameLabel.config(text='Name *', fg='red')


            else:
                p_nameLabel.config(text='Name ', fg='black')


            if ageEntry.get() == '':
                ageLabel.config(text='Age *', fg='red')


            else:
                ageLabel.config(text='Age', fg='black')


            if phoneEntry.get() == '':
                phoneLabel.config(text='Phone *', fg='red')


            else:
                phoneLabel.config(text='Phone', fg='black')


            if ap_timeEntry.get() == '':
                ap_timeLabel.config(text='Appointment time *', fg='red')


            else:
                ap_timeLabel.config(text='Appointment time ', fg='black')

            if fees_paidEntry.get() == '':
                fees_paidLabel.config(text='Fees paid *', fg='red')


            else:
                fees_paidLabel.config(text='Fees paid ', fg='black')

            if statusEntry.get() == '':
                statusLabel.config(text='Status*', fg='red')


            else:
                statusLabel.config(text='Status ', fg='black')

            return



        else:# for entering values in table
            if not phoneEntry.get().isdigit() or len(phoneEntry.get()) != 10:
                messagebox.showerror("Error", "Phone number must be 10 digits and must be integer")
                phoneLabel.config(text='Phone *', fg='red')
                return

                # if the phone number is valid, set the phoneLabel color to black
            phoneLabel.config(text='Phone', fg='black')

            try:

                query = "INSERT INTO pdetail ( p_name, age, phone, ap_time, fees_paid,status) VALUES ( %s, %s, %s, 
                %s, %s,%s)" values = (p_nameEntry.get(), ageEntry.get(), phoneEntry.get(), ap_timeEntry.get(), 
                fees_paidEntry.get(), statusEntry.get()) mycursor.execute(query, values) con.commit() 
                p_nameLabel.config(text='Name', fg='black') ageLabel.config(text='Age', fg='black') 
                phoneLabel.config(text='Phone', fg='black') ap_timeLabel.config(text='Appointment time', fg='black') 
                fees_paidLabel.config(text='Fees paid', fg='black') statusLabel.config(text='Status',fg='black')

                result = messagebox.askyesno('condirm', 'Data added sucessfully!.\nDo you want to clear the form?')
                print(result)
                if result:  # If click yes
                    #idEntry.delete(0, END)
                    p_nameEntry.delete(0, END)
                    ageEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    ap_timeEntry.delete(0, END)
                    fees_paidEntry.delete(0, END)
                    #statusEntry.delete(0, END)

                else:
                    pass
            except:
                messagebox.showerror('Error', 'Id cannot be repeated', parent=add_window)
                return

            query = 'select *from pdetail'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            ptable.delete(*ptable.get_children())
            for data in fetched_data:
                ptable.insert('', END, values=data)

    add_window=Toplevel()
    add_window.grab_set()
    add_window.resizable(False,False)
    p_nameLabel = Label(add_window, text='Name', font=('times new roman', 20, 'bold'))
    p_nameLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    p_nameEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    p_nameEntry.grid(row=0, column=1, pady=15, padx=10)

    ageLabel = Label(add_window, text='Age', font=('times new roman', 20, 'bold'))
    ageLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    ageEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    ageEntry.grid(row=1, column=1, pady=15, padx=10)

    phoneLabel = Label(add_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    ap_timeLabel = Label(add_window, text='Appointment time', font=('times new roman', 20, 'bold'))
    ap_timeLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    ap_timeEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    ap_timeEntry.grid(row=3, column=1, pady=15, padx=10)

    fees_paidLabel = Label(add_window, text='Fees paid', font=('times new roman', 20, 'bold'))
    fees_paidLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    fees_paidEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
    fees_paidEntry.grid(row=4, column=1, pady=15, padx=10)

    statusLabel = Label(add_window, text='Status', font=('times new roman', 20, 'bold'))
    statusLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    statusEntry = Entry(add_window, font=('roman', 15, 'bold'), width=24, )
    statusEntry.insert(0, "pending")
    statusEntry.grid(row=5, column=1, pady=15, padx=10)

    p_button = ttk.Button(add_window, text='Add data', command=add_data)
    p_button.grid(row=7, columnspan=2, pady=15)


#connecting database def connect_database(): def connect(): global mycursor,con try: con=mysql.connector.connect(
host='localhost',user='user1',passwd='1234')#con is used to commit the changes mycursor=con.cursor() 
messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow) except: 
messagebox.showerror('Error','Invalid Details',parent=connectWindow) return try: query = 'create database 
dcms'#create new database as database is already created as database is alreadycreated so he except block code is 
executed mycursor.execute(query) query = 'use dcms' mycursor.execute(query) query = 'create table pdetail(id int  
AUTO_INCREMENT primary key , p_name varchar(30) not null ,age int not null,phone bigint not null,ap_time varchar(20) 
not null,fees_paid varchar(20) not null,status varchar(30) default "pending")' mycursor.execute(query) except: query 
= 'use dcms' mycursor.execute(query)

            #query = 'create table pdetail(id INT AUTO_INCREMENT primary key, p_name varchar(30) not null ,
            age int not null,phone bigint not null,ap_time varchar(20) not null,fees_paid varchar(20) not null,
            status varchar(30) default "pending")' #mycursor.execute(query) #query = 'create table pdetail(id 
            varchar(30)  primary key, p_name varchar(30) not null ,age int not null,phone bigint not null,
            ap_time varchar(20) not null,fees_paid varchar(20) not null)' #mycursor.execute(query)


        connectWindow.destroy()
        addpButton.config(state=NORMAL)
        searchpButton.config(state=NORMAL)
        updatepButton.config(state=NORMAL)
        showpButton.config(state=NORMAL)
        deletepButton.config(state=NORMAL)
        recypButton.config(state=NORMAL)


    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    usernameEntry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

count=0
text=''


#clock method for date and time
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)


#------------gui part-------------------------------
patient_details_window = Tk()
patient_details_window.title("patient_details")
patient_details_window.geometry("1000x563+10+10")
patient_details_window.resizable(0, 0)  # for fixed sized window

# define image

bg = PhotoImage(file="page.png")
my_label = Label(patient_details_window, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

#for date and time on window
datetimeLabel=Label(patient_details_window,font=('times new roman',10,'bold'),bg='white')
datetimeLabel.place(x=25,y=30)
clock()

#title
label1 = Label(patient_details_window, text="patient details", font=("Arial", 14), bg="white", fg="black")
label1.place(x=450, y=30)
#connect button : connect to database when click
connectButton=tk.Button(patient_details_window,text='Connect database',command=connect_database)
connectButton.configure(bg='white',fg='black')
connectButton.place(x=850,y=35)

#leftframe
leftFrame=Frame(patient_details_window)
leftFrame.configure(bg="white")
leftFrame.place(x=30,y=65,width=300,height=450)

#button on frameleft addpButton=tk.Button(leftFrame, text='add data', width=25,state=DISABLED,
command =add_patient)#lambda :toplevel_patient('Add Patient', 'Add', add_data)) addpButton.configure(
bg='mediumslateblue',fg='white') addpButton.grid(row=1,column=0,pady=20)

searchpButton=tk.Button(leftFrame,text='Search Patient',width=25,state=DISABLED,command=lambda :toplevel_patient(
'Search Patient','Search',search_data)) searchpButton.configure(bg='#EE82EE',fg='white') searchpButton.grid(row=2,
column=0,pady=20)

deletepButton=tk.Button(leftFrame, text='Delete Patient', width=25, state=DISABLED, command=delete_patient)
deletepButton.configure(bg='mediumslateblue',fg='white')
deletepButton.grid(row=3,column=0,pady=20)

updatepButton=tk.Button(leftFrame,text='Update Patient',width=25,state=DISABLED,command=lambda :toplevel_patient(
'Update Patient','Update',update_data)) updatepButton.configure(bg='#EE82EE',fg='white') updatepButton.grid(row=4,
column=0,pady=20)

showpButton=tk.Button(leftFrame,text='Show Patient',width=25,state=DISABLED,command=show_patient)
showpButton.configure(bg='mediumslateblue',fg='white')
showpButton.grid(row=5,column=0,pady=20)

recypButton=tk.Button(leftFrame,text='Recycle bin',width=25,state=DISABLED,command=recycle_data)
recypButton.configure(bg='#EE82EE',fg='white')
recypButton.grid(row=6,column=0,pady=20)

exitButton=tk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.configure(bg='mediumslateblue',fg='white')
exitButton.grid(row=7,column=0,pady=20)
#right frame
rightFrame=Frame(patient_details_window)
rightFrame.configure(bg="white")
rightFrame.place(x=320,y=65,width=650,height=450)

#treeview

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

ptable=ttk.Treeview(rightFrame, columns=('id','p_name', 'age','phone', 'ap_time', 'fees_paid','status'),
                                xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=ptable.xview)
scrollBarY.config(command=ptable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

ptable.pack(expand=1, fill=BOTH)

ptable.heading("id", text='Id')
ptable.heading("p_name", text='Patient Name')
ptable.heading("age", text='Age')
ptable.heading("phone", text='Mobile no')
ptable.heading("ap_time", text='Appointment time')
ptable.heading("fees_paid", text='Fees paid')
ptable.heading("status", text='status')

ptable.column("id", width=200, anchor=CENTER)
ptable.column("p_name", width=300, anchor=CENTER)
ptable.column("age", width=100, anchor=CENTER)
ptable.column("phone", width=300, anchor=CENTER)
ptable.column("ap_time", width=200, anchor=CENTER)
ptable.column("fees_paid", width=300, anchor=CENTER)
ptable.column("status", width=300, anchor=CENTER)


style=ttk.Style()

style.configure('Treeview', rowheight=25,font=('arial', 10, 'bold'), fieldbackground='white', background='white',)
style.configure('Treeview.Heading',font=('arial', 14, 'bold'),foreground='#7868d5')

ptable.config(show='headings')



patient_details_window.mainloop()
'''
