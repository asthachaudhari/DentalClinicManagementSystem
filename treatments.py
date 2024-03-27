from tkinter import *

bg = bg1 = bg2 = bg3 = bg4 = bg5 = bg6 = bg7 = bg_img = None

class Treatments:
    def __init__(self, master):
        self.master = master
        self.master.title("Treatments")
        self.master.geometry("1000x563+10+10")
        self.master.resizable(False, False)  # for fixed sized window

        def treatment1():
            global bg1
            bg1 = PhotoImage(file="dental treatment 1.png")
            my_label = Label(right_frame, image=bg1)
            my_label.place(x=0, y=0)

        def treatment2():
            global bg2
            bg2 = PhotoImage(file="dental treatment 2.png")
            my_label = Label(right_frame, image=bg2)
            my_label.place(x=0, y=0)

        def treatment3():
            global bg3
            bg3 = PhotoImage(file="dental treatment 3.png")
            my_label = Label(right_frame, image=bg3)
            my_label.place(x=0, y=0)

        def treatment4():
            global bg4
            bg4 = PhotoImage(file="dental treatment 4.png")
            my_label = Label(right_frame, image=bg4)
            my_label.place(x=0, y=0)

        def treatment5():
            global bg5
            bg5 = PhotoImage(file="dental treatment 5.png")
            my_label = Label(right_frame, image=bg5)
            my_label.place(x=0, y=0)

        def treatment6():
            global bg6
            bg6 = PhotoImage(file="dental treatment 6.png")
            my_label = Label(right_frame, image=bg6)
            my_label.place(x=0, y=0)

        def treatment7():
            global bg7
            bg7 = PhotoImage(file="dental treatment 7.png")
            my_label = Label(right_frame, image=bg7)
            my_label.place(x=0, y=0)

        def main_page():
            self.master.destroy()

        global bg
        bg = PhotoImage(file="page.png")
        # create a label for bg
        my_label = Label(self.master, image=bg)
        my_label.place(x=0, y=0, relwidth=1, relheight=1)

        treatments_frame = Frame(self.master, width=250, height=504, bg="#604cd7")
        treatments_frame.place(x=23, y=30)

        right_frame = Frame(self.master, width=701, height=502, bg="white")
        right_frame.place(x=275, y=30)

        global bg_img
        bg_img = PhotoImage(file="dms project img.png")
        bg_img_label = Label(right_frame, image=bg_img, bg="white")
        bg_img_label.place(x=120, y=20)

        button1 = Button(treatments_frame, text="Teeth Whitening", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment1)
        button1.place(x=20, y=20)

        button2 = Button(treatments_frame, text="Braces", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment2)
        button2.place(x=20, y=140)

        button3 = Button(treatments_frame, text="Teeth Cleaning", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment3)
        button3.place(x=20, y=80)

        button4 = Button(treatments_frame, text="Cosmetic Re-Contouring", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment4)
        button4.place(x=20, y=200)

        button5 = Button(treatments_frame, text="Orthodontic Treatment", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment5)
        button5.place(x=20, y=260)

        button6 = Button(treatments_frame, text="Implants", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment6)
        button6.place(x=20, y=320)

        button6 = Button(treatments_frame, text="Oral Care Tips", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=treatment7)
        button6.place(x=20, y=380)

        button7 = Button(treatments_frame, text="Main Page", fg="#7868d5",
                         font=("Arial", 12, "bold"), bg="white", anchor=CENTER, width=20, command=main_page)
        button7.place(x=20, y=440)


if __name__ == "__main__":
    root = Tk()
    treatments_page = Treatments(root)
    root.mainloop()
