import numpy.random as rand
import csv
import sys

def random(lower, upper):
    return (upper - lower) * rand.random() + lower

n_data = int(sys.argv[1])
lower = int(sys.argv[2])
upper = int(sys.argv[3])

with open('datos.csv', 'w') as data:
    writer = csv.writer(data, delimiter=',')
    for i in range(n_data):
        writer.writerow([i+1,random(lower, upper)])
