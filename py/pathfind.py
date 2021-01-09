import numpy as np
from py import social_distancing_config as config

# create global variables accessible whilst running recursion
# increment recursion iteration everytime function gets called
# to then limit the recursion if it goes over PATHFIND_RECURSION_LIMIT
recursion_iteration = 0
# create empty ndarray for floodfilling with recursion
path = np.zeros((config.ZONES_X, config.ZONES_Y))


# get spots that aren't out of bounds
def getNotNullSpots(x, y):
    # create list to contain possible spots
    spots = []

    # get relative spots from config and iterate over them
    for spot in config.PATHFIND_SPOTS:
        # getting actual x and y coords from spots
        skew_x = x + spot[0]
        skew_y = y + spot[1]

        # detect if coords are in bounds, ie not negative nor bigger than array
        if config.ZONES_X > skew_x > 0 and config.ZONES_Y > skew_y > 0:
            # add spots that are in bounds to list
            spots.append((skew_x, skew_y))

    # return possible spots
    return spots


def getSafestPerson(centroids, average):
    # 2d list for storing coords and "safety" factors
    # [[safety values][coords (x, y)]]
    safety_values = [[], []]

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

            # iterate over every centroid
            for centroid in centroids:
                # centroid is a tuple with following items
                # (x, y)

                # get centroid coords
                cx = centroid[0]
                cy = centroid[1]

                # detect if centroid is within bounds of current square
                if x1 <= cx < x2:
                    if y1 <= cy < y2:
                        # start with safety factor of 0%
                        safety = 0

                        # get possible spots
                        spots = getNotNullSpots(x, y)

                        # iterate over all possible spots
                        for spot in spots:
                            # add current spot's percentage to safety factor
                            # will do average later
                            safety += average[spot[0]][spot[1]]

                        # average safety factor and add them to list for comparing later
                        safety_values[0].append(round(safety / len(spots), 8))
                        # add coords to the same list, at the same 2nd dimensional index
                        # to request them later at the same time
                        safety_values[1].append((x, y))

    # get smallest value, ie safest spot
    # then get its index
    i = safety_values[0].index(min(safety_values[0]))
    # return the smallest value's coords
    return safety_values[1][i]


def getPath(average, safest_centroid):
    # use global variables
    global recursion_iteration, path

    # create empty array to store path
    path = np.zeros((config.ZONES_X, config.ZONES_Y))

    # reset recursion iteration to 0
    recursion_iteration = 0

    # unpack tuple to get coords, (x, y)
    x = safest_centroid[0]
    y = safest_centroid[1]
    # start recursion
    recursionFinder(average, x, y)

    # get percentage of "frame" that is part of the path
    # ie, detect if path generated is a fluke or not
    average = 0
    # iterate over path
    # horizontally
    for x in range(config.ZONES_X):
        # vertically
        for y in range(config.ZONES_Y):
            # if current spot is part of path
            # then add value to average
            if path[x][y] == 1:
                average += 1

    # divide average by total number of spots
    # to get percentage of "frame" filled
    percentage = average / (config.ZONES_X * config.ZONES_Y)
    # if percentage is over preset
    if percentage > config.PATH_PERCENTAGE:
        # return correct path
        return path
    else:
        # else: path is not correct
        # then return null
        return None


def recursionFinder(average, x, y):
    # use global variables
    global recursion_iteration, path

    # if recursion is not over limit
    if recursion_iteration < config.PATHFIND_RECURSION_LIMIT:
        # iterate over every relative spot to floodfill
        for spot in config.RECURSION_SPOTS:
            # get actual coords
            skew_x = x + spot[0]
            skew_y = y + spot[1]

            # if actual coords are within bounds
            # horizontally
            if 0 <= skew_x < config.ZONES_X:
                # vertically
                if 0 <= skew_y < config.ZONES_Y:
                    # if current spot is clear and that it has not been set
                    # by another instance of recursionFinder()
                    if average[skew_x][skew_y] == 0 and path[skew_x][skew_y] == 0:
                        # set current spot to be triggered
                        # so that it will not be set twice by another instance
                        path[skew_x][skew_y] = 1

                        # increment iteration before running recursion
                        recursion_iteration += 1
                        # recursion, to continue flooding all available areas
                        recursionFinder(average, skew_x, skew_y)
    else:
        # else: recursion is over limit, stop
        # return to stop
        return


def findRegressionLine(path):
    # return points to use with linear regression
    # init two lists where points are going to be stored
    x = []
    y = []

    # iterate over every spot
    # horizontally
    for x1 in range(config.ZONES_X):
        # vertically
        for y1 in range(config.ZONES_Y):
            # if current spot has been set as a viable path
            if path[x1][y1] == 1:
                # add current spot's coords to lists
                x.append(x1)
                y.append(y1)

    # return lists
    return x, y
