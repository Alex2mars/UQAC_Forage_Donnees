from tkinter import *
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk

image = None


def apply_transformations():
    img_array = np.array(image)
    print(img_array)

def FindNeighbours(Point, Points, distanceFunction, eps):
    tempNeighbours = []
    for y in range(len(Points)):
        for x in range(len(Points[0])):
            if distanceFunction == "e":
                if EuclideanDistance(Point, Points[y][x]) <= eps:
                    tempNeighbours.append(Points[y][x])
            if distanceFunction == "m":
                if MaximumDistance(Point, Points[y][x]) <= eps:
                    tempNeighbours.append(Points[y][x])
    return tempNeighbours


def browseFiles():
    global image
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Image files",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    image = Image.open(filename)
    image = image.convert("RGB")
    tkImg = ImageTk.PhotoImage(image)
    b2 = Button(ws, image=tkImg)  # using Button
    b2.image = tkImg
    b2.grid(row=3, column=1)

    apply_transformations()


ws = Tk()
ws.title('Clustering de couleurs')

label_file_explorer = Label(ws,
                            text="File Explorer using Tkinter",
                            width=100, height=4,
                            fg="blue")
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
