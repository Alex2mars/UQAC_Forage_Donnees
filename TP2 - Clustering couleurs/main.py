from tkinter import *
from tkinter import filedialog
import tkinter as tk

def browseFiles():
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    img = PhotoImage(file=filename)
    b2 = tk.Button(ws, image=img)  # using Button
    b2.grid(row=3, column=1)

ws = Tk()
ws.title('PythonGuides')

label_file_explorer = Label(ws,
                            text = "File Explorer using Tkinter",
                            width = 100, height = 4,
                            fg = "blue")
button_explore = Button(ws,
                        text="Browse Files",
                        command=browseFiles)

button_exit = Button(ws,
                     text="Exit",
                     command=exit)
label_file_explorer.grid(column=1, row=1)

button_explore.grid(column=1, row=2)

button_exit.grid(column=1, row=3)


ws.mainloop()