import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from imports.data import S1, G_DATA
from imports.stats import StatsName, StatsColumns
from imports.logger import Logger
import graph_count
import graph_rate

logger = Logger.lastLog(StatsColumns)
rows = logger.getRows()

fig, ((ax0, ax1) ) = plt.subplots(nrows=1, ncols=2)

graph_rate.make_graph(ax0, rows)
graph_count.make_graph(ax1, rows)

fig.tight_layout()
plt.show()