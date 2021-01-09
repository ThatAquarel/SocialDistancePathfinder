from py import social_distancing_config as config
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2


def init(x, y):
    # use matplotlib interactive mode
    matplotlib.use('TkAgg')

    # create a matplotlib figure
    fig = plt.figure()

    # set x and y limits of graph
    plt.xlim(config.ZONES_X)
    plt.ylim(config.ZONES_Y)

    # plot points to use for regression
    plot, = plt.plot(x, y, 'o')

    # add linear regression line to scatterplot
    plot, plt.plot(x, getResult(x, y))

    # return figure and plot objects
    return plot, fig


def update(x, y, plot, fig):
    # clear
    fig.clf()

    # set x and y limits of graph
    plt.xlim(config.ZONES_X)
    plt.ylim(config.ZONES_Y)

    # get results of regression
    results = getResult(x, y)

    # plot results of regression
    plt.plot(x, results)

    # plot points used for regression
    plt.plot(x, y, 'o')

    # update figure
    fig.canvas.draw()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
                        sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # return opencv image and regression results
    return img, results


def getResult(x, y):
    # get data of linear regression line
    model = np.polyfit(x, y, 1)

    # make sure returned array is of ndarray type
    model = np.asarray(model)

    # extract regression variables, slope and intercept from list
    # m, slope
    m = model[0]
    # b, intercept
    b = model[1]

    # create list result, where regression results are going to get saved
    result = []

    # iterate over every x position
    for x_ in x:
        # add y value of current x position with linear regression
        result.append(m * x_ + b)

    # return results
    return result


def drawLine(frame, x, result):
    # iterate over every point that forms the regression line
    for i in range(len(x)):
        # the next point's index is j
        j = i + 1
        # if j is not out of bounds
        if j < len(x):
            # get first point of line relative to frame
            x1 = int(x[i] * config.BLOCKSIZE_X)
            y1 = int(result[i] * config.BLOCKSIZE_Y)

            # get second point of line relative to frame
            x2 = int(x[j] * config.BLOCKSIZE_X)
            y2 = int(result[j] * config.BLOCKSIZE_Y)

            # draw line onto frame
            cv2.line(frame, (x1, y1), (x2, y2), (3, 227, 252), 4)

    # return frame
    return frame
