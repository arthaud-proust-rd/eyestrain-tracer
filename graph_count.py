import matplotlib.pyplot as plt
import numpy as np
from imports.data import S1, G_DATA
from imports.stats import StatsName, StatsColumns
from imports.logger import Logger


def make_graph(_plt, rows):
    title = 'Blink count evolution'
    dataX = StatsName.TIME_ELAPSED
    dataY = StatsName.BLINK_COUNT

    # blink rate evolution line
    x = [float(row[dataX]) for row in rows]
    y = [float(row[dataY]) for row in rows]
    _plt.plot(x, y, label=title)

    # Linear evolution
    _plt.plot([x[0], x[-1]], [x[0], x[-1]], label='Linear evolution')

    _plt.title(title)
    _plt.xlabel(dataX)
    _plt.ylabel(dataY)

    _plt.legend()
    _plt.show()

if __name__ == "__main__":
    logger = Logger.lastLog(StatsColumns)
    rows = logger.getRows()
    make_graph(plt, rows)