#run: python3 export_health_to_csv.py

import xml.etree.ElementTree as ET
import datetime
import csv

filename='export.xml'

print('parsing ' + filename + '...')

root = ET.parse('./' + filename).getroot()

raw = root.findall('Record/[@type="HKQuantityTypeIdentifierHeartRate"]')
print('found ' + str(len(raw)) + ' records...')

tasks = [ 
	{'raw_start_time': "2022-12-02 08:23:00 +0100", 'raw_end_time': "2022-12-02 09:07:00 +0100", 'title': "Walking"}, 
	{'raw_start_time': "2022-12-02 01:52:00 +0100", 'raw_end_time': "2022-12-02 07:46:00 +0100", 'title': "Sleep"},
]


for idx, task in enumerate(tasks):
	sources = {}

	raw_start_time = task.get('raw_start_time')
	raw_end_time = task.get('raw_end_time')
	title = task.get('title')
	print('extracting ' + title + ' records between ' + raw_start_time + ' and ' + raw_end_time + '...')

	start_time = datetime.datetime.strptime(raw_start_time,'%Y-%m-%d %H:%M:%S %z')
	end_time = datetime.datetime.strptime(raw_end_time,'%Y-%m-%d %H:%M:%S %z')

	for record in raw:
		value = float(record.get('value'))
		date = datetime.datetime.strptime(record.get('startDate'),'%Y-%m-%d %H:%M:%S %z')
		sourceName = record.get('sourceName')

		if (date >= start_time) and (date <= end_time):
			if not sourceName in sources:
				sources[sourceName] = []

			sources[sourceName].append({'value': value, 'date': date, 'sourceName': sourceName})

	f = open(title + '.csv', 'w')
	writer = csv.writer(f)
	writer.writerow(['date', 'value', 'sourceName'])

	for key in sources:
		sources[key].sort(key=lambda x: x.get('date'), reverse=False)
		print('writing ' + str(len(sources[key])) + ' records from ' + key + '...')

		for value in sources[key]:
			writer.writerow([value.get('date').strftime('%Y-%m-%d %H:%M:%S %z'), str(value.get('value')), str(value.get('sourceName'))])
		
	f.close()