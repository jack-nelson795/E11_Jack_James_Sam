import csv
import time
import numpy as np
import sys

arguments = sys.argv
print(arguments[0])

file = open("test.csv", "w", newline = None)

csvwriter = csv.writer(file, delimiter=',')

meta = ['time', 'data']
csvwriter.writerow(meta)

for i in range(arguments[0]):
    now = time.time()
    value = np.random.random()
    csvwriter.writerow([now, value])

file.close()
