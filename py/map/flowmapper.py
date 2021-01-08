import numpy as np
from py import social_distancing_config as config
import cv2


def getMap(centroids, frame, iteration):
    return frame