from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")
mycursor = mydb.cursor()


class Recycle:
    def __init__(self, master):
        self.master = master
        self.master.title("Deleted Reports")
        self.master.geometry("760x472+230+70")
        self.master.resizable(False, False)  # for fixed sized window

        query = "Select * from recycletable"
        mycursor.execute(query)
        result = mycursor.fetchall()

        def show_patient():
            query = 'select * from recycletable'
            mycursor.execute(query)
            fetched_data = mycursor.fetchall()
            patientTable.delete(*patientTable.get_children())
            for data in fetched_data:
                patientTable.insert('', END, values=data)

        main_frame = Frame(self.master, bg="#7868d5", width=700, height=472)
        main_frame.place(x=0, y=0)

        # heading
        heading_label = Label(main_frame, text="Sweet Tooth Dental Clinic",
                              font=("Arial", 20, "bold"), bg="#7868d5", fg="white")
        heading_label.place(x=200, y=5)

        scrollBarX = Scrollbar(main_frame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(main_frame, orient=VERTICAL)

        patientTable = Treeview(main_frame, columns=('Id', 'Name', 'D.O.B', 'Age', 'Weight', 'Gender', 'Contact'),
                                height=17, xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

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

        patientTable.column('Id', width=100, anchor=CENTER)
        patientTable.column('Name', width=200, anchor=CENTER)
        patientTable.column('D.O.B', width=100, anchor=CENTER)
        patientTable.column('Age', width=50, anchor=CENTER)
        patientTable.column('Weight', width=100, anchor=CENTER)
        patientTable.column('Gender', width=60, anchor=CENTER)
        patientTable.column('Contact', width=125, anchor=CENTER)

        def onDoubleClick(event):
            if patientTable.selection()[0]:
                msg = messagebox.askquestion("", "Do you want to restore the file?", parent=self.master)
                if msg == "yes":
                    indexing = patientTable.focus()
                    content = patientTable.item(indexing)
                    listdata = content['values']
                    idEntry = listdata[0]
                    query = "select * from recycletable where id=%s"
                    mycursor.execute(query, (idEntry,))
                    result = mycursor.fetchone()
                    query = 'insert into reports values(%s,%s,%s,%s,%s,%s,%s,%s)'
                    mycursor.execute(query, result)
                    query = 'delete from recycletable where id=%s'
                    mycursor.execute(query, (idEntry,))
                    mydb.commit()
                    show_patient()
                else:
                    show_patient()

        patientTable.bind("<Double-1>", onDoubleClick)

        show_patient()


if __name__ == "__main__":
    root = Tk()
    recycle_page = Recycle(root)
    root.mainloop()
