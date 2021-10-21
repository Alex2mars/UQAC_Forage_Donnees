from math import sqrt
from tkinter import *
from tkinter import filedialog
import numpy as np
import random as rnd
from PIL import Image, ImageTk

image = None


def euclidian_distance(p1, p2):
    size = len(p1)
    distance = 0
    for i in range(size):
        distance += (p1[i] - p2[i]) ** 2
    return sqrt(distance)


def k_means(np_array: np.ndarray, k=32, max_iter=10000):
    cluster_means = []
    cluster_sets = []

    # Init randomly init means
    for i in range(k):
        cluster_means.append((rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)))

    for i in range(max_iter):
        # Clear cluster sets
        cluster_sets.clear()
        for _ in range(k):
            cluster_sets.append([])

        # Start iteration
        for x in range(np_array.shape[0]):
            for y in range(np_array.shape[1]):
                value = np_array[x][y]

                # Choose cluster for value (R,G,B)
                closest_cluster_index = -1
                min_distance = 66000 # sqrt(255^2+255^2+255^2)
                for cluster_index in range(len(cluster_means)):
                    cluster_mean = cluster_means[cluster_index]
                    dist = euclidian_distance(value, cluster_mean)
                    if dist <= min_distance:
                        closest_cluster_index = cluster_index
                        min_distance = dist

                cluster_sets[closest_cluster_index].append(value)



def apply_transformations():
    img_array = np.array(image)
    k_means_res = k_means(img_array, k=32)
    k_means_img = Image.fromarray(k_means_res[1])

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
    filename = "D:\\Dossiers\\UQAC\\UQAC_Forage_Donnees\\TP2 - Clustering couleurs\\img\\dolmanax.png"
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
