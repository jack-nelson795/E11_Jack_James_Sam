import csv
import time
import numpy as np
import sys

arguments = sys.argv

file = open("test.csv", "w", newline = None)

csvwriter = csv.writer(file, delimiter=',')

meta = ['time', 'data']
csvwriter.writerow(meta)

for i in range(int(arguments[1])):
    now = time.time()
    value = np.random.random()
    csvwriter.writerow([now, value])

file.close()
