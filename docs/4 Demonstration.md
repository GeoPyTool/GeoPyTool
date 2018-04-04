Title: Demonstration
Date: 2018-04-04 11:46
Category: Doc
Tags: Doc,English


## Demonstration of the Functions


## Open and Import Data
To start a plot or calculation, raw data file should be imported to GeoPyTool first.

![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/01.ImportData.png?raw=true)


The Data file can be Xlsx/Xls or CSV.
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/ChooseAndImport.png)

## Set Up Data

If there is no setting up information such as the 'Label'/'Color'/'Marker'/'Style'/'Alpha'/'Width', you need to click on the Set Format button to add these items and make modification by yourself.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/SetDataUp.png)

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/SettingDataUp.png)

## Data Setting Details

As shown in the [Data File Samples](https://github.com/GeoPyTool/GeoPyTool/tree/master/DataFileSamples), all data files contain the following Items:

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/images/SettingArea.png)

1. 'Label': control the group of sample and will be shown on legend
2. 'Color': control the 'Color' of both drawn line and plotted point
3. 'Marker': control the points shape
4. 'Size': control the points 'Size'
5. 'Width': control the line 'Width'
6. 'Style': control the line shape
7. 'Alpha': control the transparency of both drawn line and plotted point

'Label' can be set to any character，word or phrase.
'Color' can only be chosen from following words: 'blue','green','red','cyan','magenta','yellow','black','white','grey'.
'Size', 'Width', and 'Alpha' are number values. The unit used for 'Size' and 'Width' is pt. 'Size' normally should be larger than '10', and 'Width' usually is '1'. 'Alpha' can be set from '0' to '1', for example, setting 'Alpha' as '0.4' means 40% transparency.
'Marker' and 'Style', these two are slightly more complicated and can be set as the contents of the following lists.

'Marker' :
![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/MarkerList.png?raw=true)

'Style':
![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/StyleList.png?raw=true)

The effect of setting:
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/images/SettingEffect.png)


## Click the Function you need

After setting up, you can just click to use the function you need.
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/ClickOnTheFunction.png)

## TAS/REE/Trace Elements

These functions are quite commonly used and the details are shown as the picture below.

![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/02.Save%20Image.png?raw=true)

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/TAS-REE-Trace.png)


## Pearce Diagram

Pearce Diagram just use some trace elements and is also quite easy to know how to use.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/Pearce.png)

## Harker Diagram

Harker Diagram is a little bit complicated. Both the X and Y items used for the picture can be selectable by the slider.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/Harker.png)

## QFL and QmFLt

These two diagrams are very easy. But you must find the right data file used for them to import.
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/ImportQFL.png)

Remind to set up data, then you can run these two functions.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/QFLandQmFLt.png)

## Stereographic Projection and Rose Map

Wulf or Schmidt Net can be chosen, and so is to use Lines or Points on the generated diagram.
In the Rose Map function, all data in one data files can be treated as a single group of data to draw Rose Map, and can also be treated as seperated teams to compare the Rose Map from each other. The step of the Rose Map can be set by slider. And so does the items chosen to use in the Rose Map. Dip/Dip-Angle/Strike are all available.

Notice that the first Letters must be in UPPER case.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/StereoAndRose.png)

## Zircon Ce4/3 Ratio Calculation

The data file used here is quite complicated. Please follow the guidance shown in the picture below.

In the template data file for this calculation, the row with the **Base** symbol needs to be filled with the bulk REE data, and the **zircon** rows and **'Label'** column is where the REE data is input. The **Zr** value for zircon should be set as the **“constant”** **497555**. The **“use”** row tells the program to use the data in the row in the calculation if set as yes or excluded if set at no, but all of the data will be plotted on the graph generated. The Ri and Ro values are from Ballard et al. (2002) where La is set as No as the default setting, because of the anomaly of La in their data.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/ZriconCeCalculation.png)


## Zircon and Rutile Thermometer

These two function are super easy. Notice the ASiO2 and ATiO2 here are the Activity of these two components.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/Thermometer.png)




## User Defined X-Y plot

This function allows users to load any picture from any articles as a base map to plot on.

But you must understand the original plot first and know the mathematical setting of it. So you can set up the right format in your plot.

For example, as the picture below shown,  the original diagram used Nb and Th, normalized by N-MORB(Sun and McDonough 1989), and then used the Log function of these two items. So we do the same setting up as shown by the picture. The Left/Right/Down/Up limit of the original diagram are 0.01/100/0.01/1000, so we need to use the Log function and find out that we should set the Left/Right/Down/Up limit to be -2/2/-2/3. If you can not understand why, please take a rest and good bye.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/UserDefinedXY.png)

![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/03.LoadBaseMap.png?raw=true)


## 3D and Statistics
![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/04.Statistical.png?raw=true)


## Cluster

![](https://github.com/GeoPyTool/GeoPyTool/blob/master/images/05.Cluster.png?raw=true)




