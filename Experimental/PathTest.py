import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import path
import matplotlib.patches as patches

Types = {'item3': 3}

# test=path.Path( ([41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]))
# path.contains_point((0,10), radius=0.0)

fig = plt.figure()
ax = fig.add_subplot(111)



ItemNames = ['Foidolite',
             'Peridotgabbro',
             'Foid Gabbro',
             'Foid Monzodiorite',
             'Foid Monzosyenite',
             'Foid Syenite',
             'Gabbro Bs',
             'Gabbro Ba',
             'Monzogabbro',
             'Monzodiorite',
             'Monzonite',
             'Syenite',
             'Quartz Monzonite',
             'Gabbroic Diorite',
             'Diorite',
             'Granodiorite',
             'Granite',
             'Quartzolite',
             ]

LocationAreas = [[[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]],
                 [[41, 0], [41, 3], [45, 3], [45, 0]],
                 [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]],
                 [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]],
                 [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]],
                 [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]],
                 [[45, 0], [45, 2], [52, 5], [52, 0]],
                 [[45, 2], [45, 5], [52, 5]],
                 [[45, 5], [49.4, 7.3], [52, 5]],
                 [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]],
                 [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]],
                 [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]],
                 [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]],
                 [[52, 0], [52, 5], [57, 5.9], [57, 0]],
                 [[57, 0], [57, 5.9], [63, 7], [63, 0]],
                 [[63, 0], [63, 7], [69, 8], [77.3, 0]],
                 [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]],
                 [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]],
                 ]

AreasHeadClosed = []
TasDic={}

for i in range(len(LocationAreas)):
    tmpi = LocationAreas[i]+[LocationAreas[i][0]]
    path = Path(tmpi)
    AreasHeadClosed.append(path)
    patch = patches.PathPatch(path, facecolor='orange', lw=0.3, alpha= 0.3)

    TasDic[ItemNames[i]]=path

    #ax.add_patch(patch)
    #ax.set_xlim(30,100)
    #ax.set_ylim(-1,20)

#print(TasDic)
#plt.show()