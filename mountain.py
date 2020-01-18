#!/usr/local/bin/python3
#
# Authors: Deepali Tolia, Suyash Poredi, Kaustubh Bhalerao
# dtolia, sporedi, kbhaler
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image

# Argmax Approach
# we returned y-coordinates which have max values in that row
def simple(edge_strgth):
    tr_es = edge_strgth.T
    coord_list = []
    for row in tr_es:
        for coord, val in enumerate(row):
            if val == max(row):
                coord_list.append(coord)
                break
    return coord_list

# Calculate emission probability
# P(Observed|Current state)
# Smoothing factor m=1, V= # of rows
#numerator + m / Denominator + mV
def emission_prob(edge_strgth):
    tr_es = edge_strgth.T
    emission_list = []
    for i in range(0, tr_es.shape[0]):
        if i != tr_es.shape[0]-1:
            count_intersect = len(intersect1d(tr_es[i], tr_es[i+1]))
        emission_list.append(count_intersect+1/2*tr_es.shape[0])
    #print(emission_list)
    return emission_list


# Viterbi Algorithm
# V = P(Q = q)prod(P(Q(t+1)|Q(t)))prod(P(O|Q)) i.e. initial_state*transition*emission
def vert_algo(edge_strgth):
    emission = emission_prob(edge_strgth)
# Transition State P(Q(t+1)|Q(t))
    transition = full((edge_strgth.shape[1]), 1/edge_strgth.shape[0], dtype=double)
    vij = dot(edge_strgth.T,dot(transition, emission))
    coord_list = []
    for row in vij:
        for coord, val in enumerate(row):
            if val == max(row):
                coord_list.append(coord)
                break
    return coord_list

# viterbi algorithm with human input
# we split the array column wise based on th human input
# first part has 0 to input_col-1
# second part has input_col to last column
# the column given by human is changed all the values except that row is changed to 0
# we apply the viterbi algorithm to both the parts and return y-coordinates
def human_ip_vert_algo(edge_strgth, ip_row, ip_col):
    indx_b = list(range(ip_col, edge_strgth.shape[1]))
    array1 = delete(edge_strgth,indx_b, axis=1)
    emission1 = emission_prob(array1)
    transition1 = full((array1.shape[1]), 1 / array1.shape[0], dtype=double)
    vij1 = dot(array1.T, dot(transition1, emission1))
    coord_list = []
    for row in vij1:
        for coord, val in enumerate(row):
            if val == max(row):
                coord_list.append(coord)
                break

    indx_f = list(range(0, ip_col))
    array2 = delete(edge_strgth,indx_f, axis=1)
    for row_indx in range(array2.shape[0]):
        if row_indx != ip_row:
            array2[row_indx][0] = 0
    emission2 = emission_prob(array2)
    transition2 = full((array2.shape[1]), 1/array2.shape[0], dtype=double)
    vij2 = dot(array2.T,dot(transition2, emission2))
    for row in vij2:
        for coord, val in enumerate(row):
            if val == max(row):
                coord_list.append(coord)
                break
    return coord_list


# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
lv_edge_strgth = edge_strength(input_image)

imageio.imwrite('edges.jpg', uint8(255 * lv_edge_strgth / (amax(lv_edge_strgth))))

# You'll need to add code here to figure out the results! For now,
ridge_simple = simple(lv_edge_strgth)
ridge_map = vert_algo(lv_edge_strgth)
ridge_human = human_ip_vert_algo(lv_edge_strgth,int(gt_row), int(gt_col))
# just create a horizontal centered line.
# ridge = [ edge_strength.shape[0]/2 ] * edge_strength.shape[1]

# output answer
imageio.imwrite("output_simple.jpg", draw_edge(input_image, ridge_simple, (0, 0, 255), 5))
imageio.imwrite("output_map.jpg", draw_edge(input_image, ridge_map, (255, 0, 0), 5))
imageio.imwrite("output_human.jpg", draw_edge(input_image, ridge_human, (0, 255, 0), 5))
