import psutil
import datetime
import time
from pandas import DataFrame
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt


class dataColl:
    def __init__(self):
        self.cpu_cnt = psutil.cpu_count()
        self.cpu_string = [
            'cpu_{}'.format(str(n)) for n in range(1, self.cpu_cnt + 1)
        ]

        # Output data file
        self.columns = ['date', 'month', 'day', 'hour', 'min', 'disk'
                        ] + self.cpu_string

        # Initialize values
        self.init_date, self.init_month, self.init_day = datetime.datetime.now(
        ).strftime("%d:%m:%a").split(':')

    def createFile(self):
        try:
            if os.stat('data/data.csv').st_size == 0:
                self.data_file = open('data/data.csv', 'w+')
                self.data_file.write(','.join(self.columns) + '\n')
            else:
                self.data_file = open('data/data.csv', 'a+')
        except FileNotFoundError:
            self.data_file = open('data/data.csv', 'w+')
            self.data_file.write(','.join(self.columns) + '\n')

    # Data collection module
    def data_collect(self):
        self.createFile()
        self.temp_date, self.temp_month, self.temp_day, self.temp_hour, self.temp_min = datetime.datetime.now(
        ).strftime("%d:%m:%a:%H:%M").split(':')
        self.temp_cpu_perc = psutil.cpu_percent(percpu=True)
        self.temp_disk_usage = psutil.disk_usage('/').percent
        self.fin_list = [
            self.temp_date, self.temp_month, self.temp_day, self.temp_hour,
            self.temp_min, self.temp_disk_usage
        ] + self.temp_cpu_perc
        return [str(x) for x in self.fin_list]

    def mainRun(self):
        i = 1
        while True:
        # for i in range(2):
            # Fields collected
            data_list = self.data_collect()
            print('[INFO] Done for iteration {}'.format(i))
            self.data_file.write(','.join(data_list) + '\n')
            self.data_file.flush()
            time.sleep(1800)  # 3600 for an hour
            i+=1

class analyse:
    def __init__(self):
        self.data = pd.read_csv('data/data.csv')

    def fill_missing(self):
        print(self.data)


# instance = dataColl()
# instance.mainRun()
# instance.data_file.close()

instance = analyse()
instance.fill_missing()
