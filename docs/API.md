Title: Temperary API Ref of GeoPython
Date: 2017-3-18 16:20
Category: Python


# API Ref of GeoPython



created on Sat Dec 17 22:28:24 2016
@author: cycleuser
Create Date: 2015-07-13
Modify Date: 2017-04-10
a tool set for daily geology related task.
# prerequisite:
   based on Python 3.x
   need math,numpy,pandas,matplotlib,xlrd,chempy

# Simple Sample:
    1) opern a ipython console
    2) import geopython as gp
    3) TasSample= Tas("tas.xlsx")
    4) TasSample.read()
    5) from geopython import gui
    6) gui.Show()

# Geology related classes available:
    1) Tas
    2) Ree
    3) Trace & Trace2 (with different sequence of trace elements)
    4) Qfl & Qmflt & Qapf
    5) Polar (projection of wulf net & schmidt net)
    6) Harker diagram
    7) CIPW Norm calculation
    8) Zircon Ce4/Ce3 calculation (Ballard 2002)


# know issues:
    1) Only work on Python 3.x

# Other

Any issues or improvements please open an issue at [here](https://github.com/chinageology/GeoPython/issues)
or leave a message to [our website](http://geopython.com)





## DualTri



	a class of a double triangulars frame



Label: the label at the tree corners of the triangular

>type:    Label: a list consist of three strings




LabelPosition: just the Position of these Labels

>type:    LabelPosition: x-y style coords , three of them




Labels: description of the different region

>type:    Labels: a list containing multiple strings




Locations: the locations of those each one in the Labels

>type:    Locations: a list of triangular coord points




Offset: the offset value used to adjust the appearance of each one in the Labels

>type:    Offset: a list of x-y coord offset values




name: the file name used to read and use

>type:    name: a string






### __init__(self, name=['Q', 'A', 'P', 'F'], Label=qapf.xlsx)



	Initialize self.  See help(type(self)) for accurate signature.



### show(self)





## Frame



	a Frame of TAS, REE, Trace Elements and other similar x-y plots



Width,Height: the width and height of the generated figure

>type:    Width,Height: two int numbers




Dpi: dots per inch

>type:    Dpi: an int number




Left,Right: the left and right limit of X axis

>type:    Left,Right: two int numbers




Base,Top: the left and right limit of Y axis

>type:    Base,Top: two int numbers




X0,X1,X_Gap: the left and right limit of X label, and the numbers of gap between them

>type:    X0,X1,X_Gap: three int numbers




Y0,Y1,Y_Gap: the left and right limit of Y label, and the numbers of gap between them

>type:    Y0,Y1,Y_Gap: three int numbers




FontSize: size of font of labels

>type:    FontSize: an int number




xLabel, yLabel: the labels put alongside with x and y axises

>type:    xLabel, yLabel: two strings




### __init__(self, Width=Y Label, Height=X Label, Dpi=16, Left=7, Right=60, X_Gap=0, Base=9, Top=80, Y_Gap=0, FontSize=80, xLabel=6, yLabel=8)



	Just set up all.



### show(self)



Use the setup to set up figure feature.



## Line



	a line class



Begin: the Beginning point of the line

>type:    Begin: a Point Instance




End: the End point of the line

>type:    End: a Point Instance




Points: gathering all the Point Instances

>type:    Points: a list




X,Y: the gathered x and y values of the line to use in plotting

>type:    X,Y: two lists containing float numbers




Width: the width of the line

>type:    Width: an int number , mayby float is OK




Color: the color of the Line to draw on canvas

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white




Style: the style used for the Line

>type:    Style: a string; -, --,-., : maybe there would be some other types , from matplotlib




Alpha: the transparency of the Point

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




Label: label of the Line, telling what it is and distinguish it from other lines

>type:    Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas




Sort: the sequence used for sorting the points consisting the line

>type:    Sort: a string, x means sort the points with their x values, y means use y instead of x, other means use the sequence of points as these points  are put to the line




### __init__(self, Points=, Sort=0.3, Width=-, Color=blue, Style=1, Alpha=, Label=[(0, 0), (1, 1)])



	setup the datas



### order(self, TMP=[])







### sequence(self)



sort the points in the line with given option



### show(self)



draw the line on canvas with its setup



## Point



a Point class

X,Y: the values of its x-y coord

>type:    X,Y: two float numbers


Location: gather X and Y as a tuple for further use

>type:    Location: just a tuple with two numbers


Size: the size of the Point to draw on canvas

>type:    Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small


Color: the color of the Point to draw on canvas

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency of the Point

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent


Marker: the marker used for the Point

>type:    Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib


Label: label of the Point, telling what it is and distinguish it from other points

>type:    Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas




### __init__(self, X=, Y=o, Size=0.3, Color=red, Alpha=12, Marker=0, Label=0)



just set up the values



### show(self)



plot the Point to the canvas



## Points



a class for multiple Points

X,Y: the values of its x-y coords

>type:    X,Y: two lists consist of float numbers


Size: the size of the Points to draw on canvas

>type:    Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small


Color: the color of the Points to draw on canvas

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency of the Points

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent


Marker: the marker used for the Points

>type:    Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib


Label: label of the Points, telling what they are and distinguish them from other points

>type:    Label: a string , if leave as "" or '' such kind of blank string, the label will not show on canvas




### __init__(self, points=8, Size=, Color=o, Alpha=0.3, Marker=red, Label=12, FontSize=[(0, 0), (0, 1)])



just set up the values



### show(self)



plot the Point to the canvas



## Polar



Polar Stereographic projection for structural data

name: the file used to plot

>type:    name: a string




### __init__(self, name=['N', 'S', 'W', 'E'], Label=strike.xlsx)



Initialize self.  See help(type(self)) for accurate signature.



### eqan(self, A)







### eqar(self, A)







### getangular(self, A, B, C)







### read(self)







### schmidt(self, Width=k, Color=1)



read the Excel, then draw the schmidt net and Plot points, job done~



### wulf(self, Width=k, Color=1)



read the Excel, then draw the wulf net and Plot points, job done~



## Qapf



inherit DualTri and Tool, read xlsx or csv file and make basic Qapf diagram

Tags: the Tags on this diagram for description of different units

>type:    Tags: a list of strings


Labels: the labels of the different units

>type:    Labels: a list of strings


Locations: the triangular coord location of these Labels

>type:    Locations: a list of tuples, these tuples contains the triangular coords


Offset: the x-y offset of these labels on canvas

>type:    Offset: a list of tuples containing x-y values




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, name=10, Label=['Q', 'A', 'P', 'F'], FontSize=qapf.xlsx)



Initialize self.  See help(type(self)) for accurate signature.



### draw(self)







### lowtri(self)







### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)







### uptri(self)







## QapfP



inherit Qapf, read xlsx or csv file and make Qapf diagram for Plutonic Rocks

Tags: the Tags on this diagram for description of different units

>type:    Tags: a list of strings


Labels: the labels of the different units

>type:    Labels: a list of strings


Locations: the triangular coord location of these Labels

>type:    Locations: a list of tuples, these tuples contains the triangular coords


Offset: the x-y offset of these labels on canvas

>type:    Offset: a list of tuples containing x-y values




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, name=10, Label=['Q', 'A', 'P', 'F'], FontSize=qapf.xlsx)



