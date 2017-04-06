# !/usr/bin/env python3#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2017-03-13
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd

# usage:
    1) opern a ipython console
    2) import geopython as gp
    3) TasSample= Tas("tas.xlsx")
    4) TasSample.read()

# Geology related classes available:
    1) Tas
    2) Ree
    3) Trace & Trace2 (with different sequence of trace elements)
    4) Qfl & Qmflt & Qapf
    5) Polar (projection of wulf net & schmidt net)

# know issues:
    1) Only work on Python 3.x

# Other
    Any issues or improvements please contact cycleuser@cycleuser.org
    or leave a message to my blog: http://blog.cycleuser.org
"""

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
from chempy import Substance

class Tool():
    """
    a tool set for basic tasks, crosspoint calc, coord transfer and fill region with color
    """

    def ToCsv(self,name='FileName.csv', DataToWrite=[
        ["First", "Second", "Third"], ]):
        # Write DataResult to CSV file
        with open(name, 'w', newline='') as fp:
            a = csv.writer(fp)
            a.writerows(DataToWrite)

    def Mass(self,name='O'):
        # Mole Mass Calculated by chempy
        return Substance.from_formula(name).mass

    def GenList(mylist):
        for x in mylist:
            globals()[x] = []

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

class Frame():

    """
    a Frame of TAS, REE, Trace Elements and other similar x-y plots
    :param Width,Height: the width and height of the generated figure
    :type Width,Height: two int numbers
    :param Dpi: dots per inch
    :type Dpi: an int number
    :type

    :param Left,Right: the left and right limit of X axis
    :typeLeft,Right: two int numbers

    :param Base,Top: the left and right limit of Y axis
    :typeBase,Top: two int numbers

    :param X0,X1,X_Gap: the left and right limit of X label, and the numbers of gap between them
    :typeX0,X1,X_Gap: three int numbers

    :param Y0,Y1,Y_Gap: the left and right limit of Y label, and the numbers of gap between them
    :typeY0,Y1,Y_Gap: three int numbers

    :param FontSize: size of font of labels
    :typeFontSize: an int number

    :param xLabel, yLabel: the labels put alongside with x and y axises
    :type xLabel, yLabel: two strings
    """

    Width = 16
    Height = 9
    Dpi = 80

    Left = 0
    Right = 80

    Base = 0
    Top = 60

    X0 = 0
    X1 = 80
    X_Gap = 8

    Y0 = 0
    Y1 = 60
    Y_Gap = 6

    FontSize = 16
    xLabel = r'X Label'
    yLabel = r'Y Label'

    def __init__(self, Width=16, Height=9, Dpi=80, Left=0, Right=80, X_Gap=9, Base=0, Top=60, Y_Gap=7, FontSize=16,
                 xLabel=r'X Label', yLabel=r'Y Label'):
        """
        Just set up all.
        """

        super().__init__()

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = Left
        self.X1 = Right
        self.X_Gap = X_Gap

        self.Y0 = Base
        self.Y1 = Top
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel
        self.yLabel = yLabel

    def show(self):

        """
        Use the setup to set up figure feature.
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)

        plt.xlim(self.Left, self.Right)
        plt.ylim(self.Base, self.Top)

        plt.xticks(np.linspace(self.X0, self.X1, self.X_Gap, endpoint=True))
        plt.yticks(np.linspace(self.Y0, self.Y1, self.Y_Gap, endpoint=True))

        plt.xlabel(self.xLabel, fontsize=self.FontSize)
        plt.ylabel(self.yLabel, fontsize=self.FontSize)

class Point():

    """
    a Point class
    :param X,Y: the values of its x-y coord
    :type X,Y: two float numbers
    :param Location: gather X and Y as a tuple for further use
    :type Location: just a tuple with two numbers
    :param Size: the size of the Point to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Point to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Point
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Point, telling what it is and distinguish it from other points
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    """

    X = 0
    Y = 0
    Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''

    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        """
        just set up the values
        """
        super().__init__()
        self.X = X
        self.Y = Y
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

    def show(self):
        """
        plot the Point to the canvas
        """

        plt.scatter(self.X, self.Y, marker=self.Marker, s=self.Size, color=self.Color, alpha=self.Alpha,
                    label=self.Label, edgecolors='black')
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

class Points():

    """
    a class for multiple Points
    :param X,Y: the values of its x-y coords
    :type X,Y: two lists consist of float numbers
    :param Size: the size of the Points to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Points to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Points
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Points
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Points, telling what they are and distinguish them from other points
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    """

    X = []
    Y = []
    # Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''
    FontSize = 8

    def __init__(self, points=[(0, 0), (0, 1)], Size=12, Color='red', Alpha=0.3, Marker='o', Label='', FontSize=8):
        """
        just set up the values
        """
        super().__init__()
        self.X = []
        self.Y = []
        for i in points:
            self.X.append(i[0])
            self.Y.append(i[1])
        # self.Location = (self.X, self.Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label
        self.FontSize = FontSize

    def show(self):
        """
        plot the Point to the canvas
        """
        plt.scatter(self.X, self.Y, marker=self.Marker, s=self.Size, color=self.Color, alpha=self.Alpha,
                        label=self.Label)

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        # plt.legend((m,),(self.Label,),scatterpoints=1,loc='upper left',ncol=3, fontsize=8)

class Tag():
    """
    a class for Tag put on canvas
    :param Label: label of the Tag, telling what it is and distinguish them from other tags
    :type Label: a strings , if leave as "" or '' such kind of blank string, the label will not show on canvas
    :param Location: the location of the Tag
    :type Location: a tuple consist of x-y values of its coords
    :param X_offset,Y_offset: the values of its x-y offsets on coords
    :type X_offset,Y_offset: two float numbers
    :param FontSize: the size of font of the Tag
    :type FontSize: a number , int or maybe float also OK , better around 8 to 12, not too large or too small
    """

    Label = u'Label'
    Location = (0, 0)
    X_offset = -6
    Y_offset = 3
    FontSize = 12

    def __init__(self, Label=u'Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=12):
        """
        set up the values
        """

        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

    def show(self):

        """
        show the Tag on canvas with its offsets and font size, color and alpha are fixed for now
        """
        plt.annotate(self.Label, xy=self.Location, xycoords='data', xytext=(self.X_offset, self.Y_offset),
                     textcoords='offset points',
                     fontsize=self.FontSize, color='grey', alpha=0.8)

class TriTag(Tag,Tool):
    """
    inherit Tag and Tool,a Tag for triangular coord
    """

    def __init__(self, Label=u'Label', Location=(0, 1, 2), X_offset=-6, Y_offset=3, FontSize=12):

        """
        set up the values, transfer x,y,z coords to x-y coords
        """

        self.Label = Label
        self.Location = self.TriToBin(Location[0], Location[1], Location[2])
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class Line():
    """
    a line class
    :param Begin: the Beginning point of the line
    :type Begin: a Point Instance
    :param End: the End point of the line
    :type End: a Point Instance
    :param Points: gathering all the Point Instances
    :type Points: a list
    :param X,Y: the gathered x and y values of the line to use in plotting
    :type X,Y: two lists containing float numbers
    :param Width: the width of the line
    :type Width: an int number , mayby float is OK
    :param Color: the color of the Line to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Style: the style used for the Line
    :type Style: a string; -, --,-., : maybe there would be some other types , from matplotlib
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Label: label of the Line, telling what it is and distinguish it from other lines
    :type Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas
    :param Sort: the sequence used for sorting the points consisting the line
    :type Sort: a string, x means sort the points with their x values, y means use y instead of x, other means use the sequence of points as these points are put to the line
    """

    Begin = Point(0, 0)
    End = Point(1, 1)
    Points = []
    X = [Begin.X, End.X]
    Y = [Begin.Y, End.Y]
    Width = 1
    Color = 'blue'
    Style = "-"
    Alpha = 0.3
    Label = ''
    Sort = ''

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style="-", Alpha=0.3, Label=''):
        """
        setup the datas
        """
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):
            self.X = [Points[0][0], Points[1][0]]
            self.Y = [Points[0][1], Points[1][1]]
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

        else:
            print("Cannot draw line with one point")

    def sequence(self):
        """
        sort the points in the line with given option
        """
        if (len(self.Points[0]) == 2):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            else:
                self.order(self.Points)

        if (len(self.Points[0]) == 3):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            elif (self.Sort == 'Z' or self.Sort == 'Z'):
                self.Points.sort(key=lambda x: x[2])
                self.order(self.Points)
            else:
                self.order(self.Points)

    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
        self.X = X_TMP
        self.Y = Y_TMP

    def show(self):
        """
        draw the line on canvas with its setup
        """
        self.sequence()
        line, = plt.plot(self.X, self.Y, color=self.Color, linewidth=self.Width, linestyle=self.Style, alpha=self.Alpha,
                         label=self.Label)

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

class TriPoint(Point,Tool):

    """
    inherit Point and Tool, a Point class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    :param sum: a value used in calc of coord transfer
    :type sum: just a number, both int or float are OK
    """
    x = 0
    y = 0
    z = 0
    sum=1

    def __init__(self, P=(10, 20, 70), Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        super().__init__()

        self.sum=P[0]+P[1]+abs(P[2])
        self.x = P[0]*100/self.sum
        self.y = P[1]*100/self.sum
        self.z = P[2]*100/self.sum

        self.Location = P
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

        self.X, self.Y = self.TriToBin(self.x,self.y,self.z)


    def show(self):
        plt.scatter(self.X, self.Y, marker=self.Marker, s=self.Size, color=self.Color, alpha=self.Alpha,
                    label=self.Label, edgecolors='black')
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

class TriLine(Line,Tool):

    """
    inherit Line and Tool, line class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    """
    x = []
    y = []
    z = []

    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', Style="-", Alpha=0.3, Label=''):
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):

            TriPoint(Points[0])

            self.x = [Points[0][0], Points[1][0]]
            self.y = [Points[0][1], Points[1][1]]
            self.z = [Points[0][2], Points[1][2]]
            self.tritrans()
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

            for i in Points:
                self.x.append(i[0])
                self.y.append(i[1])
                self.z.append(i[2])

        else:
            print("Cannot draw line with one point")



    def tritrans(self):
        self.X = []
        self.Y = []
        for i in range(len(self.x)):
            self.X.append((self.TriToBin(self.x[i],self.y[i],self.z[i]))[0])
            self.Y.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[1])


    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        Z_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
            Z_TMP.append(i[2])
        self.x = X_TMP
        self.y = Y_TMP
        self.z = Z_TMP

    def show(self):
        self.sequence()
        self.tritrans()
        line, = plt.plot(self.X, self.Y, color=self.Color, linewidth=self.Width, linestyle=self.Style, alpha=self.Alpha,
                         label=self.Label)
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

class Tri():
    """
    a class of triangular frame
    :param Label: the label at the tree corners of the triangular
    :type Label: a list consist of three strings
    :param LabelPosition: just the Position of these Labels
    :type LabelPosition: x-y style coords , three of them
    """
    Label = [u'Q', u'F', u'L']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    def __init__(self, Label=[u'Q', u'F', u'L']):
        """
        set up the values
        """
        super().__init__()
        self.Label = Label

    def show(self):
        """
        just show the triangular frame on the canvas
        """
        plt.figure(figsize=(8, 4 * np.sqrt(3)), dpi=80)
        plt.xlim(-10, 110)
        plt.ylim(-10, 100)
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_color('none')
        TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='').show()
        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

class DualTri():
    """
    a class of a double triangulars frame
    :param Label: the label at the tree corners of the triangular
    :type Label: a list consist of three strings
    :param LabelPosition: just the Position of these Labels
    :type LabelPosition: x-y style coords , three of them
    :param Labels: description of the different region
    :type Labels: a list containing multiple strings
    :param Locations: the locations of those each one in the Labels
    :type Locations: a list of triangular coord points
    :param Offset: the offset value used to adjust the appearance of each one in the Labels
    :type Offset: a list of x-y coord offset values
    :param name: the file name used to read and use
    :type name: a string
    """


    Label = [u'Q', u'A', u'P', u'F']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1),
                     (49, -50 * np.sqrt(3) - 4)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',
              u'Recycled \n Orogenic',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc']
    Locations = [(8.5, 1.5, 90),
                 (28.5, 1.5, 70),
                 (58.5, 1.5, 40),
                 (18, 22, 70),
                 (35, 30, 35),
                 (15, 60, 15),
                 (11, 80, 9)]
    Offset = [(-80, 2),
              (-80, 2),
              (-80, 2),
              (-20, -5),
              (-20, -8),
              (-60, -2),
              (-40, -5)]



    name = "qapf.xlsx"
    def __init__(self,name="qapf.xlsx", Label=[u'Q', u'A', u'P', u'F']):
        super().__init__()
        self.Label = Label
        self.name=name


    def show(self):
        plt.figure(figsize=(8, 8 * np.sqrt(3)), dpi=80)
        plt.xlim(-10, 110)
        plt.ylim(-105* np.sqrt(3)/2, 105* np.sqrt(3)/2)
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_color('none')
        TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0),(0, 0, -100),(100, 0, 0),(35, 65, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='').show()
        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

