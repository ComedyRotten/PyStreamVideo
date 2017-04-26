from tkinter import *

# Create a blank window
# root = Tk()
'''
# EXAMPLE 1 - Windows
# Put text in the window
theLabel = Label(root, text="This is too easy!")
# Designate where to put the text - pack it in wherever you can
theLabel.pack()
'''

'''
# EXAMPLE 2 - Buttons
# Make a container in the program
topFrame = Frame(root)
# Place the frame in the root window
topFrame.pack()
# Make another frame/container in the program
bottomFrame = Frame(root)
# Place the frame at the bottom of the root window
bottomFrame.pack(side=BOTTOM)

# Create 4 colored buttons labeled "Button #" in the topFrame
button1 = Button(topFrame, text="Button 1", fg="red")
button2 = Button(topFrame, text="Button 2", fg="blue")
button3 = Button(topFrame, text="Button 3", fg="green")
button4 = Button(bottomFrame, text="Button 4", fg="purple")

# Display the buttons in the window frames
button1.pack(side=LEFT)
button2.pack(side=RIGHT)
button3.pack(side=LEFT)
button4.pack(side=BOTTOM)
'''

'''
# EXAMPLE 3 - Fitting Widgets in the Layout
one = Label(root, text="One", bg="red", fg="white")
one.pack()
two = Label(root, text="Two", bg="green", fg="black")
# Fill it as long as the parent frame is in the x direction
two.pack(fill=X)
three = Label(root, text="Three", bg="blue", fg="white")
# Fill it as long as the parent frame is in the y direction on the left
three.pack(side=LEFT, fill=Y)
'''

'''
# EXAMPLE 4 - Grid Layout
# Create widgets
label_1 = Label(root, text="Name")
label_2 = Label(root, text="Password")
entry_1 = Entry(root)
entry_2 = Entry(root)

# Place the widgets in a grid aligned to the East
label_1.grid(row=0, sticky=E)
label_2.grid(row=1, sticky=E)
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)

# Create a checkbox
c = Checkbutton(root, text="Keep me logged in.")
c.grid(columnspan=2)
'''

'''
# EXAMPLE 5 - Binding Functions to Layouts
# def print_name():
def print_name(event):
    print("Hello, my name is Bucky!")

# button_1 = Button(root, text="Print my name", command=print_name)
button_1 = Button(root, text="Print my name")
button_1.bind("<Button-1>", print_name)  # New line
button_1.pack()
'''

'''
# EXAMPLE 6 - Mouse-Click Events
def left_click(event):
    print("Left")


def middle_click(event):
    print("Middle")


def right_click(event):
    print("Right")

frame = Frame(root, width=300, height=240)
frame.bind("<Button-1>", left_click)
frame.bind("<Button-2>", middle_click)
frame.bind("<Button-3>", right_click)
frame.pack()
'''

'''
# EXAMPLE 7 - Using Classes
class MyButtons:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.printButton = Button(frame, text="Print message", command=self.print_message)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    @staticmethod
    def print_message():
        print("Printing a message!!!")

# Create a blank window
root = Tk()
b = MyButtons(root)

# The mainloop is keeping the window on the screen
root.mainloop()
'''

# Stuff after the window is closed is executed here before the program ends
print("Ended the loop!")
