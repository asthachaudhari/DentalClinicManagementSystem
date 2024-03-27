from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import mysql.connector
import re

bg = error_label = None

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms")
cursor = mydb.cursor()


class ForgetPassword:
    def __init__(self, master):
        self.master = master
        self.master.title("Forget Password")
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)  # for fixed sized window

        def close():
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

        def reset_pass():
            global error_label
            if s_combo.get() == "Select" or s_entry.get() == "" or u_entry.get() == "" or pw_entry.get() == "" \
                    or cpw_entry.get() == "":
                messagebox.showwarning("Warning", "All fields are required", parent=self.master)
                '''error_label = Label(self.master, text="All fields are required", font=("Arial", 10),
                                    fg="red", bg="white")
                error_label.place(x=200, y=510)'''
            else:
                security_answer = s_entry.get()
                username = u_entry.get()
                password = pw_entry.get()
                c_password = cpw_entry.get()

                cursor = mydb.cursor()
                query = "SELECT * FROM users WHERE username = %s"
                values = (username,)
                cursor.execute(query, values)
                user = cursor.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Username does not exist", parent=self.master)
                    # error_label.config(text="Username does not exist")
                elif password != c_password:
                    messagebox.showerror("Error", "New Password does not match Confirm New Password",
                                         parent=self.master)
                    # error_label.config(text="Password does not match")
                else:
                    global error_label
                    error_label = Label(self.master, font=("Arial", 10), fg="red", bg="white")
                    error_label.place(x=200, y=510)
                    if not validate_password(password):
                        error_label.config(text="Password must be at least 8 characters long having "
                                                "a combination of uppercase letters, lowercase letters, "
                                                "numbers, and symbols.")
                        return
                    if validate_password(password):
                        error_label.config(text="")
                        query = "SELECT security FROM users WHERE username = %s"
                        values = (username,)
                        cursor.execute(query, values)
                        row = cursor.fetchone()
                        while row is not None:
                            # Extract the value of the first element
                            ans = row[0]
                            row = cursor.fetchone()
                            if ans != security_answer:
                                messagebox.showerror("Error", "Wrong Security Question or Password", parent=self.master)
                                # error_label.config(text="Wrong Security Question or Password")
                            else:
                                query = "UPDATE users SET password=%s WHERE username=%s"
                                values = (password, username)
                                cursor.execute(query, values)
                                try:
                                    error_label.config(text="")
                                    messagebox.showinfo("Message", "Successfully updated password, Continue to login?",
                                                        parent=self.master)
                                    self.master.destroy()
                                except Exception as e:
                                    messagebox.showerror("", "Some error has occurred, Try Again?", parent=self.master)
                                    s_combo.current(0)
                                    u_entry.delete(0, END)
                                    pw_entry.delete(0, END)
                                    cpw_entry.delete(0, END)
                                    s_entry.delete(0, END)

        global bg
        bg = PhotoImage(file="dmsbg.png")
        bg_label = Label(self.master, image=bg)
        bg_label.place(x=0, y=0)

        # create an account label
        heading = Label(self.master, text="Reset Password", font=("Arial", 20, "bold"), fg="#7868d5", bg="white")
        heading.place(x=650, y=90)

        security_question = Label(self.master, text="Security Question", font=("Arial", 15, "bold"),
                                  fg="#7868d5", bg="white")
        security_question.place(x=580, y=140)

        # security question combo box
        s_choices = ["Select", "Favourite animal", "Favourite movie", "First movie you saw in theatre",
                     "Name of the hospital you were born in"]
        s_combo = Combobox(self.master, values=s_choices, font=("Arial", 20),
                           state="readonly", foreground="#7868d5", width=19)
        s_combo.current(0)
        s_combo.place(x=578, y=170)

        # security question answer entry
        s_entry = Entry(self.master, font=("Arial", 20), width=20, fg="white", bg="#7868d5", bd=2)
        s_entry.place(x=580, y=210)

        u_label = Label(self.master, text="Username", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        u_label.place(x=580, y=250)

        # username entry
        u_entry = Entry(self.master, font=("Arial", 20), width=20, fg="white", bg="#7868d5", bd=2)
        u_entry.place(x=580, y=280)

        pw_label = Label(self.master, text="New Password", font=("Arial", 15, "bold"), fg="#7868d5", bg="white")
        pw_label.place(x=580, y=320)
        # password entry
        pw_entry = Entry(self.master, font=("Arial", 20), width=20, fg="white", bg="#7868d5", bd=2)
        pw_entry.config(show="*")
        pw_entry.place(x=580, y=350)

        cpw_label = Label(self.master, text="Confirm New Password", font=("Arial", 15, "bold"),
                          fg="#7868d5", bg="white")
        cpw_label.place(x=580, y=390)
        # password entry
        cpw_entry = Entry(self.master, font=("Arial", 20), width=20, fg="white", bg="#7868d5", bd=2)
        cpw_entry.config(show="*")
        cpw_entry.place(x=580, y=420)

        reset = Button(self.master, text="RESET", font=("Arial", 15, "bold"), bg="#604cd7", fg="white",
                       activebackground="white", bd=0, command=reset_pass)
        reset.place(x=580, y=470)

        go_back_label = Label(self.master, text="Go back to login page?", font=("Arial", 10), bg="white",
                              fg="#604cd7", activebackground="white", bd=0)
        go_back_label.place(x=670, y=490)

        go_back = Button(self.master, text="Sign In", font=("Arial", 10, "bold"), bg="white", fg="#604cd7",
                         activebackground="white", bd=0, command=close)
        go_back.place(x=804, y=488)


if __name__ == "__main__":
    root = Tk()
    forget_pass = ForgetPassword(root)
    root.mainloop()
