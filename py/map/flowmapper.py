from py import social_distancing_config as config
from scipy.spatial import distance as dist

first = True

# create list for recording past centroids
lastCentroids = []

# create list of lines for mapping flow
lines = []


def getMap(centroids):
    # global variables
    global pastCentroids, first, lines

    # skip flow mapping if first iteration
    if first:
        # record current centroids for future use
        pastCentroids = centroids
        first = False
    else:
        # get map of distances between current centroids and past centroids
        distances = dist.cdist(centroids, pastCentroids, 'euclidean')

        # distances returns the distance between every current centroid to its possible past self

        # iterate over every current centroid
        for i in range(len(centroids)):

            # assume that the closest past centroid is the same as the current centroid
            # get index of closes past centroid
            j = distances[i].argmin()

            # get coords of current centroid
            cx1 = centroids[i][0]
            cy1 = centroids[i][1]

            # get coords of past centroid
            cx2 = pastCentroids[j][0]
            cy2 = pastCentroids[j][1]

            # if closest distance is below a certain preset
            if distances[i][j] < config.FLOWMAP_DISTANCE:
                # add points to draw line into array
                lines.append(((cx1, cy1), (cx2, cy2)))

        # make current centroid the past centroid
        # so that next time this runs
        # current centroid becomes past centroid
        # and new data will become new centroid
        pastCentroids = centroids

    # if the number of lines is over a certain preset
    if len(lines) > config.FLOWMAP_SIZE:
        # slice first elements of list to clear space for new lines
        lines = lines[config.FLOWMAP_BATCH:]

    # return current lines
    return lines
