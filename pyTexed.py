from Tkinter import *
import os, re, ast

TITLE = 'pyTexed'
ABOUT_TEXT = 'something'
CURRENT_APPEARANCE = None

FILETYPES = [
    ("Python Files", "*.py"), ("Text files", "*.txt"), ("All files", "*")
    ]

APPEARANCE_DARK = {'borderwidth': 0,
            'font':"{Lucida Sans Typewriter} 11",
            'foreground':"#cc9900",
            'background':"black",
            'insertbackground':"green",
            'selectforeground':"white",
            'selectbackground':"#008000"}

APPEARANCE_LIGHT = {'borderwidth': 0,
                   'font': "{Lucida Sans Typewriter} 11",
                   'foreground': "black",
                   'background': "white",
                   'insertbackground': "black",
                   'selectforeground': "white",
                   'selectbackground': "blue"}

class RoomEditor(Text, object):

    modified = None

    def __init__(self, master, **options):
        Text.__init__(self, master, **options)
        self.configure(dict=APPEARANCE_DARK)

        self.filename = None  # current document

    def configure(self, dict):
        global CURRENT_APPEARANCE

        if isinstance(dict, basestring):
            dictionary = ast.literal_eval(dict)
        else:
            dictionary = dict

        CURRENT_APPEARANCE = dictionary

        self.config(
            borderwidth=dictionary['borderwidth'],
            font=dictionary['font'],
            foreground=dictionary['foreground'],
            background=dictionary['background'],
            insertbackground=dictionary['insertbackground'],
            selectforeground=dictionary['selectforeground'],
            selectbackground=dictionary['selectbackground'],
            wrap=WORD,
            undo=True,
            width=64,
        )



    def _getfilename(self):
        return self._filename

    def _setfilename(self, filename):
        self._filename = filename
        title = os.path.basename(filename or "(new document)")
        title = title + " - " + TITLE
        self.winfo_toplevel().title(title)

    filename = property(_getfilename, _setfilename)

    def edit_modified(self, value=None):
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

def change_appearance():

    v = StringVar()
    v.set("L")

    APPEARNCES = {"Light": APPEARANCE_LIGHT, "Dark": APPEARANCE_DARK}

    toplevel = Toplevel()
    Label(toplevel, text='Change Appearance', height=0, width=100).pack()

    def select():
        try:
            editor.configure(v.get())
        except ValueError as e:
            pass
        toplevel.destroy()

    for text, mode in APPEARNCES.iteritems():
        b = Radiobutton(toplevel, text=text, variable=v, value=mode)
        b.pack(anchor=W)

    Button(toplevel, text="Ok", height=0, width=100, command=select).pack()

def temp(val):
    for k, v in val.iteritems():
        print k, v

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

def about(event=None):
    toplevel = Toplevel()
    Label(toplevel, text='About pyTexed', height=0, width=100).pack()
    Label(toplevel, text=ABOUT_TEXT , height=0, width=100).pack()
    Button(toplevel, text="Ok", height=0, width=100, command=toplevel.destroy).pack()

def find(event=None):

    toplevel = Toplevel()
    entry = Entry(toplevel)
    entry.pack()

    v = StringVar()
    def select():
        v = entry.get()
        editor.configure(CURRENT_APPEARANCE)
        search_and_highlight(pattern=v, tag="found")

    def destroy_and_reset():
        editor.tag_config('', background="black", foreground="#cc9900")
        start = editor.index('1.0')
        end = editor.index('end')
        editor.mark_set("matchStart", start)
        editor.mark_set("matchEnd", end)
        editor.tag_add('', "matchStart", "matchEnd")
        toplevel.destroy()

    Button(toplevel, text="Find", height=0, width=100, command=select).pack()
    Button(toplevel, text="Ok", height=0, width=100, command=destroy_and_reset).pack()

def search_and_highlight(pattern, tag="found", start="1.0", end="end", regexp=False):

    start = editor.index(start)
    end = editor.index(end)
    editor.mark_set("matchStart", start)
    editor.mark_set("matchEnd", start)
    editor.mark_set("searchLimit", end)

    count = IntVar()
    editor.tag_config(tag.__str__(), background="white", foreground="black")
    while True:
        index = editor.search(pattern, "matchEnd", "searchLimit",
                            count=count, regexp=regexp)
        if index == "": break
        if count.get() == 0: break  # degenerate pattern which matches zero-length strings
        editor.mark_set("matchStart", index)
        editor.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        editor.tag_add(tag, "matchStart", "matchEnd")

def find_and_replace(event=None):
    """
    work in progress

    """

    match_string = 'tes'
    newline = "\n"
    data = editor.get("1.0", END)
    lines = data.split(newline)
    p = re.compile(match_string)

    results = []
    line_num = 0
    for line in lines:
        line_num += 1
        iterator = p.finditer(line)
        for match in iterator:
            res = match.span()
            sys.stdout.write(str(res))
            results.append((line_num, res[0], res[1]))
        sys.stdout.write(newline)

    print results

def main(root):

    menu = Menu(root)
    root.config(menu=menu)

    # file menu dro down
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)

    filemenu.add_command(label="New", command=file_new)
    filemenu.add_command(label="Open", command=file_open)
    filemenu.add_command(label="Save", command=file_save)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=file_quit)

    # help menu drop down
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About...", command=about)

    # tools menu drop down
    toolsmenu = Menu(menu)
    menu.add_cascade(label="Tools", menu=toolsmenu)
    toolsmenu.add_command(label="Find", command=find)

    # settings menu drop down
    settingsmenu = Menu(menu)
    menu.add_cascade(label="Settings", menu=settingsmenu)
    settingsmenu.add_command(label="Change Appearance", command=change_appearance)

    # tools menu drop down
    toolsmenu = Menu()
    toolsmenu.add_cascade(label="Tools", menu=filemenu)

    toolsmenu.add_command(label="Find", command=find)

    # editor set up
    root.config(background="black")
    root.wm_state("zoomed")

    editor.pack(fill=Y, expand=1, pady=10)

    editor.focus_set()

    # key bindings for short cuts
    editor.bind("<Control-n>", file_new)
    editor.bind("<Control-o>", file_open)
    editor.bind("<Control-s>", file_save)
    editor.bind("<Control-Shift-S>", file_save_as)
    editor.bind("<Control-q>", file_quit)
    editor.bind("<Control-f>", find)
    # editor.bind("<Control-r>", editor.configure)

    root.protocol("WM_DELETE_WINDOW", file_quit) # window close button

    try:
        editor.load(sys.argv[1])
    except (IndexError, IOError):
        pass

    mainloop()


root = Tk()
editor = RoomEditor(root)

main(root)
sys.exit(0)