class Tas(Frame):

    """
    inherit Frame, read xlsx or csv file and use SiO2 , Na2O and K2O to plot tas diagram
    :param Lines: the lines consisting the Tas frame
    :type Lines: a list of lines
    :param Tags: tags used for the items of Tas diagram
    :type Tagas: a list of strings
    :param Labels: labels on the canvas
    :type Labels: a list of strings
    :param Locations: the locations of these labels
    :type Locations: a list of tuple containing two numbers as x-y coords
    :param description: the description of the tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """

    Lines = []
    Tags = []
    Labels = [u'F', u'Pc', u'U1', u'B', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T', u'R']
    Locations = [(39, 10), (43, 1.5), (44, 6), (48.5, 2.5), (49, 6), (49, 9.5), (54, 3), (53, 7), (53, 12), (60, 4),
                 (57, 8.5), (57, 14), (67, 5), (65, 10), (75, 9)]
    description = "TAS (total alkali–silica) diagram (after Le Bas et al., 1986, Fig. 2).\nF foidite, Ph phonolite, Pc pocro- basalt,\nU1 tephrite (ol < 10%) basanite(ol > 10%), U2 phonotephrite, U3 tephriphonolite,\nB basalt, S1 trachy- basalt, S2 basaltic trachy- andesite, S3 trachyandesite,\nO1 basaltic andesite, O2 dacite,  O3 andesite,\nT trachyte (q < 20%) trachydacite (q > 20%), R rhyolite"

    name = "tas.xlsx"

    def __init__(self, name="tas.xlsx", Width=8, Height=6, Dpi=80, Left=35, Right=79, X0=37, X1=77, X_Gap=11, Base=0, Top=16, Y0=1,
                 Y1=15, Y_Gap=15, FontSize=12,
                 xLabel=r'$SiO_2 wt\%$', yLabel=r'$na_2O + K_2O wt\%$'):
        """
        just set up the basic settings
        """
        super().__init__()
        self.raw = ''


        self.name = name
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i], Location=self.Locations[i]))

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel+"\n"+self.description
        self.yLabel = yLabel

        self.Lines = [
            Line([(41, 0.5), (41, 3), (45, 3)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
            Line([(45, 0.5), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (63, 14)], Sort='', Width=1,
                 Color='black', Style="-", Alpha=0.3),
            Line([(45, 5), (52, 5), (57, 5.9), (63, 7), (69, 8)], Sort='', Width=1, Color='black', Style="-",
                 Alpha=0.3),
            Line([(76.5, 0.5), (69, 8), (69, 13)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
            Line([(63, 0.5), (63, 7), (57.6, 11.7), (52.5, 14), (50, 2.5 * 2.3 / 5.1 + 14)], Sort='', Width=1,
                 Color='black', Style="-", Alpha=0.3),
            Line([(57, 0.5), (57, 5.9), (53, 9.3), (48.4, 11.5)], Sort='', Width=1, Color='black', Style="-",
                 Alpha=0.3),
            Line([(52, 0.5), (52, 5), (49.4, 7.3), (45, 9.4)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
            Line([(41, 3), (41, 7), (45, 9.4)], Sort='', Width=1, Color='black', Style="--", Alpha=0.3),
            Line([(45, 9.4), (48.4, 11.5), (52.5, 14)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
            Line([(41.75, 1), (52.5, 5)], Sort='x', Color='black', Style=':', Label='MacDonald & Katsura 1964'),
            Line([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),
                  (61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)], Sort='x',
                 Color='green', Style='-.', Label='Kuno 1966'),
            Line([(39.8, 0.35), (65.6, 9.7)], Sort='x', Color='red', Style='--', Label='MacDonald 1968'),
            Line([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),
                  (55.0, 6.4), (60.0, 8.0), (65.0, 8.8)], Sort='x', Color='blue', Style='-',
                 Label='Irvine & Baragar 1971')]

    def show(self):
        """
        show the tas frame and lines of tas on canvas
        """

        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)

        plt.xlim(self.Left, self.Right)
        plt.ylim(self.Base, self.Top)

        plt.xticks(np.linspace(self.X0, self.X1, self.X_Gap, endpoint=True))
        plt.yticks(np.linspace(self.Y0, self.Y1, self.Y_Gap, endpoint=True))

        plt.xlabel(self.xLabel, fontsize=self.FontSize)
        plt.ylabel(self.yLabel, fontsize=self.FontSize)
        for i in self.Lines:
            i.show()
        for i in self.Tags:
            i.show()

        x = np.arange(self.X0, self.X1, 1)
        y1 = np.power((x - 43) * 3.3, 0.5)
        y2 = np.power((x - 43) * 9, 0.5)
        y3 = np.power((x - 43) * 6, 0.5)

        line_up, = plt.plot(x, y1, color='black', linewidth=0.8, linestyle=':', alpha=0.8, label='sigma=3.3')
        line_down, = plt.plot(x, y2, color='black', linewidth=0.8, linestyle='-.', alpha=0.9, label='sigma=9')

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            Point(raw.at[i, 'SiO2'], (raw.at[i, 'Na2O'] + raw.at[i, 'K2O']), Size=raw.at[i, 'Size'],
                  Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel).show()
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        plt.savefig(self.name+"tas.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"tas.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Ree(Frame):

    """
    inherit Frame, read xlsx or csv file and use the Rare Earth Elements to plot the ree diagram
    :param Element: the elements used in this diagram
    :type Element: a list of strings
    :param Labels: a ref of Element
    :type Labels: a list of strings
    :param WholeData: gathering all data and find the min and max of the data file to set the limits of Y
    :type WholeData: a list of float numbers
    :param X0,X1: the left and right limits of X
    :type X0,X1: two int or float numbers
    :param X_Gap: the space between the left and right limits of X
    :type X_Gap: an int number
    :param name: the file name to use in this diagram
    :type name: a string
    """

    Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    Labels = Element
    WholeData = []
    X0 = 1
    X1 = 15
    X_Gap = 15
    name="ree.xlsx"

    def __init__(self, name="ree.xlsx",Width=8, Height=6, Dpi=80, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1, Top=6, Y0=-1,
                 Y1=3, Y_Gap=5, FontSize=16,
                 xLabel=r'$REE-Standardlized-Pattern$', yLabel=''):
        super().__init__()
        self.raw = ''

        self.name=name
        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = 1
        self.X1 = len(self.Element) + 1
        self.X_Gap = X1

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel
        self.yLabel = yLabel

    def show(self):
        """
        set the figure basic with the settings
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)

        plt.xlim(self.Left, self.Right)
        plt.ylim(self.Base, self.Top)

        plt.xticks(np.linspace(self.X0, self.X1, self.X1-self.X0+1, endpoint=True), self.Labels)
        plt.xlabel(self.xLabel, fontsize=self.FontSize)
        plt.ylabel(self.yLabel, fontsize=self.FontSize)

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []
        k = 0
        for l in range(len(raw)):
            if (raw.at[l, 'DataType'] == 'Standard' or raw.at[l, 'DataType'] == 'standard' or raw.at[
                l, 'DataType'] == 'STANDARD'):
                k = l




        for i in range(len(raw)):
            if (raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[
                i, 'DataType'] == 'USER'):

                TmpLabel = ''


                Lines = []
                for j in range(len(self.Element)):
                    tmp= raw.at[i, self.Element[j]]/ raw.at[k, self.Element[j]]
                    Lines.append((j + 1, math.log(tmp,10)))
                    self.WholeData.append(math.log(tmp,10))

                    if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        PointLabels.append(raw.at[i, 'Label'])
                        TmpLabel = raw.at[i, 'Label']

                    Point(j + 1, math.log(tmp,10),
                          Size=raw.at[i, 'Size'], Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'],
                          Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

                Line(Lines, Color=raw.at[i, 'Color'], Width=raw.at[i, 'Width'],
                     Style=raw.at[i, 'Style'], Alpha=raw.at[i, 'Alpha']).show()

        self.Base = min(self.WholeData)
        self.Top = max(self.WholeData)

        T=int(self.Top)
        B=int(self.Base)

        plt.ylim(B-1, T+1)

        txt = np.arange(-1, T+8, 1)
        temptxt=[]
        text = [u'', u'1', u'10', u'100', u'1000',u'10000',u'100000',u'1000000',u'10000000']

        for i in txt:
            temptxt.append(str(np.power(10.0, i)))

        gap = T+2

        plt.yticks(np.linspace(-1, T, gap, endpoint=True), text )

        plt.legend(loc=5, bbox_to_anchor=(1.2, 0.5))

        plt.savefig(self.name+".png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+".svg", dpi=300, bbox_inches='tight')
        plt.show()

class Trace(Ree):

    """
    inherit Frame, read xlsx or csv file and use the Trace Elements to plot the trace diagram
    :param Element: the elements used in this diagram
    :type Element: a list of strings
    :param Labels: a ref of Element
    :type Labels: a list of strings
    :param name: the file name to use in this diagram
    :type name: a string
    """

    Element = ['Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy', u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']
    Labels = Element
    name = "trace.xlsx"

    def __init__(self,name="trace.xlsx", Width=16, Height=9, Dpi=80, Left=0, Right=16, X0=1, X1=37, X_Gap=15, Base=-1, Top=6, Y0=-1,
                 Y1=3, Y_Gap=5, FontSize=16,
                 xLabel=r'$Trace-Elements-Standardlized-Pattern$', yLabel=''):
        super().__init__()
        self.raw = ''

        self.name=name
        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = 1
        self.X1 = len(self.Element)+1
        self.X_Gap = len(self.Element)

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel
        self.yLabel = yLabel

class Trace2(Trace):
    """
    inherit Frame, read xlsx or csv file and use the Trace Elements to plot the trace2 diagram
    :param Element: the elements used in this diagram
    :type Element: a list of strings
    :param Labels: a ref of Element
    :type Labels: a list of strings
    :param name: the file name to use in this diagram
    :type name: a string
    """
    Element = ['Rb',u'Ba',u'Th',u'U',u'Nb',u'Ta',u'K',u'La',u'Ce',u'Pr',u'Sr',u'P',u'Nd',u'Zr',u'Hf',u'Sm',u'Eu',u'Ti',u'Tb',u'Dy',u'Y',u'Ho',u'Er',u'Tm',u'Yb',u'Lu']
    Labels = Element
    name = "trace2.xlsx"

    def __init__(self,name="trace2.xlsx", Width=16, Height=9, Dpi=80, Left=0, Right=16, X0=1, X1=26, X_Gap=25, Base=-1, Top=6, Y0=-1,
                 Y1=3, Y_Gap=5, FontSize=16,
                 xLabel=r'$Trace-Elements-Standardlized-Pattern$', yLabel=''):
        super().__init__()

        self.raw = ''

        self.name=name
        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = 1
        self.X1 = len(self.Element)+1
        self.X_Gap = len(self.Element)

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel
        self.yLabel = yLabel

class Qfl(Tri,Tool):

    """
    inherit Tri and Tool, read xlsx or csv file and make QFL diagram
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []
    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',
              u'Recycled \n Orogenic',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc']
    Locations = [(8.5, 1.5, 90),
                 (28.5, 1.5, 70),
                 (58.5, 1.5, 40),
                 (18, 22, 70),
                 (35, 30, 35),
                 (15, 60, 15),
                 (11, 80, 9)]
    Offset = [(-80, 2),
              (-80, 2),
              (-80, 2),
              (-20, -5),
              (-20, -8),
              (-60, -2),
              (-40, -5)]

    name = "qfl.xlsx"

    def __init__(self, name="qfl.xlsx",Label=[u'Q', u'F', u'L']):
        super().__init__()

        self.raw = ''

        self.Label = Label
        self.name=name
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1], self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def draw(self):
        """
        use the values to set up the general frame and lines, fill particular zone with given colors
        """

        TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()
        T0 = (85, 15, 0)
        T1 = (0, 3, 97)
        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T4 = self.TriCross(A=[T0,T1] , B=[T2,T3])

        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T5 = (45, 0, 55)
        T6 = (0, 75, 25)


        T7 = self.TriCross(A=[T2,T3] , B=[T5,T6])


        TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='').show()

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)


        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        for i in self.Tags:
            i.show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            TriPoint((raw.at[i, 'F'], raw.at[i, 'L'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"qfl.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"qfl.svg", dpi=300, bbox_inches='tight')

class Qmflt(Qfl,Tool):

    """
    inherit Qfl and Tool, read xlsx or csv file and make Qmflt diagram
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []
    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',

              u'Mixed',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc',

              u'Quartzose \n Recycled',
              u'Transitional \n Recycled',
              u'Lithic \n Recycled']
    Locations = [(15, 5, 90),
                 (30, 8, 62),
                 (60, 10, 30),

                 (30, 25, 45),
                 (40, 20, 40),
                 (40, 40, 20),
                 (20, 70, 10),

                 (10, 3, 60),
                 (10, 50, 40),
                 (10, 80, 10)]

    Offset = [(-66, 2),
              (-108, 2),
              (-95, 2),

              (-10, +10),
              (-10, -25),
              (-40, -20),
              (-30, -35),

              (+68, -28),
              (+50, -2),
              (+52, -15)]
    name = "qmflt.xlsx"
    def __init__(self, name="qmflt.xlsx",Label=[u'Qm', u'F', u'Lt']):
        super().__init__()

        self.raw = ''


        self.name="qmflt.xlsx"
        self.Label = Label
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1], self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def draw(self):
        """
        use the values to set up the general frame and lines, fill particular zone with given colors
        """
        TriLine(Points=[(77, 23, 0), (0, 11, 89)], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()
        T0 = (77, 23, 0)
        T1 = (0, 11, 89)
        T2 = (43,0,57)
        T3 = (0, 87, 13)


        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (43,0,57)
        T3 = (0, 87, 13)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)


        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)


        T8 = self.TriCross(A=[T0, T1], B=[T5, T6])

        TriLine(Points=[T4, T2], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T7, T3], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T8, T7], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T7, (0, 68, 32)], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='').show()

        T9 = (13, 87,0)



        self.TriFill(P=[(100, 0, 0), T0, T1, (0, 0, 100)], Color='blue', Alpha=0.13)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T0 = (77, 23, 0)
        T1 = (0, 11, 89)


        T12 = self.TriCross(A=[T10, T11], B=[T0, T1])

        TriLine(Points=[T9, T12], Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        self.TriFill(P=[T12, T11,(0,100,0), T1], Color='red', Alpha=0.13)


        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T13 = (47,53,0)
        T14 = (0, 82, 18)

        T15 = self.TriCross(A=[T10, T11], B=[T13, T14])

        TriLine(Points=[T15, T13], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=[T15, T14], Sort='', Width=1, Color='black', Style=":", Alpha=0.7,
                Label='').show()



        T10 = (20, 0, 80)
        T16 = (0, 40, 60)

        T17 = self.TriCross(A=[T10, T16], B=[T0, T1])

        TriLine(Points=[T17, T10], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T18 = (0,42,59 )
        T19 = (84,0,16)

        T20 = self.TriCross(A=[T10, T11], B=[T18, T19])

        TriLine(Points=[T18, T20], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        T21 = (0, 71, 29)
        T22 = (58, 42, 0)

        T23 = self.TriCross(A=[T10, T11], B=[T21, T22])

        TriLine(Points=[T23, T21], Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()



        for i in self.Tags:
            i.show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            TriPoint((raw.at[i, 'F'], raw.at[i, 'Lt'], raw.at[i, 'Qm']), Size=raw.at[i, 'Size'],
                     Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                     Label=TmpLabel).show()

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"qmflt.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"qmflt.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Qapf(DualTri,Tool):


    """
    inherit DualTri and Tool, read xlsx or csv file and make basic Qapf diagram
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []

    Labels = ["quartzolite",

                "quartz-rich\ngranitoid",

                "granite",

                "alkali\nfeldspar\ngranite",
                "(syeno\ngranite)",
                "(monzo\ngranite)",
                "granodiorite",
                "tonalite",

                "quartz\nalkali\nfeldspar\nsyenite",
                "quartz\nsyenite",
                "quartz\nmonzonite",
                "quartz\nmonzodiorite\nquartz\nmonzogabbro",
                "quartz\ndiorite\nquartz gabbro\n quartz\nanorthosite",

                "alkali\nfeldspar\nsyenite",
                "syenite",
                "monzonite",
                "monzodiorite\nmonzogabbro",
                "diorite\ngabbro\nanorthosite",

                "foid-bearing\nalkali\nfeldspar\nsyenite",
                "foid-bearing\nsyenite",
                "foid-bearing\nmonzonite",
                "foid-bearing\nmonzodiorite\nfoid-bearing\nmonzogabbro",
                "foid-bearing\ndiorite\nfoid-bearing gabbro\nfoid-bearing\nanorthosite",

                "foid\nsyenite",
                "foid\nmonzosyenite",
                "foid\nmonzodiorite\nfoid\nmonzogabbro",
                "foid\ndiorite\nfoid\ngabbro",
                "foidolite"]

    Locations = [(5,5,95),

                (10,10,80),

                (35,15,50),

                (45,5,50),
                (45,25,30),
                (35,35,30),
                (25,45,30),
                (5,45,50),

                (85,5,10),
                (75,15,10),
                (45,45,10),
                (15,75,10),
                (5,85,10),

                (93,5,2),
                (83,15,2),
                (53,53,2),
                (15,83,2),
                (5,93,2),

                (95,3,-8),
                (75,23,-8),
                (49,49,-8),
                (23,75,-8),
                (3,95,-8),

                (63,7,-30),
                (50,20,-30),
                (20,50,-30),
                (7,63,-30),
                (10,10,-80)]

    Offset = [  (-30,0),

                (-30,0),

                (-20,0),

                (-70, 30),
                (-50, 30),
                (-30, 0),
                (0, 0),
                (30, 20),

                (-70, 15),
                (-10, 0),
                (-40, 0),
                (-30, -5),
                (30, 15),

                (-80, 5),
                (0, 0),
                (-40, 0),
                (-30, -5),
                (60, 5),

                (-80, -15),
                (-40, 0),
                (-40, 0),
                (-20, -15),
                (50, -30),

                (-80,0),
                (-40,0),
                (-40,0),
                (60,0),
                (-30,0)]
    name = "qapf.xlsx"
    FontSize = 10

    def __init__(self,name="qapf.xlsx", Label=[u'Q', u'A', u'P', u'F'],FontSize = 10):
        super().__init__()

        self.raw = ''


        self.Label = Label
        self.name=name
        self.FontSize=FontSize

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1], self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1],FontSize=self.FontSize))

    def uptri(self):
        D=(0,0,100)
        L1 = [(10, 0, 90), (0, 10, 90)]
        L2 = [(40,0,60), (0,40,60)]
        L3 = [(80,0,20), (0,80,20)]

        L4 = [(95, 0, 5), (0, 95, 5)]

        TriLine(Points=L1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [ D, (90,10,0)]
        SL2 = [ D, (65,35,0)]
        SL3 = [ D, (35,65,0)]
        SL4 = [ D, (10,90,0)]

        CL1 = self.TriCross(SL1,L2)
        CL21 = self.TriCross(SL2,L2)
        CL22 = self.TriCross(SL2,L3)
        CL3 = self.TriCross(SL3,L2)
        CL41 = self.TriCross(SL4,L2)
        CL42 = self.TriCross(SL4,L3)

        TL4= self.TriCross(SL3,L4)

        NL4= [(95, 0, 5),TL4]

        NSL1 = [ CL1, (90,10,0)]
        NSL21 = [ CL21, CL22]
        NSL22 = [CL22, (65, 35, 0)]
        NSL3 = [ CL3, (35,65,0)]
        NSL4 = [ CL41, CL42]

        TriLine(Points=NL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

    def lowtri(self):

        D = (0, 0, -100)
        L1 = [(10, 0, -90), (0, 10, -90)]
        L2 = [(40, 0, -60), (0, 40, -60)]
        L3 = [(90, 0, -10), (0, 90, -10)]


        TriLine(Points=L1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL5 = [(5, 5, -90), (45, 45, -10)]

        TriLine(Points=SL5, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [D, (90, 10, 0)]
        SL2 = [D, (65, 35, 0)]
        SL3 = [D, (35, 65, 0)]
        SL4 = [D, (10, 90, 0)]



        CL1 = self.TriCross(SL1, L2)
        CL2 = self.TriCross(SL2, L3)
        CL3 = self.TriCross(SL3, L3)
        CL41 = self.TriCross(SL4, L2)
        CL42 = self.TriCross(SL4, L3)




        NSL1 = [CL1, (90, 10, 0)]
        NSL2 = [CL2, (65, 35, 0)]
        NSL3 = [CL3, (35, 65, 0)]
        NSL4 = [CL41, CL42]


        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

    def draw(self):

        l=self.Locations

        self.uptri()

        self.lowtri()

        for i in self.Tags:
            i.show()


    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            q = raw.at[i, 'Q']
            f = raw.at[i, 'F']
            a = raw.at[i, 'A']
            p = raw.at[i, 'P']

            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            if(q!=0 and q!=''):
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()
            else:
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], -raw.at[i, 'F']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"qapf.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"qapf.svg", dpi=300, bbox_inches='tight')
        plt.show()

class QapfP(Qapf):

    """
    inherit Qapf, read xlsx or csv file and make Qapf diagram for Plutonic Rocks
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []

    Labels = ["quartzolite",

              "quartz-rich\ngranitoid",

              "granite",

              "alkali\nfeldspar\ngranite",
              "(syeno\ngranite)",
              "(monzo\ngranite)",
              "granodiorite",
              "tonalite",

              "quartz\nalkali\nfeldspar\nsyenite",
              "quartz\nsyenite",
              "quartz\nmonzonite",
              "quartz\nmonzodiorite\nquartz\nmonzogabbro",
              "quartz\ndiorite\nquartz gabbro\n quartz\nanorthosite",

              "alkali\nfeldspar\nsyenite",
              "syenite",
              "monzonite",
              "monzodiorite\nmonzogabbro",
              "diorite\ngabbro\nanorthosite",

              "foid-bearing\nalkali\nfeldspar\nsyenite",
              "foid-bearing\nsyenite",
              "foid-bearing\nmonzonite",
              "foid-bearing\nmonzodiorite\nfoid-bearing\nmonzogabbro",
              "foid-bearing\ndiorite\nfoid-bearing gabbro\nfoid-bearing\nanorthosite",

              "foid\nsyenite",
              "foid\nmonzosyenite",
              "foid\nmonzodiorite\nfoid\nmonzogabbro",
              "foid\ndiorite\nfoid\ngabbro",
              "foidolite"]

    Locations = [(5, 5, 95),

                 (10, 10, 80),

                 (35, 15, 50),

                 (45, 5, 50),
                 (45, 25, 30),
                 (35, 35, 30),
                 (25, 45, 30),
                 (5, 45, 50),

                 (85, 5, 10),
                 (75, 15, 10),
                 (45, 45, 10),
                 (15, 75, 10),
                 (5, 85, 10),

                 (93, 5, 2),
                 (83, 15, 2),
                 (53, 53, 2),
                 (15, 83, 2),
                 (5, 93, 2),

                 (95, 3, -8),
                 (75, 23, -8),
                 (49, 49, -8),
                 (23, 75, -8),
                 (3, 95, -8),

                 (63, 7, -30),
                 (50, 20, -30),
                 (20, 50, -30),
                 (7, 63, -30),
                 (10, 10, -80)]

    Offset = [(-30, 0),

              (-30, 0),

              (-20, 0),

              (-70, 30),
              (-50, 30),
              (-30, 0),
              (0, 0),
              (30, 20),

              (-70, 15),
              (-10, 0),
              (-40, 0),
              (-50, -5),
              (30, 15),

              (-80, 5),
              (0, 0),
              (-40, 0),
              (-50, -5),
              (60, 5),

              (-80, -15),
              (-40, 0),
              (-40, 0),
              (-20, -15),
              (50, -30),

              (-80, 0),
              (-40, 0),
              (-40, 0),
              (60, 0),
              (-30, 0)]

    def show(self):
        plt.figure(figsize=(8, 8 * np.sqrt(3)), dpi=80)
        plt.xlim(-10, 110)
        plt.ylim(-105* np.sqrt(3)/2, 105* np.sqrt(3)/2)
        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        ax.spines['left'].set_color('none')
        TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0),(0, 0, -100),(100, 0, 0),(0, 100, 0)], Sort='', Width=1, Color='black', Style="-",
                Alpha=0.7, Label='').show()
        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

    def uptri(self):
        D=(0,0,100)
        L1 = [(10, 0, 90), (0, 10, 90)]
        L2 = [(40,0,60), (0,40,60)]
        L3 = [(80,0,20), (0,80,20)]

        L4 = [(95, 0, 5), (0, 95, 5)]


        TriLine(Points=L1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [ D, (90,10,0)]
        SL2 = [ D, (65,35,0)]
        SL3 = [ D, (35,65,0)]
        SL4 = [ D, (10,90,0)]

        CL1 = self.TriCross(SL1,L2)
        CL21 = self.TriCross(SL2,L2)
        CL22 = self.TriCross(SL2,L3)
        CL3 = self.TriCross(SL3,L2)
        CL41 = self.TriCross(SL4,L2)
        CL42 = self.TriCross(SL4,L3)


        NSL1 = [ CL1, (90,10,0)]
        NSL21 = [ CL21, CL22]
        NSL22 = [CL22, (65, 35, 0)]
        NSL3 = [ CL3, (35,65,0)]
        NSL4 = [ CL41, (10,90,0)]



        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

    def lowtri(self):

        D = (0, 0, -100)
        L2 = [(40, 0, -60), (0, 40, -60)]
        L3 = [(90, 0, -10), (0, 90, -10)]



        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL5 = [(20, 20, -60), (45, 45, -10)]

        TriLine(Points=SL5, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [D, (90, 10, 0)]
        SL2 = [D, (65, 35, 0)]
        SL3 = [D, (35, 65, 0)]
        SL4 = [D, (10, 90, 0)]



        CL1 = self.TriCross(SL1, L2)
        CL2 = self.TriCross(SL2, L3)
        CL3 = self.TriCross(SL3, L3)
        CL41 = self.TriCross(SL4, L2)
        CL42 = self.TriCross(SL4, L3)




        NSL1 = [CL1, (90, 10, 0)]
        NSL2 = [CL2, (65, 35, 0)]
        NSL3 = [CL3, (35, 65, 0)]
        NSL4 = [CL41, (10, 90, 0)]


        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()

        description="QAPF modal classification of plutonic rocks (based on Streckeisen, 1976, Fig. 1a).\nQ = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%."
        Tag(Label=description,Location=(80,40*math.sqrt(3)-1),X_offset=0,Y_offset=0,FontSize=12).show()


        TriPoint((0, 0, -100),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()
        TriPoint((10, 10, -80),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()
        TriPoint((20, 20, -60),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            q = raw.at[i, 'Q']
            f = raw.at[i, 'F']
            a = raw.at[i, 'A']
            p = raw.at[i, 'P']

            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            if(q!=0 and q!=''):
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()
            else:
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], -raw.at[i, 'F']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"qapfP.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"qapfP.svg", dpi=300, bbox_inches='tight')
        plt.show()

class QapfV(Qapf):
    """
    inherit Qapf, read xlsx or csv file and make Qapf diagram for Volcanic rocks
    :param Tags: the Tags on this diagram for description of different units
    :type Tags: a list of strings
    :param Labels: the labels of the different units
    :type Labels: a list of strings
    :param Locations: the triangular coord location of these Labels
    :type Locations: a list of tuples, these tuples contains the triangular coords
    :param Offset: the x-y offset of these labels on canvas
    :type Offset: a list of tuples containing x-y values
    """

    Tags = []

    Labels = ["rhyolite",

              "alkali\nfeldspar\rhyolite",

              "dacite",

              "quartz\nalkali\nfeldspar\ntrachyte",
              "quartz\ntrachyte",
              "quartz\nlatite",
              "basalt\nandesite",

              "alkali\nfeldspar\ntrachyte",
              "trachyte",
              "latite",

              "foid-bearing\nalkali\nfeldspar\ntrachyte",
              "foid-bearing\ntrachyte",
              "foid-bearing\nlatite",

              "phonolite",
              "tephritic\nphonolite",
              " phonolitic\nbasanite\n(olivine > 10%)\nphonolitic\ntephrite\n(olivine < 10%)",
              " basanite\n(olivine > 10%)\ntephrite\n(olivine < 10%)",
              "phonolitic\nfoidite",
              "tephritic\nfoidite",
              "foidoite"]

    Locations = [(35, 15, 50),

                 (45, 5, 50),

                 (20, 50, 30),

                 (85, 5, 10),
                 (75, 15, 10),
                 (45, 45, 10),
                 (15, 75, 10),

                 (93, 5, 2),
                 (83, 15, 2),
                 (53, 53, 2),

                 (95, 3, -8),
                 (75, 23, -8),
                 (49, 49, -8),

                 (63, 7, -30),
                 (50, 20, -30),
                 (20, 50, -30),
                 (7, 63, -30),
                 (16, 8, -76),
                 (8, 16, -76),
                 (4, 4, -92)]

    Offset = [(-20, 0),

              (-70, 30),

              (0, 0),

              (-70, 15),
              (-10, 0),
              (-40, 0),
              (-30, -5),

              (-80, 5),
              (0, 0),
              (-40, 0),

              (-80, -15),
              (-40, 0),
              (-40, 0),

              (-80, 0),
              (-40, 0),
              (-40, 0),
              (60, 0),
              (-40, 20),
              (0, 20),
              (-20, 0)]

    def uptri(self):
        D=(0,0,100)
        L1 = [(10, 0, 90), (0, 10, 90)]
        L2 = [(40,0,60), (0,40,60)]
        L3 = [(80,0,20), (0,80,20)]

        L4 = [(95, 0, 5), (0, 95, 5)]

        TriLine(Points=L1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [ D, (90,10,0)]
        SL2 = [ D, (65,35,0)]
        SL3 = [ D, (35,65,0)]
        SL4 = [ D, (10,90,0)]

        CL1 = self.TriCross(SL1,L2)
        CL21 = self.TriCross(SL2,L2)
        CL22 = self.TriCross(SL2,L3)
        CL3 = self.TriCross(SL3,L2)
        CL41 = self.TriCross(SL4,L2)
        CL42 = self.TriCross(SL4,L3)

        TL4= self.TriCross(SL3,L4)

        NL4= [(95, 0, 5),TL4]

        NSL1 = [ CL1, (90,10,0)]
        NSL21 = [ CL21, CL22]
        NSL22 = [CL22, (65, 35, 0)]
        NSL3 = [ CL3, (35,65,0)]
        NSL4 = [ CL41, CL42]

        TriLine(Points=NL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="--", Alpha=0.7,
                Label='').show()

    def lowtri(self):

        D = (0, 0, -100)
        L1 = [(10, 0, -90), (0, 10, -90)]
        L2 = [(40, 0, -60), (0, 40, -60)]
        L3 = [(90, 0, -10), (0, 90, -10)]


        TriLine(Points=L1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=L3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL5 = [(5, 5, -90), (45, 45, -10)]

        TriLine(Points=SL5, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        SL1 = [D, (90, 10, 0)]
        SL2 = [D, (65, 35, 0)]
        SL3 = [D, (35, 65, 0)]
        SL4 = [D, (10, 90, 0)]



        CL1 = self.TriCross(SL1, L2)
        CL2 = self.TriCross(SL2, L3)
        CL3 = self.TriCross(SL3, L3)
        CL41 = self.TriCross(SL4, L2)
        CL42 = self.TriCross(SL4, L3)




        NSL1 = [CL1, (90, 10, 0)]
        NSL2 = [CL2, (65, 35, 0)]
        NSL3 = [CL3, (35, 65, 0)]
        NSL4 = [CL41, CL42]


        TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()


        TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

        TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style="-", Alpha=0.7,
                Label='').show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """
        self.show()
        self.draw()

        description="QAPF modal classification of volcanic rocks (based on Streckeisen, 1978, Fig. 1).\nQ = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%."

        Tag(Label=description,Location=(80,40*math.sqrt(3)-1),X_offset=0,Y_offset=0,FontSize=12).show()

        TriPoint((0, 0, -100),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()
        TriPoint((10, 10, -80),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()
        TriPoint((20, 20, -60),Size=50, Color='red', Alpha=0.5, Marker="*",Label="test").show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            q = raw.at[i, 'Q']
            f = raw.at[i, 'F']
            a = raw.at[i, 'A']
            p = raw.at[i, 'P']

            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            if(q!=0 and q!=''):
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()
            else:
                TriPoint((raw.at[i, 'A'], raw.at[i, 'P'], -raw.at[i, 'F']), Size=raw.at[i, 'Size'],
                         Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                         Label=TmpLabel).show()

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"qapfV.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"qapfV.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Polar(Frame):

    """
    Polar Stereographic projection for structural data
    :param name: the file used to plot
    :type name: a string
    """
    Label = [u'N', u'S', u'W', u'E']
    LabelPosition = []
    name = "strike.xlsx"

    def __init__(self, name="strike.xlsx",Label=[u'N',u'S', u'W', u'E']):
        super().__init__()

        self.raw = ''

        self.Label = [u'N', u'S', u'W', u'E']
        self.LabelPosition = []
        self.name = "strike.xlsx"


        self.Label = Label
        self.name=name

    def read(self):
        self.wulf()

        plt.figure(2)
        plt.subplot(111)
        self.schmidt()

    def eqar(self,A):
        return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))

    def eqan(self,A):
        return 90 * np.tan(np.pi * (90. - A) / (2. * 180.))

    def getangular(self,A, B, C):
        a = np.radians(A)
        b = np.radians(B)
        c = np.radians(C)
        result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
        result = np.rad2deg(result)
        return result

    def wulf(self, Width=1, Color='k'):
        """
        read the Excel, then draw the wulf net and Plot points, job done~
        """

        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        Data = []
        Labels=[]

        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))

        list1 = [self.eqan(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, 90, 15)]
        plt.rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, "Name"], raw.at[i, "Strike"], raw.at[i, "Dip"], raw.at[i, "Color"],
                         raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Label"]])
            S = raw.at[i, "Strike"]
            D = raw.at[i, "Dip"]
            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Label=raw.at[i, "Label"]
            if(Label not in Labels):
                Labels.append(Label)
            else:
                Label=""

            r = np.arange(S - 90, S + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]
            Line = (self.eqan(self.getangular(D, S, r)))

            plt.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha,label= Label)

        plt.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"Wulff.png", dpi=300)
        plt.savefig(self.name+"Wulff.svg", dpi=300)
        plt.show()

    def schmidt(self, Width=1, Color='k'):
        """
        read the Excel, then draw the schmidt net and Plot points, job done~
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        Data = []
        Labels=[]
        plt.axes(polar=True)
        plt.polar([0], [90])
        plt.xlim((0, 360))
        plt.ylim((0, 90))

        list1 = [self.eqar(x) for x in range(0, 90, 15)]
        list2 = [str(x) for x in range(0, 90, 15)]
        plt.rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append(
                [raw.at[i, "Name"], raw.at[i, "Strike"], raw.at[i, "Dip"], raw.at[i, "Color"],
                 raw.at[i, "Width"], raw.at[i, "Alpha"], raw.at[i, "Marker"], raw.at[i, "Label"]])
            S = raw.at[i, "Strike"]
            D = raw.at[i, "Dip"]
            Width = raw.at[i, "Width"]
            Color = raw.at[i, "Color"]
            Alpha = raw.at[i, "Alpha"]
            Marker = raw.at[i, "Marker"]
            Label = raw.at[i, "Label"]

            if(Label not in Labels):
                Labels.append(Label)
            else:
                Label=""


            plt.plot(np.radians(90 - S), self.eqar(D), color=Color, linewidth=Width, alpha=Alpha, marker=Marker,label=Label)

        #plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        plt.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))

        plt.savefig(self.name+"Schmidt.png", dpi=300)
        plt.savefig(self.name+"Schmidt.svg", dpi=300)
        plt.show()

class LogLine(Line):

    """
    inherit Line, a class for plotting lines with math.log(x,10)
    """

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style="-", Alpha=0.3, Label=''):
        """
        setup the datas
        """
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):
            self.X = [math.log(Points[0][0],10), math.log(Points[1][0],10)]
            self.Y = [math.log(Points[0][1],10), math.log(Points[1][1],10)]
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

        else:
            print("Cannot draw line with one point")


    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        for i in TMP:
            X_TMP.append(math.log(i[0],10))
            Y_TMP.append(math.log(i[1],10))
        self.X = X_TMP
        self.Y = Y_TMP

class LogPoint(Point):

    """
    inherit Point, a class for plotting Points with math.log(x,10)
    """
    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        """
        just set up the values
        """
        super().__init__()
        self.X = math.log(X,10)
        self.Y = math.log(Y,10)
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

class Pearce1(Frame):
    """
    inherit Frame, read xlsx or csv file and use Rb-(Y+Nb) to plot tas diagram
    :param Lines: the lines consisting the frame
    :type Lines: a list of lines
    :param Tags: tags used for the items of diagram
    :type Tagas: a list of strings
    :param Labels: labels on the canvas
    :type Labels: a list of strings
    :param Locations: the locations of these labels
    :type Locations: a list of tuple containing two numbers as x-y coords
    :param description: the description of the tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """

    Lines = []
    Tags = []
    Labels = [u'syn-COLG', u'VAG', u'WPG', u'ORG']
    Locations = [(1, 3), (1, 1), (3, 3), (3, 1)]
    description = "Pearce diagram (after Julian A. Pearce et al., 1984).\n syn-COLG: syn-collision granites\n VAG: volcanic arc granites\n WPG: within plate granites\n ORG: ocean ridge granites "
    text = [u'0.1', u'1', u'10', u'100', u'1000', u'10000', u'100000', u'1000000', u'10000000']
    name = "pearce.xlsx"

    def __init__(self, name="pearce.xlsx", Width=8, Height=8, Dpi=80, Left=0, Right=3.5, X0=0, X1=3, X_Gap=4, Base=0, Top=3.5, Y0=0,
                 Y1=3, Y_Gap=4, FontSize=12, xLabel=r'Y+Nb (PPM)', yLabel=r'Rb (PPM)',text = [u'1', u'10', u'100', u'1000', u'10000'], Labels = [u'syn-COLG', u'VAG', u'WPG', u'ORG'],Locations = [(1, 3), (1, 1), (3, 3), (3, 1)]):
        """
        just set up the basic settings
        """
        super().__init__()

        self.raw = ''

        self.name = name

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel+"\n"+self.description
        self.yLabel = yLabel

        self.Tags = []
        self.Labels = []
        self.Locations = []
        self.text = []

        self.text = text
        self.Labels=Labels
        self.Locations=Locations

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i], Location=self.Locations[i]))


        self.text = text
        self.Lines = [LogLine([(2, 80), (55, 300)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(55,300),(400,2000)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(55,300),(51.5,8)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(51.5,8),(50,1)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(51.5,8),(2000,400)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),]

    def show(self):
        """
        show the frame and lines on canvas
        """
        plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)
        plt.xlim(self.Left, self.Right)
        plt.ylim(self.Base, self.Top)
        plt.xticks(np.linspace(self.X0, self.X1, self.X_Gap, endpoint=True), self.text)
        plt.yticks(np.linspace(self.Y0, self.Y1, self.Y_Gap, endpoint=True), self.text)
        plt.xlabel(self.xLabel, fontsize=self.FontSize)
        plt.ylabel(self.yLabel, fontsize=self.FontSize)
        for i in self.Lines:
            i.show()
        for i in self.Tags:
            i.show()

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            LogPoint( (raw.at[i, 'Y'] + raw.at[i, 'Nb']),raw.at[i, 'Rb'], Size=raw.at[i, 'Size'],
                  Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel).show()
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        plt.savefig(self.name+"pearce1.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"pearce1.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Pearce2(Pearce1):
    """
    inherit Frame, read xlsx or csv file and use Rb-(Yb-Ta) plot tas diagram
    :param Lines: the lines consisting the frame
    :type Lines: a list of lines
    :param Tags: tags used for the items of diagram
    :type Tagas: a list of strings
    :param Labels: labels on the canvas
    :type Labels: a list of strings
    :param Locations: the locations of these labels
    :type Locations: a list of tuple containing two numbers as x-y coords
    :param description: the description of the tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """


    def __init__(self, name="pearce.xlsx", Width=8, Height=8, Dpi=80, Left=-0.5, Right=3.5, X0=0, X1=3, X_Gap=4, Base=0, Top=3.5, Y0=0,
                 Y1=3, Y_Gap=4, FontSize=12, xLabel=r'Yb+Ta (PPM)', yLabel=r'Rb (PPM)',text = [u'1', u'10', u'100', u'1000'],Labels = [u'syn-COLG', u'VAG', u'WPG', u'ORG'],Locations = [(0.5, 3), (0.5, 1), (2, 2.8), (2, 1)]):
        """
        just set up the basic settings
        """
        super().__init__()

        self.raw = ''

        self.name = name

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel+"\n"+self.description
        self.yLabel = yLabel

        self.Tags = []
        self.Labels = []
        self.Locations = []
        self.text = []

        self.text = text
        self.Labels=Labels
        self.Locations=Locations

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i], Location=self.Locations[i]))


        self.Lines = [LogLine([(0.5,140),(6,200)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(6,200),(50,2000)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(6,200),(6,8)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(6,8),(6,1)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(6,8),(200,400)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),]

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            LogPoint( (raw.at[i, 'Yb'] + raw.at[i, 'Ta']),raw.at[i, 'Rb'], Size=raw.at[i, 'Size'],
                  Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel).show()
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        plt.savefig(self.name+"pearce2.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"pearce2.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Pearce3(Pearce1):
    """
    inherit Frame, read xlsx or csv file and use Nb-Y to plot tas diagram
    :param Lines: the lines consisting the frame
    :type Lines: a list of lines
    :param Tags: tags used for the items of diagram
    :type Tagas: a list of strings
    :param Labels: labels on the canvas
    :type Labels: a list of strings
    :param Locations: the locations of these labels
    :type Locations: a list of tuple containing two numbers as x-y coords
    :param description: the description of the tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """

    def __init__(self, name="pearce.xlsx", Width=8, Height=8, Dpi=80, Left=-0.5, Right=3.5, X0=0, X1=3, X_Gap=4, Base=0, Top=3.5, Y0=0,
                 Y1=3, Y_Gap=4, FontSize=12, xLabel=r'Y (PPM)', yLabel=r'Nb (PPM)',text = [u'1', u'10', u'100', u'1000'],Labels = [u'syn-COLG', u'VAG', u'WPG', u'ORG'],Locations = [(0.5, 1.5), (0.5, 2), (2, 2), (2, 1)]):
        """
        just set up the basic settings
        """
        super().__init__()

        self.raw = ''




        self.name = name

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel+"\n"+self.description
        self.yLabel = yLabel

        self.Tags = []
        self.Labels = []
        self.Locations = []
        self.text = []

        self.text = text
        self.Labels=Labels
        self.Locations=Locations

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i], Location=self.Locations[i]))

        self.Lines = [LogLine([(1,2000),(50,10)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(40,1),(50,10)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(50,10),(1000,100)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(25,25),(1000,400)], Sort='', Width=1, Color='black', Style="--", Alpha=0.3)]

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            LogPoint( raw.at[i, 'Y'],raw.at[i, 'Nb'], Size=raw.at[i, 'Size'],
                  Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel).show()
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        plt.savefig(self.name+"pearce3.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"pearce3.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Pearce4(Pearce1):
    """
    inherit Frame, read xlsx or csv file and use Ta-Yb to plot tas diagram
    :param Lines: the lines consisting the frame
    :type Lines: a list of lines
    :param Tags: tags used for the items of diagram
    :type Tagas: a list of strings
    :param Labels: labels on the canvas
    :type Labels: a list of strings
    :param Locations: the locations of these labels
    :type Locations: a list of tuple containing two numbers as x-y coords
    :param description: the description of the tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """


    def __init__(self, name="pearce.xlsx", Width=8, Height=8, Dpi=80, Left=-1.5, Right=2.5, X0=-1, X1=2, X_Gap=4, Base=-1.5, Top=2.5, Y0=-1,
                 Y1=2, Y_Gap=4, FontSize=12, xLabel=r'Yb (PPM)', yLabel=r'Ta (PPM)',text = [u'0.1', u'1', u'10', u'100'],Labels = [u'syn-COLG', u'VAG', u'WPG', u'ORG'],Locations = [ (-1, 0.1),(-1, -1), (0.7, 1), (2, 0.5)]):
        """
        just set up the basic settings
        """
        super().__init__()

        self.raw = ''

        self.name = name

        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel+"\n"+self.description
        self.yLabel = yLabel

        self.Tags = []
        self.Labels = []
        self.Locations = []
        self.text=[]

        self.text=text
        self.Labels=Labels
        self.Locations=Locations

        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i], Location=self.Locations[i]))

        self.Lines = [LogLine([(0.55,20),(3,2)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(0.1,0.35),(3,2)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(3,2),(5,1)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(5,0.05),(5,1)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(5,1),(100,7)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(3,2),(100,20)], Sort='', Width=1, Color='black', Style="--", Alpha=0.3),]

    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)
        PointLabels = []

        for i in range(len(raw)):
            TmpLabel = ''
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            LogPoint( raw.at[i, 'Yb'],raw.at[i, 'Ta'] , Size=raw.at[i, 'Size'],
                  Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel).show()
        plt.legend(loc=5, bbox_to_anchor=(1.5, 0.5))
        plt.savefig(self.name+"pearce4.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name+"pearce4.svg", dpi=300, bbox_inches='tight')
        plt.show()

class MultiFrame(Frame):

    """
    Multiple Frames of Rb-Y+Nb or Rb-Yb+Ta and other similar x-y plots
    :param Width,Height: the width and height of the generated figure
    :type Width,Height: two int numbers
    :param Dpi: dots per inch
    :type Dpi: an int number
    :type

    :param Left,Right: the left and right limit of X axis
    :typeLeft,Right: two lists of int numbers

    :param Base,Top: the left and right limit of Y axis
    :typeBase,Top: two lists of int numbers

    :param X0,X1,X_Gap: the left and right limit of X label, and the numbers of gap between them
    :typeX0,X1,X_Gap: three lists of int numbers

    :param Y0,Y1,Y_Gap: the left and right limit of Y label, and the numbers of gap between them
    :typeY0,Y1,Y_Gap: three lists of int numbers

    :param FontSize: size of font of labels
    :typeFontSize: an int number

    :param xLabel, yLabel: the labels put alongside with x and y axises
    :type xLabel, yLabel: two lists of strings
    """


    Left = []
    Right = []

    Base = []
    Top = []

    X0 = []
    X1 = []
    X_Gap = []

    Y0 = []
    Y1 = []
    Y_Gap = []

    xLabel = []
    yLabel = []

    all=[]
    Lines=[]

    def __init__(self, Width=8, Height=8, Dpi=80, Left=[0,0,0], Right=[10,10,10], X0=[0,0,0],X1=[10,10,10],X_Gap=[11,11,11],Y0=[0,0,0],Y1=[10,10,10],Y_Gap=[11,11,11],Base=[0,0,0], Top=[10,10,10],FontSize=16,
                 xLabel=[r'X Label',r'X Label',r'X Label'], yLabel=[r'Y Label',r'Y Label',r'Y Label']):
        """
        Just set up all.
        """
        super().__init__()

        self.Left = []
        self.Right = []

        self.Base = []
        self.Top = []

        self.X0 = []
        self.X1 = []
        self.X_Gap = []

        self.Y0 = []
        self.Y1 = []
        self.Y_Gap = []

        self.xLabel = []
        self.yLabel = []

        self.all = []
        self.Lines = []



        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.Base = Base
        self.Top = Top

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.Y0 = Y0
        self.Y1 = Y1
        self.Y_Gap = Y_Gap

        self.FontSize = FontSize
        self.xLabel = xLabel
        self.yLabel = yLabel

    def show(self):

        """
        Use the setup to set up figure feature.
        """
        fig = plt.figure(figsize=(self.Width, self.Height), dpi=self.Dpi)

        l=len(self.xLabel)
        if(l%2==0):
            a = int(l/ 2)
        else:
            a = int((l+1) / 2)

        gs = gridspec.GridSpec(a, 2, width_ratios=[1, 1])

        for i in range(len(self.xLabel)):
            self.all.append(plt.subplot(gs[i]))


        for i in range(len(self.y)):
            self.all[i].set_xlim(self.Left[i],self.Right[i])
            self.all[i].set_ylim(self.Base[i], self.Top[i])
            self.all[i].set_xticks(np.linspace(self.X0[i], self.X1[i], self.X_Gap[i], endpoint=True))
            self.all[i].set_yticks(np.linspace(self.Y0[i], self.Y1[i], self.Y_Gap[i], endpoint=True))
            self.all[i].set_xlabel(self.xLabel[i], fontsize=self.FontSize)
            self.all[i].set_ylabel(self.yLabel[i], fontsize=self.FontSize)

        self.Lines = [LogLine([(2, 80), (55, 300)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(55,300),(400,2000)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(55,300),(51.5,8)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(51.5,8),(50,1)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),
                      LogLine([(51.5,8),(2000,400)], Sort='', Width=1, Color='black', Style="-", Alpha=0.3),]
        for i in self.Lines:
            i.show()

class Pearce():
    """
    just a wrapper, read xlsx or csv file and use Rb-(Y+Nb) and Rb-(Yb+Ta) to plot tas diagram
    :param name: the file name used for tas diagram
    :type name: a string
    """
    name="pearce.xlsx"
    def __init__(self,name="pearce.xlsx"):
        self.raw = ''
        self.name=name
    def read(self):
        Pearce1(self.name).read()
        Pearce2(self.name).read()
        Pearce3(self.name).read()
        Pearce4(self.name).read()

class Harker():

    """
    Multiple Frames of Rb-Y+Nb or Rb-Yb+Ta and other similar x-y plots
    :param Width,Height: the width and height of the generated figure
    :type Width,Height: two int numbers
    :param Dpi: dots per inch
    :type Dpi: an int number
    :type

    :param Left,Right: the left and right limit of X axis
    :typeLeft,Right: two lists of int numbers

    :param Base,Top: the left and right limit of Y axis
    :typeBase,Top: two lists of int numbers

    :param X0,X1,X_Gap: the left and right limit of X label, and the numbers of gap between them
    :typeX0,X1,X_Gap: three lists of int numbers

    :param Y0,Y1,Y_Gap: the left and right limit of Y label, and the numbers of gap between them
    :typeY0,Y1,Y_Gap: three lists of int numbers

    :param FontSize: size of font of labels
    :typeFontSize: an int number

    :param xLabel, yLabel: the labels put alongside with x and y axises
    :type xLabel, yLabel: two lists of strings
    """


    Left = 45
    Right = 75


    X0 = 45
    X1 = 75
    X_Gap = 6


    xLabel = r'$SiO_2 wt\%$'
    yLabel = []

    all=[]
    Lines=[]

    Base=[]
    Top=[]
    Gap=[]

    raw=''

    PointLabels = []

    name = "harker.xlsx"
    x='SiO2'
    y = ['Al2O3', 'MgO', 'FeO', 'CaO', 'Na2O', 'TiO2', 'K2O', 'P2O5']

    def __init__(self,name = "harker.xlsx", Width=8, Height=16, Dpi=80, Left=45, Right=75, X0=45,X1=75,X_Gap=6,FontSize=12,
                 x='SiO2', y=['Al2O3','MgO','FeO','CaO','Na2O','TiO2','K2O','P2O5']):
        """
        Just set up all.
        """
        super().__init__()


        self.raw = ''


        self.name = "harker.xlsx"
        self.x = 'SiO2'
        self.y = ['Al2O3', 'MgO', 'FeO', 'CaO', 'Na2O', 'TiO2', 'K2O', 'P2O5']




        self.name=name

        self.x= x
        self.y= y


        self.Width = Width
        self.Height = Height
        self.Dpi = Dpi

        self.Left = Left
        self.Right = Right

        self.X0 = X0
        self.X1 = X1
        self.X_Gap = X_Gap

        self.FontSize = FontSize
        self.xLabel = r'$SiO_2 wt\%$'
        self.yLabel = [r'$Al_2O_3 wt\%$',r'$MgO wt\%$',r'$FeO wt\%$',r'$CaO wt\%$',r'$Na_2O wt\%$',r'$TiO_2 wt\%$',r'$K_2O wt\%$',r'$P_2O_5 wt\%$']

    def show(self):

        """
        Use the setup to set up figure feature.
        """

        l=len(self.y)
        if(l%2==0):
            a = int(l/ 2)
        else:
            a = int((l+1) / 2)



        fig = plt.figure(figsize=(self.Width,self.Width*a/2), dpi=self.Dpi)

        gs = gridspec.GridSpec(a, 2, width_ratios=[1, 1])

        for i in range(len(self.y)):
            self.all.append(plt.subplot(gs[i]))





    def plot(self,k=0):



        if (self.x == 'SiO2'):
            self.Left = 45
            self.Right = 75
            self.X0, self.X1= 45,75

        else:
            Total = []
            for i in range(len(self.raw)):
                tmp = self.raw.at[i, self.x]
                Total.append(tmp)
            X_Base = int(min(Total)) - 1
            X_Top = int(max(Total)) + 1
            X_Gap = X_Top - X_Base + 1

            self.Left,self.Right,self.X_Gap= X_Base,X_Top,X_Gap
            self.X0, self.X1,self.X_Gap=  X_Base,X_Top,X_Gap

        for i in range(len(self.y)):
            self.all[i].set_xlim(self.Left, self.Right)
            self.all[i].set_xticks(np.linspace(self.X0, self.X1, self.X_Gap, endpoint=True))
            self.all[i].set_xlabel(self.x, fontsize=self.FontSize)
            self.all[i].set_ylabel(self.y[i], fontsize=self.FontSize)



        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        self.raw=raw


        Total = []
        for i in range(len(self.raw)):
            tmp=self.raw.at[i,self.y[k]]
            Total.append(tmp)
            TmpLabel = ''
            TmpLabel = ''
            if (raw.at[i, 'Label'] in self.PointLabels or raw.at[i, 'Label'] =='' ):
                TmpLabel = ''
            else:
                self.PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            self.all[k].scatter(self.raw.at[i, self.x],  tmp, marker=self.raw.at[i, 'Marker'], s=self.raw.at[i, 'Size'], color=self.raw.at[i, 'Color'], alpha=self.raw.at[i, 'Alpha'],
                         label=TmpLabel, edgecolors='black')

        Y_Base= int(min(Total))-1
        Y_Top= int(max(Total))+1
        Y_Gap= Y_Top -Y_Base + 1

        self.all[k].set_ylim(Y_Base, Y_Top)
        self.all[k].set_yticks(np.linspace(Y_Base, Y_Top, Y_Gap, endpoint=True))
        if k==0:
            self.all[k].legend(loc=5, bbox_to_anchor=(2.8, 0.5))



    def read(self):
        """
        read the Excel, then use self.show() to show the frame, then Plot points, job done~
        """

        self.show()

        if ("csv" in self.name):
            raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            raw = pd.read_excel(self.name)

        self.raw=raw

        for k in range(len(self.y)):
            self.plot(k)

        plt.savefig(self.name + "harker.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name + "harker.svg", dpi=300, bbox_inches='tight')
        plt.show()

class Ballard():
    """
    Claculation of Ce4/Ce3 in Zircon
    """

    name = "Ballard.xlsx"
    raw = ''



    Elements = []
    Elements3 = []
    UnUsedElements3 = []
    Elements4 = []
    E3 = []
    UnUsedE3 = []
    E4 = []

    Sample = []
    Rock = []

    x3 = []
    y3 = []

    UnUsedx3 = []
    UnUsedy3 = []

    x4 = []
    y4 = []

    Ce3 = []
    Ce4 = []

    a = []
    b = []

    def __init__(self,name="Ballard.xlsx"):
        self.raw=''
        self.raw=pd.read_excel(self.name)

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()


        self.RockCe = self.raw.at['Rock', 'Ce']

        for i in self.b:
            if i != 'Label' and i != 'Eu(II)' and i != 'Ce' and i != 'Ce(+4)':
                self.Elements.append(i)

                Ri = self.raw.at['Ri', i]
                Ro = self.raw.at['Ro', i]
                X = (Ri / 3 + Ro / 6) * (Ri - Ro) * (Ri - Ro)

                S = self.raw.at['Sample', i]
                R = self.raw.at['Rock', i]

                self.Sample.append(S)
                self.Rock.append(R)
                Y = np.log(S / R)

                if self.raw.at['valence', i] == 3 and self.raw.at['use', i] == 'yes':
                    self.Elements3.append(i)
                    self.E3.append([i, S, R])
                    self.x3.append(X)
                    self.y3.append(Y)

                elif self.raw.at['valence', i] == 3 and self.raw.at['use', i] == 'no':
                    self.UnUsedElements3.append(i)
                    self.UnUsedE3.append([i, S, R])
                    self.UnUsedx3.append(X)
                    self.UnUsedy3.append(Y)

                elif self.raw.at['valence', i] == 4 and self.raw.at['use', i] == 'yes':

                    self.Elements4.append(i)
                    self.E3.append([i, S, R])
                    self.x4.append(X)
                    self.y4.append(Y)


            elif i == 'Ce':
                Ri = self.raw.at['Ri', i]
                Ro = self.raw.at['Ro', i]
                X = (Ri / 3 + Ro / 6) * (Ri - Ro) * (Ri - Ro)

                S = self.raw.at['Sample', i]
                R = self.raw.at['Rock', i]

                self.Sample.append(S)
                self.Rock.append(R)
                Y = np.log(S / R)
                self.Ce3 = [X, Y]



            elif i == 'Ce(+4)':
                Ri = self.raw.at['Ri', i]
                Ro = self.raw.at['Ro', i]
                X = (Ri / 3 + Ro / 6) * (Ri - Ro) * (Ri - Ro)

                S = self.raw.at['Sample', i]
                R = self.raw.at['Rock', i]

                self.Sample.append(S)
                self.Rock.append(R)
                self.Y = np.log(S / R)
                self.Ce4 = [X, Y]


    def Calc3(self):

        self.z3 = np.polyfit(self.x3, self.y3, 1)
        self.p3 = np.poly1d(self.z3)

        Xline3 = np.linspace(min(self.x3), max(self.UnUsedx3), 30)
        Yline3 = self.p3(Xline3)

        Ce3test = str(np.power(np.e, self.p3(self.Ce3[0]) + np.log(self.RockCe)))
        DCe3test = str(np.power(np.e, self.p3(self.Ce3[0])))

        xlabel3 = "ZirconData is " + str(self.Ce3[1]) + "\n Testdata is" + str(self.p3(self.Ce3[0]))+ "\n  est'd Ce(III) (ppm)=" + Ce3test + "\n  est'd DCe(III)(Zir/Met) (ppm)=" + DCe3test

        plt.xlabel(xlabel3, fontsize=12)

        plt.ylabel(r'Ln D $Zircon/Rock%$', fontsize=12)
        plt.plot(Xline3, Yline3, 'r-')

        Point(self.Ce3[0], self.p3(self.Ce3[0]), Label='', Color='red').show()
        plt.annotate("Ce3 Calculated", xy=(self.Ce3[0], self.p3(self.Ce3[0])), xytext=(10, -25), textcoords='offset points',
                     ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        Point(self.Ce3[0], self.Ce3[1], Label='', Color='red').show()
        plt.annotate("Ce3 Zircon", xy=(self.Ce3[0], self.Ce3[1]), xytext=(10, 25), textcoords='offset points', ha='right',
                     va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        Line(Points=[(self.Ce3[0], self.Ce3[1]), (self.Ce3[0], self.p3(self.Ce3[0]))], Style='--', Color='red', Alpha=0.5).show()

        for i in range(len(self.x3)):
            Point(self.x3[i], self.y3[i], Label='', Color='red').show()
            plt.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[i]), xytext=(10, 25), textcoords='offset points', ha='right',
                         va='bottom',
                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                         arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in range(len(self.UnUsedx3)):
            Point(self.UnUsedx3[i], self.UnUsedy3[i], Label='', Color='red').show()
            plt.annotate(self.UnUsedElements3[i], xy=(self.UnUsedx3[i], self.UnUsedy3[i]), xytext=(10, 25), textcoords='offset points',
                         ha='right', va='bottom',
                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                         arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        plt.savefig("zircon-Ce3.png", dpi=300, bbox_inches='tight')
        plt.savefig("zircon-Ce3.svg", dpi=300, bbox_inches='tight')

    def Calc4(self):
        plt.figure(2)
        plt.subplot(111)
        self.z4 = np.polyfit(self.x4, self.y4, 1)
        self.p4 = np.poly1d(self.z4)

        Xline4 = np.linspace(min(self.x4), max(self.x4), 30)
        Yline4 = self.p4(Xline4)

        Ce4test = str(np.power(np.e, self.p4(self.Ce4[0]) + np.log(self.RockCe)))
        DCe4test = str(np.power(np.e, self.p4(self.Ce4[0])))

        xlabel4 = "ZirconData is " + str(self.Ce4[1]) + "\n Testdata is" + str(self.p4(self.Ce4[0]))+ "\n  est'd Ce(III) (ppm)=" + Ce4test + "\n  est'd DCe(III)(Zir/Met) (ppm)=" + DCe4test

        plt.xlabel(xlabel4, fontsize=12)

        plt.ylabel(r'Ln D $Zircon/Rock%$', fontsize=12)
        plt.plot(Xline4, Yline4, 'r-')

        Point(self.Ce4[0], self.p4(self.Ce4[0]), Label='', Color='red').show()
        plt.annotate("Ce4 Calculated", xy=(self.Ce4[0], self.p4(self.Ce4[0])), xytext=(10, -25), textcoords='offset points',
                     ha='right', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.4),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        Point(self.Ce4[0], self.Ce4[1], Label='', Color='red').show()
        plt.annotate("Ce4 Zircon", xy=(self.Ce4[0], self.Ce4[1]), xytext=(10, 25), textcoords='offset points', ha='right',
                     va='bottom',
                     bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.4),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        Line(Points=[(self.Ce4[0], self.Ce4[1]), (self.Ce4[0], self.p4(self.Ce4[0]))], Style='--', Color='red', Alpha=0.5).show()

        for i in range(len(self.x4)):
            Point(self.x4[i], self.y4[i], Label='', Color='red').show()
            plt.annotate(self.Elements4[i], xy=(self.x4[i], self.y4[i]), xytext=(10, 25), textcoords='offset points', ha='right',
                         va='bottom',
                         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.4),
                         arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))


        plt.savefig("zircon-Ce4.png", dpi=300, bbox_inches='tight')
        plt.savefig("zircon-Ce4.svg", dpi=300, bbox_inches='tight')

    def read(self):
        self.Calc3()
        self.Calc4()

class MultiBallard():
    """
    Claculation of Ce4/Ce3 of multiple Zircons in a same rock
    """
    # -*- coding: utf-8 -*-
    """
    Created on Mon Nov  7 15:55:03 2016

    @author: cycleuser
    """
    name = "MultiBallard.xlsx"

    PointLabels = []

    Base = 0
    Zircon = []
    Elements = []
    Elements3 = []
    Elements3_Plot_Only = []
    Elements4 = []
    x = []
    x3 = []
    x3_Plot_Only = []
    x4 = []
    y = []
    y3 = []
    y3_Plot_Only = []
    y4 = []
    z3 = []
    z4 = []
    xCe3 = []
    yCe3 = []
    xCe4 = []
    yCe4 = []
    Ce3test = []
    DCe3test = []
    Ce4test = []
    DCe4test = []
    Ce4_3_Ratio = []
    a = 0
    b = 0
    raw = 0
    RockCe = 0
    ZirconCe = []


    def getx(self,Ri=1, Ro=1):
        X = (Ri / 3 + Ro / 6) * (Ri - Ro) * (Ri - Ro)
        return (X)

    def ToCsv(self,name='MultiBallardResultCalculated.csv', DataToWrite=[
        ["Zircon Sample Label", "Zircon Ce4_3 Ratio", "Melt Ce4_3 Ratio", "DCe4", "DCe3", "DCe Zircon/Melt"], ]):
        with open(name, 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(DataToWrite)

    def __init__(self,name="MultiBallard.xlsx"):
        self.raw=[]
        self.name=name

        if ("csv" in self.name):
            self.raw = pd.read_csv(self.name)
        elif ("xlsx" in name):
            self.raw = pd.read_excel(self.name)

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()

        self.RockCe = self.raw.at[4, 'Ce']
        self.ZirconCe = []

        for i in range(len(self.raw)):
            if (self.raw.at[i, "DataType"] == "Base"):
                self.Base = i
            elif (self.raw.at[i, "DataType"] == "Zircon"):
                self.Zircon.append(i)

        for j in self.b:
            if (j == 'Ce'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.xCe3.append(self.getx(ri, ro))
            elif (j == 'Ce4'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 4):
                    self.xCe4.append(self.getx(ri, ro))

            elif (self.raw.at[1, j] == 'yes'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3.append(self.getx(ri, ro))
                    self.Elements3.append(j)

                elif (self.raw.at[0, j] == 4):
                    self.x4.append(self.getx(ri, ro))
                    self.Elements4.append(j)
                    self.Elements.append(j)

            elif (self.raw.at[1, j] == 'no'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3_Plot_Only.append(self.getx(ri, ro))
                    self.Elements3_Plot_Only.append(j)
                    self.Elements.append(j)

    def read(self):
        for i in self.Zircon:
            self.ZirconCe.append(self.raw.at[i, 'Ce'])
            tmpy3 = []
            tmpy4 = []
            tmpy3_Plot_Only = []

            for j in self.b:
                if (j == 'Ce'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe3.append(ytemp)
                elif (j == 'Ce4'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe4.append(ytemp)
                elif (self.raw.at[1, j] == 'yes'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3.append(ytemp)

                    elif (self.raw.at[0, j] == 4):
                        tmpy4.append(ytemp)
                elif (self.raw.at[1, j] == 'no'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3_Plot_Only.append(ytemp)
            self.y3.append(tmpy3)
            self.y4.append(tmpy4)
            self.y3_Plot_Only.append(tmpy3_Plot_Only)

        plt.ylabel(r'Ln D $Zircon/Rock%$', fontsize=12)

        for k in range(len(self.y3)):

            tmpz3 = np.polyfit(self.x3, self.y3[k], 1)
            self.z3.append(tmpz3)

            for i in range(len(self.x3)):
                x, y = self.x3[i], self.y3[k][i]
                Point(x, y, Label='', Size=5, Color='blue', Alpha=0.5).show()

            if k == 0:
                for i in range(len(self.x3)):
                    plt.annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]), xytext=(10, 25), textcoords='offset points',
                                 ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z3:
            Xline3 = np.linspace(min(self.x3), max(max(self.x3_Plot_Only), max(self.x3)), 30)
            p3 = np.poly1d(i)
            Yline3 = p3(Xline3)
            plt.plot(Xline3, Yline3, 'b-')

            self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.RockCe))[0])
            self.DCe3test.append(np.power(np.e, p3(self.xCe3))[0])

        for k in range(len(self.yCe3)):

            x, y = self.xCe3, self.yCe3[k]
            Point(x, y, Label='', Size=20, Color='k', Alpha=0.5).show()

            if k == 0:
                plt.annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), xytext=(10, 25), textcoords='offset points', ha='right',
                             va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y3_Plot_Only)):

            for i in range(len(self.x3_Plot_Only)):
                x, y = self.x3_Plot_Only[i], self.y3_Plot_Only[k][i]
                Point(x, y, Label='', Size=10, Color='blue', Alpha=0.3).show()

            if k == 0:
                for i in range(len(self.x3_Plot_Only)):
                    plt.annotate(self.Elements3_Plot_Only[i], xy=(self.x3_Plot_Only[i], self.y3_Plot_Only[0][i]), xytext=(10, -25),
                                 textcoords='offset points', ha='right', va='bottom',
                                 bbox=dict(boxstyle='round,pad=0.5', fc='green', alpha=0.2),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        plt.savefig(self.name + "zircon-Ce3.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name + "zircon-Ce3.svg", dpi=300, bbox_inches='tight')

        plt.figure(2)

        plt.ylabel(r'Ln D $Zircon/Rock%$', fontsize=12)
        plt.subplot(111)

        for k in range(len(self.y4)):

            tmpz4 = np.polyfit(self.x4, self.y4[k], 1)
            self.z4.append(tmpz4)

            for i in range(len(self.x4)):
                x, y = self.x4[i], self.y4[k][i]
                Point(x, y, Label='', Size=5, Color='r', Alpha=0.5).show()

            if k == 0:
                for i in range(len(self.x4)):
                    plt.annotate(self.Elements4[i], xy=(self.x4[i], self.y4[0][i]), xytext=(10, 25), textcoords='offset points',
                                 ha='right', va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z4:
            Xline4 = np.linspace(min(self.x4), max(self.x4), 30)
            p4 = np.poly1d(i)
            Yline4 = p4(Xline4)
            plt.plot(Xline4, Yline4, 'r-')

            self.Ce4test.append(np.power(np.e, p4(self.xCe4) + np.log(self.RockCe))[0])
            self.DCe4test.append(np.power(np.e, p4(self.xCe4))[0])

        for k in range(len(self.yCe4)):

            x, y = self.xCe4, self.yCe4[k]
            Point(x, y, Label='', Size=20, Color='k', Alpha=0.5).show()
            if k == 0:
                plt.annotate('Ce4', xy=(self.xCe4[k], max(self.yCe4)), xytext=(10, 25), textcoords='offset points', ha='right',
                             va='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.3),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        plt.savefig(self.name + "zircon-Ce4.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.name + "zircon-Ce4.svg", dpi=300, bbox_inches='tight')

        DataToWrite = [
            ["Zircon Sample Label", "Zircon Ce4_3 Ratio", "Melt Ce4_3 Ratio", "DCe4", "DCe3", "DCe Zircon/Melt"], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], "Label"]
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            DataToWrite.append([TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        Tool().ToCsv(name= self.name+'_ResultCalculated.csv', DataToWrite=DataToWrite)

class CIPW():

    addon= 'Name Author DataType Label Marker Color Size Alpha Style Width TOTAL total LOI loi'

    Minerals=["Quartz",
                "Zircon",
                "K2SiO3",
                "Anorthite",
                "Na2SiO3",
                "Acmite",
                "Diopside",
                "Sphene",
                "Hypersthene",
                "Albite",
                "Orthoclase",
                "Wollastonite",
                "Olivine",
                "Perovskite",
                "Nepheline",
                "Leucite",
                "Larnite",
                "Kalsilite",
                "Apatite",
                "Halite",
                "Fluorite",
                "Anhydrite",
                "Thenardite",
                "Pyrite",
                "Magnesiochromite",
                "Chromite",
                "Ilmenite",
                "Calcite",
                "Na2CO3",
                "Corundum",
                "Rutile",
                "Magnetite",
                "Hematite",]

    Calced=[    'Fe3+/(Total Fe) in rock',
                'Mg/(Mg+Total Fe) in rock',
                'Mg/(Mg+Fe2+) in rock',
                'Mg/(Mg+Fe2+) in silicates',
                'Ca/(Ca+Na) in rock',
                'Plagioclase An content',
                'Differentiation Index']
    DataWeight={}
    DataVolume={}
    DataBase={}
    DataCalced = {}

    def __init__(self,name= "CIPW.xlsx"):


        self.DataBase.update({"Quartz":[60.0843,2.65]})
        self.DataBase.update({"Zircon":[183.3031,4.56]})
        self.DataBase.update({"K2SiO3":[154.2803,2.5]})
        self.DataBase.update({"Anorthite":[278.2093,2.76]})
        self.DataBase.update({"Na2SiO3":[122.0632,2.4]})
        self.DataBase.update({"Acmite":[462.0083,3.6]})
        self.DataBase.update({"Diopside":[229.0691997,3.354922069]})
        self.DataBase.update({"Sphene":[196.0625,3.5]})
        self.DataBase.update({"Hypersthene":[112.9054997,3.507622212]})
        self.DataBase.update({"Albite":[524.446,2.62]})
        self.DataBase.update({"Orthoclase":[556.6631,2.56]})
        self.DataBase.update({"Wollastonite":[116.1637,2.86]})
        self.DataBase.update({"Olivine":[165.7266995,3.68429065]})
        self.DataBase.update({"Perovskite":[135.9782,4]})
        self.DataBase.update({"Nepheline":[284.1088,2.56]})
        self.DataBase.update({"Leucite":[436.4945,2.49]})
        self.DataBase.update({"Larnite":[172.2431,3.27]})
        self.DataBase.update({"Kalsilite":[316.3259,2.6]})
        self.DataBase.update({"Apatite":[493.3138,3.2]})
        self.DataBase.update({"Halite":[66.44245,2.17]})
        self.DataBase.update({"Fluorite":[94.0762,3.18]})
        self.DataBase.update({"Anhydrite":[136.1376,2.96]})
        self.DataBase.update({"Thenardite":[142.0371,2.68]})
        self.DataBase.update({"Pyrite":[135.9664,4.99]})
        self.DataBase.update({"Magnesiochromite":[192.2946,4.43]})
        self.DataBase.update({"Chromite":[223.8366,5.09]})
        self.DataBase.update({"Ilmenite":[151.7452,4.75]})
        self.DataBase.update({"Calcite":[100.0892,2.71]})
        self.DataBase.update({"Na2CO3":[105.9887,2.53]})
        self.DataBase.update({"Corundum":[101.9613,3.98]})
        self.DataBase.update({"Rutile":[79.8988,4.2]})
        self.DataBase.update({"Magnetite":[231.5386,5.2]})
        self.DataBase.update({"Hematite":[159.6922,5.25]})

        self.name = name


        if ("csv" in self.name):
            self.raw = pd.read_csv(self.name)
        elif ("xlsx" in self.name):
            self.raw = pd.read_excel(self.name)

        self.b=self.raw.columns
        self.WeightCorrectionFactor=[]
        self.BaseMass={}
        self.Elements=[]
        self.DataMole=[]
        self.DataCalculating ={}
        self.DataResult={}

        for i in self.b:
            if i in self.addon.split() :
                pass
            else:
                """
                Get the list of Elements
                """
                if i in ['Sr','Ba','Ni']:
                    k=i+"O"
                elif i =='Cr':
                    k=i+"2O3"
                elif i =='Zr':
                    k=i+"O2"
                else:
                    k=i
                    
                m=0
                try:
                    m=Tool().Mass(k)
                except: # catch *all* exceptions
                    e = sys.exc_info()[0]
                """
                Get the Mole Mass of each Element
                """

                self.Elements.append(i)
                self.BaseMass.update({i:m})


        for i in range(len(self.raw)):
            TmpWhole=0
            TmpMole={}
            for j in self.Elements:
                """
                Get the Whole Mole of the dataset
                """
                if j in ['Sr','Ba','Ni']:

                    T_TMP=self.raw.at[i,j]
                    TMP = T_TMP/ ( Tool().Mass(j)/Tool().Mass(j+'O') *10000 )

                elif j =='Cr':
                    T_TMP=self.raw.at[i,j]
                    TMP = T_TMP/((2*Tool().Mass("Cr"))/Tool().Mass("Cr2O3")*10000)

                elif j =='Zr':
                    T_TMP=self.raw.at[i,j]
                    TMP = T_TMP/((2*Tool().Mass("Zr"))/Tool().Mass("ZrO2")*10000)

                else:
                    TMP=self.raw.at[i,j]

                V= TMP
                TmpWhole+=V


            self.WeightCorrectionFactor.append(100/TmpWhole)


            for j in self.Elements:
                """
                Get the Mole percentage of each element
                """
                T_TMP = self.raw.at[i, j]
                if j in ['Sr','Ba','Ni']:
                    TMP = T_TMP/ ( Tool().Mass(j)/Tool().Mass(j+'O') *10000 )

                elif j =='Cr':
                    TMP = T_TMP/((2*Tool().Mass("Cr"))/Tool().Mass("Cr2O3")*10000)


                elif j =='Zr':
                    TMP = T_TMP/((Tool().Mass("Zr"))/Tool().Mass("ZrO2")*10000)


                else:
                    TMP=self.raw.at[i,j]

                M= TMP/self.BaseMass[j] * self.WeightCorrectionFactor[i]
                # M= TMP/NewMass(j) * WeightCorrectionFactor[i]

                TmpMole.update({j:M})
            self.DataMole.append(TmpMole)

        self.DataCalculating= {k: [] for k in self.Elements}

        for i in range(len(self.DataMole)):
            k=self.raw.at[i,'Label']
            self.DataResult.update({ k: {} } )
            self.DataWeight.update({ k: {} } )
            self.DataVolume.update({ k: {} } )
            self.DataCalced.update({k: {}})


            a=self.DataMole[i]
            for j in list(a):
                self.DataCalculating[j].append(a[j])

            Fe3 = self.DataCalculating['Fe2O3'][i]
            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]
            Ca = self.DataCalculating['CaO'][i]
            Na = self.DataCalculating['Na2O'][i]

            self.DataCalced[k].update({'Fe3+/(Total Fe) in rock': 100 * Fe3 * 2 / (Fe3 * 2 + Fe2)})
            self.DataCalced[k].update({'Mg/(Mg+Total Fe) in rock': 100 * Mg / (Mg + Fe3 * 2 + Fe2)})
            self.DataCalced[k].update({'Mg/(Mg+Fe2+) in rock': 100 * Mg / (Mg + Fe2)})
            self.DataCalced[k].update({'Ca/(Ca+Na) in rock': 100 * Ca / (Ca + Na * 2)})



            self.DataCalculating['CaO'][i]+=self.DataCalculating['Sr'][i]
            self.DataCalculating['Sr'][i]=0

            self.DataCalculating['K2O'][i]+=2*self.DataCalculating['Ba'][i]
            self.DataCalculating['Ba'][i]=0


            if self.DataCalculating['CaO'][i]>=10/3*self.DataCalculating['P2O5'][i]:
                self.DataCalculating['CaO'][i]-=10/3*self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['CaO'][i]=0

            self.DataCalculating['P2O5'][i]=self.DataCalculating['P2O5'][i]/1.5

            Apatite=self.DataCalculating['P2O5'][i]


            #IF(S19>=T15,S19-T15,0)

            if self.DataCalculating['F'][i]>=self.DataCalculating['P2O5'][i]:
                self.DataCalculating['F'][i]-=self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['F'][i]=0

            if self.DataCalculating['Na2O'][i]>=self.DataCalculating['Cl'][i]:
                self.DataCalculating['Na2O'][i]-=self.DataCalculating['Cl'][i]
            else:
                self.DataCalculating['Na2O'][i]=0

            Halite=self.DataCalculating['Cl'][i]

            #IF(U12>=(U19/2),U12-(U19/2),0)
            if self.DataCalculating['CaO'][i]>=0.5*self.DataCalculating['F'][i]:
                self.DataCalculating['CaO'][i]-=0.5*self.DataCalculating['F'][i]
            else:
                self.DataCalculating['CaO'][i]=0

            self.DataCalculating['F'][i]*=0.5

            Fluorite=self.DataCalculating['F'][i]

            #=IF(V17>0,IF(V13>=V17,"Thenardite",IF(V13>0,"Both","Anhydrite")),"None")
            AorT=0
            if self.DataCalculating['SO3'][i]<=0:
                AorT='None'
            else:
                if self.DataCalculating['Na2O'][i]>=self.DataCalculating['SO3'][i]:
                    AorT='Thenardite'
                else:
                    if self.DataCalculating['Na2O'][i]>0:
                        AorT='Both'
                    else:
                        AorT='Anhydrite'

            #=IF(W26="Anhydrite",V17,IF(W26="Both",V12,0))
            #=IF(W26="Thenardite",V17,IF(W26="Both",V17-W17,0))

            if AorT =='Anhydrite':
                self.DataCalculating['Sr'][i]=0
            elif AorT =='Thenardite':
                self.DataCalculating['Sr'][i]=self.DataCalculating['SO3'][i]
                self.DataCalculating['SO3'][i]=0
            elif AorT =='Both':
                self.DataCalculating['Sr'][i]=self.DataCalculating['SO3'][i]-self.DataCalculating['CaO'][i]
                self.DataCalculating['SO3'][i]=self.DataCalculating['CaO'][i]
            else:
                self.DataCalculating['SO3'][i]=0
                self.DataCalculating['Sr'][i]=0

            self.DataCalculating['CaO'][i] -=self.DataCalculating['SO3'][i]

            self.DataCalculating['Na2O'][i] -=self.DataCalculating['Sr'][i]


            Anhydrite=self.DataCalculating['SO3'][i]
            Thenardite=self.DataCalculating['Sr'][i]

            Pyrite=0.5*self.DataCalculating['S'][i]


            #=IF(W9>=(W18*0.5),W9-(W18*0.5),0)

            if self.DataCalculating['FeO'][i]>=self.DataCalculating['S'][i]*0.5:
                self.DataCalculating['FeO'][i]-=self.DataCalculating['S'][i]*0.5
            else:
                self.DataCalculating['FeO'][i]=0

            #=IF(X24>0,IF(X9>=X24,"Chromite",IF(X9>0,"Both","Magnesiochromite")),"None")

            if self.DataCalculating['Cr'][i]>0:
                if self.DataCalculating['FeO'][i]>= self.DataCalculating['Cr'][i]:
                    CorM='Chromite'
                elif self.DataCalculating['FeO'][i]>0:
                    CorM='Both'
                else:
                    CorM='Magnesiochromite'
            else:
                CorM='None'




            #=IF(Y26="Chromite",X24,IF(Y26="Both",X9,0))
            #=IF(Y26="Magnesiochromite",X24,IF(Y26="Both",X24-Y24,0))

            if CorM=='Chromite':
                self.DataCalculating['Cr'][i]=self.DataCalculating['Cr'][i]
                self.DataCalculating['Ni'][i]=0

            elif CorM=='Magnesiochromite':
                self.DataCalculating['Ni'][i]=self.DataCalculating['Cr'][i]
                self.DataCalculating['Cr'][i]=0

            elif CorM=='Both':
                self.DataCalculating['Ni'][i]=self.DataCalculating['Cr'][i]-self.DataCalculating['FeO'][i]
                self.DataCalculating['Cr'][i]=self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['Cr'][i]=0
                self.DataCalculating['Ni'][i]=0



            self.DataCalculating['MgO'][i]-= self.DataCalculating['Ni'][i]

            Magnesiochromite=self.DataCalculating['Ni'][i]
            Chromite=self.DataCalculating['Cr'][i]

            #=IF(X9>=Y24,X9-Y24,0)

            if self.DataCalculating['FeO'][i]>= self.DataCalculating['Cr'][i]:
                self.DataCalculating['FeO'][i]-=self.DataCalculating['Cr'][i]
            else:
                self.DataCalculating['FeO'][i]=0




            #=IF(Y6>0,IF(Y9>=Y6,"Ilmenite",IF(Y9>0,"Both","Sphene")),"None")

            if self.DataCalculating['TiO2'][i]<0:
                IorS='None'
            else:
                if self.DataCalculating['FeO'][i]>= self.DataCalculating['TiO2'][i]:
                    IorS='Ilmenite'
                else:
                    if self.DataCalculating['FeO'][i]>0:
                        IorS='Both'
                    else:
                        IorS='Sphene'

            #=IF(Z26="Ilmenite",Y6,IF(Z26="Both",Y9,0))
            #=IF(Z26="Sphene",Y6,IF(Z26="Both",Y6-Z6,0))

            if IorS== 'Ilmenite'    :
                self.DataCalculating['TiO2'][i]=self.DataCalculating['TiO2'][i]
                self.DataCalculating['MnO'][i]=0

            elif IorS=='Sphene':
                self.DataCalculating['MnO'][i]=self.DataCalculating['TiO2'][i]
                self.DataCalculating['TiO2'][i]=0

            elif IorS=='Both':

                self.DataCalculating['MnO'][i]=self.DataCalculating['TiO2'][i]-self.DataCalculating['FeO'][i]
                self.DataCalculating['TiO2'][i]=self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['TiO2'][i]=0
                self.DataCalculating['MnO'][i]=0


            self.DataCalculating['FeO'][i]-=self.DataCalculating['TiO2'][i]

            Ilmenite=self.DataCalculating['TiO2'][i]

            #=IF(Z16>0,IF(Z12>=Z16,"Calcite",IF(Z12>0,"Both","Na2CO3")),"None")


            if  self.DataCalculating['CO2'][i]<=0:
                CorN='None'
            else:
                if self.DataCalculating['CaO'][i]>=self.DataCalculating['CO2'][i]:
                    CorN='Calcite'
                else:
                    if self.DataCalculating['CaO'][i]>0:
                        CorN='Both'
                    else:
                        CorN='Na2CO3'





            #=IF(AA26="Calcite",Z16,IF(AA26="Both",Z12,0))


            #=IF(AA26="Na2CO3",Z16,IF(AA26="Both",Z16-AA16,0))

            if CorN=='None':
                self.DataCalculating['CO2'][i]=0
                self.DataCalculating['SO3'][i]=0

            elif CorN =='Calcite':
                self.DataCalculating['CO2'][i]=self.DataCalculating['CO2'][i]
                self.DataCalculating['SO3'][i]=0

            elif CorN =='Na2CO3':
                self.DataCalculating['SO3'][i]=self.DataCalculating['SO3'][i]
                self.DataCalculating['CO2'][i]=0

            elif CorN =='Both':
                self.DataCalculating['SO3'][i]= self.DataCalculating['CO2'][i]-self.DataCalculating['CaO'][i]
                self.DataCalculating['CO2'][i]=self.DataCalculating['CaO'][i]


            self.DataCalculating['CaO'][i]-=self.DataCalculating['CO2'][i]


            Calcite=self.DataCalculating['CO2'][i]

            Na2CO3=self.DataCalculating['SO3'][i]

            #=IF(AA17>Z13,0,Z13-AA17)
            if self.DataCalculating['SO3'][i]>self.DataCalculating['Na2O'][i]:
                self.DataCalculating['Na2O'][i]=0
            else:
                self.DataCalculating['Na2O'][i]-=self.DataCalculating['SO3'][i]

            self.DataCalculating['SiO2'][i]-=self.DataCalculating['Zr'][i]
            Zircon=self.DataCalculating['Zr'][i]

            #=IF(AB14>0,IF(AB7>=AB14,"Orthoclase",IF(AB7>0,"Both","K2SiO3")),"None")

            if self.DataCalculating['K2O'][i]<=0:
                OorK='None'
            else:
                if self.DataCalculating['Al2O3'][i]>= self.DataCalculating['K2O'][i]:
                    OorK='Orthoclase'
                else:
                    if self.DataCalculating['Al2O3'][i]>0:
                        OorK='Both'
                    else:
                        OorK ='K2SiO3'



            #=IF(AC26="Orthoclase",AB14,IF(AC26="Both",AB7,0))
            #=IF(AC26="K2SiO3",AB14,IF(AC26="Both",AB14-AB7,0))

            if OorK== 'None':
                self.DataCalculating['K2O'][i]=0
                self.DataCalculating['P2O5'][i]=0


            elif OorK== 'Orthoclase':
                self.DataCalculating['K2O'][i]=self.DataCalculating['K2O'][i]
                self.DataCalculating['P2O5'][i]=0


            elif OorK== 'K2SiO3':
                self.DataCalculating['P2O5'][i]=self.DataCalculating['K2O'][i]
                self.DataCalculating['K2O'][i]=0



            elif OorK== 'Both':

                self.DataCalculating['P2O5'][i]=self.DataCalculating['K2O'][i]-self.DataCalculating['Al2O3'][i]
                self.DataCalculating['K2O'][i]=self.DataCalculating['Al2O3'][i]

            self.DataCalculating['Al2O3'][i]-=self.DataCalculating['K2O'][i]


            #=IF(AC13>0,IF(AC7>=AC13,"Albite",IF(AC7>0,"Both","Na2SiO3")),"None")

            if self.DataCalculating['Na2O'][i]<=0:
                AorN='None'
            else:
                if self.DataCalculating['Al2O3'][i]>=self.DataCalculating['Na2O'][i]:
                    AorN='Albite'
                else:
                    if self.DataCalculating['Al2O3'][i]>0:
                        AorN='Both'
                    else:
                        AorN='Na2SiO3'


            #=IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)

            if self.DataCalculating['Al2O3'][i]>=self.DataCalculating['Na2O'][i] and self.DataCalculating['Al2O3'][i]>0:
                self.DataCalculating['Al2O3'][i]-=self.DataCalculating['Na2O'][i]
            else:
                self.DataCalculating['Al2O3'][i]=0


            #=IF(AD26="Albite",AC13,IF(AD26="Both",AC7,0))
            #=IF(AD26="Na2SiO3",AC13,IF(AD26="Both",AC13-AD13,0))


            if AorN =='Albite':
                self.DataCalculating['Cl'][i]=0

            elif AorN=='Both':
                self.DataCalculating['Cl'][i]=self.DataCalculating['Na2O'][i]-self.DataCalculating['Al2O3'][i]
                self.DataCalculating['Na2O'][i]=self.DataCalculating['Al2O3'][i]

            elif AorN =='Na2SiO3':
                self.DataCalculating['Cl'][i]=self.DataCalculating['Na2O'][i]
                self.DataCalculating['Na2O'][i]=0

            elif AorN =='None':
                self.DataCalculating['Na2O'][i]=0
                self.DataCalculating['Cl'][i]=0


            #=IF(AD7>0,IF(AD12>0,"Anorthite","None"),"None")

            """
            Seem like should be =IF(AD7>0,IF(AD12>AD7,"Anorthite","Corundum"),"None")

            If Al2O3 is left after alloting orthoclase and albite, then:
            Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
            If Al2O3 exceeds CaO in the preceding calculation, then:
            Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
            Corundum = Al2O3, CaO =0, Al2O3 = 0


                if self.DataCalculating['Al2O3'][i]<=0:
                    AorC='None'
                else:
                    if self.DataCalculating['CaO'][i]>self.DataCalculating['Al2O3'][i]:
                        AorC= 'Anorthite'
                    else:
                        Aorc='Corundum'

            """

            if self.DataCalculating['Al2O3'][i]<=0:
                AorC='None'
            else:
                if self.DataCalculating['CaO'][i]>0:
                    AorC= 'Anorthite'
                else:
                    Aorc='None'


            #=IF(AE26="Anorthite",IF(AD12>AD7,0,AD7-AD12),AD7)

            #=IF(AE26="Anorthite",IF(AD7>AD12,0,AD12-AD7),AD12)

            #=IF(AE26="Anorthite",IF(AD7>AD12,AD12,AD7),0)

            if AorC== 'Anorthite':
                if self.DataCalculating['Al2O3'][i]>=self.DataCalculating['CaO'][i]:
                    self.DataCalculating['Sr'][i] = self.DataCalculating['CaO'][i]
                    self.DataCalculating['Al2O3'][i]-=self.DataCalculating['CaO'][i]
                    self.DataCalculating['CaO'][i]=0

                else:
                    self.DataCalculating['Sr'][i]=self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['CaO'][i]-=self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['Al2O3'][i]=0

            else:
                self.DataCalculating['Sr'][i]=0

            Corundum=self.DataCalculating['Al2O3'][i]
            Anorthite=self.DataCalculating['Sr'][i]

            #=IF(AE10>0,IF(AE12>=AE10,"Sphene",IF(AE12>0,"Both","Rutile")),"None")

            if self.DataCalculating['MnO'][i]<=0:
                SorR='None'
            else:
                if self.DataCalculating['CaO'][i]>=self.DataCalculating['MnO'][i]:
                    SorR='Sphene'
                elif self.DataCalculating['CaO'][i]>0:
                    SorR='Both'
                else:
                    SorR='Rutile'


            #=IF(AF26="Sphene",AE10,IF(AF26="Both",AE12,0))

            #=IF(AF26="Rutile",AE10,IF(AF26="Both",AE10-AE12,0))

            if SorR=='Sphene':
                self.DataCalculating['MnO'][i]=self.DataCalculating['MnO'][i]
                self.DataCalculating['S'][i]=0

            elif SorR=='Rutile':
                self.DataCalculating['S'][i]=self.DataCalculating['MnO'][i]
                self.DataCalculating['MnO'][i]=0


            elif SorR=='Both':
                self.DataCalculating['S'][i]=self.DataCalculating['MnO'][i]-self.DataCalculating['CaO'][i]
                self.DataCalculating['MnO'][i]=self.DataCalculating['CaO'][i]

            elif SorR=='None':
                self.DataCalculating['MnO'][i]=0
                self.DataCalculating['S'][i]=0

            self.DataCalculating['CaO'][i]-=self.DataCalculating['MnO'][i]



            Rutile=self.DataCalculating['S'][i]

            #=IF(AND(AF20>0),IF(AF8>=AF20,"Acmite",IF(AF8>0,"Both","Na2SiO3")),"None")

            if self.DataCalculating['Cl'][i]<=0:
                ACorN='None'
            else:
                if self.DataCalculating['Fe2O3'][i]>=self.DataCalculating['Cl'][i]:
                    ACorN='Acmite'
                else:
                    if self.DataCalculating['Fe2O3'][i]>0:
                        ACorN='Both'
                    else:
                        ACorN='Na2SiO3'


            #=IF(AG26="Acmite",AF20,IF(AG26="Both",AF8,0))


            #=IF(AG26="Na2SiO3",AF20,IF(AG26="Both",AF20-AG19,0))

            if ACorN=='Acmite':
                self.DataCalculating['F'][i]=self.DataCalculating['Cl'][i]
                self.DataCalculating['Cl'][i]=0

            elif ACorN =='Na2SiO3':
                self.DataCalculating['Cl'][i]=self.DataCalculating['Cl'][i]
                self.DataCalculating['F'][i]=0

            elif ACorN=='Both':
                self.DataCalculating['F'][i]=self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Cl'][i]=self.DataCalculating['Cl'][i]-self.DataCalculating['F'][i]

            elif ACorN=='None':
                self.DataCalculating['F'][i]=0
                self.DataCalculating['Cl'][i]=0


            self.DataCalculating['Fe2O3'][i]-=self.DataCalculating['F'][i]

            Acmite=self.DataCalculating['F'][i]

            #=IF(AG8>0,IF(AG9>=AG8,"Magnetite",IF(AG9>0,"Both","Hematite")),"None")


            if self.DataCalculating['Fe2O3'][i]<=0:
                MorH='None'
            else:
                if self.DataCalculating['FeO'][i]>=self.DataCalculating['Fe2O3'][i]:
                    MorH='Magnetite'
                else:
                    if self.DataCalculating['FeO'][i]>0:
                        MorH='Both'
                    else:
                        MorH='Hematite'



            #=IF(AH26="Magnetite",AG8,IF(AH26="Both",AG9,0))
            #=IF(AH26="Hematite",AG8,IF(AH26="Both",AG8-AG9,0))



            if MorH=='Magnetite':
                self.DataCalculating['Fe2O3'][i]=self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Ba'][i]=0

            elif MorH== 'Hematite':
                self.DataCalculating['Fe2O3'][i]=0
                self.DataCalculating['Ba'][i]=self.DataCalculating['FeO'][i]


            elif MorH=='Both':
                self.DataCalculating['Fe2O3'][i]=self.DataCalculating['FeO'][i]
                self.DataCalculating['Ba'][i]= self.DataCalculating['Fe2O3'][i]-self.DataCalculating['FeO'][i]


            elif MorH=='None':
                self.DataCalculating['Fe2O3'][i]=0
                self.DataCalculating['Ba'][i]==0


            self.DataCalculating['FeO'][i]-=self.DataCalculating['Fe2O3'][i]

            Magnetite=self.DataCalculating['Fe2O3'][i]
            Hematite=self.DataCalculating['Ba'][i]



            # =IF(AH11>0,AH11/(AH11+AH9),0)

            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]

            if Mg > 0:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 100 * Mg / (Mg + Fe2)})
            else:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 0})




            self.DataCalculating['FeO'][i]+=self.DataCalculating['MgO'][i]

            self.DataCalculating['MgO'][i]=0


            #=IF(AI12>0,IF(AI9>=AI12,"Diopside",IF(AI9>0,"Both","Wollastonite")),"None")


            if self.DataCalculating['CaO'][i]<=0:
                DorW='None'
            else:
                if self.DataCalculating['FeO'][i]>=self.DataCalculating['CaO'][i]:
                    DorW='Diopside'
                else:
                    if self.DataCalculating['FeO'][i]>0:
                        DorW='Both'
                    else:
                        DorW='Wollastonite'


            #=IF(AJ26="Diopside",AI12,IF(AJ26="Both",AI9,0))

            #=IF(AJ26="Wollastonite",AI12,IF(AJ26="Both",AI12-AI9,0))



            if DorW =='Diopside':
                self.DataCalculating['CaO'][i]=self.DataCalculating['CaO'][i]
                self.DataCalculating['S'][i]=0

            elif DorW =='Wollastonite':
                self.DataCalculating['S'][i]=self.DataCalculating['CaO'][i]
                self.DataCalculating['CaO'][i]=0

            elif DorW =='Both':
                self.DataCalculating['S'][i]=self.DataCalculating['CaO'][i]-self.DataCalculating['FeO'][i]
                self.DataCalculating['CaO'][i]=self.DataCalculating['FeO'][i]

            elif DorW =='None':
                self.DataCalculating['CaO'][i]=0
                self.DataCalculating['S'][i]=0

            self.DataCalculating['FeO'][i]-=self.DataCalculating['CaO'][i]


            Diopside=self.DataCalculating['CaO'][i]

            Quartz=self.DataCalculating['SiO2'][i]

            Zircon= self.DataCalculating['Zr'][i]
            K2SiO3= self.DataCalculating['P2O5'][i]

            Na2SiO3=self.DataCalculating['Cl'][i]

            Sphene= self.DataCalculating['MnO'][i]

            Hypersthene= self.DataCalculating['FeO'][i]

            Albite= self.DataCalculating['Na2O'][i]

            Orthoclase= self.DataCalculating['K2O'][i]

            Wollastonite = self.DataCalculating['S'][i]

            #=AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)

            Quartz-=(Zircon+
                    K2SiO3+
                    Anorthite*2+
                    Na2SiO3+
                    Acmite*4+
                    Diopside*2+
                    Sphene+
                    Hypersthene+
                    Albite*6+
                    Orthoclase*6+
                    Wollastonite)

            #=IF(AL5>0,AL5,0)

            if Quartz>0:
                Quartz=Quartz
            else:Quartz=0


            #=IF(AL13>0,IF(AL5>=0,"Hypersthene",IF(AL13+(2*AL5)>0,"Both","Olivine")),"None")

            if Hypersthene<=0:
                HorO='None'
            else:
                if Quartz>=0:
                    HorO='Hypersthene'
                else:
                    if Hypersthene+2*Quartz>0:
                        HorO='Both'
                    else:
                        HorO='Olivine'





            #=IF(AN26="Hypersthene",AL13,IF(AN26="Both",AL13+(2*AL5),0))
            #=IF(AN26="Olivine",AL13*0.5,IF(AN26="Both",ABS(AL5),0))
            Old_Hypersthene=Hypersthene
            if HorO=='Hypersthene':
                Hypersthene=Hypersthene
                Olivine=0

            elif HorO=='Both':
                Hypersthene=Hypersthene+Quartz*2
                Olivine=abs(Quartz)

            elif HorO=='Olivine':
                Olivine=Hypersthene/2
                Hypersthene=0

            elif HorO=='None':
                Hypersthene=0
                Olivine=0


            #=AL5+AL13-(AN13+AN17)
            Quartz+= Old_Hypersthene-(Hypersthene+Olivine)


            #=IF(AL12>0,IF(AN5>=0,"Sphene",IF(AL12+AN5>0,"Both","Perovskite")),"None")

            if Sphene<=0:
                SorP='None'
            else:
                if Quartz>=0:
                    SorP='Sphene'
                else:
                    if Sphene+Quartz>0:
                        SorP='Both'
                    else:
                        SorP='Perovskite'


            #=IF(AO26="Sphene",AL12,IF(AO26="Both",AL12+AN5,0))
            #=IF(AO26="Perovskite",AL12,IF(AO26="Both",AL12-AO12,0))

            Old_Sphene=Sphene

            if SorP=='Sphene':
                Sphene=Sphene
                Perovskite=0

            elif SorP=='Perovskite' :
                Perovskite=Sphene
                Sphene=0

            elif SorP=='Both' :
                Sphene+=Quartz
                Perovskite=Old_Sphene-Sphene

            elif SorP=='None' :
                Sphene=0
                Perovskite=0

            Quartz+=Old_Sphene-Sphene


            #=IF(AL14>0,IF(AO5>=0,"Albite",IF(AL14+(AO5/4)>0,"Both","Nepheline")),"None")


            if Albite<=0:
                AlorNe='None'
            else:
                if Quartz>=0:
                    AlorNe='Albite'
                else:
                    if Albite+(Quartz/4)>0:
                        AlorNe='Both'
                    else:
                        AlorNe='Nepheline'

            #=AO5+(6*AL14)-(AP14*6)-(AP19*2)


            #=IF(AP26="Albite",AL14,IF(AP26="Both",AL14+(AO5/4),0))
            #=IF(AP26="Nepheline",AL14,IF(AP26="Both",AL14-AP14,0))


            Old_Albite=Albite

            if AlorNe=='Albite':
                Albite=Albite
                Nepheline=0

            elif AlorNe=='Nepheline':
                Nepheline=Albite
                Albite=0

            elif AlorNe=='Both':
                Albite+=Quartz/4
                Nepheline=Old_Albite-Albite

            elif AlorNe=='None':
                Nepheline=0
                Albite=0


            Quartz+=(6*Old_Albite)-(Albite*6)-(Nepheline*2)

            # =IF(AL8=0,0,AL8/(AL8+(AP14*2)))

            if Anorthite == 0:
                self.DataCalced[k].update({'Plagioclase An content': 0})
            else:
                self.DataCalced[k].update({'Plagioclase An content': 100 * Anorthite / (Anorthite + 2 * Albite)})

            #=IF(AL15>0,IF(AP5>=0,"Orthoclase",IF(AL15+(AP5/2)>0,"Both","Leucite")),"None")

            if Orthoclase<=0:
                OorL='None'
            else:
                if Quartz>=0:
                    OorL='Orthoclase'
                else:
                    if Orthoclase+Quartz/2>0:
                        OorL='Both'
                    else:
                        OorL='Leucite'

            #=IF(AQ26="Orthoclase",AL15,IF(AQ26="Both",AL15+(AP5/2),0))
            #=IF(AQ26="Leucite",AL15,IF(AQ26="Both",AL15-AQ15,0))

            Old_Orthoclase=Orthoclase

            if OorL =='Orthoclase':
                Orthoclase=Orthoclase
                Leucite=0

            elif OorL =='Leucite':
                Leucite=Orthoclase
                Orthoclase=0

            elif OorL =='Both':
                Orthoclase+=Quartz/2
                Leucite=Old_Orthoclase-Orthoclase

            elif OorL =='None':
                Orthoclase=0
                Leucite=0


            #=AP5+(AL15*6)-(AQ15*6)-(AQ20*4)

            Quartz+=(Old_Orthoclase*6)-(Orthoclase*6)-(Leucite*4)



            #=IF(AL16>0,IF(AQ5>=0,"Wollastonite",IF(AL16+(AQ5*2)>0,"Both","Larnite")),"None")
            if Wollastonite<=0:
                WorB='None'
            else:
                if Quartz>=0:
                    WorB='Wollastonite'
                else:
                    if Wollastonite + Quartz/2 >0:
                        WorB='Both'
                    else:
                        WorB='Larnite'


            #=IF(AR26="Wollastonite",AL16,IF(AR26="Both",AL16+(2*AQ5),0))
            #=IF(AR26="Larnite",AL16/2,IF(AR26="Both",(AL16-AR16)/2,0))

            Old_Wollastonite=Wollastonite
            if WorB=='Wollastonite':
                Wollastonite=Wollastonite
                Larnite=0

            elif WorB=='Larnite':
                Larnite=Wollastonite/2
                Wollastonite=0

            elif WorB=='Both':
                Wollastonite+=Quartz*2
                Larnite=(Old_Wollastonite-Wollastonite)/2

            elif WorB=='None':
                Wollastonite=0
                Larnite=0


            #=AQ5+AL16-AR16-AR21
            Quartz+=Old_Wollastonite-Wollastonite-Larnite

            #=IF(AL11>0,IF(AR5>=0,"Diopside",IF(AL11+AR5>0,"Both","LarniteOlivine")),"None")

            if Diopside<=0:
                DorL='None'
            else:
                if Quartz>=0:
                    DorL='Diopside'
                else:
                    if Diopside+Quartz>0:
                        DorL='Both'
                    else:
                        DorL='LarniteOlivine'



            #=IF(AS26="Diopside",AL11,IF(AS26="Both",AL11+AR5,0))
            #=(IF(AS26="LarniteOlivine",AL11/2,IF(AS26="Both",(AL11-AS11)/2,0)))+AN17
            #=(IF(AS26="LarniteOlivine",AL11/2,IF(AS26="Both",(AL11-AS11)/2,0)))+AR21

            Old_Diopside=Diopside
            Old_Larnite=Larnite
            Old_Olivine=Olivine
            if DorL=='Diopside':
                Diopside=Diopside



            elif DorL=='LarniteOlivine':
                Larnite+=Diopside/2
                Olivine+=Diopside/2
                Diopside=0

            elif DorL=='Both':
                Diopside+=Quartz
                Larnite+=Old_Diopside-Diopside
                Olivine+=Old_Diopside-Diopside



            elif DorL=='None':
                Diopside=0

            #=AR5+(AL11*2)+AN17+AR21-AS21-(AS11*2)-AS17
            Quartz+=(Old_Diopside*2)+Old_Olivine+Old_Larnite-Larnite-(Diopside*2)-Olivine


            #=IF(AQ20>0,IF(AS5>=0,"Leucite",IF(AQ20+(AS5/2)>0,"Both","Kalsilite")),"None")

            if Leucite<=0:
                LorK='None'
            else:
                if Quartz>=0:
                    LorK='Leucite'
                else:
                    if Leucite+Quartz/2>0:
                        LorK='Both'
                    else:
                        LorK='Kalsilite'



            #=IF(AT26="Leucite",AQ20,IF(AT26="Both",AQ20+(AS5/2),0))
            #=IF(AT26="Kalsilite",AQ20,IF(AT26="Both",AQ20-AT20,0))


            Old_Leucite=Leucite

            if LorK=='Leucite':
                Leucite=Leucite
                Kalsilite=0

            elif LorK=='Kalsilite':
                Kalsilite=Leucite
                Leucite=0

            elif LorK=='Both':
                Leucite+=Quartz/2
                Kalsilite=Old_Leucite-Leucite

            elif LorK=='None':
                Leucite=0
                Kalsilite=0


            #=AS5+(AQ20*4)-(AT20*4)-(AT22*2)
            Quartz+=Old_Leucite*4-Leucite*4-Kalsilite*2


            for i in self.Minerals:
                exec('self.DataResult[k].update({\"'+i+'\":'+i+'}) ')
                exec('self.DataWeight[k].update({\"'+i+'\":'+i+'*self.DataBase[\"'+i+'\"][0]}) ')
                exec('self.DataVolume[k].update({\"'+i+'\":'+i+'*self.DataBase[\"'+i+'\"][0]/self.DataBase[\"'+i+'\"][1]}) ')

            self.DI = 0
            for i in ['Quartz', 'Anorthite', 'Albite', 'Orthoclase', 'Nepheline', 'Leucite', 'Kalsilite']:
                exec('self.DI+=' + i + '*self.DataBase[\"' + i + '\"][0]')

            self.DataCalced[k].update({'Differentiation Index': self.DI})

    def WriteData(self,target='DataResult'):
        DataToWrite=[]
        TMP_DataToWrite=['Samples']
        for j in self.Minerals:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite=[]
            k=self.raw.at[i,'Label']
            TMP_DataToWrite=[k]
            for j in self.Minerals:
                command='TMP_DataToWrite.append(str(self.'+target+'[k][j]))'
                exec(command)
            DataToWrite.append(TMP_DataToWrite)
        Tool().ToCsv(name= self.name[0:-5]+'_'+target[4:]+'_CIPW.csv', DataToWrite=DataToWrite)


    def WriteCalced(self,target='DataCalced'):
        DataToWrite=[]
        TMP_DataToWrite=['Samples']
        for j in self.Calced:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite=[]
            k=self.raw.at[i,'Label']
            TMP_DataToWrite=[k]
            for j in self.Calced:
                command='TMP_DataToWrite.append(str(self.'+target+'[k][j]))'
                exec(command)
            DataToWrite.append(TMP_DataToWrite)
        Tool().ToCsv(name= self.name[0:-5]+'_'+target[4:]+'_CIPW.csv', DataToWrite=DataToWrite)


    def read(self):
        self.WriteData(target='DataResult')
        self.WriteData(target='DataWeight')
        self.WriteData(target='DataVolume')
        self.WriteCalced(target='DataCalced')

if __name__ == '__main__':
    CIPW().read()

"""
    Tas().read()
    Ree().read()
    Trace().read()
    Qfl().read()
    Qmflt().read()
    QapfP().read()
    QapfV().read()
    Polar().read()
    Pearce().read()
    Harker().read()
    Harker(x='SiO2', y=['CaO', 'Na2O', 'TiO2', 'K2O', 'P2O5']).read()
    MultiBallard().read()
"""

