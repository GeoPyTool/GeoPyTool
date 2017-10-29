lang = "python"

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
import math
import sys
import csv


"""
a tool set for basic tasks, crosspoint calc, coord transfer and fill region with color
"""

def Cross(self,A=[(0, 0), (10, 10)], B=[(0, 10), (100, 0)]):

    """
    Return the crosspoint of two line A and B.
    :param A: first line
    :type A: a list consist of two tuples, beginning and end point of the line
    :param B: second line
    :type B: a list consist of two tuples, beginning and end point of the line
    :return: the crosspoint of A and B
    :rtype: a list consist of two numbers, the x-y of the crosspoint
    """

    x0, y0 = A[0]
    x1, y1 = A[1]
    x2, y2 = B[0]
    x3, y3 = B[1]

    b1 = (y1 - y0) / (x1 - x0)
    b2 = (y3 - y2) / (x3 - x2)
    c1 = y0 - b1 * x0
    c2 = y2 - b2 * x2

    x = (c2 - c1) / (b1 - b2)
    y = b1 * x + c1

    return ([x, y])

def TriToBin(self,x, y, z):

    """
    Turn an x-y-z triangular coord to an a-b coord.
    if z is negative, calc with its abs then return (a, -b).
    :param x,y,z: the three numbers of the triangular coord
    :type x,y,z: float or double are both OK, just numbers
    :return:  the corresponding a-b coord
    :rtype:   a tuple consist of a and b
    """

    if(z>=0):
        if (x + y + z == 0):
            return (0, 0)
        else:
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if (X + Y != 0):
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * (np.sqrt(3))
            return (a, b)
    else:
        z=abs(z)
        if (x + y + z == 0):
            return (0, 0)
        else:
            Sum = x + y + z
            X = 100.0 * x / Sum
            Y = 100.0 * y / Sum
            Z = 100.0 * z / Sum
            if (X + Y != 0):
                a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
            else:
                a = Z / 2.0
            b = Z / 2.0 * (np.sqrt(3))
            return (a, -b)

def BinToTri(self,a, b):


    """
    Turn an a-b coord to an x-y-z triangular coord .
    if z is negative, calc with its abs then return (a, -b).
    :param a,b: the numbers of the a-b coord
    :type a,b: float or double are both OK, just numbers
    :return:  the corresponding x-y-z triangular coord
    :rtype:   a tuple consist of x,y,z
    """

    if(b>=0):
        y = a - b / np.sqrt(3)
        z = b * 2 / np.sqrt(3)
        x = 100 - (a + b / np.sqrt(3))
        return (x, y, z)
    else:
        y = a + b / np.sqrt(3)
        z = b * 2 / np.sqrt(3)
        x = 100 - (a -b / np.sqrt(3))
        return (x, y, z)

def TriCross(self,A=[(100, 0, 0), (0, 50, 60)], B=[(50, 50, 0), (0, 0, 100)]):

    """
    Return the crosspoint of two line A and B in triangular coord.
    :param A: first line
    :type A: a list consist of two tuples, beginning and end point of the line
    :param B: second line
    :type B: a list consist of two tuples, beginning and end point of the line
    :return:  the crosspoint of A and B
    :rtype:   a list consist of three numbers, the x-y-z of the triangular coord
    """

    x0, y0 = self.TriToBin(A[0][0], A[0][1], A[0][2])
    x1, y1 = self.TriToBin(A[1][0], A[1][1], A[1][2])
    x2, y2 = self.TriToBin(B[0][0], B[0][1], B[0][2])
    x3, y3 = self.TriToBin(B[1][0], B[1][1], B[1][2])

    b1 = (y1 - y0) / (x1 - x0)
    b2 = (y3 - y2) / (x3 - x2)
    c1 = y0 - b1 * x0
    c2 = y2 - b2 * x2

    x = (c2 - c1) / (b1 - b2)
    y = b1 * x + c1

    result = self.BinToTri(x, y)
    return(result)

def TriFill(self,P=[(100, 0, 0), (85, 15, 0), (0, 3, 97)], Color='blue', Alpha=0.3):

    """
     Fill a region in triangular coord.
    :param P: the peak points of the region in triangular coord
    :type P: a list consist of at least three tuples, which are the points in triangular coord
    :param Color: the color used to fill the region
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency used to fill the region
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    """

    a = []
    b = []

    for i in P:
        a.append(self.TriToBin(i[0], i[1], i[2])[0])
        b.append(self.TriToBin(i[0], i[1], i[2])[1])
    plt.fill(a, b, Color=Color, Alpha=Alpha, )

def Fill(self,P=[(100, 0), (85, 15), (0, 3)], Color='blue', Alpha=0.3):

    """
    Fill a region in planimetric rectangular coord.
    :param P: the peak points of the region in planimetric rectangular coord
    :type P: a list consist of at least three tuples, which are the points in planimetric rectangular coord
    :param Color: the color used to fill the region
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency used to fill the region
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    """
    a = []
    b = []

    for i in P:
        a.append(i[0])
        b.append(i[1])

    plt.fill(a, b, Color=Color, Alpha=Alpha, )

def SetAxis(self,x=[0,10,5],y=[0,10,5]):

    if len(x) == len(y) == 3:
        plt.xticks(np.linspace(x[0], x[1], x[2]+1, endpoint=True))
        plt.yticks(np.linspace(y[0], y[1], y[2]+1, endpoint=True))
    elif len(x)==len(y)==2:
        plt.xticks(np.linspace(x[0], x[1],x[1]-x[0]+1, endpoint=True))
        plt.yticks(np.linspace(y[0], y[1],y[1]-y[0]+1,  endpoint=True))
    else:
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_color('none')
        plt.xticks([])
        plt.yticks([])

def SetLim(self,x=[0,10],y=[0,10]):
    if len(x) == len(y) == 2:
        plt.xlim(x[0], x[1])
        plt.ylim(y[0], y[1])

def SetLabel(self,Label=['x','y'],FontSize=12):
    if len(Label)==2:
        plt.xlabel(Label[0], fontsize=FontSize)
        plt.ylabel(Label[1], fontsize=FontSize)

def SetSize(self,Width=8,Height=6,Dpi=80):
    plt.figure(figsize=(Width, Height), dpi=Dpi)

def SavePic(self,name='Picture'):
    plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
    plt.savefig(name+".png", dpi=300, bbox_inches='tight')
    plt.savefig(name+".svg", dpi=300, bbox_inches='tight')

