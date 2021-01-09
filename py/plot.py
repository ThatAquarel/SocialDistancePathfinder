from py import social_distancing_config as config
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2


def init(x, y):
    matplotlib.use('TkAgg')
    fig = plt.figure()
    plt.xlim(config.ZONES_X)
    plt.ylim(config.ZONES_Y)
    plot, = plt.plot(x, y, 'o')

    # add linear regression line to scatterplot
    plot, plt.plot(x, getResult(x, y))

    return plot, fig


def update(x, y, plot, fig):
    fig.clf()

    plt.xlim(config.ZONES_X)
    plt.ylim(config.ZONES_Y)

    results = getResult(x, y)

    plt.plot(x, results)
    plt.plot(x, y, 'o')

    fig.canvas.draw()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
                        sep='')
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # display image with opencv or any operation you like

    return img, results


def getResult(x, y):
    # obtain m (slope) and b(intercept) of linear regression line
    model = np.polyfit(x, y, 1)

    model = np.asarray(model)

    m = model[0]
    b = model[1]

    result = []
    for x_ in x:
        result.append(m * x_ + b)

    return result


def drawLine(frame, x, result):
    for i in range(len(x)):
        j = i + 1
        if j < len(x):
            x1 = int(x[i] * config.BLOCKSIZE_X)
            y1 = int(result[i] * config.BLOCKSIZE_Y)
            x2 = int(x[j] * config.BLOCKSIZE_X)
            y2 = int(result[j] * config.BLOCKSIZE_Y)

            cv2.line(frame, (x1, y1), (x2, y2), (3, 227, 252), 4)
    return frame