Initialize self.  See help(type(self)) for accurate signature.



### draw(self)







### lowtri(self)







### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)







### uptri(self)







## QapfV



inherit Qapf, read xlsx or csv file and make Qapf diagram for Volcanic rocks

Tags: the Tags on this diagram for description of different units

>type:    Tags: a list of strings


Labels: the labels of the different units

>type:    Labels: a list of strings


Locations: the triangular coord location of these Labels

>type:    Locations: a list of tuples, these tuples contains the triangular coords


Offset: the x-y offset of these labels on canvas

>type:    Offset: a list of tuples containing x-y values




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, name=10, Label=['Q', 'A', 'P', 'F'], FontSize=qapf.xlsx)



Initialize self.  See help(type(self)) for accurate signature.



### draw(self)







### lowtri(self)







### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)







### uptri(self)







## Qfl



inherit Tri and Tool, read xlsx or csv file and make QFL diagram

Tags: the Tags on this diagram for description of different units

>type:    Tags: a list of strings


Labels: the labels of the different units

>type:    Labels: a list of strings


Locations: the triangular coord location of these Labels

>type:    Locations: a list of tuples, these tuples contains the triangular coords


Offset: the x-y offset of these labels on canvas

>type:    Offset: a list of tuples containing x-y values




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, name=['Q', 'F', 'L'], Label=qfl.xlsx)



