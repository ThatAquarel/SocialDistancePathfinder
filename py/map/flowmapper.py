import numpy as np
from py import social_distancing_config as config
from scipy.spatial import distance as dist
import cv2

first = True

pastCentroids = []
lines = []


def getMap(centroids, frame, iteration):
    global pastCentroids, first, lines

    if first:
        pastCentroids = centroids
        first = False
    else:
        distances = dist.cdist(centroids, pastCentroids, 'euclidean')

        for i in range(len(centroids)):
            j = distances[i].argmin()
            cx1 = centroids[i][0]
            cy1 = centroids[i][1]
            cx2 = pastCentroids[j][0]
            cy2 = pastCentroids[j][1]

            if distances[i][j] < config.FLOWMAP_DISTANCE:
                lines.append(((cx1, cy1), (cx2, cy2)))

        pastCentroids = centroids

    print(len(lines))
    if len(lines) > config.FLOWMAP_SIZE:
        lines = lines[config.FLOWMAP_BATCH:]

    return lines
