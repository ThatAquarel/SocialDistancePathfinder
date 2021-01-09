import numpy as np
from py import social_distancing_config as config


def getNotNullSpots(x, y, zones_x, zones_y):
    spots = []

    for spot in config.PATHFIND_SPOTS:
        skew_x = x + spot[0]
        skew_y = y + spot[1]
        if zones_x > skew_x > 0 and zones_y > skew_y > 0:
            spots.append((skew_x, skew_y))

    return spots


def getSafestPerson(centroids, average, zones_x, zones_y):
    safety_values = [[], []]

    for x in range(zones_x):
        for y in range(zones_y):
            x1 = x * config.BLOCKSIZE_X
            y1 = y * config.BLOCKSIZE_Y
            x2 = (x + 1) * config.BLOCKSIZE_X
            y2 = (y + 1) * config.BLOCKSIZE_X

            for centroid in centroids:
                cx = centroid[0]
                cy = centroid[1]

                if x1 <= cx < x2:
                    if y1 <= cy < y2:
                        safety = 0
                        spots = getNotNullSpots(x, y, zones_x, zones_y)
                        for spot in spots:
                            safety += average[spot[0]][spot[1]]

                        safety_values[0].append(round(safety / len(spots), 8))
                        safety_values[1].append((x, y))

    i = safety_values[0].index(min(safety_values[0]))
    return safety_values[1][i]
