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
# fine >> 15
# medium >> 30
# coarse >> 60
BLOCKSIZE_X = 30
BLOCKSIZE_Y = BLOCKSIZE_X

# output frame size
OUTPUT_X = 960
OUTPUT_Y = 540

# get how many subdivisions, ie how many squares
# horizontal
ZONES_X = int(OUTPUT_X / BLOCKSIZE_X)
# vertical
ZONES_Y = int(OUTPUT_Y / BLOCKSIZE_Y)

# spots to check for pathfinding, relative to current spot
# top left corner is origin point (skew x, skew y)
# | -1 -1 | 0 -1 | 1 -1 |
# | -1  0 |center| 1  0 |
# | -1  1 | 0  1 | 1  1 |
# check for spots in a 3x3 area relative to current spot
PATHFIND_SPOTS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
# check for a smaller area to prevent reaching max recursion depth
# only check 4 cardinal points
# | ----- | 0 -1 | ---- |
# | -1  0 |center| 1  0 |
# | ----- | 0  1 | ---- |
RECURSION_SPOTS = [(0, -1), (-1, 0), (1, 0), (0, 1)]
# pathfinding algorithm recursion limit
# ie how many recursions will be run before it stops automatically
PATHFIND_RECURSION_LIMIT = 500
# minimum amount of area the path can fill
# in a percentage, meaning that if less than 5% of the area is filled
# current path will be scraped and generated next frame
PATH_PERCENTAGE = 0.05

SHOW_REGRESSION = True
