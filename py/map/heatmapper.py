import numpy as np
from py import social_distancing_config as config
import cv2

zones_x = int(config.OUTPUT_X / config.BLOCKSIZE_X)
zones_y = int(config.OUTPUT_Y / config.BLOCKSIZE_Y)
zones = np.zeros(shape=(zones_x, zones_y))
average = np.zeros(shape=(zones_x, zones_y))


def getGradient(percent):
    red = int(percent * 255)
    green = int(255 - (percent * 255))

    return 0, green, red


def getMap(centroids, frame, iteration):
    heatmap = np.copy(frame)

    trig = np.zeros(shape=(zones_x, zones_y)).copy()

    for x in range(zones_x):
        for y in range(zones_y):
            x1 = x * config.BLOCKSIZE_X
            y1 = y * config.BLOCKSIZE_Y
            x2 = (x + 1) * config.BLOCKSIZE_X
            y2 = (y + 1) * config.BLOCKSIZE_X

            cv2.rectangle(heatmap, (x1, y1), (x2, y2), (255, 255, 255), 2)

            for centroid in centroids:
                cx = centroid[0]
                cy = centroid[1]

                cv2.circle(heatmap, (cx, cy), 10, (255, 255, 255), 4)

                if trig[x][y] != 1:
                    if x1 <= cx < x2:
                        if y1 <= cy < y2:
                            zones[x][y] += (iteration / 4)
                            trig[x][y] = 1

            average[x][y] = round(zones[x][y] / iteration, 8)
            cv2.rectangle(heatmap, (x1, y1), (x2, y2), getGradient(average[x][y]), -1)

    return heatmap
