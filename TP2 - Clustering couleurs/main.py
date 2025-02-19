import datetime
import uuid
import math
from collections import defaultdict
from tkinter import *
from tkinter import filedialog
import numpy as np
import random as rnd
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
from tkinter.ttk import *
image = None


def euclidian_distance(p1, p2):
    size = len(p1)
    distance = 0
    for i in range(size):
        distance += (p1[i] - p2[i]) ** 2
    return math.sqrt(distance)


def manhattan_distance(p1, p2):
    size = len(p1)
    distance = 0
    for i in range(size):
        distance += abs(p1[i] - p2[i])
    return math.sqrt(distance)


def get_neighbour_indexes(db: np.ndarray, point_index, dist_fn, distance):
    neighbours = []
    point = db[point_index]
    rgb_index = -1
    for rgb in db:
        rgb_index += 1
        if rgb_index == point_index:
            continue
        if dist_fn(rgb, point) <= distance:
            neighbours.append(rgb_index)
    return neighbours


def db_scan(np_array: np.ndarray, min_pts=4, max_distance=6, distance_function=manhattan_distance):
    flat_array = np_array.flatten().reshape((-1, 3))  # [[r, g, b], [...], [...], ...]

    labels = dict()  # (index_in_array: label, ...)

    cluster_n = 0

    rgb_index = -1
    for rgb in flat_array:
        rgb_index += 1
        if rgb_index in labels:  # Already labeled/visited
            continue
        neighbour_indexes = get_neighbour_indexes(flat_array, rgb_index, distance_function, max_distance)
        if len(neighbour_indexes) < min_pts:
            labels[rgb_index] = "noise"
            continue
        cluster_n += 1
        labels[rgb_index] = cluster_n

        expand_indexes = neighbour_indexes.copy()
        for ex_ind in expand_indexes:
            if ex_ind in labels and labels[ex_ind] == "noise":
                labels[ex_ind] = cluster_n
            if ex_ind in labels:
                continue
            labels[ex_ind] = cluster_n
            expand_neighbour_indexes = get_neighbour_indexes(flat_array, ex_ind, distance_function, max_distance)
            if len(expand_neighbour_indexes) >= min_pts:
                expand_indexes.extend(expand_indexes)

    clusters = defaultdict(list)
    for key, value in labels.items():
        clusters[value].append(key)
    cluster_means = defaultdict(tuple)

    for cluster, indexes in clusters.items():
        cluster_means[cluster] = mean_value(list(map(lambda ind: flat_array[ind], indexes)))

    res_flat_array = []
    for index in range(len(flat_array)):
        res_flat_array.append(cluster_means[labels[index]])
    res_flat_array = np.array(res_flat_array)

    return labels, res_flat_array.reshape((-1, 2, 3))



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

    def check_means_equal_interval(means1, means2, interval=2):
        for ind in range(len(means1)):
            mean1 = means1[ind]
            mean2 = means2[ind]
            for ind_x in range(len(mean1)):
                val_1 = mean1[ind_x]
                val_2 = mean2[ind_x]
                possible_values = [val_1 + v for v in range(-interval, interval + 1)]
                if val_2 not in possible_values:
                    return False
        return True

    cluster_means = []
    cluster_sets = []

    # Init randomly k-means
    for i in range(k):
        cluster_means.append((rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)))

    for i in range(max_iter):
        print("Iteration : ", i)
        bar(max_iter)
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
        old_means = cluster_means.copy()
        for cluster_mean_index in range(len(cluster_means)):
            # Compute centroid
            if len(cluster_sets[cluster_mean_index]) > 0:
                cluster_means[cluster_mean_index] = np.floor(mean_value(cluster_sets[cluster_mean_index]))
            else:
                cluster_means[cluster_mean_index] = (rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0,
                                                                                                           255))  # if no value in cluster, we choose to try a new random point
        if check_means_equal_interval(old_means, cluster_means, interval=2):
            print("L'algorithme a trouvé des clusters stables avant max_iter !")
            break
    np_means = np_array.copy()
    for x in range(np_means.shape[0]):
        for y in range(np_means.shape[1]):
            val = np_means[x][y]
            np_means[x][y] = cluster_means[get_closest_cluster_mean_index(val, cluster_means)]

    return cluster_means, np_means


