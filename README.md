Title: Introduction
Date: 2018-04-21 15:15:13
Category: Doc
Tags: Doc,English

# Welcome to GeoPyTool

[![Build Status](https://travis-ci.org/GeoPyTool/GeoPyTool.svg?branch=master)](https://travis-ci.org/GeoPyTool/GeoPyTool)



## Preface

Few years ago, I had tumor and some other lifelong disease.
Then I lost the ability to engage in geological field work.
I hate to be a useless person and hope to contribute to other people and the world.
Then I started learning programming.
I began to learn and use Python by translating a text book called "Think Python 2 edition" to [Chinese](https://github.com/cycleuser/ThinkPython-en-cn).
After translating [Think Python 2 edition](https://github.com/cycleuser/ThinkPython-en-cn), I translated [Kivy Document](https://github.com/Kivy-CN/Kivy-CN), [CS229 notes from Stanford University](https://github.com/Kivy-CN/Stanford-CS-229-CN) and [STA663 notes from Duke University](https://github.com/Kivy-CN/Duke-STA-663-CN).
I publish all my translation works on Github, as open source projects.

When I began to use Python, from time to time, there have been some people asking me for help by writing some codes to help them solve some of their problems in geological research.

I gathered these scripts together, built a GUI and packed them into a standalone application, which is originally called GeoPython and later renamed GeoPyTool because of the former name had been taken by a conference.

That is the story of how GeoPyTool was born.

## Citation

Article Here: [https://www.sciencedirect.com/science/article/pii/S1674987118301609](https://www.sciencedirect.com/science/article/pii/S1674987118301609)

Please cite this article as:

`Yu, Q.-Y., Bagas, L., Yang, P.-H., Zhang, D., GeoPyTool: a cross-platform software solution for common geological calculations and plots, Geoscience Frontiers (2018), doi: 10.1016/j.gsf.2018.08.001.`



## Introduction

GeoPyTool is an application based on Python and designed as a solution for geology related daily work. **It can run on alomost all mainstream operating systems**, such as Windows 7 SP1, Windows 8, Windows 10, macOS Sierra, macOS High Sierra, Ubuntu Linux, Debian Linux, Fedora Linux, and alomost all other widely used desktop platforms.

**GeoPyTool doesn't rely on any other software**, such as MS Excel or CorelDraw, it can directly transport your data into the plot as vector graphic files and the calculation results into data sheets such as Xlsx or CSV files.

GeoPyTool contains both traditional routines and newly developed methods.
Over time, this software will contain more and more functions.
The function list can be found [here](http://geopytool.com/functions.html).



## Get GeoPyTool

This section used to be called "Installation".
While, in fact you almost need no Installation to use the packed application of GeoPyTool. The latest download links can be found at the [Download page](http://geopytool.com/download.html).



If you want to use GeoPyTool as a module inside Python, then you might need to read the detailed guide at [Installation Guide For Expert](http://geopytool.com/installation-expert.html).


## License

GeoPyTool now is an open source project under the GNU General Public License v3.0.
It is a **free software**: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

In simple terms, you can use, share and modify it for free, under the same terms of GPLv3.

## Bug Report 

Any program may have a bug or many bugs. So does GeoPyTool.
I am not a programming expert or a magic superman, so I will inevitably make mistakes.
I am open minded and happy to solve problems after being told the details about bugs.

If you find bugs but don’t tell me where how that happens, then I'm helpless.
If you don’t even provide any detailed information, but just blaming me, then I’m deeply hurt.
Please do not repeating "many bugs many bugs" with no feedback, that make very frustrated in a long period of pain and self-reproach.

I need your help to find out where the bugs locate and how they happen.
I need to know the version of GeoPyTool that has these bugs.
I might also need a piece of your data file that triggers the bugs.
If you find any bug, I am happy to be told the details and fix it as soon as possible. 

Please open a issue in [GeoPyTool's repo](https://github.com/GeoPyTool/GeoPyTool/issues/). 

You can share your ideas or problems on [Github](https://github.com/GeoPyTool/GeoPyTool/issues).
If you encounter problems using GeoPyTool, please screenshot the error message from the cmd or other ternimal window and send it with your post (shown as the sample below).

## Feedback

If you have some wanted functions, please tell us also opening a issue in [GeoPyTool's repo](https://github.com/GeoPyTool/GeoPyTool/issues/) containing references and sample data. 
It's best to give a brief introduction, which can save developers' time.
If you don't understand how that works at all, don't expect us to figure it out by ourselves.
I am certainly not smarter than you, even much worse than you.



### For Mac Users

On macOS, everything is extremely easy to use GeoPyTool. 
There is **no need to touch the SIP**(System Integrity Protection) at all.
Please leave a message if you encounter different situations, which should contain the version of your operating system.

Please believe me that I have tried this on several brand new Mac machines.


Just download and unzip the packed file, then double click on the GeoPyTool.app file, you will find the APP available as the following picture shows.
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/MacOSScreenShot.png)

To Update the GeoPyTool.app, you need to go to the location inside the app file, `GeoPyTool.app/Contents/Resources/UpDateGeoPytool`.
Double click on this file named `UpDateGeoPytool` at `GeoPyTool.app/Contents/Resources/`. 
As the following screenshot shows:
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/OSXUpdate.png)

It will update the GeoPyTool inside your GeoPyTool.app file. Remember that never modify any files directly under the same folder unless you are an expert on dealing with Python.


### For Windows Users
On Windows 8/8.1/10, everything is also extremely easy to use GeoPyTool. Just download and unzip the file, then double click on a bat file in the unzipped folder, and make sure that you don't delete any file form the unzipped folder because they are all required by the program, then you will find the APP available as the following picture shows.

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/RunWin.jpg)

To use GeoPyTool on Windows 7, some system patches need to be installed. You need to install the SP1 of Windows and then install KB2999226 and the Visual C++ Redistributable 2015. If you are using Windows 7 without the SP1 package installed, there might comes `anapi-ms-win-crtrelated error`. So believe me my friend, just install these patched below, they won't harm you after all.

The SP1 package of Windows 7 can be found at [the official website of MicroSoft](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1).

The installation packages of KB2999226 and the Visual C++ Redistributable 2015 are already contained in the Zip file of GeoPyTool for Windows, and can also be found here: [32 bit Windows7](https://pan.baidu.com/s/1kVwSQ95) ，[64 bit WInodws7](https://pan.baidu.com/s/1qY34ocW) . 
So if you encounter any `api-ms-win-crtrelated errors`, please check those installations first.

If you are using Windows XP or Vista, sorry, I do not have the magic to save those systems that Microsoft has abandoned. 
Expect me to provide support for those antique systems?
Please forgive me for not having time or ability.



### For Linux Users

Awesome, man, good for you. You are a Linux user? So am I.
Then I believe that you are completely capable of using pip to complete the installation under the terminal. There is no need to download a large and bloated package file.

Read the [Installation Guide For Expert](http://geopytool.com/installation-expert.html) if you need some reference information.


## Data Templates


Latest Data File Templates are at [DataFileSamples](https://github.com/GeoPyTool/GeoPyTool/tree/master/DataFileSamples).

Settings.xlsx shows you the meaning and **effects** of those **setting up information** contained in other data templates.

Geochemistry functions in GeoPyTool use **Geochemistry.xlsx**. Structure geology functions use **Structure.xlsx**.
Other functions also have their corresponding data template files.

Please do follow the data templates, maybe you can just paste your data into a copied data template file and try it.


## Blank Data

Sorry, I am not superhero and can not make decision for you on how to treat the blanks in your data. Maybe you want to replace blank with zeros or some random values, or maybe you want to draw a flower in your data file with those blanks.
But I cannot make your choice, nor does GeoPyTool.
The program will only ignore those blanks.

Blanks can not be used in matrix calculation and data fitting, that is how math works and the cruel rules of the real world. Please don't blame me for your lack of enough data or making decision on how to fill the blanks.


## Usage

A detailed demonstration can be found at [Demonstration](http://geopytool.com/demonstration.html).

## Outcome

### Figures 

GeoPyTool offer three choices for format of generated figure, which are PDF, SVG, and PNG.
PDF and SVG are both vector graphic formats, while PNG is not.


#### Adjusting Axises of Figure
There is a menubar on almost all interface of GeoPyTool that generating figures, which can be used to modify and adjust your picture, such as modifying the axis range and axis scale, etc.

As shown in the picture below:

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/Axis%20Adjustment.png)


Please do not blame me for not giving enough options to control your plots without even trying to use these menubar.
Maybe you want me to make pasta for you?

### Result Sheets

GeoPyTool has some calculating related functions, result sheets generated by which can be saved as CSV or Excel files.
The CSV in fact is just a form of plain text, which can be edited by almost any editor.
After all, please find your own way to open these files and do not act like a baby.





![](https://github.com/GeoPyTool/GeoPyTool/blob/master/img/Samples.png?raw=true)

# Support Us

If you want to support GeoPyTool and you also use WeChat, please scan the following QR code to reward us.
I can use this money to pay for medical expenses to stay healthy and add more functions to GeoPyTool.
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/WeChatQrCode.png)


