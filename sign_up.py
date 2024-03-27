from tkinter import *
from tkinter import messagebox
from details import Details
import mysql.connector
import re

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")
cursor = mydb.cursor()

bg = error_label = None


class SignUp:
    def __init__(self, master):
        self.master = master
        self.master.title("Signup Page")
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)  # for fixed sized window

        def signin():
            self.master.destroy()

        def validate_password(password):
            """
            Validates that the password meets the criteria of being at least 8 characters long,
            containing at least one uppercase letter, one number, and one special character.
            """
            if len(password) < 8:
                return False
            if not re.search(r"[A-Z]", password):
                return False
            if not re.search(r"\d", password):
                return False
            if not re.search(r"[!@#$%^&*()_+]", password):
                return False
            return True

        def connect_database():
            if un_entry.get() == "" or email_entry.get() == "" \
                    or pw_entry.get() == "" or cpw_entry.get() == "":
                messagebox.showwarning("Warning", "All fields are required", parent=self.master)

            elif pw_entry.get() != cpw_entry.get():
                messagebox.showerror("Error", "New password does not match confirm new password", parent=self.master)

            else:
                username = un_entry.get()
                email = email_entry.get()
                password = pw_entry.get()

                if not validate_password(password):
                    error_label = Label(self.master, text="", font=("Arial", 14),
                                        fg="red", bg="white", width=20)
                    error_label.place(x=710, y=450)
                    check_lbl.config(text="Password must be at least 8 characters "
                                          "long having a combination of uppercase letters, "
                                          "lowercase letters, numbers, and symbols.", fg="red")
                    return
                else:
                    check_lbl.config(text="", fg="white", bg="white")

                # Check if the email is already in use
                cursor = mydb.cursor()
                query = "SELECT * FROM users WHERE email = %s"
                values = (email,)
                cursor.execute(query, values)
                user = cursor.fetchone()
                if user:
                    messagebox.showinfo("", "Email already in use", parent=self.master)

                else:
                    # Check if the username is already taken
                    query = "SELECT * FROM users WHERE username = %s"
                    values = (username,)
                    cursor.execute(query, values)
                    user = cursor.fetchone()
                    if user:
                        messagebox.showinfo("", "Username already in use", parent=self.master)
                    else:
                        # Insert the new user into the database
                        query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
                        values = (email, username, password)
                        cursor.execute(query, values)
                        mydb.commit()
                        messagebox.showinfo("", "Registration successful, Continue to fill details?",
                                            parent=self.master)
                        email_entry.delete(0, END)
                        un_entry.delete(0, END)
                        pw_entry.delete(0, END)
                        cpw_entry.delete(0, END)
                        self.new_window = Toplevel(self.master)
                        self.app = Details(self.new_window)

        global bg
        bg = PhotoImage(file="dmsbg.png")
        # create a label for bg
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # create an account label
        heading = Label(self.master, text="CREATE AN ACCOUNT", font=("Arial", 20, "bold"), fg="#7868d5", bg="white")
        heading.place(x=580, y=90)

        # email label
        email_label = Label(self.master, text="Email", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        email_label.place(x=580, y=140)

        # email entry
        email_entry = Entry(self.master, font=("Arial", 20), width=23, bg="#7868d5", fg="white", bd=2)
        email_entry.place(x=580, y=165)

        # username label
        un_label = Label(self.master, text="Username", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        un_label.place(x=580, y=215)

        #  username entry
        un_entry = Entry(self.master, font=("Arial", 20), width=23, bg="#7868d5", fg="white", bd=2)
        un_entry.place(x=580, y=240)

        # password label
        pw_label = Label(self.master, text="Password", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        pw_label.place(x=580, y=290)

        # password entry
        pw_entry = Entry(self.master, font=("Arial", 20), width=23, bg="#7868d5", fg="white", bd=2)
        pw_entry.place(x=580, y=315)
        pw_entry.config(show="*")

        # confirm password label
        cpw_label = Label(self.master, text="Confirm Password", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        cpw_label.place(x=580, y=365)

        # confirm password entry
        cpw_entry = Entry(self.master, font=("Arial", 20), width=23, bg="#7868d5", fg="white", bd=2)
        cpw_entry.place(x=580, y=390)
        cpw_entry.config(show="*")

        # add button
        signup_btn = Button(self.master, width=15, height=2, text="Sign Up", bg="#7868d5", fg="white",
                            bd=2, command=connect_database)
        signup_btn.place(x=580, y=440)

        # password status label
        check_lbl = Label(self.master, text="", height=1, bg="white", font=("Arial", 10, "bold"), anchor="e")
        check_lbl.place(x=95, y=510)

        # sign in
        label2 = Label(self.master, text="Already have an account?", font=("Arial", 10), bg="white", fg="#7868d5")
        label2.place(x=580, y=490)
        signin_btn = Button(self.master, text="Sign In", font=("Arial", 10, "bold"), bg="white", fg="#604cd7",
                            activebackground="white", bd=0, command=signin)
        signin_btn.place(x=733, y=489)


if __name__ == "__main__":
    root = Tk()
    login_page = SignUp(root)
    root.mainloop()
