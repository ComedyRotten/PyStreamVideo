from tkinter import *
import tkinter.messagebox


def doNothing():
    print("Ok, ok, I won't...")


def askQuestion():
    # ******* Message Box ********
    # tkinter.messagebox.showinfo("Window Title", "Monkey's can live in space...")
    answer = tkinter.messagebox.askyesno("My Question", "Do you love me?")
    if answer:
        print("<3")
    else:
        print("):")

root = Tk()

# ******* Main Menu ********

menu = Menu(root)
# configure a menu using the previously instantiated menu
root.config(menu=menu)
# add a submenu (e.g. "File, Edit, Help, etc.")
subMenu = Menu(menu)
# create a File button with the drop-down menu with the subMenu
menu.add_cascade(label="File", menu=subMenu)
# add a sub-option/command and assign a method to each
subMenu.add_command(label="New Project...", command=doNothing)
subMenu.add_command(label="Save Project...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Undo...", command=doNothing)

# ******* Toolbar ********
toolbar = Frame(root, bg="blue")
insert_button = Button(toolbar, text="Insert Image", command=doNothing)
insert_button.pack(side=LEFT, padx=2, pady=2)
print_button = Button(toolbar, text="Print", command=doNothing)
print_button.pack(side=LEFT, padx=2, pady=2)
question_button = Button(toolbar, text="Question", command=askQuestion)
question_button.pack(side=LEFT, padx=2, pady=2)

toolbar.pack(side=TOP, fill=X)

# ******* Status Bar ********
# bd = border, anchor = West (make sure text appears on the left)
status = Label(root, text="Ready", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

'''
# ******* Graphics ********
canvas = Canvas(root, width=200, height=100)
canvas.pack()

black_line = canvas.create_line(25, 25, 175, 75)
red_line = canvas.create_line(0, 0, 200, 50, fill="red")
green_box = canvas.create_rectangle(50, 10, 80, 40, fill="green")

# delete graphics
canvas.delete(red_line)
'''
# ******* Sprites and Icons *******

photo = PhotoImage(file="pic.png")
label = Label(root, image=photo)
label.pack()

root.mainloop()
