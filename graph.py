import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from stats import StatsName, StatsColumns

last_log = sorted(os.listdir('logs/'))[-1]
print(last_log)


csvfile = open(f'logs/{last_log}', newline='')
dictreader = csv.DictReader(csvfile, StatsColumns, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
rows = [row for row in dictreader]
# remove header
rows = rows[1:]
csvfile.close()



def create_blink_rate_plot(plot_to_create):
    title = 'Blink rate evolution'
    dataX = StatsName.TIME_ELAPSED
    dataY = StatsName.BLINK_PER_MINUTE

    # blink rate evolution line
    x = [float(row[dataX]) for row in rows]
    y = [float(row[dataY]) for row in rows]
    plot_to_create.plot(x, y, label=title)

    # average blink rate
    plot_to_create.plot([x[0], x[-1]], [4,4])

    plot_to_create.set_title(title)
    plot_to_create.set_xlabel(dataX)
    plot_to_create.set_ylabel(dataY)

def create_blink_count_plot(plot_to_create):
    title = 'Blink count evolution'
    dataX = StatsName.TIME_ELAPSED
    dataY = StatsName.BLINK_COUNT

    # add blink rate evolution
    x = [float(row[dataX]) for row in rows]
    y = [float(row[dataY]) for row in rows]
    plot_to_create.plot(x, y, label=title)

    plot_to_create.set_title(title)
    plot_to_create.set_xlabel(dataX)
    plot_to_create.set_ylabel(dataY)


fig, ((ax0, ax1) ) = plt.subplots(nrows=1, ncols=2)

create_blink_rate_plot(ax0)
create_blink_count_plot(ax1)

fig.tight_layout()
plt.show()