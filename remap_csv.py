#run: python3 remap_csv.py

from datetime import datetime, timedelta, timezone
import csv

filename='t_hr.csv'
tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo

with open(filename, newline='\n') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')

	f = open('modified.csv', 'w')
	writer = csv.writer(f)
	writer.writerow(['date', 'value', 'sourceName'])

	for row in reader:
		date = datetime.fromtimestamp(int(row['timestamp'])).replace(tzinfo=tz)
		value = row['value']
		writer.writerow([date.strftime('%Y-%m-%d %H:%M:%S %z'), value, 'Alpha Watch'])

f.close()