set up the values



### draw(self)



use the values to set up the general frame and lines, fill particular zone with given colors



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



just show the triangular frame on the canvas



## Qmflt



inherit Qfl and Tool, read xlsx or csv file and make Qmflt diagram

Tags: the Tags on this diagram for description of different units

>type:    Tags: a list of strings


Labels: the labels of the different units

>type:    Labels: a list of strings


Locations: the triangular coord location of these Labels

>type:    Locations: a list of tuples, these tuples contains the triangular coords


Offset: the x-y offset of these labels on canvas

>type:    Offset: a list of tuples containing x-y values




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, name=['Qm', 'F', 'Lt'], Label=qmflt.xlsx)



set up the values



### draw(self)



use the values to set up the general frame and lines, fill particular zone with given colors



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



just show the triangular frame on the canvas



## Ree



inherit Frame, read xlsx or csv file and use the Rare Earth Elements to plot the ree diagram

Element: the elements used in this diagram

>type:    Element: a list of strings


Labels: a ref of Element

>type:    Labels: a list of strings


WholeData: gathering all data and find the min and max of the data file to set the limits of Y

>type:    WholeData: a list of float numbers


X0,X1: the left and right limits of X

>type:    X0,X1: two int or float numbers


X_Gap: the space between the left and right limits of X

>type:    X_Gap: an int number


name: the file name to use in this diagram

>type:    name: a string




### __init__(self, name=, Width=$REE-Standardlized-Pattern$, Height=16, Dpi=5, Left=3, Right=-1, X0=6, X1=-1, X_Gap=15, Base=15, Top=1, Y0=16, Y1=0, Y_Gap=80, FontSize=6, xLabel=8, yLabel=ree.xlsx)



Just set up all.



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



set the figure basic with the settings



## Tag



a class for Tag put on canvas

Label: label of the Tag, telling what it is and distinguish them from other tags

>type:    Label: a strings , if leave as "" or '' such kind of blank string, the label will not show on canvas


Location: the location of the Tag

>type:    Location: a tuple consist of x-y values of its coords


X_offset,Y_offset: the values of its x-y offsets on coords

>type:    X_offset,Y_offset: two float numbers


FontSize: the size of font of the Tag

>type:    FontSize: a number , int or maybe float also OK , better around 8 to 12, not too large or too small




### __init__(self, Label=12, Location=3, X_offset=-6, Y_offset=(0, 0), FontSize=Label)



set up the values



### show(self)



show the Tag on canvas with its offsets and font size, color and alpha are fixed for now



## Tas



inherit Frame, read xlsx or csv file and use SiO2 , Na2O and K2O to plot tas diagram

Lines: the lines consisting the Tas frame

>type:    Lines: a list of lines


Tags: tags used for the items of Tas diagram

>type:    Tagas: a list of strings


Labels: labels on the canvas

>type:    Labels: a list of strings


Locations: the locations of these labels

>type:    Locations: a list of tuple containing two numbers as x-y coords


description: the description of the tas diagram

name: the file name used for tas diagram

>type:    name: a string




### __init__(self, name=$na_2O + K_2O wt\%$, Width=$SiO_2 wt\%$, Height=12, Dpi=15, Left=15, Right=1, X0=16, X1=0, X_Gap=11, Base=77, Top=37, Y0=79, Y1=35, Y_Gap=80, FontSize=6, xLabel=8, yLabel=tas.xlsx)



just set up the basic settings



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



show the tas frame and lines of tas on canvas



## Tool



a tool set for basic tasks, crosspoint calc, coord transfer and fill region with color



### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



## Trace



inherit Frame, read xlsx or csv file and use the Trace Elements to plot the trace diagram

Element: the elements used in this diagram

>type:    Element: a list of strings


Labels: a ref of Element

>type:    Labels: a list of strings


name: the file name to use in this diagram

>type:    name: a string




### __init__(self, name=, Width=$Trace-Elements-Standardlized-Pattern$, Height=16, Dpi=5, Left=3, Right=-1, X0=6, X1=-1, X_Gap=15, Base=37, Top=1, Y0=16, Y1=0, Y_Gap=80, FontSize=9, xLabel=16, yLabel=trace.xlsx)



Just set up all.



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



set the figure basic with the settings



## Trace2



inherit Frame, read xlsx or csv file and use the Trace Elements to plot the trace2 diagram

