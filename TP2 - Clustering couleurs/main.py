from math import sqrt
from tkinter import *
from tkinter import filedialog
import numpy as np
import random as rnd
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk

image = None


def euclidian_distance(p1, p2):
    size = len(p1)
    distance = 0
    for i in range(size):
        distance += (p1[i] - p2[i]) ** 2
    return sqrt(distance)

def manhattan_distance(p1, p2):
    size = len(p1)
    distance = 0
    for i in range(size):
        distance += abs(p1[i] - p2[i])
    return sqrt(distance)


def Neighbours(p1, p2, eps):
    temp = []
    for y in range(len(p2)):
        for x in range(len(p2[0])):
            if euclidian_distance(p1, p2[y][x]) <= eps:
                temp.append(p2[y][x])
    return temp


def db_scan():

    return 0


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


def run_search():
    search_method = combobox_start.current()
    search_option = combobox_end.current()
    if search_method == 1:  # Kmeans
        if search_option == 1:
            k_means(8)
        if search_option == 2:
            k_means(16)
        if search_option == 3:
            k_means(32)
        if search_option >= 4:
            return 0
    elif search_method == 2:  # DBSCAN
        if search_option <= 3:
            return 0
        if search_option == 4:
            db_scan('e')
        if search_option == 5:
            db_scan('m')


canvas1 = tk.Canvas(ws)
canvas1.grid(row=0, column=0, columnspan=4)
label_start = tk.Label(ws, text="Method")
label_start.grid(row=1, column=0)
combobox_start = ttk.Combobox(ws, state='readonly')
combobox_start.grid(row=1, column=1)
label_end = tk.Label(ws, text="Option")
label_end.grid(row=1, column=2)
combobox_end = ttk.Combobox(ws, state='readonly')
combobox_end.grid(row=1, column=3)
combobox_start['values'] = ['k-means','dbscan']
combobox_end['values'] = ['k-8','k-16','k-32','db-eucli','db-manhattan']
button_run = tk.Button(ws, text='Calculate', command=run_search)
button_run.grid(row=5, column=0)

ws.mainloop()
