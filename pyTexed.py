import Tkinter
from Tkinter import *
from ScrolledText import *
import tkFileDialog
import tkMessageBox

root = Tkinter.Tk(className="Just another Text Editor")
editor = ScrolledText(root, width=100, height=80)

# create a menu & define functions for each menu item

def open_command():
        filename = tkFileDialog.askopenfile(parent=root,mode='rb',title='Select a file')
        if filename != None:
            text = open(filename).read()
            editor.delete(1.0, END)
            editor.insert(END, text)
            editor.mark_set(INSERT, 1.0)

def save_command():
    filename = tkFileDialog.asksaveasfile(parent=root, mode='w',title='Enter a Destination',defaultextension=".txt")
    if filename != None:
        f = open(filename, "w")
        text = editor.get(1.0, END)
        try:
            # normalize trailing whitespace
            f.write(text.rstrip())
            f.write("\n")
        finally:
            f.close()

def exit_command():
    if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
        sys.exit(0)

def about_command():
    label = tkMessageBox.showinfo("About", "Just Another TextPad \n Copyright \n No rights left to reserve")


def dummy():
    print "I am a Dummy Command, I will be removed in the next step"

def main():
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=dummy)
    filemenu.add_command(label="Open...", command=open_command)
    filemenu.add_command(label="Save", command=save_command)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit_command)
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=about_command)

    # theme changing
    editor.pack(fill=Y, expand=1)
    editor.config(borderwidth=0,
    font="{Lucida Sans Typewriter} 12",
    foreground="green",
    background="black",
    insertbackground="white", # cursor
    selectforeground="green", # selection
    selectbackground="#008000",
    wrap=WORD, # use word wrapping
    width=64,
    undo=True, # Tk 8.4
    )

    editor.focus_set()

    root.mainloop()

main()