# base path to YOLO directory
MODEL_PATH = "yolo-coco"
# initialize minimum probability to filter weak detections along with
# the threshold when applying non-maxima suppression
MIN_CONF = 0.3
NMS_THRESH = 0.3
# boolean indicating if NVIDIA CUDA GPU should be used
USE_GPU = True
# define the minimum safe distance (in pixels) that two people can be
# from each other
MIN_DISTANCE = 50

FLOWMAP_DISTANCE = 25
FLOWMAP_SIZE = 1000
FLOWMAP_BATCH = 100

BLOCKSIZE_X = 30
BLOCKSIZE_Y = BLOCKSIZE_X

OUTPUT_X = 960
OUTPUT_Y = 540
