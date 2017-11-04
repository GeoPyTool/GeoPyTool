Title: GeoPython, 用于地质学日常研究的一站式跨平台解决方案
Date: 2017-11-04 16:20:48
Category: Python

# GeoPython, 用于地质学日常研究的一站式跨平台解决方案

##### 作者: cycleuser
##### 邮箱: cycleuser@cycleuser.org
##### Copyright 2017 cycleuser
##### [官方 BBS](http://bbs.geopython.com/)



|标志性事件|日期|新功能|
|--|--|--|
|开源启动|2016-07-07 6:20|TAS|
|新增 QAPF|2016-07-09 08:32|QAPF|
|新增  Wulff|2016-12-18 08:32|Wulf|
|功能重构|2017-03-15 15:30|Pearce、  Harker 图解|
|单颗粒锆石的 Ce4/3 比值计算|2017-03-25 15:30|Ballard|
|多颗粒锆石 Ce4/3 比值计算|2017-03-28 15:30|MultiBallard|
|多样本的 CIPW 标准矿物计算|2017-04-3 12:30|MultiCIPW|
|全新重构图形界面|2017-07-23 12:30|使用了 PyQt5|
|全部核心功能重构|2017-08-31 23:30|全新多可自定项的 Harker 图解|
|锆石金红石温度计|2017-10-17 20:48:21|Zircon/Rutile|
|加载 PNG/JPG/SVG 做底图|2017-10-23  17:38:21|任意图片都可以做底图来投图|
|中英双语切换|2017-10-25 21:00:20|语言文件模块化|
|更多语言支持|2017-10-30 23:00:20|用户可以自行翻译界面文字并且加载，可以使用任意一种语言|


## 简介

GeoPython 是一个基于 Python 实现的开源应用，针对的是地质学研究中的日常用途。由于使用了 Python，天生跨平台天赋加持，所以几乎能运行于所有主流操作系统，比如 Windows 7 SP1, Windows 8, Windows 10, macOS Sierra, macOS High Sierra, Ubuntu Linux, Debian Linux, Fedora Linux 等等几乎全部主流的桌面操作系统。

GeoPython 不需依赖任何其他软件，不像 GeoKit 那样依赖特定版本的 32bit 的 Office，也不像 CGDK 那样需要依赖 CorelDRAW 的安装，单独有 GeoPython 一个，就可以实现从原始数据到出矢量图，以及导出各种计算的结果为 Xlsx 或者 CSV 这种表格文件。

GeoPython 是一个自由软件:您可以根据自由软件基金会发布的GNU通用公共许可证的条款重新发布或者对其进行修改，但必须也基于同样的 GPLV3（GNU通用公共许可证第三版 ） ，或者更新版本的 GNU General Public License。

GeoPython 包含了一些常用的传统方法，也实现了一些近年来新诞生的研究成果，主要功能如下表格所示。

|功能|简介|文献出处
|--|--|--|
|TAS plot|使用 SiO2 和 (Na2O+K2O) 对火山岩或者侵入岩进行分类判别|Maitre et al., 1989, Middlemost, 1994|
|QAPF plot|使用 Q (quartz 石英), A (alkali feldspar 碱性长石), P (plagioclase 斜长石) ，F (feldspathoid 似长石) 来对深成岩或者火山岩进行分类|Maitre et al., 2004|
|REE（Rare Earth Elements） |使用标准样品对样品的稀土元素进行标准化，分析其分配曲线、倾向、异常值等等|Boynton, 1984|
|Trace elements |使用标准样品对样品的微量元素进行标准化，分析其分配曲线、倾向、异常值等等|Sun and McDonough, 1989|
|Rb-Y+Nb, Rb-Yb+Ta, Nb-Y, and Ta-Yb plots|利用花岗岩中的 Y-Nb, Yb-Ta, Rb- (Y + Nb)，Rb- (Yb + Ta) 来推断其大地构造位置|Pearce et al., 1984|
|极射赤平投影和玫瑰花土|使用吴尔福网或者施密特网来对地质体的产状，包括走向倾向倾角，进行可视化|Zhou et al., 2003|
|QFL、QmFLt plots|三角图解，使用砂岩中的石英碎屑、长石碎屑、岩屑等的比例关系来推断其大地构造单元|Dickinson et al. 1983|
|CIPW 标准化计算|经典计算方法，利用原始主微量数据中的特定氧化物和元素组合来推算标准化的矿物比例，计算的结果可以用于 QAPF 分类|Johannsen, 1939; Washington, 1917; CIPW norm Excel spreadsheet by Kurt Hollocher|
|锆石中 Ce4/Ce3 比值计算|计算锆石中的变价稀土元素 Ce(IV)/Ce(III) 的比值来作为斑岩氧逸度相对高低的半定量指标|Ballard et al., 2002|
|锆石和金红石温度计|使用锆石中 Ti 和金红石中的 Zr 两种元素以及 SiO2 和 TiO2 的活度来计算结晶体系的温度值。|Watson et al., 2006|
|谱系聚类分析|对数据中的数值项目进行统计，根据相关系数等等来进行谱系聚类，初级阶段，后续会有进一步丰富和改进|
|加载任意图片做底图|支持平面图和三角图解，可以使用任意文章中的任意图片来做底图使用，这样即便没有现成的软件提供具体的功能，用户也可以自行使用他人文献中的图片来投图使用作为参考。|An original function|



