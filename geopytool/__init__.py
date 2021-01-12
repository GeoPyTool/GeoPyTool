#!/usr/bin/python3
# coding:utf-8
import sys, os

print(sys.path)

LocationOfMySelf = os.path.dirname(__file__)
sys.path.append(LocationOfMySelf)
# print(LocationOfMySelf,' init')

from ImportDependence import *
from CustomClass import *

sign = '''
created on Sat Dec 17 22:28:24 2016
@author: cycleuser
# Create Date: 2015-07-13
# Modify Date: 2018-02-09
a tool set for daily geology related task.
# prerequisite:
#   based on Python 3.x
#   need math,numpy,pandas,matplotlib,xlrd,pyqt5,BeautifulSoup4,pyopengl,pyqtgraph
    Any issues or improvements please contact cycleuser@cycleuser.org
    or Open An Issue at GitHub:https://github.com/GeoPyTool/GeoPyTool/issues     
    Website For Chinese Users：https://zhuanlan.zhihu.com/p/28908475
'''

t = 'You are using GeoPyTool ' + version + ', released on' + date + '\n' + sign
_translate = QtCore.QCoreApplication.translate

from CustomClass import TableViewer
from CIPW import CIPW
from Niggli import Niggli
from Cluster import Cluster
from Harker import Harker
from HarkerOld import HarkerOld

# from Magic import Magic

from Clastic import Clastic
from CIA import CIA

from IsoTope import IsoTope

from KArIsoTope import KArIsoTope

from MultiDimension import MultiDimension

from Combine import MyCombine

from Flatten import MyFlatten



from MyDT import MyDT

from MyFA import MyFA

from MyLDA import MyLDA

from MyPCA import MyPCA

from MyMLP import MyMLP

from MyGAN import MyGAN


from Trans import MyTrans

from Dist import MyDist

from Sta import MySta

from ThreeD import MyThreeD

from TwoD import MyTwoD

from TwoD_Grey import MyTwoD_Grey

from Pearce import Pearce
from QAPF import QAPF
from QFL import QFL
from QmFLt import QmFLt
from REE import REE
from Rose import Rose
from Stereo import Stereo
from TAS import TAS
from K2OSiO2 import K2OSiO2
from ZrYSrTi import ZrYSrTi
from TiAlCaMgMnKNaSi import TiAlCaMgMnKNaSi

from Saccani import Saccani
from Raman import Raman
from FluidInclusion import FluidInclusion
from MyHist import MyHist

from Temp import *
from TraceNew import TraceNew
from Trace import Trace
from XY import XY
from XYZ import XYZ
from ZirconCe import ZirconCe
from ZirconCeOld import ZirconCeOld
from Magic import Magic


# Create a custom "QProxyStyle" to enlarge the QMenu icons
# -----------------------------------------------------------
class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 24
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


