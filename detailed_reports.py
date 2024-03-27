from tkinter import *
from io import BytesIO
import mysql.connector
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox, Treeview
from PIL import Image, ImageTk

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")
mycursor = mydb.cursor()

addEntry = img_label = None


class Detailed:
    def __init__(self, master):
        self.master = master
        self.master.title("Detailed Diagnostic Reports")
        self.master.geometry("660x700+230+0")
        self.master.resizable(False, False)  # for fixed sized window

        def search():
            if id_Entry.get() == "":
                messagebox.showerror("Error", "Please enter an valid id", parent=self.master)
            else:
                id_user = id_Entry.get()
                query = "Select diagnosis from reports where id=%s"
                mycursor.execute(query, (id_user,))
                fetched_data = mycursor.fetchone()
                result = fetched_data[0]
                image_file = BytesIO(result)
                image1 = Image.open(image_file)
                image1 = image1.resize((534, 755))
                photo1 = ImageTk.PhotoImage(image1)
                img_label.configure(image=photo1)
                img_label.image = photo1

        main_frame = Frame(self.master, bg="white", height=700, width=660)
        main_frame.pack()

        left_frame = Frame(self.master, width=200, height=563, bg="white")
        left_frame.place(x=0, y=0)

        id_label = Label(left_frame, text="Enter Id", font=("Arial", 15), width=10, fg="black", bg="white")
        id_label.grid(row=0, column=0, pady=5, padx=20)

        id_Entry = Entry(left_frame, font=("Arial", 15), width=10, fg="white", bg="#604cd7")
        id_Entry.grid(row=1, column=0, pady=5, padx=20)

        search_button = Button(left_frame, width=15, text="Search Report", bd=0, bg="#604cd7", fg="white", height=2,
                               command=search)
        search_button.grid(row=2, column=0, pady=20, padx=20)

        right_frame = Frame(self.master, bg="#604cd7")
        right_frame.place(x=155, y=0, height=700, width=1000)

        global img_label
        img_label = Label(right_frame, bg="#604cd7")
        img_label.place(x=0, y=0)


"""

        patientTable = Treeview(right_frame, columns='Report')

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
        patientTable.pack(expand=1, fill=BOTH)

        patientTable.heading('Report', text='Report')
        patientTable.config(show='headings')
        patientTable.column('Report', width=50, anchor=CENTER)
"""

if __name__ == "__main__":
    root = Tk()
    details_page = Detailed(root)
    root.mainloop()
