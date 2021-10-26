import uuid
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


def mean_value(array):
    elem_dim = len(array[0])
    size = len(array)
    mean = []
    for _ in range(elem_dim):
        mean.append(0)
    for elem in array:
        for index in range(elem_dim):
            mean[index] += elem[index]
    for index in range(elem_dim):
        mean[index] = mean[index] / size
    return tuple(mean)


def k_means(np_array: np.ndarray, k=16, max_iter=10):
    print("Début k-means")
    def get_closest_cluster_mean_index(v, cl_means):
        cl_index = -1
        min_distance = 442  # sqrt(255^2+255^2+255^2) max distance possible for rgb
        for cluster_index in range(len(cl_means)):
            cluster_mean = cl_means[cluster_index]
            dist = manhattan_distance(v, cluster_mean)
            if dist <= min_distance:
                cl_index = cluster_index
                min_distance = dist
        return cl_index

    cluster_means = []
    cluster_sets = []

    # Init randomly k-means
    for i in range(k):
        cluster_means.append((rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)))

    for i in range(max_iter):
        print("Iteration : ", i)
        # Clear cluster sets
        cluster_sets.clear()
        for _ in range(k):
            cluster_sets.append([])

        # Choose cluster for every value of the array
        for x in range(np_array.shape[0]):  # np_array.shape[0] -> number of x pixels
            for y in range(np_array.shape[1]):  # np_array.shape[1] -> number of y pixels
                value = np_array[x][y]

                # Choose cluster for value (R,G,B)
                closest_cluster_index = get_closest_cluster_mean_index(value, cluster_means)
                cluster_sets[closest_cluster_index].append(value)

        # Compute new means
        for cluster_mean_index in range(len(cluster_means)):
            # Compute centroid
            if len(cluster_sets[cluster_mean_index]) > 0:
                cluster_means[cluster_mean_index] = mean_value(cluster_sets[cluster_mean_index])
            else:
                cluster_means[cluster_mean_index] = (rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))  # if no value in cluster, we choose to try a new random point

    np_means = np_array.copy()
    for x in range(np_means.shape[0]):
        for y in range(np_means.shape[1]):
            val = np_means[x][y]
            np_means[x][y] = cluster_means[get_closest_cluster_mean_index(val, cluster_means)]

    return cluster_means, np_means


def apply_transformations():
    global image
    k = 16
    img_array = np.array(image)
    k_means_res = k_means(img_array, k=k)
    k_means_img = Image.fromarray(k_means_res[1])
    print(k_means_res[0])
    k_means_img.save("img/k_means_" + str(k) + ".png")


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

button_explore.grid(column=3, row=2)

button_exit.grid(column=3, row=3)

iterations = ('5', '10','20','50')
options = ('k-8','k-16','k-32','db-eucli','db-manhattan')
b3 = Button(ws, image=None)  # using Button
b3.grid(row=6, column=1)


def run_search():
    global image
    if image is None:
        print("Pas d'image sélectionnée !")
        return
    search_method = combobox_method.current()
    search_option = combobox_option.current()
    iter = int(iterations[combobox_iter.current() + 1])

    np_image = np.array(image)
    print(search_method)
    if search_method == 0:  # Kmeans
        print("KMEANS")
        k = 8
        if search_option == 0:
            k = 8
        if search_option == 1:
            k = 16
        if search_option == 2:
            k = 32
        if search_option >= 3:
            print("Mauvais search_option ! 1 <= x <= 4")
            return 0
        res = k_means(np_image, k=k, max_iter=iter)
        k_means_img = Image.fromarray(res[1])
        print("Moyennes calculées : ", res[0])
        k_means_img.save("output/k_means_" + str(k) + "_" + str(uuid.uuid4()) + ".png")
        resImg = ImageTk.PhotoImage(k_means_img)
        b3.image = resImg
    elif search_method == 1:  # DBSCAN
        if search_option <= 2:
            return 0
        if search_option == 3:
            db_scan('e')
        if search_option == 4:
            db_scan('m')




canvas1 = tk.Canvas(ws)
canvas1.grid(row=0, column=0, columnspan=4)
label_method = tk.Label(ws, text="Method")
label_method.grid(row=1, column=0)
combobox_method = ttk.Combobox(ws, state='readonly')
combobox_method.grid(row=1, column=1)
label_option = tk.Label(ws, text="Option")
label_option.grid(row=1, column=2)
combobox_option = ttk.Combobox(ws, state='readonly')
combobox_option.grid(row=1, column=3)
label_iter = tk.Label(ws, text="Iteration")
label_iter.grid(row=2, column=0)
combobox_iter = ttk.Combobox(ws, state='readonly')
combobox_iter.grid(row=2, column=1)
combobox_method['values'] = ['k-means','dbscan']
combobox_option['values'] = options
combobox_iter['values'] = iterations
button_run = tk.Button(ws, text='Calculate', command=run_search)
button_run.grid(row=5, column=0)



ws.mainloop()