Element: the elements used in this diagram

>type:    Element: a list of strings


Labels: a ref of Element

>type:    Labels: a list of strings


name: the file name to use in this diagram

>type:    name: a string




### __init__(self, name=, Width=$Trace-Elements-Standardlized-Pattern$, Height=16, Dpi=5, Left=3, Right=-1, X0=6, X1=-1, X_Gap=25, Base=26, Top=1, Y0=16, Y1=0, Y_Gap=80, FontSize=9, xLabel=16, yLabel=trace2.xlsx)



Just set up all.



### read(self)



read the Excel, then use self.show() to show the frame, then Plot points, job done~



### show(self)



set the figure basic with the settings



## Tri



a class of triangular frame

Label: the label at the tree corners of the triangular

>type:    Label: a list consist of three strings


LabelPosition: just the Position of these Labels

>type:    LabelPosition: x-y style coords , three of them




### __init__(self, Label=['Q', 'F', 'L'])



set up the values



### show(self)



just show the triangular frame on the canvas



## TriLine



inherit Line and Tool, line class for triangular coord

x,y,z: the list for gathering the x,y,z values of points consisting the line

>type:    x,y,z: three lists




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, Points=, Sort=0.3, Width=-, Color=blue, Style=1, Alpha=, Label=[(0, 0, 0), (1, 1, 1)])



setup the datas



### order(self, TMP=[])







### sequence(self)



sort the points in the line with given option



### show(self)



draw the line on canvas with its setup



### tritrans(self)







## TriPoint



inherit Point and Tool, a Point class for triangular coord

x,y,z: the list for gathering the x,y,z values of points consisting the line

>type:    x,y,z: three lists


sum: a value used in calc of coord transfer

>type:    sum: just a number, both int or float are OK




### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, P=, Size=o, Color=0.3, Alpha=red, Marker=12, Label=(10, 20, 70))



just set up the values



### show(self)



plot the Point to the canvas



## TriTag



inherit Tag and Tool,a Tag for triangular coord



### BinToTri(self, a, b)



Turn an a-b coord to an x-y-z triangular coord .

if z is negative, calc with its abs then return (a, -b).

a,b: the numbers of the a-b coord

>type:    a,b: float or double are both OK, just numbers


return:  the corresponding x-y-z triangular coord

teturn type :      a tuple consist of x,y,z



### Cross(self, A=[(0, 10), (100, 0)], B=[(0, 0), (10, 10)])



Return the crosspoint of two line A and B.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return: the crosspoint of A and B

teturn type :    a list consist of two numbers, the x-y of the crosspoint



### Fill(self, P=0.3, Color=blue, Alpha=[(100, 0), (85, 15), (0, 3)])



Fill a region in planimetric rectangular coord.

P: the peak points of the region in planimetric rectangular coord

>type:    P: a list consist of at least three tuples, which are the points in planimetric rectangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriCross(self, A=[(50, 50, 0), (0, 0, 100)], B=[(100, 0, 0), (0, 50, 60)])



Return the crosspoint of two line A and B in triangular coord.

A: first line

>type:    A: a list consist of two tuples, beginning and end point of the line


B: second line

>type:    B: a list consist of two tuples, beginning and end point of the line


return:  the crosspoint of A and B

teturn type :      a list consist of three numbers, the x-y-z of the triangular coord



### TriFill(self, P=0.3, Color=blue, Alpha=[(100, 0, 0), (85, 15, 0), (0, 3, 97)])



 Fill a region in triangular coord.

P: the peak points of the region in triangular coord

>type:    P: a list consist of at least three tuples, which are the points in triangular coord


Color: the color used to fill the region

>type:    Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white


Alpha: the transparency used to fill the region

>type:    Alpha: a float number from 0 to 1, higher darker, lower more transparent




### TriToBin(self, x, y, z)



Turn an x-y-z triangular coord to an a-b coord.

if z is negative, calc with its abs then return (a, -b).

x,y,z: the three numbers of the triangular coord

>type:    x,y,z: float or double are both OK, just numbers


return:  the corresponding a-b coord

teturn type :      a tuple consist of a and b



### __init__(self, Label=12, Location=3, X_offset=-6, Y_offset=(0, 1, 2), FontSize=Label)



set up the values, transfer x,y,z coords to x-y coords



### show(self)



show the Tag on canvas with its offsets and font size, color and alpha are fixed for now


