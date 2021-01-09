# base path to YOLO directory
MODEL_PATH = "yolo-coco"
# initialize minimum probability to filter weak detections along with
# the threshold when applying non-maxima suppression
MIN_CONF = 0.3
NMS_THRESH = 0.3
# boolean indicating if NVIDIA CUDA GPU should be used
USE_GPU = False
# define the minimum safe distance (in pixels) that two people can be
# from each other
MIN_DISTANCE = 50

# flowmap parameters
FLOWMAP_DISTANCE = 25
# flowmap maximum size, will get cleared if larger
FLOWMAP_SIZE = 1000
# how much to clear each time
FLOWMAP_BATCH = 100

# "power" of when a person follow social distancing
# larger number = affecting the heatmap less
NON_VIOLATE = 16
# "power" of when a person does not follow social distancing
# larger number = affecting the heatmap less
VIOLATE = 12

# size of every square, needs to be a multiple of OUTPUT_X and OUTPUT_Y
BLOCKSIZE_X = 30
BLOCKSIZE_Y = BLOCKSIZE_X

# output frame size
OUTPUT_X = 960
OUTPUT_Y = 540

# spots to check for pathfinding, relative to current spot
# (skew x, skew y)
# | -1 -1 | 0 -1 | 1 -1 |
# | -1  0 | 0  0 | 1  0 |
# | -1  1 | 0  1 | 1  1 |
# spots in a 3x3 area relative to current spot
PATHFIND_SPOTS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
