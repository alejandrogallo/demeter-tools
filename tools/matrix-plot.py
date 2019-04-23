#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import csv
import math
import numpy as np
import os


with open('data.csv') as fd:
    data = list(csv.reader(fd, delimiter='\t'))

title = os.path.basename(os.path.abspath(os.path.dirname(__file__))).replace('_', ' ')
ndim = math.ceil(math.sqrt(len(data)))
print(ndim)
data.extend([['', 0] for i in range(ndim**2 - len(data))])
print(data)

xdata = [[int(data[i + j * ndim][1]) for i in range(ndim)] for j in range(ndim)]
labels = [[data[i + j * ndim][0] for i in range(ndim)] for j in range(ndim)]

print(xdata)

plt.imshow(xdata, cmap='OrRd')
for j, column in enumerate(labels):
    for i, l in enumerate(column):
        plt.text(
            i, j, l,
            horizontalalignment='center',
            verticalalignment='center',
            color='black'
        )
plt.axis('off')
plt.title(title, fontdict={'fontsize': 20})
plt.colorbar(extend='both')
#plt.clim(0, 100)
plt.savefig('plot.pdf')
#plt.show()
