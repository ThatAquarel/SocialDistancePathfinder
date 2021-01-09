from py import social_distancing_config as config
from py.map import heatmapper
from py.map import flowmapper
from py import pathfind
from py import plot as plot_
from py.detection import detect_people
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import argparse
import imutils
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
                help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
                help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
                help="whether or not output frame should be displayed")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")
# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# check if we are going to use GPU
if config.USE_GPU:
    # set CUDA as the preferable backend and target
    print("[INFO] setting preferable backend and target to CUDA...")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)

# record program iteration to get average
iteration = 1

# frame skipping
frame_skip = False

# plot
plot = None
fig = None
init = True

# loop over the frames from the video stream
while True:
    # skip one out of two frames to increase speed
    if frame_skip:
        frame_skip = False
        continue
    else:
        frame_skip = True

        # read the next frame from the file
        (grabbed, frame) = vs.read()
        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break
        # resize the frame and then detect people (and only people) in it
        frame = imutils.resize(frame, width=700)
        results = detect_people(frame, net, ln,
                                personIdx=LABELS.index("person"))
        # initialize the set of indexes that violate the minimum social
        # distance
        violate = set()

        # ensure there are *at least* two people detections (required in
        # order to compute our pairwise distance maps)
        if len(results) >= 2:
            # extract all centroids from the results and compute the
            # Euclidean distances between all pairs of the centroids
            violate_centroids = np.array([r[2] for r in results])
            D = dist.cdist(violate_centroids, violate_centroids, metric="euclidean")
            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    # check to see if the distance between any two
                    # centroid pairs is less than the configured number
                    # of pixels
                    if D[i, j] < config.MIN_DISTANCE:
                        # update our violation set with the indexes of
                        # the centroid pairs
                        violate.add(i)
                        violate.add(j)

        # create groups of people
        violate_centroids = []
        non_violate_centroids = []

        # loop over the results
        for (i, (prob, bbox, centroid)) in enumerate(results):
            # extract the bounding box and centroid coordinates, then
            # initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid

            color = (0, 255, 0)
            # if the index pair exists within the violation set, then
            # update the color

            # rescale centroids to fit final output frame
            resize_x = int((config.OUTPUT_X / frame.shape[1]) * cX)
            resize_y = int((config.OUTPUT_Y / frame.shape[0]) * cY)

            # if person violates social distancing
            if i in violate:
                # change bounding box color
                color = (0, 0, 255)

                # add person to violate list
                violate_centroids.append((resize_x, resize_y))
            else:
                # else: add person to non-violate list
                non_violate_centroids.append((resize_x, resize_y))

            # draw (1) a bounding box around the person and (2) the
            # centroid coordinates of the person,
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 1)

        # get person centroids by adding violations and non-violations
        all_centroids = []
        for centroid in violate_centroids:
            all_centroids.append((centroid[0], centroid[1], True))
        for centroid in non_violate_centroids:
            all_centroids.append((centroid[0], centroid[1], False))

        # resize frame to output size
        frame = cv2.resize(frame, (config.OUTPUT_X, config.OUTPUT_Y))

        # generate heatmap using py/map/heatmapper.py
        heatmap, average = heatmapper.getMap(all_centroids, frame, iteration)

        # generate flowmap using py/map/flowmapper.py
        flowmap = flowmapper.getMap(all_centroids)

        # wait for some iterations to go by, making sure there is some data in average
        if iteration > 10:
            # get safest coords with /py/pathfind.py
            safest_centroid = pathfind.getSafestPerson(non_violate_centroids, average)

            # draw filled white rectangle of where the safest centroid is
            cv2.rectangle(frame, (safest_centroid[0] * config.BLOCKSIZE_X, safest_centroid[1] * config.BLOCKSIZE_Y),
                          (
                              (safest_centroid[0] + 1) * config.BLOCKSIZE_X,
                              (safest_centroid[1] + 1) * config.BLOCKSIZE_Y),
                          (252, 152, 3), -1)

            # pathfinding using py/pathfind.py
            path = pathfind.getPath(average, safest_centroid)

            if path is not None:
                empty = np.zeros(frame.shape, np.uint8)
                for x in range(config.ZONES_X):
                    for y in range(config.ZONES_Y):
                        if path[x][y] == 1:
                            cv2.rectangle(empty, (x * config.BLOCKSIZE_X, y * config.BLOCKSIZE_Y),
                                          ((x + 1) * config.BLOCKSIZE_X, (y + 1) * config.BLOCKSIZE_Y),
                                          (255, 255, 255), -1)

                frame = cv2.addWeighted(frame, 1.0, empty, 0.25, 1)

                # global init, plot, fig
                x, y = pathfind.findRegressionLine(path)
                if init:
                    plot, fig = plot_.init(x, y)
                    init = False
                else:
                    img, results = plot_.update(x, y, plot, fig)
                    if config.SHOW_REGRESSION:
                        cv2.imshow("plot", img)

                    frame = plot_.drawLine(frame, x, results)

        # iterate over every line generated by flowmap
        for line in flowmap:
            # draw every line onto frame
            cv2.line(heatmap, line[0], line[1], (255, 255, 255), 2)

        # stack frame and heatmap horizontally for displaying
        output_frame = np.hstack((frame, heatmap))

        # show the output frame
        cv2.imshow("Frame", output_frame)

        # quit program if q is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # print iteration
        print("[INFO] frame {i}, {v} social distance violations".format(i=iteration, v=len(violate)))

        # increment iteration everytime program runs
        iteration += 1

# cleanup
vs.release()
cv2.destroyAllWindows()
