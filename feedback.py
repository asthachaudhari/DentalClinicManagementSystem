from tkinter import *
import mysql.connector
from tkinter.ttk import Treeview
from tkinter import ttk


# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")
cursor = mydb.cursor()


class Feedback:
    def __init__(self, master):
        self.master = master
        self.master.title("Feedback")
        self.master.geometry("760x472+230+70")
        self.master.resizable(False, False)  # for fixed sized window

        frame = Frame(self.master, bg="pink", height=472, width=760)
        frame.place(x=0, y=0)

        scrollBarX = Scrollbar(frame, orient=HORIZONTAL)
        scrollBarY = Scrollbar(frame, orient=VERTICAL)

        patientTable = Treeview(frame, columns=('Name', 'Email', 'Message'), height=17,
                                xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#7868d5",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#7868d5")

        style.configure("Treeview.Heading",
                        background="#604cd7")

        style.map('Treeview', background=[('selected', '#604cd7')])

        scrollBarX.config(command=patientTable.xview)
        scrollBarY.config(command=patientTable.yview)

        scrollBarX.pack(side=BOTTOM, fill=X)
        scrollBarY.pack(side=RIGHT, fill=Y)

        patientTable.pack(expand=1, fill=BOTH)

        patientTable.heading('Name', text='Name')
        patientTable.heading('Email', text='Email')
        patientTable.heading('Message', text='Message')
        patientTable.config(show='headings')

        patientTable.column('Name', width=200, anchor=CENTER)
        patientTable.column('Email', width=200, anchor=CENTER)
        patientTable.column('Message', width=340, anchor=CENTER)

        query = 'select * from contactus'
        cursor.execute(query)
        fetched_data = cursor.fetchall()
        patientTable.delete(*patientTable.get_children())
        for data in fetched_data:
            patientTable.insert('', END, values=data)


if __name__ == "__main__":
    root = Tk()
    feedback_page = Feedback(root)
    root.mainloop()
