#install: pip3 install matplotlib
#run: python3 parse.py

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta, timezone
import math
from itertools import cycle
import csv
import sys

name = sys.argv[1]
paths= sys.argv[2:] #['Workout#1.csv', 'Workout#2.csv', 'Sleep#1.csv']

tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo

fig, axs = plt.subplots(len(paths), sharex=False, sharey=False, constrained_layout=True)
fig.suptitle(name)

min_datetime = datetime.min.replace(tzinfo=tz)

def round_dt_ceil(dt, delta):
    return min_datetime + math.ceil((dt - min_datetime) / delta) * delta

def round_dt_floor(dt, delta):
    return min_datetime + math.floor((dt - min_datetime) / delta) * delta

delta = timedelta(minutes=15)

for idx, path in enumerate(paths):

	with open(path, newline='\n') as csvfile:
		sources = {}
		cycol = cycle('bgrcmk')
		print('reading ' + path)

		reader = csv.DictReader(csvfile, delimiter=',')

		start_time = datetime.max.replace(tzinfo=tz)
		end_time = min_datetime

		for row in reader:
			sourceName = row['sourceName']

			if not sourceName in sources:
				sources[sourceName] = {'values': [], 'dates': []}

			date = datetime.strptime(row['date'],'%Y-%m-%d %H:%M:%S %z')
			if date < start_time:
				start_time = date

			if date > end_time:
				end_time = date

			sources[sourceName]['values'].append(float(row['value']))
			sources[sourceName]['dates'].append(date)

		for key in sources:
			axs[idx].set_xlim(round_dt_floor(start_time, delta), round_dt_ceil(end_time, delta))
			dates = sources[key]['dates']
			values = sources[key]['values']

			print('drawing plot for ' + key + ' (' + str(len(dates)) + ' records) data...')

			axs[idx].plot(dates, values, color=next(cycol), label=key, linewidth=0.33, alpha=0.7)
			axs[idx].set_title(path.split(".csv")[0] + ' (' + start_time.strftime('%m/%d %H:%M') + ' - ' + end_time.strftime('%m-%d %H:%M') + ')') 
			axs[idx].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize = 'x-small')

		hours = mdates.HourLocator(tz=tz)
		minutes = mdates.MinuteLocator(interval=15, tz=tz)
		hours_fmt = mdates.DateFormatter('%H:%M', tz=tz)
		minutes_fmt = mdates.DateFormatter('%M', tz=tz)

		axs[idx].xaxis.set_major_locator(hours)
		axs[idx].xaxis.set_major_formatter(hours_fmt)
		axs[idx].xaxis.set_minor_locator(minutes)
		axs[idx].xaxis.set_minor_formatter(minutes_fmt)
		axs[idx].tick_params(axis='x', labelsize=3, labelcolor = 'gray', which='minor')
		axs[idx].tick_params(axis='x', labelsize=6, which='major')
		axs[idx].tick_params(axis='y', labelsize=6, which='major')

		axs[idx].grid(which='major', color = 'black', linestyle = '--', linewidth = 0.2, alpha=0.3)
		axs[idx].grid(which='minor', color = 'gray', linestyle = '--', linewidth = 0.2, alpha=0.2)

plt.savefig(name + '.png', dpi=500)
plt.close()