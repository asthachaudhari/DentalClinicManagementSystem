from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import mysql.connector
from io import BytesIO

# Establish a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="Astha",
    password="A1234",
    database="dms"
)

# Create a cursor object
cursor = db.cursor()

# Retrieve the PDF file from the database
sql = "SELECT file FROM documents WHERE name = %s"
val = ("myfile.png", )
cursor.execute(sql, val)
result = cursor.fetchone()

# Convert the binary data to an image
img = Image.open(BytesIO(result))
img = img.resize((100, 100), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)

# Create a treeview widget
root = Tk()
tree = Treeview(root)
tree.pack()

# Insert the image in the treeview
tree.insert("", 0, text="My PDF File", image=photo)

# Start the main loop
root.mainloop()

# Close the database connection
db.close()
