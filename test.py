import csv
import time
import numpy as np
import sys

arguments = sys.arg
print(arguments[0])
print(arguments[1])

file = open("test.csv", "w", newline = None)

csvwriter = csv.writer(file, delimiter=',')

meta = ['time', 'data']
csvwriter.writerow(meta)

for i in range(10):
    now = time.time()
    value = np.random.random()
    csvwriter.writerow([now, value])

file.close()
