from tkinter import *
from tkinter.ttk import Combobox, Treeview
import mysql.connector
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk

dobEntry = img_label = nameEntry = ageEntry = weightEntry = genderEntry = diagnosisButton = contactEntry = screen = None

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms", connect_timeout=60)
mycursor = mydb.cursor()


class Reports:
    def __init__(self, master):
        self.master = master
        self.master.title("Reports")
        self.master.geometry("760x472+230+70")
        self.master.resizable(False, False)  # for fixed sized window

        def detailed():
            selected_record = patientTable.focus()
            # check if a record has been selected
            if not selected_record:
                messagebox.showerror("Error", "select a record to view the report.", parent=self.master)

            elif selected_record:
                screen1 = Toplevel()
                screen1.title("Detailed Diagnostic Report")
                screen1.grab_set()
                screen1.geometry("550x700+230+0")
                screen1.resizable(False, False)
                screen1.config(bg="#7868d5")
                global img_label
                img_label = Label(screen1, bg="#604cd7")
                img_label.place(x=0, y=0)
                indexing = patientTable.focus()
                content = patientTable.item(indexing)
                selected_item = content['values'][0]
                query = "Select diagnosis from reports where id=%s"
                mycursor.execute(query, (selected_item,))
                fetched_data = mycursor.fetchone()
                result = fetched_data[0]
                image_file = BytesIO(result)
                image1 = Image.open(image_file)
                image1 = image1.resize((552, 780))
                photo1 = ImageTk.PhotoImage(image1)
                img_label.configure(image=photo1)
                img_label.image = photo1

            else:
                screen1.destory()
                messagebox.showerror("Error", "Report does not exist", parent=self.master)

        def exit_page():
            self.master.destroy()

        def age_cal(event):
            birth_date = dobEntry.get_date()
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            ageEntry.delete(0, END)
            ageEntry.insert(0, age)

        def toplevel_data(title, button_text, command):
            global dobEntry, nameEntry, ageEntry, weightEntry, genderEntry, diagnosisButton, contactEntry, \
                screen
            screen = Toplevel()
            screen.title(title)
            screen.grab_set()
            screen.geometry("550x550+10+20")
            screen.resizable(False, False)
            screen.config(bg="#7868d5")

            nameLabel = Label(screen, text='Name', font=('Arial', 20, 'bold'), bg="#7868d5", fg="white")
            nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
            nameEntry = Entry(screen, font=('Arial', 15, 'bold'), width=24)
            nameEntry.grid(row=1, column=1, pady=15, padx=10)

            dobLabel = Label(screen, text='D.O.B', font=("Arial", 20, 'bold'), bg="#7868d5", fg="white")
            dobLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
            dobEntry = DateEntry(screen, date_pattern='yyyy/mm/dd', font=('Arial', 15, 'bold'), width=23)
            dobEntry.delete(0, END)
            dobEntry.grid(row=2, column=1, pady=15, padx=10)
            dobEntry.bind("<FocusIn>", age_cal)

            ageLabel = Label(screen, text='Age', font=('Arial', 20, 'bold'), bg="#7868d5", fg="white")
            ageLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
            ageEntry = Entry(screen, font=('Arial', 15, 'bold'), width=24)
            ageEntry.grid(row=3, column=1, pady=15, padx=10)

            weightLabel = Label(screen, text='Weight(kg)', font=('Arial', 20, 'bold'), bg="#7868d5", fg="white")
            weightLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
            weightEntry = Entry(screen, font=('Arial', 15, 'bold'), width=24)
            weightEntry.grid(row=4, column=1, pady=15, padx=10)

            genderLabel = Label(screen, text='Gender', font=('Arial', 20, 'bold'), bg="#7868d5", fg="white")
            genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
            genderEntry = Combobox(screen, font=('Arial', 15, 'bold'), width=23, values=["Select", "Male", "Female"],
                                   foreground="black", state="readonly")
            genderEntry.current(0)  # Set the default choice to the first item
            genderEntry.grid(row=5, column=1, pady=15, padx=10)

            contactLabel = Label(screen, text='Mobile No.', font=('Arial', 20, 'bold'), bg="#7868d5", fg="white")
            contactLabel.grid(row=7, column=0, padx=30, pady=15, sticky=W)
            contactEntry = Entry(screen, font=('Arial', 15, 'bold'), width=24)
            contactEntry.grid(row=7, column=1, pady=15, padx=10)

            patient_button = ttk.Button(screen, text=button_text, command=command)
            patient_button.grid(row=8, column=1, pady=15)
            if title == 'Update Patient':
                # get the selected record's ID
                selected_record = patientTable.focus()
                # check if a record has been selected
                if not selected_record:
                    messagebox.showerror("Error", "select a record to update.", parent=screen)
                    screen.destroy()

                else:
                    indexing = patientTable.focus()

                    content = patientTable.item(indexing)
                    listdata = content['values']
                    nameEntry.insert(0, listdata[1])
                    dobEntry.insert(0, listdata[2])
                    ageEntry.insert(0, listdata[3])
                    weightEntry.insert(0, listdata[4])
                    genderEntry.delete(0, END)
                    genderEntry.insert(0, listdata[5])
                    contactEntry.insert(0, listdata[6])

        def add_data():
            if nameEntry.get() == '' or dobEntry.get() == '' or ageEntry.get() == '' \
                    or weightEntry.get() == '' or genderEntry.get() == 'Select' \
                    or contactEntry.get() == '':
                messagebox.showerror('Error', 'All Feilds are required', parent=screen)

            elif len(contactEntry.get()) != 10:
                messagebox.showerror('Error', 'Invalid Contact No (Only 10 digits accepted)', parent=screen)

            elif not contactEntry.get().isdigit():
                messagebox.showerror('Error', 'No characters allowed', parent=screen)

            else:
                filepath = filedialog.askopenfilename(initialdir='/', title='Select Report',
                                                      filetypes=(('JPEG', '*.jpg'), ('PNG', '*.png')), parent=screen)
                if filepath:
                    image = Image.open(filepath)
                    image = image.resize((150, 150))
                    photo = ImageTk.PhotoImage(image)
                    with open(filepath, 'rb') as f:
                        img_bytes = f.read()
                    try:
                        query = 'insert into reports(name, dob, age, weight, gender, diagnosis, contactno)' \
                                ' values(%s,%s,%s,%s,%s,%s,%s)'
                        mycursor.execute(query, (
                            nameEntry.get(), dobEntry.get(), ageEntry.get(), weightEntry.get(),
                            genderEntry.get(), img_bytes, contactEntry.get()))
                        mydb.commit()
                        result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clean the '
                                                                'form?', parent=screen)
                        if result:
                            nameEntry.delete(0, END)
                            dobEntry.delete(0, END)
                            ageEntry.delete(0, END)
                            weightEntry.delete(0, END)
                            genderEntry.delete(0, END)
                            contactEntry.delete(0, END)
                    except:
                        messagebox.showerror('Error', 'Could not Add Data', parent=screen)
                        return

                query = 'select * from reports'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                patientTable.delete(*patientTable.get_children())
                for data in fetched_data:
                    patientTable.insert('', END, values=data)

        def search_data():
            dobEntry.delete(0, END)
            query = 'select * from reports where name=%s or dob=%s or contactno=%s or age=%s or gender=%s '
            mycursor.execute(query, (
                nameEntry.get(), dobEntry.get(), contactEntry.get(), ageEntry.get(), genderEntry.get()))
            patientTable.delete(*patientTable.get_children())
            fetched_data = mycursor.fetchall()
            for data in fetched_data:
                patientTable.insert('', END, values=data)
                dobEntry.delete(0, END)
                ageEntry.delete(0, END)

        def delete_patient():
            try:
                indexing = patientTable.focus()
                content = patientTable.item(indexing)
                content1 = content['values']
                for item in content:
                    query = 'insert into recycletable values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    mycursor.execute(query, content1)
                    break
                query = 'delete from reports where id=%s'
                content_id1 = content['values'][0]
                content_id = (content['values'][0],)
                mycursor.execute(query, content_id)
                mydb.commit()
                messagebox.showinfo('Deleted', f'Id {content_id1} is deleted successfully', parent=self.master)
                query = 'select * from reports'
                mycursor.execute(query)
                fetched_data = mycursor.fetchall()
                patientTable.delete(*patientTable.get_children())
                for data in fetched_data:
                    patientTable.insert('', END, values=data)
            except:
                messagebox.showerror("Error", "Please select a record to delete", parent=self.master)

        def update_data():
            try:
                # get the selected record's ID
                selected_record = patientTable.focus()
                # check if a record has been selected or not
                if not selected_record:
                    screen.destroy()
                    messagebox.showerror("Error", "select a record to update.", parent=self.master)
                else:
                    indexing = patientTable.focus()
                    content = patientTable.item(indexing)
                    selected_item = content['values'][0]
                    query = 'update reports set name=%s,dob=%s,age=%s,weight=%s,gender=%s, contactno=%s ' \
                            'where id=%s'
                    mycursor.execute(query, (nameEntry.get(), dobEntry.get(), ageEntry.get(), weightEntry.get(),
                                             genderEntry.get(), contactEntry.get(),
                                             selected_item))
                    mydb.commit()
                    screen.destroy()
                    messagebox.showinfo('Success', f'Id {selected_item} is modified successfully', parent=self.master)
                    show_patient()

            except:
                messagebox.showerror("Error", "Please select a record to update", parent=self.master)

        def show_patient():
            query = 'select * from reports'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            patientTable.delete(*patientTable.get_children())
            for data in fetched_data:
                patientTable.insert('', END, values=data)

        frame = Frame(self.master, bg="white", width=760, height=472)
        frame.place(x=0, y=0)

        main_frame = Frame(self.master, bg="#7868d5", width=760, height=472)
        main_frame.place(x=155, y=0)

        # heading
        heading_label = Label(main_frame, text="Sweet Tooth Dental Clinic",
                              font=("Arial", 20, "bold"), bg="#7868d5", fg="white")
        heading_label.place(x=120, y=5)

        left_frame = Frame(self.master, width=200, height=760, bg="white")
        left_frame.place(x=0, y=10)

        add_button = Button(left_frame, width=15, text="Add Patient", bd=0, bg="#604cd7", fg="white", height=2,
                            command=lambda: toplevel_data('Add Patient', 'Add Report', add_data))
        add_button.grid(row=0, column=0, pady=15, padx=20)

        search_button = Button(left_frame, width=15, text="Search Patient", bd=0, bg="#604cd7", fg="white", height=2,
                               command=lambda: toplevel_data('Search Student', 'Search', search_data))
        search_button.grid(row=1, column=0, pady=15, padx=20)

        delete_button = Button(left_frame, width=15, text="Delete Patient", bd=0, bg="#604cd7", fg="white", height=2,
                               command=delete_patient)
        delete_button.grid(row=2, column=0, pady=15, padx=20)

        update_button = Button(left_frame, width=15, text="Update Patient", bd=0, bg="#604cd7", fg="white", height=2,
                               command=lambda: toplevel_data('Update Patient', 'Update', update_data))
        update_button.grid(row=3, column=0, pady=15, padx=20)

        detailed_report = Button(left_frame, width=15, text="Diagnostic Report", bd=0, bg="#604cd7", fg="white",
                                 height=2,
                                 command=detailed)
        detailed_report.grid(row=4, column=0, pady=15, padx=20)

        reset_button = Button(left_frame, width=15, text="Refresh Page", bd=0, bg="#604cd7", fg="white", height=2,
                              command=show_patient)
        reset_button.grid(row=5, column=0, pady=15, padx=20)

        close_button = Button(left_frame, width=15, text="Close", bd=0, bg="#604cd7", fg="white", height=2,
                              command=exit_page)
        close_button.grid(row=6, column=0, pady=15, padx=20)

        right_frame = Frame(self.master, bg="yellow")
        right_frame.place(x=155, y=40, height=430, width=604)

        scrollBarX = Scrollbar(right_frame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(right_frame, orient=VERTICAL)

        patientTable = Treeview(right_frame, columns=('Id', 'Name', 'D.O.B', 'Age', 'Weight', 'Gender',
                                                      'Contact'), height=1,
                                xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
        show_patient()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#7868d5",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#7868d5")

        style.configure("Treeview.Heading",
                        background="#604cd7", foreground="white")

        style.map('Treeview', background=[('selected', '#604cd7')])

        scrollBarX.config(command=patientTable.xview)
        scrollBarY.config(command=patientTable.yview)

        scrollBarX.pack(side=BOTTOM, fill=X)
        scrollBarY.pack(side=RIGHT, fill=Y)

        patientTable.pack(expand=1, fill=BOTH)

        patientTable.heading('Id', text='Id')
        patientTable.heading('Name', text='Name')
        patientTable.heading('D.O.B', text='D.O.B')
        patientTable.heading('Age', text='Age')
        patientTable.heading('Weight', text='Weight(kg)')
        patientTable.heading('Gender', text='Gender')
        patientTable.heading('Contact', text='Mobile No.')
        patientTable.config(show='headings')

        patientTable.column('Id', width=50, anchor=CENTER)
        patientTable.column('Name', width=100, anchor=CENTER)
        patientTable.column('D.O.B', width=100, anchor=CENTER)
        patientTable.column('Age', width=50, anchor=CENTER)
        patientTable.column('Weight', width=100, anchor=CENTER)
        patientTable.column('Gender', width=60, anchor=CENTER)
        patientTable.column('Contact', width=100, anchor=CENTER)


if __name__ == "__main__":
    root = Tk()
    report_page = Reports(root)
    root.mainloop()
