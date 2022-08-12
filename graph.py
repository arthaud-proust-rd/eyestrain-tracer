import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from stats import StatsName

csvFileColumns = [
    StatsName.BLINK_COUNT,
    StatsName.IS_BLINKING,
    StatsName.TIME_ELAPSED,
    StatsName.BLINK_PER_MINUTE,
]

last_log = sorted(os.listdir('logs/'))[-1]
print(last_log)


csvfile = open(f'logs/{last_log}', newline='')
dictreader = csv.DictReader(csvfile, csvFileColumns, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
rows = [row for row in dictreader]
# remove header
rows = rows[1:]
csvfile.close()

def create_plot(plot_to_create, title, dataX, dataY):
    x = [float(row[dataX]) for row in rows]
    y = [float(row[dataY]) for row in rows]
    plot_to_create.plot(x, y)
    plot_to_create.set_title(title)
    plot_to_create.set_xlabel(dataX)
    plot_to_create.set_ylabel(dataY)


fig, ((ax0, ax1) ) = plt.subplots(nrows=1, ncols=2)

create_plot(ax0, 'Blink rate evolution', StatsName.TIME_ELAPSED, StatsName.BLINK_PER_MINUTE)
create_plot(ax1, 'Blink count evolution', StatsName.TIME_ELAPSED, StatsName.BLINK_COUNT)

fig.tight_layout()
plt.show()