class Ui_MainWindow(QtWidgets.QMainWindow):
    raw = pd.DataFrame(index=[], columns=[])  # raw is initialized as a blank DataFrame
    Standard = {}  # Standard is initialized as a blank Dict
    Language = ''
    app = QtWidgets.QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')  # The proxy style should be based on an existing style,
    # like 'Windows', 'Motif', 'Plastique', 'Fusion', ...
    app.setStyle(myStyle)
    trans = QtCore.QTranslator()
    talk = ''
    targetversion = '0'
    DataLocation = ''
    ChemResult = pd.DataFrame()
    AutoResult = pd.DataFrame()
    TotalResult = []

    def __init__(self):

        super(Ui_MainWindow, self).__init__()
        self.setObjectName('MainWindow')
        self.resize(800, 600)

        self.setAcceptDrops(True)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', u'GeoPyTool'))
        self.setWindowIcon(QIcon(LocationOfMySelf + '/png'))
        self.talk = _translate('MainWindow', 'You are using GeoPyTool ') + version + '\n' + _translate('MainWindow',
                                                                                                       'released on ') + date

        self.model = PandasModel(self.raw)

        self.main_widget = QWidget(self)

        self.tableView = CustomQTableView(self.main_widget)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName('menubar')

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName('menuFile')

        self.menuGeoChem = QtWidgets.QMenu(self.menubar)
        self.menuGeoChem.setObjectName('menuGeoChem')

        self.menuStructure = QtWidgets.QMenu(self.menubar)
        self.menuStructure.setObjectName('menuStructure')

        self.menuSedimentary = QtWidgets.QMenu(self.menubar)
        self.menuSedimentary.setObjectName('menuSedimentary')

        self.menuGeoCalc = QtWidgets.QMenu(self.menubar)
        self.menuGeoCalc.setObjectName('menuGeoCalc')

        self.menuAdditional = QtWidgets.QMenu(self.menubar)
        self.menuAdditional.setObjectName('menuAdditional')

        self.menuMachineLearn = QtWidgets.QMenu(self.menubar)
        self.menuMachineLearn.setObjectName('menuMachineLearn')

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName('menuHelp')

        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName('menuLanguage')

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(QIcon(LocationOfMySelf + '/open.png'), u'Open', self)
        self.actionOpen.setObjectName('actionOpen')
        self.actionOpen.setShortcut('Ctrl+O')

        self.actionClose = QtWidgets.QAction(QIcon(LocationOfMySelf + '/close.png'), u'Close', self)
        self.actionClose.setObjectName('actionClose')
        self.actionClose.setShortcut('Ctrl+N')

        self.actionSet = QtWidgets.QAction(QIcon(LocationOfMySelf + '/set.png'), u'Set', self)
        self.actionSet.setObjectName('actionSet')
        self.actionSet.setShortcut('Ctrl+F')

        self.actionFillNaN = QtWidgets.QAction(QIcon(LocationOfMySelf + '/FillNaN.png'), u'Set', self)
        self.actionFillNaN.setObjectName('actionFillNaN')
        self.actionFillNaN.setShortcut('Ctrl+Alt+F')

        self.actionSave = QtWidgets.QAction(QIcon(LocationOfMySelf + '/save.png'), u'Save', self)
        self.actionSave.setObjectName('actionSave')
        self.actionSave.setShortcut('Ctrl+S')

        self.actionCombine = QtWidgets.QAction(QIcon(LocationOfMySelf + '/combine.png'), u'Combine', self)
        self.actionCombine.setObjectName('actionCombine')
        self.actionCombine.setShortcut('Alt+C')

        self.actionCombine_transverse = QtWidgets.QAction(QIcon(LocationOfMySelf + '/combine.png'),
                                                          u'Combine_transverse', self)
        self.actionCombine_transverse.setObjectName('actionCombine_transverse')
        self.actionCombine_transverse.setShortcut('Alt+T')

        self.actionFlatten = QtWidgets.QAction(QIcon(LocationOfMySelf + '/flatten.png'), u'Flatten', self)
        self.actionFlatten.setObjectName('actionFlatten')
        self.actionFlatten.setShortcut('Alt+F')

        self.actionTrans = QtWidgets.QAction(QIcon(LocationOfMySelf + '/trans.png'), u'Trans', self)
        self.actionTrans.setObjectName('actionTrans')
        self.actionTrans.setShortcut('Ctrl+T')

        self.actionReFormat = QtWidgets.QAction(QIcon(LocationOfMySelf + '/trans.png'), u'ReFormat', self)
        self.actionReFormat.setObjectName('actionReFormat')
        self.actionReFormat.setShortcut('Alt+R')

        self.actionQuit = QtWidgets.QAction(QIcon(LocationOfMySelf + '/quit.png'), u'Quit', self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')

        self.actionWeb = QtWidgets.QAction(QIcon(LocationOfMySelf + '/forum.png'), u'English Forum', self)
        self.actionWeb.setObjectName('actionWeb')

        self.actionGoGithub = QtWidgets.QAction(QIcon(LocationOfMySelf + '/github.png'), u'GitHub', self)
        self.actionGoGithub.setObjectName('actionGoGithub')

        self.actionVersionCheck = QtWidgets.QAction(QIcon(LocationOfMySelf + '/update.png'), u'Version', self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')

        self.actionCnS = QtWidgets.QAction(QIcon(LocationOfMySelf + '/cns.png'), u'Simplified Chinese', self)
        self.actionCnS.setObjectName('actionCnS')

        self.actionCnT = QtWidgets.QAction(QIcon(LocationOfMySelf + '/cnt.png'), u'Traditional Chinese', self)
        self.actionCnT.setObjectName('actionCnT')

        self.actionEn = QtWidgets.QAction(QIcon(LocationOfMySelf + '/en.png'), u'English', self)
        self.actionEn.setObjectName('actionEn')

        self.actionLoadLanguage = QtWidgets.QAction(QIcon(LocationOfMySelf + '/lang.png'), u'Load Language', self)
        self.actionLoadLanguage.setObjectName('actionLoadLanguage')

        self.actionTAS = QtWidgets.QAction(QIcon(LocationOfMySelf + '/xy.png'), u'TAS', self)
        self.actionTAS.setObjectName('actionTAS')

        self.actionTrace = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider2.png'), u'Trace', self)
        self.actionTrace.setObjectName('actionTrace')

        self.actionTraceNew = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider2.png'), u'TraceNew', self)
        self.actionTraceNew.setObjectName('actionTraceNew')

        self.actionRee = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider2.png'), u'Ree', self)
        self.actionRee.setObjectName('actionRee')

        self.actionPearce = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider.png'), u'Pearce', self)
        self.actionPearce.setObjectName('actionPearce')

        self.actionHarker = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider.png'), u'Harker', self)
        self.actionHarker.setObjectName('actionHarker')

        self.actionHarkerOld = QtWidgets.QAction(QIcon(LocationOfMySelf + '/spider.png'), u'HarkerOld', self)
        self.actionHarkerOld.setObjectName('actionHarkerOld')

        self.actionRemoveLOI = QtWidgets.QAction(QIcon(LocationOfMySelf + '/fire.png'), u'RemoveLOI', self)
        self.actionRemoveLOI.setObjectName('actionRemoveLOI')

        self.actionK2OSiO2 = QtWidgets.QAction(QIcon(LocationOfMySelf + '/xy.png'), u'K2OSiO2', self)
        self.actionK2OSiO2.setObjectName('actionK2OSiO2')

        self.actionZrYSrTi = QtWidgets.QAction(QIcon(LocationOfMySelf + '/xy.png'), u'ZrYSrTi', self)
        self.actionZrYSrTi.setObjectName('actionZrYSrTi')

        self.actionTiAlCaMgMnKNaSi = QtWidgets.QAction(QIcon(LocationOfMySelf + '/xy.png'), u'TiAlCaMgMnKNaSi', self)
        self.actionTiAlCaMgMnKNaSi.setObjectName('actionTiAlCaMgMnKNaSi')

        self.actionStereo = QtWidgets.QAction(QIcon(LocationOfMySelf + '/structure.png'), u'Stereo', self)
        self.actionStereo.setObjectName('actionStereo')

        self.actionRose = QtWidgets.QAction(QIcon(LocationOfMySelf + '/rose.png'), u'Rose', self)
        self.actionRose.setObjectName('actionRose')

        self.actionQFL = QtWidgets.QAction(QIcon(LocationOfMySelf + '/triangular.png'), u'QFL', self)
        self.actionQFL.setObjectName('actionQFL')

        self.actionQmFLt = QtWidgets.QAction(QIcon(LocationOfMySelf + '/triangular.png'), u'QmFLt', self)
        self.actionQmFLt.setObjectName('actionQmFLt')

        self.actionCIPW = QtWidgets.QAction(QIcon(LocationOfMySelf + '/calc.png'), u'CIPW', self)
        self.actionCIPW.setObjectName('actionCIPW')

        self.actionNiggli = QtWidgets.QAction(QIcon(LocationOfMySelf + '/calc.png'), u'Niggli', self)
        self.actionNiggli.setObjectName('actionNiggli')

        self.actionZirconCe = QtWidgets.QAction(QIcon(LocationOfMySelf + '/calc.png'), u'ZirconCe', self)
        self.actionZirconCe.setObjectName('actionZirconCe')

        self.actionZirconCeOld = QtWidgets.QAction(QIcon(LocationOfMySelf + '/calc.png'), u'ZirconCeOld', self)
        self.actionZirconCeOld.setObjectName('actionZirconCeOldOld')

        self.actionZirconTiTemp = QtWidgets.QAction(QIcon(LocationOfMySelf + '/temperature.png'), u'ZirconTiTemp', self)
        self.actionZirconTiTemp.setObjectName('actionZirconTiTemp')

        self.actionRutileZrTemp = QtWidgets.QAction(QIcon(LocationOfMySelf + '/temperature.png'), u'RutileZrTemp', self)
        self.actionRutileZrTemp.setObjectName('actionRutileZrTemp')

        self.actionCluster = QtWidgets.QAction(QIcon(LocationOfMySelf + '/cluster.png'), u'Cluster', self)
        self.actionCluster.setObjectName('actionCluster')

        self.actionAuto = QtWidgets.QAction(QIcon(LocationOfMySelf + '/auto.png'), u'Auto', self)
        self.actionAuto.setObjectName('actionAuto')

        self.actionMultiDimension = QtWidgets.QAction(QIcon(LocationOfMySelf + '/multiple.png'), u'MultiDimension',
                                                      self)
        self.actionMultiDimension.setObjectName('actionMultiDimension')

        self.actionThreeD = QtWidgets.QAction(QIcon(LocationOfMySelf + '/multiple.png'), u'ThreeD', self)
        self.actionThreeD.setObjectName('actionThreeD')

        self.actionTwoD = QtWidgets.QAction(QIcon(LocationOfMySelf + '/qapf.png'), u'TwoD', self)
        self.actionTwoD.setObjectName('actionTwoD')

        self.actionTwoD_Grey = QtWidgets.QAction(QIcon(LocationOfMySelf + '/qapf.png'), u'TwoD Grey', self)
        self.actionTwoD_Grey.setObjectName('actionTwoD_Grey')

        self.actionDist = QtWidgets.QAction(QIcon(LocationOfMySelf + '/dist.png'), u'Dist', self)
        self.actionDist.setObjectName('actionDist')

        self.actionStatistics = QtWidgets.QAction(QIcon(LocationOfMySelf + '/statistics.png'), u'Statistics', self)
        self.actionStatistics.setObjectName('actionStatistics')

        self.actionMyHist = QtWidgets.QAction(QIcon(LocationOfMySelf + '/h.png'), u'Histogram', self)
        self.actionMyHist.setObjectName('actionMyHist')

        self.actionPie = QtWidgets.QAction(QIcon(LocationOfMySelf + '/pie.png'), u'Pie', self)
        self.actionPie.setObjectName('actionPie')

        self.actionBar = QtWidgets.QAction(QIcon(LocationOfMySelf + '/bar.png'), u'Bar', self)
        self.actionBar.setObjectName('actionPie')


        self.actionDT = QtWidgets.QAction(QIcon(LocationOfMySelf + '/dt.png'), u'DT', self)
        self.actionDT.setObjectName('actionDT')

        self.actionFA = QtWidgets.QAction(QIcon(LocationOfMySelf + '/fa.png'), u'FA', self)
        self.actionFA.setObjectName('actionFA')

        self.actionLDA = QtWidgets.QAction(QIcon(LocationOfMySelf + '/lda.png'), u'LDA', self)
        self.actionLDA.setObjectName('actionLDA')

        self.actionPCA = QtWidgets.QAction(QIcon(LocationOfMySelf + '/pca.png'), u'PCA', self)
        self.actionPCA.setObjectName('actionPCA')

        self.actionMLP = QtWidgets.QAction(QIcon(LocationOfMySelf + '/mlp.png'), u'MLP', self)
        self.actionMLP.setObjectName('actionMLP')

        self.actionGAN = QtWidgets.QAction(QIcon(LocationOfMySelf + '/g.png'), u'GAN', self)
        self.actionGAN.setObjectName('actionGAN')


        self.actionQAPF = QtWidgets.QAction(QIcon(LocationOfMySelf + '/qapf.png'), u'QAPF', self)
        self.actionQAPF.setObjectName('actionQAPF')

        self.actionSaccani = QtWidgets.QAction(QIcon(LocationOfMySelf + '/s.png'), u'Saccani Plot', self)
        self.actionSaccani.setObjectName('actionSaccani')

        self.actionRaman = QtWidgets.QAction(QIcon(LocationOfMySelf + '/r.png'), u'Raman Strength', self)
        self.actionRaman.setObjectName('actionRaman')

        self.actionFluidInclusion = QtWidgets.QAction(QIcon(LocationOfMySelf + '/f.png'), u'Fluid Inclusion', self)
        self.actionFluidInclusion.setObjectName('actionFluidInclusion')

        self.actionClastic = QtWidgets.QAction(QIcon(LocationOfMySelf + '/mud.png'), u'Clastic(sand-silt-clay)', self)
        self.actionClastic.setObjectName("actionClastic")

        self.actionCIA = QtWidgets.QAction(QIcon(LocationOfMySelf + '/mud.png'), u'CIA/ICV/PIA/CIW/CIW\'', self)
        self.actionCIA.setObjectName("actionCIA")

        self.actionXY = QtWidgets.QAction(QIcon(LocationOfMySelf + '/xy.png'), u'X-Y', self)
        self.actionXY.setObjectName('actionXY')

        self.actionXYZ = QtWidgets.QAction(QIcon(LocationOfMySelf + '/triangular.png'), u'Ternary', self)
        self.actionXYZ.setObjectName('actionXYZ')

        self.actionRbSrIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf + '/magic.png'), u'Rb-Sr IsoTope', self)
        self.actionRbSrIsoTope.setObjectName('actionRbSrIsoTope')

        self.actionSmNdIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf + '/magic.png'), u'Sm-Nd IsoTope', self)
        self.actionSmNdIsoTope.setObjectName('actionSmNdIsoTope')

        self.actionKArIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf + '/magic.png'), u'K-Ar IsoTope', self)
        self.actionKArIsoTope.setObjectName('actionKArIsoTope')

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionSet)
        self.menuFile.addAction(self.actionFillNaN)
        self.menuFile.addAction(self.actionSave)

        self.menuFile.addAction(self.actionCombine)
        self.menuFile.addAction(self.actionCombine_transverse)

        self.menuFile.addAction(self.actionFlatten)
        self.menuFile.addAction(self.actionTrans)
        # self.menuFile.addAction(self.actionReFormat)

        self.menuFile.addAction(self.actionQuit)

        self.menuGeoChem.addAction(self.actionRemoveLOI)
        self.menuGeoChem.addAction(self.actionAuto)
        self.menuGeoChem.addAction(self.actionTAS)
        self.menuGeoChem.addAction(self.actionTrace)
        self.menuGeoChem.addAction(self.actionRee)
        self.menuGeoChem.addAction(self.actionPearce)
        self.menuGeoChem.addAction(self.actionHarker)
        self.menuGeoChem.addAction(self.actionCIPW)
        # self.menuGeoChem.addAction(self.actionNiggli)
        self.menuGeoChem.addAction(self.actionQAPF)
        self.menuGeoChem.addAction(self.actionSaccani)
        self.menuGeoChem.addAction(self.actionK2OSiO2)
        self.menuGeoChem.addAction(self.actionRaman)
        self.menuGeoChem.addAction(self.actionFluidInclusion)
        self.menuGeoChem.addAction(self.actionHarkerOld)
        self.menuGeoChem.addAction(self.actionTraceNew)
        self.menuGeoChem.addAction(self.actionZrYSrTi)
        self.menuGeoChem.addAction(self.actionTiAlCaMgMnKNaSi)

        self.menuStructure.addAction(self.actionStereo)
        self.menuStructure.addAction(self.actionRose)
        self.menuSedimentary.addAction(self.actionQFL)
        self.menuSedimentary.addAction(self.actionQmFLt)
        self.menuSedimentary.addAction(self.actionClastic)
        self.menuSedimentary.addAction(self.actionCIA)

        self.menuGeoCalc.addAction(self.actionZirconCe)
        self.menuGeoCalc.addAction(self.actionZirconCeOld)
        self.menuGeoCalc.addAction(self.actionZirconTiTemp)
        self.menuGeoCalc.addAction(self.actionRutileZrTemp)
        self.menuGeoCalc.addAction(self.actionRbSrIsoTope)
        self.menuGeoCalc.addAction(self.actionSmNdIsoTope)
        # self.menuGeoCalc.addAction(self.actionKArIsoTope)

        self.menuAdditional.addAction(self.actionXY)
        self.menuAdditional.addAction(self.actionXYZ)
        self.menuAdditional.addAction(self.actionCluster)
        self.menuAdditional.addAction(self.actionMultiDimension)
        self.menuAdditional.addAction(self.actionDist)
        self.menuAdditional.addAction(self.actionStatistics)
        self.menuAdditional.addAction(self.actionThreeD)
        self.menuAdditional.addAction(self.actionTwoD)
        self.menuAdditional.addAction(self.actionTwoD_Grey)
        self.menuAdditional.addAction(self.actionMyHist)
        self.menuAdditional.addAction(self.actionPie)
        self.menuAdditional.addAction(self.actionBar)

        self.menuMachineLearn.addAction(self.actionDT)
        self.menuMachineLearn.addAction(self.actionFA)
        self.menuMachineLearn.addAction(self.actionLDA)
        self.menuMachineLearn.addAction(self.actionPCA)
        self.menuMachineLearn.addAction(self.actionMLP)
        self.menuMachineLearn.addAction(self.actionGAN)

        self.menuHelp.addAction(self.actionWeb)

        self.menuHelp.addAction(self.actionGoGithub)
        self.menuHelp.addAction(self.actionVersionCheck)

        self.menuLanguage.addAction(self.actionCnS)
        self.menuLanguage.addAction(self.actionCnT)
        self.menuLanguage.addAction(self.actionEn)
        self.menuLanguage.addAction(self.actionLoadLanguage)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuGeoChem.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuStructure.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuSedimentary.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuGeoCalc.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuAdditional.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuMachineLearn.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addSeparator()

        self.actionCombine.triggered.connect(self.Combine)
        self.actionCombine_transverse.triggered.connect(self.Combine_transverse)
        self.actionFlatten.triggered.connect(self.Flatten)
        self.actionTrans.triggered.connect(self.Trans)
        self.actionReFormat.triggered.connect(self.ReFormat)

        self.actionTAS.triggered.connect(self.TAS)
        self.actionTrace.triggered.connect(self.Trace)
        self.actionTraceNew.triggered.connect(self.TraceNew)
        self.actionRee.triggered.connect(self.REE)
        self.actionPearce.triggered.connect(self.Pearce)
        self.actionHarker.triggered.connect(self.Harker)
        self.actionHarkerOld.triggered.connect(self.HarkerOld)
        self.actionQAPF.triggered.connect(self.QAPF)
        self.actionSaccani.triggered.connect(self.Saccani)
        self.actionK2OSiO2.triggered.connect(self.K2OSiO2)
        self.actionZrYSrTi.triggered.connect(self.ZrYSrTi)
        self.actionTiAlCaMgMnKNaSi.triggered.connect(self.TiAlCaMgMnKNaSi)

        self.actionRaman.triggered.connect(self.Raman)
        self.actionFluidInclusion.triggered.connect(self.FluidInclusion)

        self.actionStereo.triggered.connect(self.Stereo)
        self.actionRose.triggered.connect(self.Rose)
        self.actionQFL.triggered.connect(self.QFL)
        self.actionQmFLt.triggered.connect(self.QmFLt)

        self.actionClastic.triggered.connect(self.Clastic)
        self.actionCIA.triggered.connect(self.CIA)

        self.actionCIPW.triggered.connect(self.CIPW)
        self.actionNiggli.triggered.connect(self.Niggli)
        self.actionZirconCe.triggered.connect(self.ZirconCe)
        self.actionZirconCeOld.triggered.connect(self.ZirconCeOld)
        self.actionZirconTiTemp.triggered.connect(self.ZirconTiTemp)
        self.actionRutileZrTemp.triggered.connect(self.RutileZrTemp)
        self.actionCluster.triggered.connect(self.Cluster)
        self.actionAuto.triggered.connect(self.Auto)

        self.actionMultiDimension.triggered.connect(self.MultiDimension)
        self.actionRemoveLOI.triggered.connect(self.RemoveLOI)


        self.actionDT.triggered.connect(self.DT)
        self.actionFA.triggered.connect(self.FA)
        self.actionLDA.triggered.connect(self.LDA)
        self.actionPCA.triggered.connect(self.PCA)
        self.actionMLP.triggered.connect(self.MLP)
        self.actionGAN.triggered.connect(self.GAN)

        self.actionDist.triggered.connect(self.Dist)
        self.actionStatistics.triggered.connect(self.Sta)
        self.actionThreeD.triggered.connect(self.ThreeD)
        self.actionTwoD.triggered.connect(self.TwoD)
        self.actionTwoD_Grey.triggered.connect(self.TwoD_Grey)
        self.actionMyHist.triggered.connect(self.MyHist)
        self.actionPie.triggered.connect(self.MyPie)
        self.actionBar.triggered.connect(self.MyBar)

        # self.actionICA.triggered.connect(self.ICA)
        # self.actionSVM.triggered.connect(self.SVM)

        self.actionOpen.triggered.connect(self.getDataFile)
        self.actionClose.triggered.connect(self.clearDataFile)
        self.actionSet.triggered.connect(self.SetUpDataFile)
        self.actionFillNaN.triggered.connect(self.FillNaN)
        self.actionSave.triggered.connect(self.saveDataFile)
        self.actionQuit.triggered.connect(qApp.quit)

        self.actionWeb.triggered.connect(self.goDiscussion)
        self.actionGoGithub.triggered.connect(self.goGitHub)
        self.actionVersionCheck.triggered.connect(self.checkVersion)

        self.actionCnS.triggered.connect(self.to_ChineseS)
        self.actionCnT.triggered.connect(self.to_ChineseT)
        self.actionEn.triggered.connect(self.to_English)
        self.actionLoadLanguage.triggered.connect(self.to_LoadLanguage)

        self.actionXY.triggered.connect(self.XY)
        self.actionXYZ.triggered.connect(self.XYZ)
        self.actionRbSrIsoTope.triggered.connect(self.RbSrIsoTope)
        self.actionSmNdIsoTope.triggered.connect(self.SmNdIsoTope)
        self.actionKArIsoTope.triggered.connect(self.KArIsoTope)

        self.ReadConfig()
        self.trans.load(LocationOfMySelf + '/' + self.Language)
        self.app.installTranslator(self.trans)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.talk = _translate('MainWindow', 'You are using GeoPyTool ') + version + '\n' + _translate('MainWindow',
                                                                                                       'released on ') + date + '\n'

        self.menuFile.setTitle(_translate('MainWindow', u'Data File'))
        self.menuGeoChem.setTitle(_translate('MainWindow', u'Geochemistry'))
        self.menuGeoCalc.setTitle(_translate('MainWindow', u'Calculation'))
        self.menuStructure.setTitle(_translate('MainWindow', u'Structure'))
        self.menuSedimentary.setTitle(_translate('MainWindow', u'Sedimentary'))
        self.menuAdditional.setTitle(_translate('MainWindow', u'Additional'))
        self.menuMachineLearn.setTitle(_translate('MainWindow', u'MachineLearn'))
        self.menuHelp.setTitle(_translate('MainWindow', u'Help'))
        self.menuLanguage.setTitle(_translate('MainWindow', u'Language'))

        self.actionCombine.setText(_translate('MainWindow', u'Combine'))
        self.actionCombine_transverse.setText(_translate('MainWindow', u'Combine_transverse'))

        self.actionFlatten.setText(_translate('MainWindow', u'Flatten'))

        self.actionTrans.setText(_translate('MainWindow', u'Trans'))

        self.actionReFormat.setText(_translate('MainWindow', u'ReFormat'))

        self.actionOpen.setText(_translate('MainWindow', u'Open Data'))
        self.actionClose.setText(_translate('MainWindow', u'Close Data'))
        self.actionSet.setText(_translate('MainWindow', u'Set Format'))
        self.actionFillNaN.setText(_translate('MainWindow', u'Fill Blank with 0'))
        self.actionSave.setText(_translate('MainWindow', u'Save Data'))
        self.actionQuit.setText(_translate('MainWindow', u'Quit App'))

        self.actionRemoveLOI.setText('1-0 ' + _translate('MainWindow', u'Remove LOI'))
        self.actionAuto.setText('1-1 ' + _translate('MainWindow', u'Auto'))
        self.actionTAS.setText('1-2 ' + _translate('MainWindow', u'TAS'))
        self.actionTrace.setText('1-3 ' + _translate('MainWindow', u'Trace'))
        self.actionRee.setText('1-4 ' + _translate('MainWindow', u'REE'))
        self.actionPearce.setText('1-5 ' + _translate('MainWindow', u'Pearce'))
        self.actionHarker.setText('1-6 ' + _translate('MainWindow', u'Harker'))
        self.actionCIPW.setText('1-7 ' + _translate('MainWindow', u'CIPW'))
        # self.actionNiggli.setText('1-8 '+_translate('MainWindow',u'Niggli'))
        self.actionQAPF.setText('1-9 ' + _translate('MainWindow', u'QAPF'))
        self.actionSaccani.setText('1-10 ' + _translate('MainWindow', u'Saccani Plot'))
        self.actionK2OSiO2.setText('1-11 ' + _translate('MainWindow', u'K2O-SiO2'))
        self.actionRaman.setText('1-12 ' + _translate('MainWindow', u'Raman Strength'))
        self.actionFluidInclusion.setText('1-13 ' + _translate('MainWindow', u'Fluid Inclusion'))
        self.actionHarkerOld.setText('1-14 ' + _translate('MainWindow', u'Harker Classical'))
        self.actionTraceNew.setText('1-15 ' + _translate('MainWindow', u'TraceNew'))
        self.actionZrYSrTi.setText('1-16 ' + _translate('MainWindow', u'ZrYSrTi'))
        self.actionTiAlCaMgMnKNaSi.setText('1-17 ' + _translate('MainWindow', u'TiAlCaMgMnKNaSi'))

        self.actionStereo.setText('2-1 ' + _translate('MainWindow', u'Stereo'))
        self.actionRose.setText('2-2 ' + _translate('MainWindow', u'Rose'))

        self.actionQFL.setText('3-1 ' + _translate('MainWindow', u'QFL'))
        self.actionQmFLt.setText('3-2 ' + _translate('MainWindow', u'QmFLt'))
        self.actionClastic.setText('3-3 ' + _translate('MainWindow', u'Clastic(sand-silt-clay)'))
        self.actionCIA.setText('3-4 ' + _translate('MainWindow', u'CIA/ICV/PIA/CIW/CIW\''))

        self.actionZirconCe.setText('4-1 ' + _translate('MainWindow', u'ZirconCe'))
        self.actionZirconCeOld.setText('4-2 ' + _translate('MainWindow', u'ZirconCeOld'))
        self.actionZirconTiTemp.setText('4-3 ' + _translate('MainWindow', u'ZirconTiTemp'))
        self.actionRutileZrTemp.setText('4-4 ' + _translate('MainWindow', u'RutileZrTemp'))
        self.actionRbSrIsoTope.setText('4-5 ' + _translate('MainWindow', u'Rb-Sr IsoTope'))
        self.actionSmNdIsoTope.setText('4-6 ' + _translate('MainWindow', u'Sm-Nd IsoTope'))
        # self.actionKArIsoTope.setText(_translate('MainWindow',u'K-Ar IsoTope'))

        self.actionXY.setText('5-1 ' + _translate('MainWindow', u'X-Y plot'))
        self.actionXYZ.setText('5-2 ' + _translate('MainWindow', u'X-Y-Z plot'))
        self.actionCluster.setText('5-3 ' + _translate('MainWindow', u'Cluster'))
        self.actionMultiDimension.setText('5-4 ' + _translate('MainWindow', u'MultiDimension'))

        self.actionDist.setText('5-5 ' + _translate('MainWindow', u'Distance'))

        self.actionStatistics.setText('5-6 ' + _translate('MainWindow', u'Statistics'))

        self.actionThreeD.setText('5-7 ' + _translate('MainWindow', u'ThreeD'))
        self.actionTwoD.setText('5-8 ' + _translate('MainWindow', u'TwoD'))
        self.actionTwoD_Grey.setText('5-9 ' + _translate('MainWindow', u'TwoD Grey'))

        self.actionMyHist.setText('5-10 ' + _translate('MainWindow', u'Histogram + KDE Curve'))
        self.actionPie.setText('5-11 ' + _translate('MainWindow', u'Pie Chart'))
        self.actionBar.setText('5-12 ' + _translate('MainWindow', u'Bar Chart'))

        self.actionDT.setText('6-1 ' + _translate('MainWindow', u'DT'))
        self.actionFA.setText('6-2 ' + _translate('MainWindow', u'FA'))
        self.actionLDA.setText('6-3 ' + _translate('MainWindow', u'LDA'))
        self.actionPCA.setText('6-4 ' + _translate('MainWindow', u'PCA'))
        self.actionMLP.setText('6-5 ' + _translate('MainWindow', u'MLP'))
        self.actionGAN.setText('6-6 ' + _translate('MainWindow', u'GAN'))

        self.actionVersionCheck.setText(_translate('MainWindow', u'Check Update'))
        self.actionWeb.setText(_translate('MainWindow', u'English Forum'))
        self.actionGoGithub.setText(_translate('MainWindow', u'Github'))

        '''
        self.actionCnS.setText(_translate('MainWindow',u'Simplified Chinese'))
        self.actionCnT.setText(_translate('MainWindow', u'Traditional Chinese'))
        self.actionEn.setText(_translate('MainWindow',u'English'))
        '''

        self.actionCnS.setText(u'简体中文')
        self.actionCnT.setText(u'繁體中文')
        self.actionEn.setText(u'English')
        self.actionLoadLanguage.setText(_translate('MainWindow', u'Load Language'))

    def goGitHub(self):
        webbrowser.open('https://github.com/GeoPyTool/GeoPyTool')

    def goDiscussion(self):
        webbrowser.open('https://github.com/GeoPyTool/GeoPyTool/discussions')

    def checkVersion(self):

        # reply = QMessageBox.information(self, 'Version', self.talk)

        _translate = QtCore.QCoreApplication.translate

        url = 'https://gitlab.com/cycleuser/GeoPyTool/-/raw/master/geopytool/CustomClass.py'

        r = 0
        try:
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            NewVersion = 'self.target' + r.text.splitlines()[0]

        except requests.exceptions.ConnectionError as err:
            print(err)
            r = 0
            buttonReply = QMessageBox.information(self, _translate('MainWindow', u'NetWork Error'),
                                                  _translate('MainWindow',
                                                             'You are using GeoPyTool ') + version + '\n' + 'Net work unavailable.')
            NewVersion = "targetversion = '0'"

        except requests.exceptions.HTTPError as err:
            print(err)
            r = 0
            buttonReply = QMessageBox.information(self, _translate('MainWindow', u'NetWork Error'),
                                                  _translate('MainWindow',
                                                             'You are using GeoPyTool ') + version + '\n' + 'Net work unavailable.')
            NewVersion = "targetversion = '0'"

        exec(NewVersion)
        print('web is', self.targetversion)
        print(NewVersion)

        self.talk = _translate('MainWindow', 'Version Online is ') + self.targetversion + '\n' + _translate(
            'MainWindow', 'You are using GeoPyTool ') + version + '\n' + _translate('MainWindow',
                                                                                    'released on ') + date + '\n'

        if r != 0:

            print('now is', version)
            if (version < self.targetversion):

                buttonReply = QMessageBox.question(self, _translate('MainWindow', u'Version'),
                                                   self.talk + _translate('MainWindow',
                                                                          'New version available.\n Download and update?'),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    print('Yes clicked.')
                    # qApp.quit
                    # pip.main(['install', 'geopytool', '--upgrade --no-cache-dir'])

                    # self.UpDate

                    webbrowser.open('https://github.com/chinageology/GeoPyTool/blob/master/Download.md')
                else:
                    print('No clicked.')
            else:
                buttonReply = QMessageBox.information(self, _translate('MainWindow', u'Version'),
                                                      self.talk + _translate('MainWindow',
                                                                             'This is the latest version.'))

    def Update(self):
        # webbrowser.open('https://github.com/chinageology/GeoPyTool/wiki/Download')
        pip.main(['install', 'geopytool', '--upgrade'])

    def ReadConfig(self):
        if (os.path.isfile('config.ini')):

            try:
                with open('config.ini', 'rt') as f:
                    try:
                        data = f.read()
                    except:
                        data = 'Language = \'en\''
                        pass

                    print(data)
                    try:
                        print("self." + data)
                        exec("self." + data)
                    except:
                        pass
                    print(self.Language)


            except():
                pass

    def WriteConfig(self, text=LocationOfMySelf + '/en'):
        try:
            with open('config.ini', 'wt') as f:
                f.write(text)
        except():
            pass

    def to_ChineseS(self):

        self.trans.load(LocationOfMySelf + '/cns')
        self.app.installTranslator(self.trans)
        self.retranslateUi()

        self.WriteConfig('Language = \'cns\'')

    def to_ChineseT(self):

        self.trans.load(LocationOfMySelf + '/cnt')
        self.app.installTranslator(self.trans)
        self.retranslateUi()

        self.WriteConfig('Language = \'cnt\'')

    def to_English(self):

        self.trans.load(LocationOfMySelf + '/en')
        self.app.installTranslator(self.trans)
        self.retranslateUi()
        self.WriteConfig('Language = \'en\'')

    def to_LoadLanguage(self):

        _translate = QtCore.QCoreApplication.translate
        fileName, filetype = QFileDialog.getOpenFileName(self, _translate('MainWindow', u'Choose Language File'),
                                                         '~/',
                                                         'Language Files (*.qm)')  # 设置文件扩展名过滤,注意用双分号间隔

        print(fileName)

        self.trans.load(fileName)
        self.app.installTranslator(self.trans)
        self.retranslateUi()

    def ErrorEvent(self, text=''):

        if (text == ''):
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Function.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))
        else:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Function.\n Error infor is:') + text)

    def SetUpDataFile(self):
        flag = 0
        ItemsAvalibale = self.model._df.columns.values.tolist()

        ItemsToTest = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width', 'Index']

        LabelList = []
        MarkerList = []
        ColorList = []
        SizeList = []
        AlphaList = []
        StyleList = []
        WidthList = []
        IndexList = []

        for i in range(len(self.model._df)):
            LabelList.append('Group1')
            MarkerList.append('o')
            ColorList.append('red')
            SizeList.append(10)
            AlphaList.append(0.6)
            StyleList.append('-')
            WidthList.append(1)
            IndexList.append(i + 1)

        data = {'Label': LabelList,
                'Index': IndexList,
                'Marker': MarkerList,
                'Color': ColorList,
                'Size': SizeList,
                'Alpha': AlphaList,
                'Style': StyleList,
                'Width': WidthList}

        for i in ItemsToTest:
            if i not in ItemsAvalibale:
                # print(i)
                flag = flag + 1
                tmpdftoadd = pd.DataFrame({i: data[i]})

                self.model._df = pd.concat([tmpdftoadd, self.model._df], axis=1)

        self.model = PandasModel(self.model._df)

        self.tableView.setModel(self.model)

        if flag == 0:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Ready'),
                                            _translate('MainWindow', 'Everything fine and no need to set up.'))

        else:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Ready'),
                                            _translate('MainWindow',
                                                       'Items added, Modify in the Table to set up details.'))

    def FillNaN(self):

        if (len(self.model._df) <= 0):
            self.getDataFile()
            pass

        if (len(self.model._df) > 0):
            self.model._df = self.model._df.fillna(0)
            self.model = PandasModel(self.model._df)
            self.tableView.setModel(self.model)
            reply = QMessageBox.information(self, _translate('MainWindow', 'Ready'),
                                            _translate('MainWindow', 'Blanks are now filled with 0s.'))

    def clearDataFile(self):
        self.raw = pd.DataFrame()
        self.model = PandasModel(self.raw)
        self.tableView.setModel(self.model)

    def getDataFiles(self, limit=6):
        print('get Multiple Data Files  called \n')
        DataFilesInput, filetype = QFileDialog.getOpenFileNames(self, u'Choose Data File',
                                                                '~/',
                                                                'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        # print(DataFileInput,filetype)

        DataFramesList = []

        if len(DataFilesInput) >= 1:
            for i in range(len(DataFilesInput)):
                if i < limit:
                    if ('csv' in DataFilesInput[i]):
                        DataFramesList.append(pd.read_csv(DataFilesInput[i], engine='python'))
                    elif ('xls' in DataFilesInput[i]):
                        DataFramesList.append(pd.read_excel(DataFilesInput[i]),engine='openpyxl')
                else:
                    # self.ErrorEvent(text='You can only open up to 6 Data Files at a time.')
                    pass

        return (DataFramesList, DataFilesInput)

    def getDataFile(self, CleanOrNot=True):
        _translate = QtCore.QCoreApplication.translate

        DataFileInput, filetype = QFileDialog.getOpenFileName(self, _translate('MainWindow', u'Choose Data File'),
                                                              '~/',
                                                              'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        # #print(DataFileInput,filetype)

        self.DataLocation = DataFileInput
        print(self.DataLocation)

        if ('csv' in DataFileInput):
            self.raw = pd.read_csv(DataFileInput, engine='python')
        elif ('xls' in DataFileInput):
            self.raw = pd.read_excel(DataFileInput,engine='openpyxl')
        # #print(self.raw)

        if len(self.raw) > 0:
            self.model = PandasModel(self.raw)
            # print(self.model._df)

            self.tableView.setModel(self.model)
            self.model = PandasModel(self.raw)
            # print(self.model._df)

            flag = 0
            ItemsAvalibale = self.model._df.columns.values.tolist()
            ItemsToTest = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
            for i in ItemsToTest:
                if i not in ItemsAvalibale:
                    # print(i)
                    flag = flag + 1

            if flag == 0:
                pass
                # reply = QMessageBox.information(self, _translate('MainWindow', 'Ready'), _translate('MainWindow', 'Everything fine and no need to set up.'))

            else:
                pass
                # self.SetUpDataFile()

    def getFileName(self, list=['C:/Users/Fred/Documents/GitHub/Writing/元素数据/Ag.xlsx']):
        result = []
        for i in list:
            result.append(i.split("/")[-1].split(".")[0])
        return (result)

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # #print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self, _translate('MainWindow', u'Save Data File'),
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        dftosave = self.model._df

        # self.model._df.reset_index(drop=True)

        if "Label" in dftosave.columns.values.tolist():
            dftosave = dftosave.set_index('Label')

        if (DataFileOutput != ''):

            dftosave.reset_index(drop=True)

            if ('csv' in DataFileOutput):
                dftosave.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):

                dftosave.to_excel(DataFileOutput, encoding='utf-8')

    def OldCombine(self):

        print('Combine called \n')

        pass

        DataFilesInput, filetype = QFileDialog.getOpenFileNames(self, _translate('MainWindow', u'Choose Data File'),
                                                                '~/',
                                                                'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        # #print(DataFileInput,filetype)

        DataFramesList = []

        if len(DataFilesInput) > 1:
            for i in DataFilesInput:
                if ('csv' in i):
                    DataFramesList.append(pd.read_csv(i), engine='python')
                elif ('xls' in i):
                    DataFramesList.append(pd.read_excel(i),engine='openpyxl')
                pass

        # result = pd.concat(DataFramesList,axis=1,sort=False)

        result = pd.concat(DataFramesList, ignore_index=True, sort=False)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self, _translate('MainWindow', u'Save Data File'),
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        dftosave = result
        if (DataFileOutput != ''):
            dftosave.reset_index(drop=True)
            if ('csv' in DataFileOutput):
                dftosave.to_csv(DataFileOutput, sep=',', encoding='utf-8')
            elif ('xls' in DataFileOutput):
                dftosave.to_excel(DataFileOutput, encoding='utf-8')

    def Combine(self):

        print('Combine called \n')

        pass

        DataFilesInput, filetype = QFileDialog.getOpenFileNames(self, _translate('MainWindow', u'Choose Data File'),
                                                                '~/',
                                                                'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        # #print(DataFileInput,filetype)

        DataFramesList = []

        if len(DataFilesInput) > 1:
            for i in DataFilesInput:
                if ('csv' in i):
                    DataFramesList.append(pd.read_csv(i, engine='python'))
                elif ('xls' in i):
                    DataFramesList.append(pd.read_excel(i),engine='openpyxl')
                pass

            # result = pd.concat(DataFramesList,axis=1,sort=False)

            result = pd.concat(DataFramesList, ignore_index=True, sort=False)

            print('self.model._df length: ', len(result))

            if (len(result) > 0):
                self.Combinepop = MyCombine(df=result)
                self.Combinepop.Combine()

    def getFileName(self, list=['C:/Users/Fred/Documents/GitHub/Writing/元素数据/Ag.xlsx']):
        result = []
        for i in list:
            result.append(i.split("/")[-1].split(".")[0])
        # print(result)
        return (result)

    def Combine_transverse(self):
        print('Combine called \n')
        DataFilesInput, filetype = QFileDialog.getOpenFileNames(self, _translate('MainWindow', u'Choose Data File'),
                                                                '~/',
                                                                'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        DataFramesList = []
        filenamelist = self.getFileName(DataFilesInput)
        if len(DataFilesInput) > 1:
            for i in range(len(DataFilesInput)):
                tmpdf = pd.DataFrame()
                if ('csv' in DataFilesInput[i]):
                    tmpdf = pd.read_csv(DataFilesInput[i], engine='python')
                elif ('xls' in DataFilesInput[i]):
                    tmpdf = pd.read_excel(DataFilesInput[i],engine='openpyxl')
                # name_list = tmpdf.columns.values.tolist()
                tmpname_dic = {}
                tmpname_list = []
                oldname_list = tmpdf.columns.values.tolist()
                for k in oldname_list:
                    tmpname_list.append(filenamelist[i] + k)
                    tmpname_dic[k] = filenamelist[i] + ' ' + k
                print(tmpname_dic)
                tmpdf = tmpdf.rename(index=str, columns=tmpname_dic)
                DataFramesList.append(tmpdf)
            # result = pd.concat(DataFramesList,axis=1,sort=False)
            result = pd.concat(DataFramesList, axis=1, ignore_index=False, sort=False)
            print('self.model._df length: ', len(result))
            if (len(result) > 0):
                self.Combinepop = MyCombine(df=result)
                self.Combinepop.Combine()

    def Flatten(self):

        print('Flatten called \n')
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) <= 0):
            self.getDataFile()
            pass

        if (len(self.model._df) > 0):
            self.flattenpop = MyFlatten(df=self.model._df)
            self.flattenpop.Flatten()

    def Trans(self):

        print('Trans called \n')
        if (len(self.model._df) <= 0):
            self.getDataFile()
            pass
        if (len(self.model._df) > 0):
            self.transpop = MyTrans(df=self.model._df)
            self.transpop.Trans()

    def ReFormat(self):
        print('ReFormat called \n')

        Datas = self.getDataFiles()

    def RemoveLOI(self):

        _translate = QtCore.QCoreApplication.translate

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        self.model._df_back = self.model._df

        if (len(self.model._df) > 0):

            loi_list = ['LOI', 'loi', 'Loi']
            all_list = ['Total', 'total', 'TOTAL', 'ALL', 'All', 'all']
            itemstocheck = ['Total', 'total', 'TOTAL', 'ALL', 'All', 'all', 'Al2O3', 'MgO', 'FeO', 'Fe2O3', 'CaO',
                            'Na2O', 'K2O', 'TiO2', 'P2O5', 'SiO2', 'TFe2O3', 'MnO', 'TFeO']

            for i in range(len(self.model._df)):
                Loi_flag = False

                for k in all_list:
                    if k in self.model._df.columns.values:
                        de_loi = self.model._df.iloc[i][k]
                        for m in itemstocheck:
                            if m in self.model._df.columns.values:
                                self.model._df.at[i, m] = 100 * self.model._df.at[i, m] / de_loi
                        Loi_flag = True
                        break
                    else:
                        Loi_flag = False

                for j in loi_list:
                    if Loi_flag == False:
                        if j in self.model._df.columns.values:
                            de_loi = 100 - self.model._df.iloc[i][k]
                            for m in itemstocheck:
                                if m in self.model._df.columns.values:
                                    self.model._df.at[i, m] = 100 * self.model._df.at[i, m] / de_loi

                                    Loi_flag = True
                                    break
                                else:
                                    Loi_flag = False

                if Loi_flag == False:
                    tmp_all = 0
                    for m in itemstocheck:
                        if m in self.model._df.columns.values:
                            tmp_all = tmp_all + self.model._df.at[i, m]
                    if round(tmp_all) != 100:
                        print(tmp_all)
                        for m in itemstocheck:
                            if m in self.model._df.columns.values:
                                self.model._df.at[i, m] = 100 * self.model._df.at[i, m] / tmp_all

            reply = QMessageBox.information(self, _translate('MainWindow', 'Done'), _translate('MainWindow',
                                                                                               'LOI has been removed!:'))

    def TAS(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.taspop = TAS(df=self.model._df)

            self.taspop.TAS()
            self.taspop.show()

            try:
                self.taspop.TAS()
                self.taspop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Saccani(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.sacpop = Saccani(df=self.model._df)

            try:
                self.sacpop.Saccani()
                self.sacpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Raman(self):

        print('self.model._df length: ', len(self.raw))
        if (len(self.raw) <= 0):
            self.getDataFile()

        if (len(self.raw) > 0):
            self.ramanpop = Raman(df=self.raw, filename=self.DataLocation)
            try:
                self.ramanpop.Raman()
                self.ramanpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def FluidInclusion(self):
        print('self.model._df length: ', len(self.raw))
        if (len(self.raw) <= 0):
            self.getDataFile()

        if (len(self.raw) > 0):
            self.FluidInclusionpop = FluidInclusion(df=self.raw, filename=self.DataLocation)

            try:
                self.FluidInclusionpop.FluidInclusion()
                self.FluidInclusionpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def MyHist(self):

        print('self.model._df length: ', len(self.raw))
        if (len(self.raw) <= 0):
            self.getDataFile()

        if (len(self.raw) > 0):
            self.MyHistpop = MyHist(df=self.raw, filename=self.DataLocation)
            try:
                self.MyHistpop.MyHist()
                self.MyHistpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def MyPie(self):
        print('self.model._df length: ', len(self.raw))
        if (len(self.raw) <= 0):
            self.getDataFile()
        if (len(self.raw) > 0):
            self.MyPiepop = Pie(df=self.raw)
            try:
                self.MyPiepop.Magic()
                self.MyPiepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def MyBar(self):
        print('self.model._df length: ', len(self.raw))
        if (len(self.raw) <= 0):
            self.getDataFile()
        if (len(self.raw) > 0):
            self.MyBarpop = Bar(df=self.raw)
            try:
                self.MyBarpop.Magic()
                self.MyBarpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def REE(self):

        print('self.model._df length: ', len(self.model._df))

        if len(self.Standard) > 0:
            print('self.Standard length: ', len(self.Standard))

        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):

            self.reepop = REE(df=self.model._df, Standard=self.Standard)
            try:
                self.reepop.REE()
                self.reepop.show()

            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Trace(self):

        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.tracepop = Trace(df=self.model._df, Standard=self.Standard)
            try:
                self.tracepop.Trace()
                self.tracepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def TraceNew(self):

        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.TraceNewpop = TraceNew(df=self.model._df, Standard=self.Standard)
            try:
                self.TraceNewpop.Trace()
                self.TraceNewpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Pearce(self):

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.pearcepop = Pearce(df=self.model._df)

            try:
                self.pearcepop.Pearce()
                self.pearcepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Harker(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.harkerpop = Harker(df=self.model._df)
            try:
                self.harkerpop.Harker()
                self.harkerpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def HarkerOld(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.harkeroldpop = HarkerOld(df=self.model._df)
            try:
                self.harkeroldpop.HarkerOld()
                self.harkeroldpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def CIPW(self):

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.cipwpop = CIPW(df=self.model._df)

            try:
                self.cipwpop.CIPW()
                self.cipwpop.show()
            except():
                self.ErrorEvent()

    def Niggli(self):

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.Nigglipop = Niggli(df=self.model._df)

            try:
                self.Nigglipop.Niggli()
                self.Nigglipop.show()
            except():
                self.ErrorEvent()

    def ZirconTiTemp(self):

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.ztpop = ZirconTiTemp(df=self.model._df)
            try:
                self.ztpop.ZirconTiTemp()
                self.ztpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def RutileZrTemp(self):

        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rzpop = RutileZrTemp(df=self.model._df)
            try:
                self.rzpop.RutileZrTemp()
                self.rzpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Cluster(self):
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) <= 0):
            self.getDataFile()
            pass

        if (len(self.model._df) > 0):
            try:
                self.clusterpop = Cluster(df=self.model._df)
                self.clusterpop.Cluster()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Stereo(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.stereopop = Stereo(df=self.model._df)

            try:
                self.stereopop.Stereo()
                self.stereopop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Rose(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rosepop = Rose(df=self.model._df)
            try:
                self.rosepop.Rose()
                self.rosepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QFL(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.qflpop = QFL(df=self.model._df)
            try:
                self.qflpop.Tri()
                self.qflpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QmFLt(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.qmfltpop = QmFLt(df=self.model._df)
            try:
                self.qmfltpop.Tri()
                self.qmfltpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Clastic(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.clusterpop = Clastic(df=self.model._df)
            try:
                self.clusterpop.Tri()
                self.clusterpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def CIA(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.ciapop = CIA(df=self.model._df)

            try:
                self.ciapop.CIA()
                self.ciapop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QAPF(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            ItemsAvalibale = self.model._df.columns.values.tolist()
            if 'Q' in ItemsAvalibale and 'A' in ItemsAvalibale and 'P' in ItemsAvalibale and 'F' in ItemsAvalibale:
                self.qapfpop = QAPF(df=self.model._df)
                try:
                    self.qapfpop.QAPF()
                    self.qapfpop.show()
                except Exception as e:
                    self.ErrorEvent(text=repr(e))
            else:
                reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                      'Your data contain no Q/A/P/F data.\n Maybe you need to run CIPW first?'))

    def ZirconCe(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile(CleanOrNot=False)
        # print('Opening a new popup window...')

        if (len(self.model._df) > 0):
            self.zirconpop = ZirconCe(df=self.model._df)

            try:
                self.zirconpop.MultiBallard()
                self.zirconpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def ZirconCeOld(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile(CleanOrNot=False)
        # print('Opening a new popup window...')

        if (len(self.model._df) > 0):
            self.zirconoldpop = ZirconCeOld(df=self.model._df)
            try:
                self.zirconoldpop.MultiBallard()
                self.zirconoldpop.show()
            except(KeyError, ValueError, TypeError):
                self.ErrorEvent()

    def RbSrIsoTope(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rbsrisotopepop = IsoTope(df=self.model._df, description='Rb-Sr IsoTope diagram', xname='87Rb/86Sr',
                                          yname='87Sr/86Sr', lambdaItem=1.42e-11, xlabel=r'$^{87}Rb/^{86}Sr$',
                                          ylabel=r'$^{87}Sr/^{86}Sr$')
            try:
                self.rbsrisotopepop.Magic()
                self.rbsrisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def SmNdIsoTope(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.smndisotopepop = IsoTope(df=self.model._df, description='Sm-Nd IsoTope diagram', xname='147Sm/144Nd',
                                          yname='143Nd/144Nd', lambdaItem=6.54e-12, xlabel=r'$^{147}Sm/^{144}Nd$',
                                          ylabel=r'$^{143}Nd/^{144}Nd$')
            try:
                self.smndisotopepop.Magic()
                self.smndisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def KArIsoTope(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.karisotopepop = KArIsoTope(df=self.model._df)
            try:
                self.karisotopepop.Magic()
                self.karisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def K2OSiO2(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.K2OSiO2pop = K2OSiO2(df=self.model._df)
            try:
                self.K2OSiO2pop.K2OSiO2()
                self.K2OSiO2pop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def ZrYSrTi(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.ZrYSrTipop = ZrYSrTi(df=self.model._df)

            try:
                self.ZrYSrTipop.Key_Func()
                self.ZrYSrTipop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def TiAlCaMgMnKNaSi(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.TiAlCaMgMnKNaSipop = TiAlCaMgMnKNaSi(df=self.model._df)

            self.TiAlCaMgMnKNaSipop.Key_Func()
            self.TiAlCaMgMnKNaSipop.show()
            try:
                pass
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def XY(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.xypop = XY(df=self.model._df, Standard=self.Standard)
            try:
                self.xypop.Magic()
                self.xypop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def XYZ(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.xyzpop = XYZ(df=self.model._df, Standard=self.Standard)

            try:
                self.xyzpop.Magic()
                self.xyzpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def MultiDimension(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.mdpop = MultiDimension(df=self.model._df)
            try:
                self.mdpop.Magic()
                self.mdpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def ThreeD(self):

        print('ThreeD called \n')
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) > 0):
            self.ThreeDpop = MyThreeD(DataFiles=[self.model._df], DataLocation=[self.DataLocation])
            self.ThreeDpop.ThreeD()
        else:
            DataFiles, DataLocation = self.getDataFiles()

            print(len(DataFiles), len(DataLocation))

            if len(DataFiles) > 0:
                self.ThreeDpop = MyThreeD(DataFiles=DataFiles, DataLocation=DataLocation)
                self.ThreeDpop.ThreeD()

    def TwoD(self):
        print('TwoD called \n')
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) > 0):
            self.TwoDpop = MyTwoD(DataFiles=[self.model._df], DataLocation=[self.DataLocation])
            self.TwoDpop.TwoD()
        else:
            DataFiles, DataLocation = self.getDataFiles()

            print(len(DataFiles), len(DataLocation))

            if len(DataFiles) > 0:
                self.TwoDpop = MyTwoD(DataFiles=DataFiles, DataLocation=DataLocation)
                self.TwoDpop.TwoD()

    def TwoD_Grey(self):
        print('TwoD_Grey called \n')
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) > 0):
            self.TwoDpop = MyTwoD_Grey(DataFiles=[self.model._df], DataLocation=[self.DataLocation])
            self.TwoDpop.TwoD()
        else:
            DataFiles, DataLocation = self.getDataFiles()

            print(len(DataFiles), len(DataLocation))

            if len(DataFiles) > 0:
                self.TwoDpop = MyTwoD_Grey(DataFiles=DataFiles, DataLocation=DataLocation)
                self.TwoDpop.TwoD()

    def Dist(self):

        print('Dist called \n')

        if (len(self.model._df) <= 0):
            self.getDataFile()
            pass

        if (len(self.model._df) > 0):
            try:
                self.Distpop = MyDist(df=self.model._df)
                self.Distpop.Dist()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Sta(self):
        # Sta on Calculated Distance
        print('Sta called \n')
        print('self.model._df length: ', len(self.model._df))

        if (len(self.model._df) <= 0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            try:
                self.stapop = MySta(df=self.model._df)
                self.stapop.Sta()
            except Exception as e:
                tmp_msg = '\n This is to do Sta on Calculated Distance.\n'
                self.ErrorEvent(text=tmp_msg + repr(e))

    def FA(self):
        print('FA called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.fapop = MyFA(df=self.model._df.fillna(0))
            try:
                self.fapop.Key_Func()
                self.fapop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def PCA(self):
        print('PCA called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.pcapop = MyPCA(df=self.model._df.fillna(0))
            try:
                self.pcapop.Key_Func()
                self.pcapop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def LDA(self):
        print('LDA called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.ldapop = MyLDA(df=self.model._df.fillna(0))

            self.ldapop.Key_Func()
            self.ldapop.show()
            try:
                pass
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def DT(self):
        print('DT called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.dtpop = MyDT(df=self.model._df.fillna(0))
            try:
                self.dtpop.Key_Func()
                self.dtpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def MLP(self):
        print('MLP called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.MLPpop = MyMLP(df=self.model._df.fillna(0))
            try:
                self.MLPpop.Key_Func()
                self.MLPpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def GAN(self):
        print('GAN called \n')
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.GANpop = MyGAN(df=self.model._df.fillna(0))

            self.GANpop.Key_Func()
            self.GANpop.show()

            try:
                self.GANpop.Key_Func()
                self.GANpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Tri(self):
        pass

    def Auto(self):
        print('self.model._df length: ', len(self.model._df))
        if (len(self.model._df) <= 0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            TotalResult = []
            df = self.model._df
            AutoResult = 0
            FileOutput, ok1 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'PDF Files (*.pdf)')  # 数据文件保存输出
            if (FileOutput != ''):

                AutoResult = pd.DataFrame()

                pdf = matplotlib.backends.backend_pdf.PdfPages(FileOutput)

                cipwsilent = CIPW(df=df)
                cipwsilent.CIPW()
                cipwsilent.QAPFsilent()
                # TotalResult.append(cipwsilent.OutPutFig)
                pdf.savefig(cipwsilent.OutPutFig)

                # AutoResult = pd.concat([cipwsilent.OutPutData, AutoResult], axis=1)

                tassilent = TAS(df=df)

                tassilent.TAS()
                tassilent.GetResult()
                # TotalResult.append(tassilent.OutPutFig)

                pdf.savefig(tassilent.OutPutFig)

                AutoResult = pd.concat([tassilent.OutPutData, AutoResult], axis=1)

                reesilent = REE(df=df, Standard=self.Standard)

                if (reesilent.Check() == True):
                    reesilent.REE()
                    reesilent.GetResult()
                    # TotalResult.append(reesilent.OutPutFig)

                    pdf.savefig(reesilent.OutPutFig)

                    AutoResult = pd.concat([reesilent.OutPutData, AutoResult], axis=1)

                tracesilent = Trace(df=df, Standard=self.Standard)

                if (tracesilent.Check() == True):
                    tracesilent.Trace()
                    tracesilent.GetResult()
                    TotalResult.append(tracesilent.OutPutFig)

                    pdf.savefig(tracesilent.OutPutFig)

                harkersilent = Harker(df=df)

                harkersilent.Harker()
                harkersilent.GetResult()
                TotalResult.append(harkersilent.OutPutFig)

                pdf.savefig(harkersilent.OutPutFig)

                pearcesilent = Pearce(df=df)

                pearcesilent.Pearce()
                pearcesilent.GetResult()
                TotalResult.append(pearcesilent.OutPutFig)

                pdf.savefig(pearcesilent.OutPutFig)

                AutoResult = AutoResult.T.groupby(level=0).first().T

                pdf.close()

                AutoResult = AutoResult.set_index('Label')

                AutoResult = AutoResult.drop_duplicates()

                print(AutoResult.shape, cipwsilent.newdf3.shape)

                try:
                    AutoResult = pd.concat([cipwsilent.newdf3, AutoResult], axis=1)
                except(ValueError):
                    pass

                if ('pdf' in FileOutput):
                    FileOutput = FileOutput[0:-4]

                AutoResult.to_csv(FileOutput + '-chemical-info.csv', sep=',', encoding='utf-8')
                cipwsilent.newdf.to_csv(FileOutput + '-cipw-mole.csv', sep=',', encoding='utf-8')
                cipwsilent.newdf1.to_csv(FileOutput + '-cipw-mass.csv', sep=',', encoding='utf-8')
                cipwsilent.newdf2.to_csv(FileOutput + '-cipw-volume.csv', sep=',', encoding='utf-8')
                cipwsilent.newdf3.to_csv(FileOutput + '-cipw-index.csv', sep=',', encoding='utf-8')



            else:
                pass


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    trans = QtCore.QTranslator()
    # trans.load('cn')  # 没有后缀.qm
    app.installTranslator(trans)
    mainWin = Ui_MainWindow()
    mainWin.retranslateUi()
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
