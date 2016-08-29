from Tkinter import *
import os

TITLE = 'pyTexed'

FILETYPES = [
    ("Text files", "*.txt"), ("All files", "*")
    ]


class RoomEditor(Text, object):

    modified = None

    def __init__(self, master, **options):
        Text.__init__(self, master, **options)

        self.config(
            borderwidth=0,
            font="{Lucida Sans Typewriter} 14",
            foreground="green",
            background="black",
            insertbackground="white", # cursor
            selectforeground="green", # selection
            selectbackground="#008000",
            wrap=WORD, # use word wrapping
            undo=True,
            width=64,
            )

        self.filename = None # current document

    def _getfilename(self):
        return self._filename

    def _setfilename(self, filename):
        self._filename = filename
        title = os.path.basename(filename or "(new document)")
        title = title + " - " + TITLE
        self.winfo_toplevel().title(title)

    filename = property(_getfilename, _setfilename)

    def edit_modified(self, value=None):
        # Python 2.5's implementation is broken
        return self.tk.call(self, "edit", "modified", value)

    def load(self, filename):
        text = open(filename).read()
        self.delete(1.0, END)
        self.insert(END, text)
        self.mark_set(INSERT, 1.0)
        self.modified = False
        self.filename = filename

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        f = open(filename, "w")
        s = self.get(1.0, END)
        try:
            f.write(s.rstrip())
            f.write("\n")
        finally:
            f.close()
        self.modified = False
        self.filename = filename

    def clear(self):
        pass

class Cancel(Exception):
    pass

def open_as():
    from tkFileDialog import askopenfilename
    f = askopenfilename(parent=root, filetypes=FILETYPES)
    if not f:
        raise Cancel
    try:
        editor.load(f)
    except IOError:
        from tkMessageBox import showwarning
        showwarning("Open", "Cannot open the file.")
        raise Cancel

def save_as():
    from tkFileDialog import asksaveasfilename
    f = asksaveasfilename(parent=root, defaultextension=".txt")
    if not f:
        raise Cancel
    try:
        editor.save(f)
    except IOError:
        from tkMessageBox import showwarning
        showwarning("Save As", "Cannot save the file.")
        raise Cancel

def save():
    if editor.filename:
        try:
            editor.save(editor.filename)
        except IOError:
            from tkMessageBox import showwarning
            showwarning("Save", "Cannot save the file.")
            raise Cancel
    else:
        save_as()

def save_if_modified():
    if not editor.modified:
        return
    if askyesnocancel(TITLE, "Document modified. Save changes?"):
        save()

def askyesnocancel(title=None, message=None, **options):
    import tkMessageBox
    s = tkMessageBox.Message(
        title=title, message=message,
        icon=tkMessageBox.QUESTION,
        type=tkMessageBox.YESNOCANCEL,
        **options).show()
    if isinstance(s, bool):
        return s
    if s == "cancel":
        raise Cancel
    return s == "yes"

def file_new(event=None):
    try:
        save_if_modified()
        editor.clear()
    except Cancel:
        pass
    return "break" # don't propagate events

def file_open(event=None):
    try:
        save_if_modified()
        open_as()
    except Cancel:
        pass
    return "break"

def file_save(event=None):
    try:
        save()
    except Cancel:
        pass
    return "break"

def file_save_as(event=None):
    try:
        save_as()
    except Cancel:
        pass
    return "break"

def file_quit(event=None):
    try:
        save_if_modified()
    except Cancel:
        return
    root.quit()

root = Tk()
root.config(background="black")

root.wm_state("zoomed")

editor = RoomEditor(root)
editor.pack(fill=Y, expand=1, pady=10)

editor.focus_set()

editor.bind("<Control-n>", file_new)
editor.bind("<Control-o>", file_open)
editor.bind("<Control-s>", file_save)
editor.bind("<Control-Shift-S>", file_save_as)
editor.bind("<Control-q>", file_quit)

root.protocol("WM_DELETE_WINDOW", file_quit) # window close button

try:
    editor.load(sys.argv[1])
except (IndexError, IOError):
    pass

mainloop()
