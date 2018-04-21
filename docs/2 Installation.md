Title: Installation
Date: 2018-04-21 11:27:50
Category: English
Tags: Doc,English,Support

# Installation, Easy Way 

GeoPyTool can be used as a module inside Python, and can also run as a standalone application.



## Standalone Application （Recommended！）

Packed up executable files are provided for Windows and MacOS platform.


[Click here to get Download links.](https://github.com/GeoPyTool/GeoPyTool/blob/master/Download.md)
Unzip the zip and keep all components there. Make sure that the whole unzipped folder is under an English path.

### Mac APP

On macOS, everything is extremely easy to use GeoPyTool. Just download and unzip the file, then double click on the GeoPyTool.app file, you will find the APP available as the following picture shows.

![User Interface of the APP on macOS.](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/MacOSScreenShot.png)



### Windows Pack

#### Windows 8/8.1/10 Users

On these modern Windows platforms, everything is also extremely easy to use GeoPyTool. Just download and unzip the file, then double click on the **Rungeopytool.bat** file, and make sure that you don't delete any file form the unziped folder because they are all required by the program, then you will find the APP available as the following picture shows.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/RunWin.jpg)

![User Interface of the EXE on Windows.](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/ScreenShot.png)

#### Windows 7 Users

Of corse, you must find that the screen shot above is actrually from a Windows 7  virtual machine.

That's right, you can obviously use GeoPyTool on Windows 7, on which some system patches need to be installed. You need to install the SP1 of Windows and then install KB2999226 and the `Visual C++ Redistributable 2015`. If you are using Windows 7 without the SP1 package installed, there might comes an`api-ms-win-crt`related error. So believe me my friend, just install these patched below, they won't harm you after all.

The SP1 package of Windows 7 can be found at [here, the official website of MicroSoft](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1).

The installation packages of KB2999226 and the `Visual C++ Redistributable 2015` are already contained in the Zip file of GeoPyTool for Windows, and can also be found here: [32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)，[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW).
I am really a sweet guy, isn't it?
So if you encounter any `api-ms-win-crt`related errors, please check those installations first.

#### Windows XP or Vista Users

I failed many times on both XP and Vista, and I think there might not be a lot users of these two antique systems.
If you are using one or both of them, please be good to yourself to update you old PC to at least Windows 7 SP1 or try Linux on your antique computers. My advice is that we should not waste our life on those systems that are not even supported by their developers and manufacturer. So, if you still want to run GeoPyTool on those two old systems, good luck and good bye.


## Update

### Mac APP Update

Go to the location inside the app file, `GeoPyTool.app/Contents/Resources/UpDateGeoPytool`.Double click on this file neamed UpDateGeoPytool at `GeoPyTool.app/Contents/Resources/`. It will update the GeoPyTool inside your GeoPyTool.app file. Remember that never modify any files directly under the same folder unless you are an expert on dealing with Python.

![Update the APP on macOS.](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/OSXUpdate.png)

### Windows Bat Update

Double click on the  **Update.bat** file to run update. It will update the GeoPyTool inside your GeoPyTool folder. Remember that never modify any files directly under the same folder unless you are an expert on dealing with Python.


![Update the EXE on Windows.](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/WinUpdate.png)


## Marker/Color/Style

All these details in GeoPyTool are the same as those in Matplotlib becasue that is what GeoPyTool used to visualize data.

Markers of Points can be reffered from here:
http://matplotlib.org/api/markers_api.html

Colors can be reffered from here:
http://matplotlib.org/api/colors_api.html

Here is a picture of Line Styles and Point Markers form [nrougier](http://www.labri.fr/perso/nrougier/teaching/matplotlib/):

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/LIneStylesMarkers.png)


## Need Further Help?

Visit our BBS https://github.com/GeoPyTool/GeoPyTool/issues and write a post to describe your problems in detail. We will response as soon as we can.


## Appendix


The New Zircon Ce function need Data template file named as [ZirconCe.xlsx](https://github.com/GeoPyTool/GeoPyTool/blob/master/DataFileSamples/ZirconCe.xlsx)

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/NewZirconCe.png)


The New  TAS, REE and Trace Elements functions share a same Data template files:
[Data.xlsx](https://github.com/GeoPyTool/GeoPyTool/blob/master/DataFileSamples/Data.xlsx)


![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/NewTAS.png)
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/NewTrace.png)


The New StereoNet Projection and the RoseMap function need Data template file named as [Structure.xlsx](https://github.com/GeoPyTool/GeoPyTool/blob/master/DataFileSamples/Structure.xlsx)

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/Rose.png)

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/LoadPNG.png)

