import matplotlib.pyplot as plt
import numpy as np
from imports.data import S1, G_DATA
from imports.stats import StatsName, StatsColumns
from imports.logger import Logger


def make_graph(_plt, rows):
    title = 'Blink rate evolution'
    dataX = StatsName.TIME_ELAPSED
    dataY = StatsName.BLINK_PER_MINUTE

    # blink rate evolution line
    x = [float(row[dataX]) for row in rows]
    y = [float(row[dataY]) for row in rows]
    _plt.plot(x, y, label=title)

    # average blink rate
    _plt.plot([x[0], x[-1]], [S1.AVERAGE_BLINK]*2, label="Average rage")

    # frequent blinker rate
    _plt.plot([x[0], x[-1]], [G_DATA.FREQUENT_BLINKER]*2, label='"Frequent blinker" rate')

    _plt.title(title)
    _plt.xlabel(dataX)
    _plt.ylabel(dataY)

    _plt.legend()
    _plt.show()

if __name__ == "__main__":
    logger = Logger.lastLog(StatsColumns)
    rows = logger.getRows()
    make_graph(plt, rows)