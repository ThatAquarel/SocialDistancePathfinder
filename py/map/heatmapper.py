import numpy as np
from py import social_distancing_config as config
import cv2

# create empty ndarrays with the shape defined previously
# they are global variables because heatmap is cumulative
# it accumulates data from every frame and then updates
# raw data list
zones = np.zeros(shape=(config.ZONES_X, config.ZONES_Y))

# percentages
average = np.zeros(shape=(config.ZONES_X, config.ZONES_Y))


def getGradient(percent):
    # get gradient between red and green from percentage
    red = int(percent * 255)
    green = int(255 - (percent * 255))

    # return values
    return 0, green, red


def getMap(centroids, frame, iteration):
    # use global variables
    global zones, average

    # copy ndarray object
    heatmap = np.copy(frame)

    # create empty ndarray to check if zone has been triggered
    # to prevent two people from being registered at once
    trig = np.zeros(shape=(config.ZONES_X, config.ZONES_Y)).copy()

    # iterate over every spot
    # horizontally
    for x in range(config.ZONES_X):
        # vertically
        for y in range(config.ZONES_Y):
            # get top left corner of zone
            x1 = x * config.BLOCKSIZE_X
            y1 = y * config.BLOCKSIZE_Y

            # get bottom right corner of zone
            x2 = (x + 1) * config.BLOCKSIZE_X
            y2 = (y + 1) * config.BLOCKSIZE_X

            # draw white rectangle with previously defined points
            cv2.rectangle(heatmap, (x1, y1), (x2, y2), (255, 255, 255), 2)
            # every square is now delimited

            # iterate over every centroid
            for centroid in centroids:
                # centroid is a tuple with following items
                # (x, y, violate)

                # get centroid coords
                cx = centroid[0]
                cy = centroid[1]

                # get last element of tuple to detect if centroid has violated social distancing or not
                if centroid[2]:
                    # not following social distance
                    # will thus affect heatmap more
                    power = config.VIOLATE
                    thickness = 4
                else:
                    # following social distance
                    # will thus affect heatmap less
                    power = config.NON_VIOLATE
                    thickness = 2

                # draw circle where centroid is
                cv2.circle(heatmap, (cx, cy), 10, (255, 255, 255), thickness)

                # if spot has not been triggered by another person yet:
                if trig[x][y] != 1:
                    # detect if centroid is within bounds of current square
                    if x1 <= cx < x2:
                        if y1 <= cy < y2:
                            # set raw value of current square
                            # takes into account how much "power" is applied
                            zones[x][y] += (iteration / power)
                            # sets current zone to be triggered
                            trig[x][y] = 1

            # get current zone's average with program's iteration
            average[x][y] = round(zones[x][y] / iteration, 8)

            # draw current zone's value by getting gradient between red and green
            cv2.rectangle(heatmap, (x1, y1), (x2, y2), getGradient(average[x][y]), -1)

    # returns heatmap and average
    return heatmap, average
