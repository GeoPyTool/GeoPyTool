Title: Download
Date: 2019-1-13 11:02:14
Category: Doc
Tags: Doc, English, Chinese

#GeoPyTool Application Download Links
># GeoPyTool 打包的可执行程序下载链接


### GeoPyTool pack for Windows:
[Baidu Download 百度网盘](https://pan.baidu.com/s/1orrXwPam_nS7WvdWhDOtiw)

[OneDrive](https://1drv.ms/u/s!AnIw_Lqr4g5tgTG4UU04d2IbBdGh)




### GeoPyTool app for macOS:
[Baidu Download 百度网盘](https://pan.baidu.com/s/18sgEQlGVUVX-Ko86DoxPHw)

[OneDrive](https://1drv.ms/u/s!AnIw_Lqr4g5tgTILXh-J2igEU1Nh)



## Citation 引用

Article Here: [https://www.sciencedirect.com/science/article/pii/S1674987118301609](https://www.sciencedirect.com/science/article/pii/S1674987118301609)

Please cite this article as:

`Yu, Q.-Y., Bagas, L., Yang, P.-H., Zhang, D., GeoPyTool: a cross-platform software solution for common geological calculations and plots, Geoscience Frontiers (2018), doi: 10.1016/j.gsf.2018.08.001.`


## Update 更新

The old version (before `0.8.19.1.13`) of GeoPyTool use `pyqtgraph`, which has been replaced by `VisPy` now.
So when you double click the Update***.bat File, you might encounter following error:

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/UpdateProblem.png)

如果你下载的打包文件是`0.8.19.1.13`以前的版本, 在双击更新的时候会遇到上图所示的错误, 这是因为GeoPyTool 所用的一个模块 pyqtgraph 被移除了, 替换成了 VisPy, 而你没更新的旧版本打包内是没有VisPy的.
所以解决这个问题也很简单, 编辑更新的脚本文件, 改成下面代码部分的形式, 保存后双击运行, 就可以了:

All you need to do is to modify the `UpdateAndRun.bat` to the following form:

```
GeoPyTool\Q.exe -m pip install pip vispy -U --no-cache-dir
GeoPyTool\Q.exe -m pip install pip geopytool -U --no-cache-dir
GeoPyTool\Q.exe -c "import geopytool as gp;gp.main()"
pause
```


![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/FixTheVispy.png)

## Introduction 简介


GeoPyTool is an application based on Python and designed as a solution for geology related daily work. It can run on alomost all mainstream operating systems, such as Windows 7 SP1, Windows 8, Windows 10, macOS Sierra, macOS High Sierra, Ubuntu Linux, Debian Linux, Fedora Linux, and alomost all other widely used desktop platforms.

GeoPyTool doesn't rely on any other software, such as MS Excel or CorelDraw, it can directly transport your data into the plot as vector graphic files and the calculation results into data sheets such as Xlsx or CSV files.

It is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

GeoPyTool contains both traditional routines and newly developed methods。


GeoPyTool 是一个基于 Python 实现的开源应用，针对的是地质学研究中的日常用途。由于使用了 Python，天生跨平台天赋加持，所以几乎能运行于所有主流操作系统，比如 Windows 7 SP1, Windows 8, Windows 10, macOS Sierra, macOS High Sierra, Ubuntu Linux, Debian Linux, Fedora Linux 等等几乎全部主流的桌面操作系统。

GeoPyTool 不需依赖任何其他软件，不像 GeoKit 那样依赖特定版本的 32bit 的 Office，也不像 CGDK 那样需要依赖 CorelDRAW 的安装，单独有 GeoPyTool 一个，就可以实现从原始数据到出矢量图，以及导出各种计算的结果为 Xlsx 或者 CSV 这种表格文件。

GeoPyTool 是一个自由软件:您可以根据自由软件基金会发布的GNU通用公共许可证的条款重新发布或者对其进行修改，但必须也基于同样的 GPLV3（GNU通用公共许可证第三版 ） ，或者更新版本的 GNU General Public License。

GeoPyTool 包含了一些常用的传统方法，也实现了一些近年来新诞生的研究成果。


# Getting Help 获取帮助


You can share your ideas or problems on [Github](https://github.com/GeoPyTool/GeoPyTool/issues).
If you encounter problems using GeoPyTool, please screenshot the error message from the cmd or other ternimal window and send it with your post (shown as the sample below).

大家有各种问题交流，除了在[Github](https://github.com/GeoPyTool/GeoPyTool/issues)，还可以加入咱们的QQ群： 560675626 （为避免无关人员骚扰，加群申请填写暗号 大胖哥是个好人 来通过验证）。
如果你在使用的时候遇到出错的情况,请按下图所示将命令行窗口里面的出错信息截图发来,这会很有帮助:

![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/HowToAskForHelp.png)



# 捐助支持

如果你希望支持 GeoPyTool 的开发，可以扫描下面的二维码进行捐助。
![](https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/img/WeChatQrCode.png)


