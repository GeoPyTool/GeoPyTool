import scipy
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import cm
import numpy as np
import pandas as pd


#import pylab

# Generate random features and distance matrix.

DataFileInput='Cluster.xlsx'

raw = pd.read_excel(DataFileInput)


x = scipy.rand(40)


x=[15.98,4.86,7.222211,2.7,2.4,0.06,4.63,0.65,58.02,1.16]

D = scipy.zeros([len(x),len(x)])
for i in range(len(x)):
    for j in range(len(x)):
        D[i,j] = abs(x[i] - x[j])

# Compute and plot first dendrogram.
fig = Figure((8.0, 8.0), dpi=128)





ax1 = fig.add_axes([0.09,0.1,0.2,0.6])



Y = sch.linkage(D, method='centroid')
Z1 = sch.dendrogram(Y, orientation='right')


ax1.set_xticks([])
ax1.set_yticks([])

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Y = sch.linkage(D, method='single')
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])

# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
D = D[idx1,:]
D = D[:,idx2]
im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap='viridis')

axmatrix.set_xticks(range(40))
axmatrix.set_xticklabels(idx1, minor=False)
axmatrix.xaxis.set_label_position('bottom')
axmatrix.xaxis.tick_bottom()

plt.xticks(rotation=-90, fontsize=8)

axmatrix.set_yticks(range(40))
axmatrix.set_yticklabels(idx2, minor=False)
axmatrix.yaxis.set_label_position('right')
axmatrix.yaxis.tick_right()

axcolor = fig.add_axes([0.94,0.1,0.02,0.6])
# Plot colorbar.
axcolor = fig.add_axes([0.91,0.1,0.02,0.6])

#plt.colorbar(im, cax=axcolor)

plt.show()
#fig.savefig('dendrogram.png')