def browseFiles():
    global image
    filename = filedialog.askopenfilename(initialdir="./img/",
                                          title="Select a File",
                                          filetypes=(("Image files",
                                                      "*.png*"),
                                                     ("all files",
                                                      "*.*")))
    if not filename:
        return
    # Change label contents
    image = Image.open(filename)
    image = image.convert("RGB")
    tkImg = ImageTk.PhotoImage(image)
    b2 = Button(ws, image=tkImg)  # using Button
    b2.image = tkImg
    b2.grid(row=0, column=0)


ws = Tk()
ws.title('Clustering de couleurs')
label_input = Label(ws, text="Input")
label_output = Label(ws, text="Output")
label_input.grid(column=0, row=1)
label_output.grid(column=1, row=1)

button_explore = Button(ws,
                        text="Browse Files",
                        command=browseFiles)

button_exit = Button(ws,
                     text="Exit",
                     command=exit)

button_explore.grid(column=3, row=3)

button_exit.grid(column=2, row=4)

iterations = ('5', '10', '20', '50', "=> Clusters stables")
options = ('k-8', 'k-16', 'k-32', 'db-eucli', 'db-manhattan')


def get_date_str():
    return datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")


def run_search():
    global image
    if image is None:
        print("Pas d'image sélectionnée !")
        return
    search_method = combobox_method.current()
    search_option = combobox_option.current()
    iter_str = iterations[combobox_iter.current()]
    if iter_str == "=> Clusters stables":
        iters = 10000000
    else:
        iters = int(iter_str)

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
        res = k_means(np_image, k=k, max_iter=iters)
        k_means_img = Image.fromarray(res[1])
        print("Moyennes calculées : ", res[0])
        k_means_img.save("output/k_means_" + str(k) + "_" + get_date_str() + ".png")
        resImg = ImageTk.PhotoImage(k_means_img)
        b3 = Button(ws, image=resImg)
        b3.image = resImg
        b3.grid(row=0, column=1)
    elif search_method == 1:  # DBSCAN
        if search_option <= 2:
            return 0
        res = None
        if search_option == 3:
            res = db_scan(np_image, min_pts=5, max_distance=10, distance_function=euclidian_distance)
        if search_option == 4:
            res = db_scan(np_image, min_pts=5, max_distance=10, distance_function=manhattan_distance)
        dbscan_img = Image.fromarray(res[1])
        print("Clusters : ", res[0])
        dbscan_img.save("output/dbscan_" + "euc" if search_option == 3 else "man" + "_" + get_date_str() + ".png")
        resImg = ImageTk.PhotoImage(dbscan_img)
        b3 = Button(ws, image=resImg)
        b3.image = resImg
        b3.grid(row=0, column=1)


progress = Progressbar(ws, orient=HORIZONTAL,
                       length=100, mode='determinate')


# Function responsible for the updation
# of the progress bar value
progress_Label = tk.Label(ws, text="Progress Bar")
progress_Label.grid(row=5, column=1)


def bar(iterateNum):
    if iterateNum >= 10000:
        print("ici")
        progress_Label.config(text="Recherche en cours")
    else:
        progress['value'] += 100/iterateNum
        progress_Label['text'] = progress['value'], '%'
        ws.update_idletasks()


progress.grid(row=5, column=2)

# This button will initialize
# the progress bar


canvas1 = tk.Canvas(ws)
canvas1.grid(row=0, column=0, columnspan=4)
label_method = tk.Label(ws, text="Method")
label_method.grid(row=2, column=0)
combobox_method = ttk.Combobox(ws, state='readonly')
combobox_method.grid(row=2, column=1)
label_option = tk.Label(ws, text="Option")
label_option.grid(row=2, column=2)
combobox_option = ttk.Combobox(ws, state='readonly')
combobox_option.grid(row=2, column=3)
label_iter = tk.Label(ws, text="Iteration")
label_iter.grid(row=3, column=0)
combobox_iter = ttk.Combobox(ws, state='readonly')
combobox_iter.grid(row=3, column=1)
combobox_method['values'] = ['k-means', 'dbscan']
combobox_option['values'] = options
combobox_iter['values'] = iterations
button_run = tk.Button(ws, text='Calculate', command=run_search)
button_run.grid(row=4, column=1)

ws.mainloop()