## 安装 GeoPython

GeoPython  有两种使用方法，可以作为独立的程序运行，也可以作为 Python 下的一个模块（module）来在 Python 解释器下调用。


## 作为独立程序使用 GeoPython

打包好的可执行文件，目前支持 Windows 和 macOS 两种平台。


[点击这里查看程序文件的下载链接。](https://github.com/chinageology/GeoPython/blob/master/Download.md)

### Mac 下的 APP

macOS 下面特别省心，因为开发者本身就用的这个系统。直接下载对应的压缩包，解压缩之后，双击 GeoPython.app 这个文件，就可以看到下面的图形界面了。

![User Interface of the APP on macOS.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/MacOSScreenShot.png)


### Windows 系统下的 EXE

#### Windows 8/8.1/10 用户

这几个比较新的 Windows 系统的用户也很省心，也是下载之后解压缩，然后在文件夹里面双击 GeoPython.exe 就可以了。记住一定不要删除解压出来的文件夹里面的任何文件，那都是程序用得上的，一旦删除了就可能导致程序无法运行了。

![User Interface of the EXE on Windows.](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/ScreenShot.png)

#### Windows 7 用户

刚才上面那张图实际上是在 Windows7 系统上面运行 GeoPython 的截图。不过 Windows7 系统用户需要先安装几个补丁，才能运行 GeoPython。

首先是一定要安装 Windows 7 SP1 这个补丁，然后要安装 KB2999226 和 `Visual C++ Redistributable 2015`。如果不按照  SP1 以及其他两个补丁，运行 GeoPython.exe 的时候就会出现错误提示，说什么`api-ms-win-crt` 无法定位之类的。总之遇到这样的情况时，先检查系统是不是安装了 SP1，然后将其他两个补丁安装试一试。

针对 Windows 7 的 SP1 补丁[自然是可以在微软的官网这个地址里面找到的](https://support.microsoft.com/en-us/help/15090/windows-7-install-service-pack-1-sp1)。

其他两个安装包，包括 KB2999226 和`Visual C++ Redistributable 2015` 已经包含在 GeoPython 的压缩包里面了，也可以在下面这两个地址里面下载：[32 bit Windows7 ](https://pan.baidu.com/s/1kVwSQ95)，[64 bit WInodws7 ](https://pan.baidu.com/s/1qY34ocW).

再次重复一遍，如果你遇到不能运行的情况，并且看到了 `api-ms-win-crt` 这样的字样，先检查上面的补丁是否安装了。

#### Windows XP 和 Vista 用户

我自己试了好几次都没弄成，我也懒得在这些老古董系统上面浪费时间精力。人生宝贵，所以建议你把电脑升级成 Windows7 SP1 以上的更新的操作系统，如果配置实在太差也可以用 Linux 操作系统。反正如果你非要纠结在 XP 这类连微软自己都抛弃的系统上，那就祝你好运以及再见！



## 将 GeoPython 作为 Python 模块来使用

其他的所有操作系统，比如 Debian Linux, Ubuntu Linux, Fedora Linux, FreeBSD 甚至 GNU/Hurd，都可以将 GeoPython 作为一个 Python 模块来在 Python 解释器里面运行。实际上对于 macOS 和 Windows 用户，也建议这样使用，因为这样能够最快速更新到最新版本，下载安装都更加迅速。当然，操作起来稍微复杂点，反正不适合缺乏挑战精神和探索学习能力的人。

### 首先要安装 Python

 你需要先安装 Python，GeoPython 是用 Python3.5 写的，并且不兼容 Python2， 所以推荐你也用 3.5 或者更新的 Python。可以到 [Python 官方网站](https://www.python.org/downloads/) 或者  [清华 Tuna](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/) 去下载对应自己系统的安装包。

更推荐大家使用 Anaconda3-4.0.0 或者更新版本的 Anaconda3。因为在 Anaconda 中，包括 cython, numpy, pandas, matplotlib 等在内的很多必要的包都集成好了，安装时候省时间。


##### 对于 Windows 用户的一些有用链接

实际上网上有很多很多指南，都给说明吧了要怎么安装 Python 以及激活 PIP。所以这里面就只放几个下载链接，自己探索吧哈，没探索精神搞个毛球学术对吧。

###### 32bit：

|项目 |下载地址 |
|--|--|
|Anaconda|https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-4.4.0-Windows-x86.exe|

###### 64bit：

|项目 |下载地址 |
|--|--|
|Anaconda|https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-4.4.0-Windows-x86_64.exe|

### 使用 PIP 安装 GeoPython


安装完了 Python 并且激活了 PIP 之后，你是不是想着马上就能安装 GeoPython 了？

然而并不行。你需要安装一些基础包，GeoPython 就是基于这些包构建的。即便你用的是 Anaconda3，也还是需要安装一些包，比如 pyqt5，这是用来搭建 GeoPython 的 GUI 图形界面的模块。

所以要在终端里面输入一些命令来先安装这些基础包。

不知道终端是啥？好吧，这里我先不责怪你怎么不去百度或者谷歌自行搜索。

在 Windows 系统里面，现在的终端一般就是 CMD 或者 PowerShell。对于其他的操作系统，比如 macOS 或者各种 Linux 以及 BSD 操作系统，往往都是 Bash，在这些系统里面也往往能找到 终端 这个程序，一般就在开始菜单或者程序目录里面肯定有。

Windows 用户不知道怎么运行 CMD 或者 PowerShell？搜索去吧，不要做纯粹的伸手党，自己探索一下是有好处的。


#### 注意

	这里我用的命令都是 pip，这是假设你的 系统默认的 pip 就是 python3 的。而如果你同时安装了 Python2 和 Python3，那可能 pip 对应的未必是 Python3 的 pip 而是 Python2 的，这时候你可能就要把下面所有的 pip 替换成 pip3 来运行，应该就可以了。

接下来就把下面的命令**逐条**复制粘贴到终端里面来运行，安装依赖包吧。

```Bash
pip install cython
pip install numpy
pip install pandas
pip install xlrd
pip install matplotlib
pip install BeautifulSoup4
pip install pyqt5
pip install scipy
pip install scikit-learn
pip install sympy
```

安装完成了上面这些依赖包之后，就可以输入下面的这个命令来安装 GeoPython 了。
```Bash
pip install geopython
```

如果没有发现什么出错信息，就是说明安装成功了。

### 更新已经安装的 GeoPython 模块

如果你之前安装了 GeoPython，可以通过下面的命令来更新到最新版本。

```Bash
pip install geopython --update --no-cache-dir
```

### 在 Python 下启动 GeoPython

安装完了 GeoPython，就可以在 Python 解释器里面启动了。不过这里要推荐一个替代原生解释器的 IPython，可以通过下面命令安装。

```Bash
pip install ipython
```

安装好之后在终端中输入下面的命令启动 ipython。

```Bash
ipython
```

然后在 ipython 或者原生 Python 解释器中输入下面两行命令，回车，就可以了。

```Python
import geopython as gp
gp.main()
```

就能看到 GeoPython 的图形界面了。
例如下图就是在  Ubuntu 系统下的截图。

![GeoPython in Ubuntu](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/UbuntuScreenShot.png)

每次运行 GeoPython 之前，更新一下是个好习惯。
```Bash
pip install --upgrade geopython
```

## 点型Marker/ 颜色Color/ 线型Style

GeoPython 可视化的部分使用 Matplotlib 来实现的，所以设置的这些项目也是相似的。

点型 Markers 的设置可以参考:
http://matplotlib.org/api/markers_api.html

颜色 Colors 的设置可以参考:
http://matplotlib.org/api/colors_api.html

下面的示意图来自[nrougier](http://www.labri.fr/perso/nrougier/teaching/matplotlib/):

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/LIneStylesMarkers.png)


## 需要更多帮助？

请访问我们的论坛 http://bbs.geopython.com/ 来留言**写清楚**你使用的操作系统、安装方法、错误截图。我们会尽快给出反馈。

## 附录


锆石氧逸度计算的样例数据文件为 [ZirconCe.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/ZirconCe.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewZirconCe.png)


 TAS/REE/微量元素、Pearce  图解和 Harker 图解的数据样例文件为
[Data.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Data.xlsx)


![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTAS.png)
![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/NewTrace.png)


极射赤平投影和玫瑰花图的样例数据文件为 [Structure.xlsx](https://github.com/chinageology/GeoPython/blob/master/NewGUI/Structure.xlsx)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/Rose.png)

![](https://raw.githubusercontent.com/chinageology/GeoPython/master/img/LoadPNG.png)

