from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import mysql.connector

bg = error_label = None

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")


class Details:
    def __init__(self, master):
        self.master = master
        self.master.title("Details Page")
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)  # for fixed sized window

        # functions
        def save_fn():
            global error_label
            if un_entry.get() == "" or n_entry.get() == "" or s_entry.get() == "" or g_combo.get() == "Select" \
                    or s_combo.get() == "Select":
                messagebox.showerror("", "All fields are required", parent=self.master)
                # error_label = Label(self.master, text="All fields are required", fg="red", bg="white",
                # font=("Arial", 15))
                # error_label.place(x=700, y=490)
            else:
                cursor = mydb.cursor()
                username = un_entry.get()
                name = n_entry.get()
                gender = g_combo.get()
                dob = cal.get()
                security = s_entry.get()

                query = "SELECT * FROM users WHERE username = %s"
                values = (username,)
                cursor.execute(query, values)
                user = cursor.fetchone()
                if user is None:
                    error_label.config(text="Username does not exist")
                else:
                    query = "UPDATE users SET name=%s, gender=%s, dob=%s, security=%s where username=%s"
                    values = (name, gender, dob, security, username)
                    cursor.execute(query, values)
                    try:
                        messagebox.showinfo("Message", "Successfully saved details, Continue to login?",
                                            parent=self.master)
                        self.master.destroy()
                    except Exception as e:
                        messagebox.showerror("", "Some error has occurred, Try Again?", parent=self.master)
                        self.master.destroy()

        # define image
        global bg
        bg = PhotoImage(file="dmsbg.png")

        # create a label for bg
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # details label
        heading = Label(self.master, text="Fill In Your Details", font=("Arial", 30, "bold"), fg="#7868d5",
                        bg="white")
        heading.place(x=560, y=50)

        # username
        un_label = Label(self.master, text="Username", font=("Arial", 18, "bold"), fg="#7868d5", bg="white")
        un_label.place(x=580, y=100)
        # name entry
        un_entry = Entry(self.master, font=("Arial", 20), width=20, fg="#7868d5", bg="white", bd=2)
        un_entry.place(x=580, y=130)

        # name label
        n_label = Label(self.master, text="Name", font=("Arial", 18, "bold"), fg="#7868d5", bg="white")
        n_label.place(x=580, y=170)
        # name entry
        n_entry = Entry(self.master, font=("Arial", 20), width=20, fg="#7868d5", bg="white", bd=2)
        n_entry.place(x=580, y=200)

        # gender label
        g_label = Label(self.master, text="Gender", font=("Arial", 18, "bold"), fg="#7868d5", bg="white")
        g_label.place(x=580, y=240)
        choices = ["Select", "Male", "Female"]
        # gender combo box
        g_combo = Combobox(self.master, values=choices, font=("Arial", 20),
                           state="readonly", foreground="#7868d5", width=19)
        g_combo.current(0)
        g_combo.place(x=580, y=270)

        # date of birth
        dob_label = Label(self.master, text="Date of Birth", font=("Arial", 18, "bold"), fg="#7868d5", bg="white")
        dob_label.place(x=580, y=310)
        cal = DateEntry(self.master, date_pattern='yyyy/mm/dd',
                        font=("Arial", 10), width=41, background="#7868d5", foreground="white", bd=2)
        cal.place(x=580, y=340)

        security_question = Label(self.master, text="Security Question", font=("Arial", 18, "bold"),
                                  fg="#7868d5", bg="white")
        security_question.place(x=580, y=370)
        # security question combo box
        s_choices = ["Select", "Favourite animal", "Favourite movie", "First movie you saw in theatre",
                     "Name of the hospital you were born in"]
        s_combo = Combobox(self.master, values=s_choices, font=("Arial", 20),
                           state="readonly", foreground="#7868d5", width=19)
        s_combo.current(0)
        s_combo.place(x=580, y=400)

        # security question answer entry
        s_entry = Entry(self.master, font=("Arial", 20), width=20, fg="#7868d5", bg="white", bd=2)
        s_entry.place(x=580, y=440)

        # save button
        save = Button(self.master, width=15, height=2, text="Save", bg="#7868d5", fg="white", bd=0, command=save_fn)
        save.place(x=580, y=490)


if __name__ == "__main__":
    root = Tk()
    details_page = Details(root)
    root.mainloop()
