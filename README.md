# heartrate-visualise
Set of python scripts that exports HeartRate from Apple Health &amp; draws cool plots, so data from various devices could be visually compared.

Instruction

*Pre-requirements*
Scripts were written on Python3 because MacOS already includes it in distribution. Install `matplotlib` by triggering `pip3 install matplotlib` from console.

1) Export your data from the Apple Health app.
  - On iOS 16, open the Health app
  - Hit your avatar on the top right corner & press `Export All Health Data`
  - Send data to your laptop
  - Unzip it
  - You should see a folder called `apple_health_export` -> open it.
  
2) Prepare data.
The content inside `apple_health_export` may vary, based on your Health features usage. You need to find `export.xml` file.
  - Open `export.xml`. It is a large file (mine ~1.3 GB), so it may take some time. It contains all the data from your Health app.
  - At the very beginning of the file, there is a data types map, that my script cannot parse. You need to remove it from the file & save it. You can find `<HealthData locale="~your actual locale~">` XML tag, and delete all lines before it. (In my case it is 156 lines).
  
3) Copy scripts.
  - Put `export_health_to_csv.py` & `draw_from_csv.py` scripts from that repo inside `apple_health_export` folder.
`export_health_to_csv.py` script is intended to export your data into CSV, so you can inspect or share this data without visualization.
`draw_from_csv.py` is made to draw plots from your CSV files.
  
4) Express the time intervals you want to be analyzed.
In my case - I needed to compare some limited timeslots (for example morning workout & sleep). So if you open `export_health_to_csv.py`, you will find `tasks` array, that contains `raw_start_time` & `raw_end_time` that describes the start and end time of your activity, as well as `title` defining it. You can have as many tasks as you need. Please edit `export_health_to_csv.py` file with your activities.

My example looks like this:
```tasks = [ 
	{'raw_start_time': "2022-12-02 08:23:00 +0100", 'raw_end_time': "2022-12-02 09:07:00 +0100", 'title': "Walking"}, 
	{'raw_start_time': "2022-12-02 01:52:00 +0100", 'raw_end_time': "2022-12-02 07:46:00 +0100", 'title': "Sleeping"},
]```

5) Export data.
  - Open Terminal
  - Navigate to `apple_health_export`
  - Run `python3 export_health_to_csv.py`
As the result you'll get a CSV file for each task, containing heart rate data.

6) Visualise data.
  - Run `python3 draw_from_csv.py ImageName CSV_filenames'`, where:
    * ImageName - a name from the image to be generated
    * CSV_filenames - whitespace separated CSV file names
My example `python3 draw_from_csv.py 'OnWear Pro' 'Workout#1.csv' 'Workout#2.csv' 'Sleep#1.csv'`

7) Enjoy nice plot visualization.
From my experience - drawing more than 4 graphs on a single image - doesn't look clear. My suggestion in that case - split those plots into multiple images.
For example:
`python3 draw_from_csv.py 'OnWear Pro' 'Workout#1.csv' 'Workout#2.csv' 'Sleep#1.csv'`
`python3 draw_from_csv.py 'OnWear Pro' 'Workout#3.csv' 'Workout#4.csv' 'Sleep#2.csv'`

The resulting images look like this:
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
