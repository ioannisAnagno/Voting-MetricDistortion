from instance_opt import instance_opt_voting
import numpy as np

#import matplotlib.pyplot as plt
#plt.style.use('ggplot')

import csv

year = 2016
races = []

with open('./f1/race_results_1950-2020.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            driver_id = int(row[0])
        except ValueError:
            continue
        race_year = int(row[1])
        if (race_year != year):
            continue
        races.append(row)

drivers_names = {}
i = 0

for row in races:
    driver_name = row[5]
    if (driver_name not in drivers_names):
        drivers_names[driver_name] = i
        i += 1


m = len(drivers_names)

i = 0

for row in races:
    try:
        position = int(row[2])
    except ValueError:
        continue
    if (position == 1):
        i += 1

n = i

orders = [[-1 for i in range(m)] for j in range(n)]

i = -1

for row in races:

    try:
        position = int(row[2])
    except ValueError:
        continue
    if (position == 1):
        i += 1
    driver_name = row[5]
    orders[i][position-1] = drivers_names[driver_name]

prefs = []

for order in orders:
    pref = []
    for i in range(m):
        if (order[i] == -1):
            continue
        for j in range(m):
            if (j in order[0:(i+1)]):
                continue
            pref.append((order[i], j))
    prefs.append(pref)

costs = instance_opt_voting(n, m, prefs)

print(costs)
