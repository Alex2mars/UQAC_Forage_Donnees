import time
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
                closest_cluster_index = -1
                min_distance = 442  # sqrt(255^2+255^2+255^2) max distance possible for rgb
                for cluster_index in range(len(cluster_means)):
                    cluster_mean = cluster_means[cluster_index]
                    dist = euclidian_distance(value, cluster_mean)
                    if dist <= min_distance:
                        closest_cluster_index = cluster_index
                        min_distance = dist
                cluster_sets[closest_cluster_index].append(value)
        print("Fini cluster assignation")
        # Compute new means
        for cluster_mean_index in range(len(cluster_means)):
            # Compute centroid
            if len(cluster_sets[cluster_mean_index]) > 0:
                cluster_means[cluster_mean_index] = mean_value(cluster_sets[cluster_mean_index])
            else:
                cluster_means[cluster_mean_index] = (rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255))  # if no value in cluster, we choose to try a new random point

    def mean_for_value(val):
        closest_cluster_index = -1
        min_distance = 442  # sqrt(255^2+255^2+255^2) max distance possible for rgb
        for cluster_index in range(len(cluster_means)):
            cluster_mean = cluster_means[cluster_index]
            dist = euclidian_distance(val, cluster_mean)
            if dist <= min_distance:
                closest_cluster_index = cluster_index
                min_distance = dist
        return cluster_means[closest_cluster_index]


    np_means = np_array.copy()
    for x in range(np_means.shape[0]):
        for y in range(np_means.shape[1]):
            val = np_means[x][y]
            np_means[x][y] = mean_for_value(val)

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
