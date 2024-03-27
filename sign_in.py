from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox, Treeview
import mysql.connector
from sign_up import SignUp
from treatments import Treatments
from forget_password import ForgetPassword
from feedback import Feedback
from diagnostic_report import Reports
from receptionist_home import Receptionist
from reycle_table import Recycle
from tkcalendar import DateEntry

bg = name = my_label = doctor_bg = img1 = img_label = patient_bg = img = email_entry = profile_pic = profile_label \
    = name_entry = filepath = photo = username_entry = gender_entry = dob_entry = photo1 = main_frame_img = \
    profile_pic1 = profile_label1 = None

# Connect to the MySQL database
mydb = mysql.connector.connect(host="localhost", user="Astha", password="A1234", database="dms", connect_timeout=60)
cursor = mydb.cursor()


class DentalClinicManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Dental Clinic Management System")
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)  # for fixed sized window

        def signup():
            self.new_window = Toplevel(self.master)
            self.app = SignUp(self.new_window)

        def treatments():
            self.new_window = Toplevel(self.master)
            self.app = Treatments(self.new_window)

        def feedback():
            self.new_window = Toplevel(self.master)
            self.app = Feedback(self.new_window)

        def forget_pass():
            self.new_window = Toplevel(self.master)
            self.app = ForgetPassword(self.new_window)

        def report():
            self.new_window = Toplevel(self.master)
            self.app = Reports(self.new_window)

        def deleted_records():
            self.new_window = Toplevel(self.master)
            self.app = Recycle(self.new_window)

        def connect_database():
            if un_entry.get() == "" or pw_entry.get() == "" or combo.get() == "Select":
                messagebox.showerror("Error", "All fields are required")
                un_entry.delete(0, END)
                pw_entry.delete(0, END)
                un_entry.insert(0, "Username")
                pw_entry.insert(0, "Password")
            else:
                username = un_entry.get()
                password = pw_entry.get()
                usertype = combo.get()

                # Check if the username, password and usertype match a user in the database
                query = "SELECT * FROM users WHERE username = %s AND password = %s AND usertype = %s"
                values = (username, password, usertype)
                cursor.execute(query, values)
                user = cursor.fetchone()
                if user:
                    selected = combo.get()
                    query = "SELECT name FROM users WHERE username=%s"
                    values = (username,)
                    cursor.execute(query, values)
                    # Retrieve one row at a time
                    row = cursor.fetchone()
                    while row is not None:
                        global name
                        # Extract the value of the first element
                        name = row[0]
                        row = cursor.fetchone()

                    def logout():
                        my_class_instance = DentalClinicManagement(master)

                    def contactus():
                        def contact():
                            if fullname_entry.get() == "" or email_entry.get() == "" or message_entry.get("1.0",
                                                                                                          "end") == "":
                                messagebox.showerror("Error", "All fields are required")
                            else:
                                fullname = fullname_entry.get()
                                email = email_entry.get()
                                message = message_entry.get("1.0", "end")

                                cursor.execute("INSERT into contactus values(%s, %s, %s)", (fullname, email, message))
                                messagebox.showinfo("Message", "Successfully sent")
                                fullname_entry.delete(0, END)
                                email_entry.delete(0, END)
                                message_entry.delete(1.0, END)

                        frame3 = Frame(self.master, width=753, height=452, bg="#604cd7")
                        frame3.place(x=224, y=80)

                        global img
                        img = PhotoImage(file="cute.png")
                        cute = Label(frame3, image=img, bg="#604cd7")
                        cute.place(x=380, y=90)

                        # add labels
                        contact_lbl = Label(frame3, text="Contact Us", font=("Arial", 30, "bold"), fg="white",
                                            bg="#604cd7")
                        contact_lbl.place(x=60, y=10)

                        fullname_lbl = Label(frame3, text="Full Name", font=("Arial", 15), fg="white", bg="#604cd7")
                        fullname_lbl.place(x=10, y=60)

                        email_lbl = Label(frame3, text="Email", font=("Arial", 15), fg="white", bg="#604cd7")
                        email_lbl.place(x=10, y=150)

                        message_lbl = Label(frame3, text="Message", font=("Arial", 15), fg="white", bg="#604cd7")
                        message_lbl.place(x=10, y=240)

                        # entry
                        fullname_entry = Entry(frame3, font=("Arial", 20), width=21, fg="#7868d5", bd=2)
                        fullname_entry.place(x=10, y=90)

                        email_entry = Entry(frame3, font=("Arial", 20), width=21, fg="#7868d5", bd=2)
                        email_entry.place(x=10, y=180)

                        message_entry = Text(frame3, font=("Arial", 20), fg="#7868d5", height=3.5, width=21, bd=2)
                        message_entry.place(x=10, y=270)

                        # button
                        submit_btn = Button(frame3, text="Submit", width=10, bg="white", fg="#7868d5", command=contact)
                        submit_btn.place(x=10, y=410)

                    def profile():
                        frame5 = Frame(self.master, width=753, height=452, bg="#604cd7")
                        frame5.place(x=224, y=80)
                        pframe = Frame(frame5, bg="#604cd7", width=154, height=154, relief=GROOVE)
                        pframe.place(x=500, y=50)
                        global img1
                        img1 = PhotoImage(file="profile.png")
                        # profile image labels
                        global img_label
                        img_label = Label(pframe, bg="#604cd7", image=img1)
                        img_label.place(x=0, y=0)

                        un_label = Label(frame5, text="Username", font=("Arial", 15, "bold"), fg="white", bg="#604cd7")
                        un_label.place(x=100, y=50)

                        global username_entry
                        username_entry = Entry(frame5, font=("Arial", 15), width=25,
                                               bg="white", fg="black", bd=2)
                        username_entry.insert(0, username)
                        username_entry.config(state="readonly")
                        username_entry.place(x=100, y=80)

                        name_label = Label(frame5, text="Name", font=("Arial", 15, "bold"), fg="white",
                                           bg="#604cd7")
                        name_label.place(x=100, y=120)

                        global name_entry
                        name_entry = Entry(frame5, font=("Arial", 15), width=25, bg="white", fg="black", bd=2)
                        name_entry.place(x=100, y=150)

                        dob_label = Label(frame5, text="Date of Birth", bg="#604cd7", fg="white",
                                          font=("Arial", 15, "bold"))
                        dob_label.place(x=100, y=190)

                        global dob_entry
                        dob_entry = DateEntry(frame5, date_pattern='yyyy/mm/dd', font=("Arial", 15),
                                              width=24, bg="white", fg="#7868d5", bd=2)
                        dob_entry.place(x=100, y=220)

                        gender = Label(frame5, text="Gender:", bg="#604cd7", fg="white", font=("Arial", 15, "bold"))
                        gender.place(x=100, y=260)

                        global gender_entry
                        gender_entry = Combobox(frame5, font=("Arial", 15), width=24, foreground="black",
                                                values=["Male", "Female"])
                        gender_entry.place(x=100, y=290)

                        email_label = Label(frame5, text="Email", bg="#604cd7", fg="white", font=("Arial", 15, "bold"))
                        email_label.place(x=100, y=330)
                        global email_entry
                        email_entry = Entry(frame5, font=("Arial", 15), width=25, bg="white", fg="black", bd=2)
                        email_entry.place(x=100, y=360)

                        # upload button command
                        def doc_show_image():
                            global filepath, photo
                            filepath = filedialog.askopenfilename(initialdir='/', title='Select Image',
                                                                  filetypes=(('JPEG', '*.jpg'), ('PNG', '*.png')))
                            if filepath:
                                image = Image.open(filepath)
                                image = image.resize((150, 150))
                                photo = ImageTk.PhotoImage(image)
                                img_label.configure(image=photo)
                                img_label.image = photo
                                with open(filepath, 'rb') as f:
                                    img_bytes = f.read()
                                cursor.execute("UPDATE users SET image=%s where username=%s", (img_bytes, username))
                                try:
                                    print("success")
                                except ValueError:
                                    print("Couldn't upload and save the chosen image")

                        doc_upload_button = Button(frame5, text="Upload", width=15,
                                                   bg="white", fg="#604cd7", command=doc_show_image)
                        doc_upload_button.place(x=520, y=220)

                        def save():
                            gender = gender_entry.get()
                            cursor.execute("UPDATE users SET name=%s,"
                                           "gender=%s where username=%s", (name_entry.get(),
                                                                           gender, username,))
                            try:
                                cursor.execute("SELECT name from users where username=%s", (username,))
                                welcome_value = cursor.fetchone()
                                value = welcome_value[0]
                                messagebox.showinfo("", "Successfully saved")
                                welcome_label.config(text=f"{value}")

                            except ValueError:
                                print("Couldn't save the updated data")

                        doc_save_button = Button(frame5, text="Save", width=15, bg="white", fg="#604cd7", command=save)
                        doc_save_button.place(x=520, y=270)

                        cursor.execute("SELECT name, gender, dob, email, image FROM users WHERE username=%s",
                                       (username,))
                        doc_user_info = cursor.fetchone()
                        if doc_user_info is not None:
                            name_entry.delete(0, END)
                            name_entry.insert(0, doc_user_info[0])
                            gender_entry.delete(0, END)
                            gender_entry.insert(0, doc_user_info[1])
                            dob_entry.delete(0, END)
                            dob_entry.insert(0, doc_user_info[2])
                            email_entry.delete(0, END)
                            email_entry.insert(0, doc_user_info[3])
                            email_entry.config(state="readonly")
                            image_data = doc_user_info[4]
                            image_file = BytesIO(image_data)
                            image1 = Image.open(image_file)
                            image1 = image1.resize((150, 150))
                            global photo1
                            photo1 = ImageTk.PhotoImage(image1)
                            img_label.configure(image=photo1)
                            img_label.image = photo1
                        elif not user:
                            name_entry.delete(0, END)
                            gender_entry.delete(0, END)
                            dob_entry.delete(0, END)
                            img_label.configure(image=img1)
                            messagebox.showerror("Error", "User not found.")
                            un_entry.insert(0, "Username")
                            pw_entry.insert(0, "Password")

                    if selected == "Doctor":
                        # define image
                        global bg, my_label
                        bg = PhotoImage(file="page.png")
                        # create a label for bg
                        my_label = Label(self.master, image=bg)
                        my_label.place(x=0, y=0, relwidth=1, relheight=1)

                        profile()

                        # heading
                        heading_label = Label(self.master, text="Sweet Tooth Dental Clinic",
                                              font=("Arial", 20, "bold"), bg="white", fg="#7868d5")
                        heading_label.place(x=400, y=40)

                        # for the line
                        purple = Frame(self.master, width=2, height=452, bg="#7868d5")
                        purple.place(x=224, y=30)

                        name_frame = Frame(self.master, width=200, height=200, bg="white")
                        name_frame.place(x=23, y=180)

                        global profile_pic, profile_label
                        profile_pic = PhotoImage(file="profile_pic.png")
                        # create a label for bg
                        profile_label = Label(self.master, image=profile_pic, bg="white")
                        profile_label.place(x=75, y=40)

                        # welcome user label
                        welcome_label1 = Label(self.master, text="Welcome",
                                               font=("Arial", 18, "bold"), bg="white", fg="#7868d5", anchor="center")
                        welcome_label1.place(x=70, y=150)

                        welcome_label = Label(name_frame, text=f"{name}", font=("Arial", 18, "bold"), bg="white",
                                              fg="#7868d5")
                        welcome_label.place(relx=0.5, rely=0.1, anchor=CENTER)

                        # your profile button
                        profile_button = Button(self.master, width=18, height=2, text="Your Profile",
                                                font=("Arial", 10, "bold"), bg="#7868d5",
                                                fg="white", bd=0, command=profile)
                        profile_button.place(x=50, y=240)

                        # diagnostic report button
                        report_button = Button(self.master, width=18, height=2, text="Patient Reports",
                                               font=("Arial", 10, "bold"),
                                               bg="#7868d5", fg="white", bd=0, command=report)
                        report_button.place(x=50, y=320)

                        # feedback report button
                        feedback_button = Button(self.master, width=18, height=2, text="Feedback",
                                                 font=("Arial", 10, "bold"),
                                                 bg="#7868d5", fg="white", bd=0, command=feedback)
                        feedback_button.place(x=50, y=400)

                        # recycle bin report button
                        recycle_button = Button(self.master, width=18, height=2, text="Deleted Records",
                                                font=("Arial", 10, "bold"), bg="#7868d5", fg="white", bd=0,
                                                command=deleted_records)
                        recycle_button.place(x=50, y=480)

                        # logout button
                        logout1 = Button(self.master, height=2, width=10,
                                         text="logout", bg="#7868d5", fg="white", bd=0, command=logout)
                        logout1.place(x=895, y=37)
                    elif selected == "Receptionist":
                        un_entry.delete(0, END)
                        un_entry.insert(0, "Username")
                        pw_entry.delete(0, END)
                        pw_entry.insert(0, "Password")
                        self.new_window = Toplevel(self.master)
                        self.app = Receptionist(self.new_window)

                    elif selected == "Patient":

                        # define image
                        bg = PhotoImage(file="page.png")
                        # create a label for bg
                        my_label = Label(self.master, image=bg)
                        my_label.place(x=0, y=0, relwidth=1, relheight=1)

                        # for the line
                        purple = Frame(self.master, width=2, height=452, bg="#7868d5")
                        purple.place(x=224, y=30)

                        # data frame
                        main_frame = Frame(self.master, width=753, height=452, bg="white")
                        main_frame.place(x=224, y=80)
                        profile()

                        # heading
                        heading_label1 = Label(self.master, text="Sweet Tooth Dental Clinic",
                                               font=("Arial", 20, "bold"), bg="white", fg="#7868d5")
                        heading_label1.place(x=400, y=40)

                        # frame for buttons
                        patient_btn_frame = Frame(self.master, width=200, height=504, bg="white")
                        patient_btn_frame.place(x=23, y=30)

                        global profile_pic1, profile_label1
                        profile_pic1 = PhotoImage(file="profile_pic.png")
                        # create a label for bg
                        profile_label1 = Label(patient_btn_frame, image=profile_pic1, bg="white")
                        profile_label1.place(x=45, y=20)

                        # welcome user label
                        welcome_label2 = Label(patient_btn_frame, text="Welcome",
                                               font=("Arial", 18, "bold"), bg="white", fg="#7868d5", anchor="center")
                        welcome_label2.place(x=50, y=130)

                        name_frame1 = Frame(self.master, width=200, height=50, bg="white")
                        name_frame1.place(x=23, y=200)

                        welcome_label = Label(name_frame1, text=f"{name}", font=("Arial", 15, "bold"), bg="white",
                                              fg="#7868d5")
                        welcome_label.place(relx=0.5, rely=0.2, anchor=CENTER)

                        # your profile button
                        p_btn1 = Button(patient_btn_frame, width=18, height=3, text="Your Profile",
                                        font=("Arial", 10, "bold"),
                                        bg="#7868d5", fg="white", bd=0, command=profile)
                        p_btn1.place(x=25, y=220)

                        p_btn2 = Button(patient_btn_frame, width=18, height=3, text="Treatments",
                                        font=("Arial", 10, "bold"), bg="#7868d5", fg="white", bd=0, command=treatments)
                        p_btn2.place(x=25, y=320)

                        p_btn3 = Button(patient_btn_frame, width=18, height=3, text="Contact Us",
                                        font=("Arial", 10, "bold"), bg="#7868d5", fg="white", bd=0, command=contactus)
                        p_btn3.place(x=25, y=420)

                        # logout button
                        logout1 = Button(self.master, height=2, width=10,
                                         text="logout", bg="#7868d5", fg="white", bd=0, command=logout)
                        logout1.place(x=895, y=37)

                else:
                    messagebox.showerror("Error", "Wrong Username or Password")

        # define image
        global bg
        bg = PhotoImage(file="dmsbg.png")
        # create a label for bg
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # sign in label
        heading = Label(self.master, text="SIGN IN", font=("Arial", 30, "bold"), fg="#7868d5", bg="white")
        heading.place(x=680, y=100)

        # Create a list of choices
        choices = ["Select", "Patient", "Receptionist", "Doctor"]
        # Create the label and ComboBox for login type
        label = Label(self.master, text="Select Login type:", bg="white", fg="#7868d5", font=("Arial", 15, "bold"))
        label.place(x=580, y=180)

        combo = Combobox(self.master, values=choices, font=("Arial", 20),
                         state="readonly", foreground="#7868d5", width=22, background="white")
        combo.current(0)  # Set the default choice to the first item
        combo.place(x=580, y=210)

        # username entry
        un_entry = Entry(self.master, font=("Arial", 20), width=15, fg="#7868d5", bd=0)
        un_entry.place(x=580, y=260)
        un_entry.insert(0, "Username")

        # password entry
        pw_entry = Entry(self.master, font=("Arial", 20), width=15, fg="#7868d5", bd=0)
        pw_entry.insert(0, "Password")
        pw_entry.place(x=580, y=320)

        # for the line
        frame1 = Frame(self.master, width=350, height=2, bg="#7868d5")
        frame1.place(x=580, y=290)
        frame2 = Frame(self.master, width=350, height=2, bg="#7868d5")
        frame2.place(x=580, y=350)

        def user_enter(event):
            if un_entry.get() == "Username":
                un_entry.delete(0, END)

        def pw_enter(event):
            if pw_entry.get() == "Password":
                pw_entry.delete(0, END)
                pw_entry.config(show="*")

        # binding
        un_entry.bind("<FocusIn>", user_enter)
        pw_entry.bind("<FocusIn>", pw_enter)

        def hide():
            open_eye.config(file="closeye.png")
            pw_entry.config(show="*")
            eye_button.config(command=show)

        def show():
            open_eye.config(file="openeye.png")
            pw_entry.config(show="")
            eye_button.config(command=hide)

        # eye icon
        open_eye = PhotoImage(file="closeye.png")
        eye_button = Button(self.master, image=open_eye, bd=0, bg="white",
                            activebackground="white", cursor="hand2", command=show)
        eye_button.place(x=900, y=320)

        # login button
        login_button = Button(self.master, width=15, height=2, text="Login",
                              bg="#7868d5", fg="white", bd=0, command=connect_database)
        login_button.place(x=580, y=380)

        # forget password button
        f_pass = Button(self.master, text="Forget Password?", font=("Arial", 10, "bold"), bg="white", fg="#604cd7",
                        activebackground="white", bd=0, command=forget_pass)
        f_pass.place(x=810, y=360)

        # sign up label and button
        label2 = Label(self.master, text="Don't have an account?", font=("Arial", 10), bg="white", fg="#7868d5")
        label2.place(x=580, y=430)
        signup_button = Button(self.master, text="Sign Up", font=("Arial", 10, "bold"), bg="white", fg="#604cd7",
                               activebackground="white", bd=0, command=signup)
        signup_button.place(x=716, y=429)


if __name__ == "__main__":
    root = Tk()
    login_page = DentalClinicManagement(root)
    root.mainloop()
