#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat Dec 17 22:28:24 2016

@author: cycleuser
"""

lang = "python"


import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import math

def tasline(linewidth=1, linecolor='k'):
    # this function is used to draw the lines in the tas diagram

    plt.figure(figsize=(8, 6), dpi=80)
    plt.xlim(35, 79)
    plt.xticks(np.linspace(37, 77, 11, endpoint=True))
    plt.ylim(0, 16)
    plt.yticks(np.linspace(1, 15, 8, endpoint=True))
    plt.xlabel(r'$SiO_2 wt\%$', fontsize=16)
    plt.ylabel(r'$na_2O + K_2O wt\%$', fontsize=16)

    # ax is used to set the axies
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 35))

    # x and y are the values of the locations of points
    x = [41, 45, 48.4, 49.4, 52, 52.5, 53, 57, 57.6, 63, 69]
    y = [3, 5, 5.9, 7, 7.3, 8, 9.3, 9.4, 11.5, 11.7, 14]

    #    linelow =[(x[0],y[0]),(x[1],y[0]),(x[1],y[1]),(x[4],y[1]),(x[7],y[2]),(x[9],y[3]),(x[10],y[5])]
    xlow = [x[0], x[1], x[1], x[4], x[7], x[9], x[10]]
    ylow = [y[0], y[0], y[1], y[1], y[2], y[3], y[5]]

    #    linemid =[(x[3],y[4]),(x[6],y[6]),(x[8],y[9])]

    xmid = [x[1], x[3], x[6], x[8]]
    ymid = [y[1], y[4], y[6], y[9]]

    #    lineHigh=[(x[0],y[3]),(x[1],y[7]),(x[2],y[8]),(x[5],y[10])]

    xHigh = [x[0], x[0], x[1], x[2], x[5]]
    yHigh = [y[0], y[3], y[7], y[8], y[10]]

    #    yBase=[y[0],y[0],y[1],y[1],y[2],y[3],y[5]]

    for i in range(6):
        plt.plot([xlow[i], xlow[i]], [0.5, ylow[i]], label='DownBase', color=linecolor, linewidth=linewidth,
                 linestyle="-", )

    plt.plot([xlow[6], xlow[6]], [13, ylow[6]], label='UpBase', color=linecolor, linewidth=linewidth, linestyle="-", )
    plt.plot([76.5, xlow[6]], [0.5, ylow[6]], label='RightBase', color=linecolor, linewidth=linewidth, linestyle="-", )
    plt.plot(xlow, ylow, label='linelow', color=linecolor, linewidth=linewidth, linestyle="-", )
    plt.plot(xmid, ymid, label='linemid', color=linecolor, linewidth=linewidth, linestyle="-", )
    plt.plot([xHigh[0], xHigh[1], xHigh[2]], [yHigh[0], yHigh[1], yHigh[2]], label='linweHigh', color=linecolor,
             linewidth=linewidth, linestyle='--', )
    plt.plot([xHigh[2], xHigh[3], xHigh[4]], [yHigh[2], yHigh[3], yHigh[4]], label='linweHigh', color=linecolor,
             linewidth=linewidth, linestyle="-", )

    for i in range(3):
        plt.plot([xmid[i + 1], xlow[i + 3]], [ymid[i + 1], ylow[i + 3]], label='midtolow', color=linecolor,
                 linewidth=linewidth, linestyle="-", )

    for i in range(3):
        plt.plot([xmid[i + 1], xHigh[i + 2]], [ymid[i + 1], yHigh[i + 2]], label='midtoHigh', color=linecolor,
                 linewidth=linewidth, linestyle="-", )

    plt.plot([xHigh[4], 50], [yHigh[4], (2.5 * 2.3 / 5.1 + 14)], label='Higher', color=linecolor, linewidth=linewidth,
             linestyle="-", )
    plt.plot([xmid[3], 61], [ymid[3], (2.4 * 3.4 / 4.6 + 11.7)], label='Higher', color=linecolor, linewidth=linewidth,
             linestyle="-", )

    # labels are the names of different kinds of rocks
    labels = [u'F', u'Pc', u'U1', u'B', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O2', u'T', u'R']

    # Items are the positions of those labels
    Items = [(39, 10), (43, 1.5), (44, 6), (48.5, 2.5), (49, 6), (49, 9.5), (54, 3), (53, 7), (53, 12), (60, 4),
             (57, 8.5), (57, 14), (67, 5), (65, 10), (75, 9)]

    for i in range(len(Items)):
        plt.annotate(labels[i], xy=(Items[i]), xycoords='data', xytext=(-6, -3), textcoords='offset points',
                     fontsize=12, )

def plotpoint(x, y, size, color, alph, marker='d'):
    # this function is used to put data point on the picture
    plt.scatter(x, y, marker=marker, s=size, color=color, alpha=alph)

def drawline(X=[0, 1], Y=[0, 1], LineWidth=1, LineColor='k', LineStyle="-", LineAlpha=0.3,LineLabel= ''):
    plt.plot(X,Y,color=LineColor, linewidth=LineWidth, linestyle=LineStyle,alpha= LineAlpha,label = LineLabel)

def crosspoint(x0, y0, x1, y1, x2, y2, x3, y3):
    a = y1 - y0
    b = x1 * y0 - x0 * y1
    c = x1 - x0
    d = y3 - y2
    e = x3 * y2 - x2 * y3
    f = x3 - x2
    y = float(a * e - b * d) / (a * f - c * d)
    x = float(y * c - b) / a
    print(x, y)
    return ([x, y])


def tas(name="tas.xlsx", width=1, color='k'):
    # Read the Excel, then draw the tasline, then Plot points, job done~
    tasraw = pd.read_excel(name)
    tasline(width, color)
    Points = len(tasraw)
    for i in range(Points):
        plotpoint((tasraw.at[i, 'SiO2']), (tasraw.at[i, 'Na2O'] + tasraw.at[i, 'K2O']), tasraw.at[i, 'Size'],
                   tasraw.at[i, 'Color'], tasraw.at[i, 'Alpha'], tasraw.at[i, 'Marker'])
    plt.savefig("tas-Plot.png", dpi=600)
    plt.savefig("tas-Plot.svg", dpi=600)
    plt.show()


def qflline(LineWidth=1, LineColor='k'):
    plt.figure(figsize=(8, 4 * math.sqrt(3)), dpi=80)
    plt.xlim(-10, 110)
    plt.ylim(-10, 100)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')

    XBorder = [0, 50, 100, 0]
    YBorder = [0, 50 * math.sqrt(3), 0, 0]

    drawline(XBorder, YBorder, LineWidth=1, LineColor='k')

    XSpecialLon = [[51.5, 15],
                   [27.5, 87.5]
                   ]
    YSpecialLon = [[48.5 * math.sqrt(3), 0],
                   [27.5 * math.sqrt(3), 12.5 * math.sqrt(3)]
                   ]
    for i in range(len(XSpecialLon)):
        drawline(XSpecialLon[i], YSpecialLon[i], LineWidth=1, LineColor='k', LineStyle="-", )

    LineMid = crosspoint(13 / 2, 13 / 2 * math.sqrt(3), 100 - 37 / 2, 37 / 2 * math.sqrt(3), 55 / 2,
                         55 / 2 * math.sqrt(3), 100 - 25 / 2, 25 / 2 * math.sqrt(3))
    LineLeft = crosspoint(15, 0, 51.5, 48.5 * math.sqrt(3), 13 / 2, 13 / 2 * math.sqrt(3), 100 - 37 / 2,
                          37 / 2 * math.sqrt(3))

    LineUp = crosspoint(41, 41 * math.sqrt(3), 65, 35 * math.sqrt(3), 15, 0, 51.5, 48.5 * math.sqrt(3))

    XMid = [[LineMid[0], LineLeft[0]],
            [LineMid[0], 100 - 37 / 2],
            [50, 87.5],
            [41, LineUp[0]]
            ]
    YMid = [[LineMid[1], LineLeft[1]],
            [LineMid[1], 37 / 2 * math.sqrt(3)],
            [0, 12.5 * math.sqrt(3)],
            [41 * math.sqrt(3), LineUp[1]]
            ]
    for i in range(len(XMid)):
        drawline(XMid[i], YMid[i], LineWidth=1, LineColor='k', LineStyle="--", )

    # Label are the names of different kinds of rocks
    Label = [u'Q',
             u'F',
             u'L']

    # LabelPosition are the positions of those Labels
    LabelPosition = [(48, 50 * math.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i], xy=(LabelPosition[i]), xycoords='data', xytext=(0, 0), textcoords='offset points',
                     fontsize=16, )

def qfl(name="qfl.xlsx",width=1,color='k'):
    qflraw = pd.read_excel(name)
    qflline(width, color)
    Points = len(qflraw)
    for i in range(Points):
        q = qflraw.at[i, 'Q']
        f = qflraw.at[i, 'F']
        l = qflraw.at[i, 'L']

        Q = 100 * q / (q + f + l)
        F = 100 * f / (q + f + l)
        L = 100 * l / (q + f + l)

        x = Q / 2 + (100 - Q) * L / (L + F)
        y = Q / 2 * math.sqrt(3)

        plotpoint(x, y, qflraw.at[i, 'Size'], qflraw.at[i, 'Color'], qflraw.at[i, 'Alpha'], qflraw.at[i, 'Marker'])
    plt.savefig("QFL-Plot.png", dpi=600)
    plt.savefig("QFL-Plot.svg", dpi=600)
    plt.show()

def qmfltline(LineWidth=1, LineColor='k'):
    plt.figure(figsize=(8, 4 * math.sqrt(3)), dpi=80)
    plt.xlim(-10, 110)
    plt.ylim(-10, 100)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')

    XBorder = [0, 50, 100, 0]
    YBorder = [0, 50 * math.sqrt(3), 0, 0]

    drawline(XBorder, YBorder, LineWidth=1, LineColor='k')

    LineUp = crosspoint(23, 0, 55.5, 44.5 * math.sqrt(3), 40, 40 * math.sqrt(3), 50 + 87 * 20 / 43 / 2,
                        (50 - 87 * 20 / 43 / 2) * math.sqrt(3))

    LineLow = crosspoint(23, 0, 55.5, 44.5 * math.sqrt(3), 87, 0, 40, 40 * math.sqrt(3))

    LineMid = crosspoint(9, 9 * math.sqrt(3), 84, 16 * math.sqrt(3), 57 / 2, 57 / 2 * math.sqrt(3), 100 - 13 / 2,
                         13 / 2 * math.sqrt(3))
    LineLeft = crosspoint(23, 0, 55.5, 44.5 * math.sqrt(3), 9, 9 * math.sqrt(3), 84, 16 * math.sqrt(3))

    XSpecialLon = [[55.5, 23],
                   [27.5, 93.5],
                   [LineLow[0], 87]
                   ]
    YSpecialLon = [[44.5 * math.sqrt(3), 0],
                   [27.5 * math.sqrt(3), 6.5 * math.sqrt(3)],
                   [LineLow[1], 0]
                   ]
    for i in range(len(XSpecialLon)):
        drawline(XSpecialLon[i], YSpecialLon[i], LineWidth=1, LineColor='k', LineStyle="-", )
    XMid = [[LineMid[0], LineLeft[0]],
            [LineMid[0], 84],
            [47, 91],
            [LineUp[0], 40]
            ]
    YMid = [[LineMid[1], LineLeft[1]],
            [LineMid[1], 16 * math.sqrt(3)],
            [0, 9 * math.sqrt(3)],
            [LineUp[1], 40 * math.sqrt(3)]
            ]
    for i in range(len(XMid)):
        drawline(XMid[i], YMid[i], LineWidth=1, LineColor='k', LineStyle="--", )

    # Label are the names of different kinds of rocks
    Label = [u'Qm',
             u'F',
             u'Lt']

    # LabelPosition are the positions of those Labels
    LabelPosition = [(48, 50 * math.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i], xy=(LabelPosition[i]), xycoords='data', xytext=(0, 0), textcoords='offset points',
                     fontsize=16, )

def qmflt(name="qfl.xlsx", Width=1, Color='k'):
    QmFLtRaw = pd.read_excel(name)
    qmfltline(Width, Color)
    Points = len(QmFLtRaw)
    for i in range(Points):
        q = QmFLtRaw.at[i, 'Qm']
        f = QmFLtRaw.at[i, 'F']
        l = QmFLtRaw.at[i, 'Lt']

        Q = 100 * q / (q + f + l)
        F = 100 * f / (q + f + l)
        L = 100 * l / (q + f + l)

        x = Q / 2 + (100 - Q) * L / (L + F)
        y = Q / 2 * math.sqrt(3)

        plotpoint(x, y, QmFLtRaw.at[i, 'Size'], QmFLtRaw.at[i, 'Color'], QmFLtRaw.at[i, 'Alpha'],
                   QmFLtRaw.at[i, 'Marker'])
    plt.savefig("QmFLt-Plot.png", dpi=600)
    plt.savefig("QmFLt-Plot.svg", dpi=600)
    plt.show()


def reeline(LineWidth=1, LineColor='k'):
    # This DrawTheLines function is used to draw the lines in the figure

    Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    plt.figure(figsize=(8, 6), dpi=80)
    plt.xlim(0, 16)

    plt.xticks(np.linspace(1, 15, 15, endpoint=True),
               Element)

    plt.ylim(-1, 6)

    plt.yticks(np.linspace(-1, 3, 5, endpoint=True),
               [u'', u'1', u'10', u'100', u'1000']
               )
    plt.xlabel(r'$REE-Standardlized-Pattern$', fontsize=16)

    # ax is used to set the axies
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', -1))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

def ree(name="ree.xlsx", Width=1, Color='b', Style="-"):
    reeraw = pd.read_excel(name)
    Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    reeline(LineWidth=1, LineColor='k')
    # REEBase= pd.read_excel("REE.xlsx")

    for l in range(len(reeraw)):
        if (reeraw.at[l, 'DataType'] == 'Standard' or reeraw.at[l, 'DataType'] == 'standard' or reeraw.at[
            l, 'DataType'] == 'STANDARD'):
            k = l

    for i in range(len(reeraw)):
        if (reeraw.at[i, 'DataType'] == 'User' or reeraw.at[i, 'DataType'] == 'user' or reeraw.at[
            i, 'DataType'] == 'USER'):
            LineX = []
            LineY = []
            for j in range(len(Element) - 1):
                LineX.append(j + 1)
                LineY.append(math.log((reeraw.at[i, Element[j]]) / reeraw.at[k, Element[j]]))

                plotpoint(j + 1, math.log((reeraw.at[i, Element[j]]) / reeraw.at[k, Element[j]]),
                          size=reeraw.at[i, 'Size'], color=reeraw.at[i, 'Color'], alph=reeraw.at[i, 'Alpha'],
                          marker=reeraw.at[i, 'Marker'])

            drawline(LineX, LineY, LineColor=reeraw.at[i, 'Color'], LineWidth=reeraw.at[i, 'Width'],
                     LineStyle=reeraw.at[i, 'Style'], LineAlpha=reeraw.at[i, 'Alpha'], LineLabel=reeraw.at[i, 'Label'])
    plt.legend(loc='upper right', frameon=False)
    plt.savefig("REE-Plot.png", dpi=600)
    plt.savefig("REE-Plot.svg", dpi=600)
    plt.show()


def qapfline(LineWidth=1, LineColor='k'):
    plt.figure(figsize=(8, 8 * math.sqrt(3)), dpi=80)
    plt.xlim(-10, 110)
    plt.ylim(-100, 100)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')

    XBorder = [0, 50, 100, 50, 0]
    YBorder = [0, 50 * math.sqrt(3), 0, -50 * math.sqrt(3), 0]

    drawline(XBorder, YBorder, LineWidth=1, LineColor='k')

    # x= 65-y*math.sqrt(3)*0.1

    XLat = [[45, 55],
            [30, 70],
            [10, 90],
            [2.5, 65 - 2.5 * math.sqrt(3) * math.sqrt(3) * 0.1],
            [0, 65],
            [5, 95],
            [30, 70],
            [45, 55]
            ]
    YLat = [[45 * math.sqrt(3), 45 * math.sqrt(3)],
            [30 * math.sqrt(3), 30 * math.sqrt(3)],
            [10 * math.sqrt(3), 10 * math.sqrt(3)],
            [2.5 * math.sqrt(3), 2.5 * math.sqrt(3)],
            [0, 0],
            [-5 * math.sqrt(3), -5 * math.sqrt(3)],
            [-30 * math.sqrt(3), -30 * math.sqrt(3)],
            [-45 * math.sqrt(3), -45 * math.sqrt(3)]
            ]

    for i in range(len(XLat)):
        drawline(XLat[i], YLat[i], LineWidth=1, LineColor='k')

    XLon = [[34, 10, 34],
            [38, 35, 36.5],
            [56, 65, 63.5],
            [66, 86],
            [50, 50]
            ]

    YLon = [[30 * math.sqrt(3), 0, -30 * math.sqrt(3)],
            [10 * math.sqrt(3), 0, -5 * math.sqrt(3)],
            [30 * math.sqrt(3), 0, -5 * math.sqrt(3)],
            [-30 * math.sqrt(3), -5 * math.sqrt(3)],
            [0, -45 * math.sqrt(3)]
            ]

    for i in range(len(XLon)):
        drawline(XLon[i], YLon[i], LineWidth=1, LineColor='k', LineStyle="-", )

    XSpecialLon = [[44, 38],
                   [66, 82]
                   ]
    YSpecialLon = [[30 * math.sqrt(3), 10 * math.sqrt(3)],
                   [30 * math.sqrt(3), 10 * math.sqrt(3)]
                   ]
    for i in range(len(XSpecialLon)):
        drawline(XSpecialLon[i], YSpecialLon[i], LineWidth=1, LineColor='k', LineStyle="--", )

    # Label are the names of different kinds of rocks
    Label = [u'Q',
             u'A',
             u'F',
             u'P']

    # LabelPosition are the positions of those Labels
    LabelPosition = [(48, 50 * math.sqrt(3) + 2),
                     (-6, -1),
                     (48.5, -5 - 50 * math.sqrt(3)),
                     (104, -1)]

    for i in range(len(LabelPosition)):
        plt.annotate(Label[i], xy=(LabelPosition[i]), xycoords='data', xytext=(0, 0), textcoords='offset points',
                     fontsize=16, )

    Scale = [u'90', u'90',
             u'60', u'60',
             u'20', u'0', u'35', u'65', u'90', u'20',
             u'5',
             u'10', u'50', u'90', u'10',
             u'60', u'60',
             u'90', u'90']
    '''
    ScalePosition=[(45,45*math.sqrt(3)),(55,45*math.sqrt(3)),
                   (30,30*math.sqrt(3)),(70,30*math.sqrt(3)),
                   (10,10*math.sqrt(3)),(18,10*math.sqrt(3)),(38,10*math.sqrt(3)),(62,10*math.sqrt(3)),(82,10*math.sqrt(3)),(90,10*math.sqrt(3)),
                   (65-2.5*math.sqrt(3)*math.sqrt(3)*0.1,2.5*math.sqrt(3)),
                   (14,-5*math.sqrt(3)),(50,-5*math.sqrt(3)),(86,-5*math.sqrt(3)),(95,-5*math.sqrt(3)),
                   (30,-30*math.sqrt(3)),(70,-30*math.sqrt(3)),
                   (45,-45*math.sqrt(3)),(55,-45*math.sqrt(3))]

    '''

    ScalePosition = [(40, 45 * math.sqrt(3)), (57, 45 * math.sqrt(3)),
                     (25, 30 * math.sqrt(3)), (72, 30 * math.sqrt(3)),
                     (5, 10 * math.sqrt(3) - 2), (21, 10 * math.sqrt(3) + 2), (41, 10 * math.sqrt(3) + 2),
                     (62, 10 * math.sqrt(3) + 2), (82, 10 * math.sqrt(3) + 2), (92, 10 * math.sqrt(3) - 2),
                     (65 - 2.5 * math.sqrt(3) * math.sqrt(3) * 0.1, 2.5 * math.sqrt(3)),
                     (14, -5 * math.sqrt(3) + 2), (50, -5 * math.sqrt(3) + 2), (86, -5 * math.sqrt(3) + 2),
                     (95, -5 * math.sqrt(3) - 2),
                     (25, -30 * math.sqrt(3)), (72, -30 * math.sqrt(3)),
                     (40, -45 * math.sqrt(3)), (57, -45 * math.sqrt(3))]

    for i in range(len(ScalePosition)):
        plt.annotate(Scale[i], xy=(ScalePosition[i]), xycoords='data', xytext=(0, 0), textcoords='offset points',
                     fontsize=12, )

    Name = [u'Alkali Feldspar Rhyolite', u'Rhyolite', u'Dacite'
        , u'Quartz Alkali Feldspar Trachyte', u'Quartz Trachyte', u'Quartz Latite'
        , u'Alkali Feldspar Trachyte', u'Trachyte', u'Latite'
        , u'Foid-Bearing Alkali Feldspar Trachyte', u'Foid-Bearing Trachyte', u'Foid-Bearing Latite', u'Basalt Andesite'
        , u'Phonolite', u'Tephritic Phonolite', u'Phonolitic Basanite(olivine>10%) OR Phonolitic Tephrite(olivine<10%)',
            u'Basanite(olivine>10%) OR Tephrite(olivine<10%)'
        , u'Phonolitic Foidite', u'Tephritic Foidite'
        , u'Foidite'
            ]

    NamePosition = [u'Alkali Feldspar Rhyolite', u'Rhyolite', u'Dacite'
        , u'Quartz Alkali Feldspar Trachyte', u'Quartz Trachyte', u'Quartz Latite'
        , u'Alkali Feldspar Trachyte', u'Trachyte', u'Latite'
        , u'Foid-Bearing Alkali Feldspar Trachyte', u'Foid-Bearing Trachyte', u'Foid-Bearing Latite', u'Basalt Andesite'
        , u'Phonolite', u'Tephritic Phonolite', u'Phonolitic Basanite(olivine>10%) OR Phonolitic Tephrite(olivine<10%)',
                    u'Basanite(olivine>10%) OR Tephrite(olivine<10%)'
        , u'Phonolitic Foidite', u'Tephritic Foidite'
        , u'Foidite'
                    ]


def qapf(name="qapf.xlsx", Width=1, Color='k'):
    qapfraw = pd.read_excel(name)

    qapfline(Width, Color)

    for i in range(len(qapfraw)):

        q = qapfraw.at[i, 'Q']
        f = qapfraw.at[i, 'F']
        a = qapfraw.at[i, 'A']
        p = qapfraw.at[i, 'P']

        Q = 100 * q / (q + a + p)
        F = 100 * f / (f + a + p)

        if (Q > 0):
            A = 100 * a / (q + a + p)
            P = 100 * p / (q + a + p)
            x = Q / 2 + (100 - Q) * P / (A + P)
            y = (Q) / 2 * math.sqrt(3)
        if (F > 0):
            A = 100 * a / (f + a + p)
            P = 100 * p / (f + a + p)
            x = F / 2 + (100 - F) * P / (A + P)
            y = -(F) / 2 * math.sqrt(3)
        plotpoint(x, y, qapfraw.at[i, 'Size'], qapfraw.at[i, 'Color'], qapfraw.at[i, 'Alpha'], qapfraw.at[i, 'Marker'])

    plt.savefig("QAPF-Plot.png", dpi=600)
    plt.savefig("QAPF-Plot.svg", dpi=600)
    plt.show()


def eqar(A):  ### A is an angle in degrees
    return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))


def getangular(A, B, C):
    a = np.radians(A)
    b = np.radians(B)
    c = np.radians(C)
    result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
    result = np.rad2deg(result)
    return result


def wulf(name="strike.xlsx", Width=1, Color='k'):
    wulfraw = pd.read_excel(name)

    Data = []

    plt.axes(polar=True)
    plt.polar([0], [90])
    plt.xlim((0, 360))
    plt.ylim((0, 90))

    list1 = [eqar(x) for x in range(0, 90, 15)]
    list2 = [str(x) for x in range(0, 90, 15)]
    plt.rgrids(list1, list2)

    for i in range(len(wulfraw)):
        Data.append([wulfraw.at[i, "Name"], wulfraw.at[i, "Strike"], wulfraw.at[i, "Dip"], wulfraw.at[i, "Color"],
                     wulfraw.at[i, "Width"], wulfraw.at[i, "Alpha"]])
        S = wulfraw.at[i, "Strike"]
        D = wulfraw.at[i, "Dip"]
        Width = wulfraw.at[i, "Width"]
        Color = wulfraw.at[i, "Color"]
        Alpha = wulfraw.at[i, "Alpha"]
        r = np.arange(S - 90, S + 90, 1)
        BearR = [np.radians(-A + 90) for A in r]
        Line = (eqar(getangular(D, S, r)))

        plt.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha)

    plt.thetagrids(range(360 + 90, 0 + 90, -20), [str(x) for x in range(0, 360, 20)])
    plt.savefig("Wulff.png", dpi=600)
    plt.savefig("Wulff.svg", dpi=600)
    plt.show()


if __name__ == '__main__':
    # you need to put you data in a xlsx file in the same form as the example file
    tas("tas.xlsx")
    qfl("qfl.xlsx")
    qmflt("qfl.xlsx")
    ree("ree.xlsx")
    qapf("qapf.xlsx")
    wulf("strike.xlsx")