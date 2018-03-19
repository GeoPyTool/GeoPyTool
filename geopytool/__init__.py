#!/usr/bin/python3
# coding:utf-8

from geopytool.ImportDependence import *
from geopytool.CustomClass import *


LocationOfMySelf=os.path.dirname(__file__)

print(LocationOfMySelf,' init')


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

from geopytool.TabelViewer import TabelViewer
from geopytool.CIPW import CIPW
from geopytool.Cluster import Cluster
from geopytool.Bivariate import Bivariate
from geopytool.Harker import Harker
#from geopytool.Magic import Magic

from geopytool.Clastic import Clastic

from geopytool.IsoTope import IsoTope

from geopytool.MultiDimension import MultiDimension
from geopytool.Pearce import Pearce
from geopytool.QAPF import QAPF
from geopytool.QFL import QFL
from geopytool.QmFLt import QmFLt
from geopytool.REE import REE
from geopytool.Rose import Rose
from geopytool.Stereo import Stereo
from geopytool.TAS import TAS
from geopytool.Temp import *
from geopytool.Trace import Trace
from geopytool.XY import XY
from geopytool.XYZ import XYZ
from geopytool.ZirconCe import ZirconCe

from geopytool.Magic import Magic

# Create a custom "QProxyStyle" to enlarge the QMenu icons
#-----------------------------------------------------------
class MyProxyStyle(QProxyStyle):
    pass
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 24
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)



class Ui_MainWindow(QtWidgets.QMainWindow):
    # raw=0
    raw = pd.DataFrame(index=[], columns=[])  # raw is initialized as a blank dataframe

    Language = ''

    app = QtWidgets.QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')    # The proxy style should be based on an existing style,
                                        # like 'Windows', 'Motif', 'Plastique', 'Fusion', ...
    app.setStyle(myStyle)

    trans = QtCore.QTranslator()

    talk=''

    targetversion = '0'


    DataLocation =''

    ChemResult=pd.DataFrame()
    AutoResult=pd.DataFrame()

    TotalResult=[]



    def __init__(self):


        super(Ui_MainWindow, self).__init__()
        self.setObjectName('MainWindow')
        self.resize(800, 600)


        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', u'GeoPyTool'))
        self.setWindowIcon(QIcon(LocationOfMySelf+'/geopytool.png'))
        self.talk=  _translate('MainWindow','You are using GeoPyTool ') + version +'\n'+  _translate('MainWindow','released on ') + date

        self.model = PandasModel(self.raw)

        self.main_widget = QWidget(self)

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName('centralwidget')
        self.setCentralWidget(self.centralwidget)

        self.tableView = CustomQTableView(self.centralwidget)

        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.pushButtonOpen = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonOpen.setObjectName('pushButtonOpen')

        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setObjectName('pushButtonSave')

        self.pushButtonSort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSort.setObjectName('pushButtonSort')

        self.pushButtonQuit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonQuit.setObjectName('pushButtonQuit')

        self.pushButtonUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonUpdate.setObjectName('pushButtonUpdate')



        w=self.width()
        h=self.height()


        if h<360:
            h=360
            self.resize(w,h)

        if w<640:
            w = 640
            self.resize(w, h)

        step = (w * 94 / 100) / 5
        foot=h*3/48


        #if foot<=10: foot=10

        self.tableView.setGeometry(QtCore.QRect(w/100, h/48, w*98/100, h*38/48))

        self.pushButtonOpen.setGeometry(QtCore.QRect(w/100, h*40/48, step, foot))

        self.pushButtonSave.setGeometry(QtCore.QRect(2*w/100+step, h*40/48, step, foot))

        self.pushButtonSort.setGeometry(QtCore.QRect(3*w/100+step*2, h*40/48, step, foot))

        self.pushButtonQuit.setGeometry(QtCore.QRect(4*w/100+step*3, h*40/48, step, foot))

        self.pushButtonUpdate.setGeometry(QtCore.QRect(5*w/100+step*4, h*40/48, step, foot))

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


        self.menuDIY = QtWidgets.QMenu(self.menubar)
        self.menuDIY.setObjectName('menuDIY')

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName('menuHelp')

        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName('menuLanguage')

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName('statusbar')
        self.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(QIcon(LocationOfMySelf+'/open.png'), u'Open',self)
        self.actionOpen.setObjectName('actionOpen')
        self.actionOpen.setShortcut('Ctrl+O')

        self.actionSave = QtWidgets.QAction(QIcon(LocationOfMySelf+'/save.png'), u'Save',self)
        self.actionSave.setObjectName('actionSave')
        self.actionSave.setShortcut('Ctrl+S')

        self.actionCnWeb = QtWidgets.QAction(QIcon(LocationOfMySelf+'/forum.png'), u'Chinese Forum',self)
        self.actionCnWeb.setObjectName('actionCnWeb')

        self.actionEnWeb = QtWidgets.QAction(QIcon(LocationOfMySelf+'/forum.png'), u'English Forum',self)
        self.actionEnWeb.setObjectName('actionEnWeb')

        self.actionGoGithub = QtWidgets.QAction(QIcon(LocationOfMySelf+'/github.png'), u'GitHub',self)
        self.actionGoGithub.setObjectName('actionGoGithub')

        self.actionVersionCheck = QtWidgets.QAction(QIcon(LocationOfMySelf+'/update.png'), u'Version',self)
        self.actionVersionCheck.setObjectName('actionVersionCheck')


        self.actionCnS = QtWidgets.QAction(QIcon(LocationOfMySelf+'/cns.png'), u'Simplified Chinese',self)
        self.actionCnS.setObjectName('actionCnS')

        self.actionCnT = QtWidgets.QAction(QIcon(LocationOfMySelf+'/cnt.png'), u'Traditional Chinese',self)
        self.actionCnT.setObjectName('actionCnT')

        self.actionEn = QtWidgets.QAction(QIcon(LocationOfMySelf+'/en.png'), u'English',self)
        self.actionEn.setObjectName('actionEn')

        self.actionLoadLanguage = QtWidgets.QAction(QIcon(LocationOfMySelf+'/lang.png'), u'Load Language',self)
        self.actionLoadLanguage.setObjectName('actionLoadLanguage')

        self.actionTAS = QtWidgets.QAction(QIcon(LocationOfMySelf+'/xy.png'), u'TAS',self)
        self.actionTAS.setObjectName('actionTAS')

        self.actionTrace = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider2.png'), u'Trace',self)
        self.actionTrace.setObjectName('actionTrace')

        self.actionRee = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider2.png'), u'Ree',self)
        self.actionRee.setObjectName('actionRee')

        self.actionPearce = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider.png'),u'Pearce',self)
        self.actionPearce.setObjectName('actionPearce')

        self.actionBivariate = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider.png'),u'Bivariate',self)
        self.actionBivariate.setObjectName('actionBivariate')

        self.actionHarker = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider.png'),u'Harker',self)
        self.actionHarker.setObjectName('actionHarker')

        self.actionStereo = QtWidgets.QAction(QIcon(LocationOfMySelf+'/structure.png'),u'Stereo',self)
        self.actionStereo.setObjectName('actionStereo')

        self.actionRose = QtWidgets.QAction(QIcon(LocationOfMySelf+'/rose.png'),u'Rose',self)
        self.actionRose.setObjectName('actionRose')

        self.actionQFL = QtWidgets.QAction(QIcon(LocationOfMySelf+'/triangular.png'),u'QFL',self)
        self.actionQFL.setObjectName('actionQFL')

        self.actionQmFLt = QtWidgets.QAction(QIcon(LocationOfMySelf+'/triangular.png'),u'QmFLt',self)
        self.actionQmFLt.setObjectName('actionQmFLt')

        self.actionCIPW = QtWidgets.QAction(QIcon(LocationOfMySelf+'/calc.png'),u'CIPW',self)
        self.actionCIPW.setObjectName('actionCIPW')

        self.actionZirconCe = QtWidgets.QAction(QIcon(LocationOfMySelf+'/calc.png'),u'ZirconCe',self)
        self.actionZirconCe.setObjectName('actionZirconCe')

        self.actionZirconTiTemp = QtWidgets.QAction(QIcon(LocationOfMySelf+'/temperature.png'),u'ZirconTiTemp',self)
        self.actionZirconTiTemp.setObjectName('actionZirconTiTemp')

        self.actionRutileZrTemp = QtWidgets.QAction(QIcon(LocationOfMySelf+'/temperature.png'),u'RutileZrTemp',self)
        self.actionRutileZrTemp.setObjectName('actionRutileZrTemp')

        self.actionCluster = QtWidgets.QAction(QIcon(LocationOfMySelf+'/cluster.png'),u'Cluster',self)
        self.actionCluster.setObjectName('actionCluster')

        self.actionAuto = QtWidgets.QAction(QIcon(LocationOfMySelf+'/auto.png'),u'Auto',self)
        self.actionAuto.setObjectName('actionAuto')

        self.actionMultiDimension = QtWidgets.QAction(QIcon(LocationOfMySelf+'/multiple.png'),u'MultiDimension',self)
        self.actionMultiDimension.setObjectName('actionMultiDimension')

        self.actionQAPF = QtWidgets.QAction(QIcon(LocationOfMySelf+'/qapf.png'),u'QAPF',self)
        self.actionQAPF.setObjectName('actionQAPF')

        self.actionClastic = QtWidgets.QAction(QIcon(LocationOfMySelf+'/mud.png'),u'Clastic',self)
        self.actionClastic.setObjectName("actionClastic")

        self.actionXY = QtWidgets.QAction(QIcon(LocationOfMySelf+'/xy.png'), u'X-Y',self)
        self.actionXY.setObjectName('actionXY')

        self.actionXYZ = QtWidgets.QAction(QIcon(LocationOfMySelf+'/triangular.png'),u'Ternary',self)
        self.actionXYZ.setObjectName('actionXYZ')

        self.actionRbSrIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf+'/magic.png'),u'Rb-Sr IsoTope',self)
        self.actionRbSrIsoTope.setObjectName('actionRbSrIsoTope')

        self.actionSmNdIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf+'/magic.png'),u'Sm-Nd IsoTope',self)
        self.actionSmNdIsoTope.setObjectName('actionSmNdIsoTope')





        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)

        self.menuGeoChem.addAction(self.actionAuto)
        self.menuGeoChem.addAction(self.actionTAS)
        self.menuGeoChem.addAction(self.actionTrace)
        self.menuGeoChem.addAction(self.actionRee)
        self.menuGeoChem.addAction(self.actionPearce)
        self.menuGeoChem.addAction(self.actionHarker)
        self.menuGeoChem.addAction(self.actionBivariate)
        self.menuGeoChem.addAction(self.actionQAPF)
        self.menuGeoChem.addAction(self.actionCIPW)
        self.menuGeoChem.addAction(self.actionZirconCe)
        self.menuGeoChem.addAction(self.actionZirconTiTemp)
        self.menuGeoChem.addAction(self.actionRutileZrTemp)
        self.menuGeoChem.addAction(self.actionRbSrIsoTope)
        self.menuGeoChem.addAction(self.actionSmNdIsoTope)




        self.menuStructure.addAction(self.actionStereo)
        self.menuStructure.addAction(self.actionRose)
        self.menuSedimentary.addAction(self.actionQFL)
        self.menuSedimentary.addAction(self.actionQmFLt)
        self.menuSedimentary.addAction(self.actionClastic)


        self.menuDIY.addAction(self.actionXY)
        self.menuDIY.addAction(self.actionXYZ)
        self.menuDIY.addAction(self.actionCluster)
        self.menuDIY.addAction(self.actionMultiDimension)




        self.menuHelp.addAction(self.actionCnWeb)
        self.menuHelp.addAction(self.actionEnWeb)


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


        self.menubar.addAction(self.menuDIY.menuAction())
        self.menubar.addSeparator()




        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addSeparator()


        self.actionTAS.triggered.connect(self.TAS)
        self.actionTrace.triggered.connect(self.Trace)
        self.actionRee.triggered.connect(self.REE)
        self.actionPearce.triggered.connect(self.Pearce)
        self.actionBivariate.triggered.connect(self.Bivariate)
        self.actionHarker.triggered.connect(self.Harker)
        self.actionQAPF.triggered.connect(self.QAPF)

        self.actionStereo.triggered.connect(self.Stereo)
        self.actionRose.triggered.connect(self.Rose)
        self.actionQFL.triggered.connect(self.QFL)
        self.actionQmFLt.triggered.connect(self.QmFLt)

        self.actionClastic.triggered.connect(self.Mud)

        self.actionCIPW.triggered.connect(self.CIPW)
        self.actionZirconCe.triggered.connect(self.ZirconCe)
        self.actionZirconTiTemp.triggered.connect(self.ZirconTiTemp)
        self.actionRutileZrTemp.triggered.connect(self.RutileZrTemp)
        self.actionCluster.triggered.connect(self.Cluster)
        self.actionAuto.triggered.connect(self.Auto)


        self.actionMultiDimension.triggered.connect(self.MultiDimension)

        self.actionOpen.triggered.connect(self.getDataFile)
        self.actionSave.triggered.connect(self.saveDataFile)

        self.actionCnWeb.triggered.connect(self.goCnBBS)
        self.actionEnWeb.triggered.connect(self.goEnBBS)
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



        self.pushButtonOpen.clicked.connect(self.getDataFile)
        self.pushButtonSave.clicked.connect(self.saveDataFile)
        self.pushButtonSort.clicked.connect(self.SetUpDataFile)
        self.pushButtonQuit.clicked.connect(qApp.quit)
        self.pushButtonUpdate.clicked.connect(self.checkVersion)


        self.actionQuit = QtWidgets.QAction('Quit', self)
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.triggered.connect(qApp.quit)


        self.pushButtonOpen.setText(_translate('MainWindow',u'Open Data'))
        self.pushButtonSave.setText(_translate('MainWindow',u'Save Data'))
        self.pushButtonSort.setText(_translate('MainWindow',u'Set Format'))
        self.pushButtonQuit.setText(_translate('MainWindow',u'Quit App'))
        self.pushButtonUpdate.setText(_translate('MainWindow', u'Check Update'))



        self.pushButtonOpen.setIcon(QtGui.QIcon(LocationOfMySelf+'/open.png'))
        self.pushButtonSave.setIcon(QtGui.QIcon(LocationOfMySelf+'/save.png'))
        self.pushButtonSort.setIcon(QtGui.QIcon(LocationOfMySelf+'/set.png'))
        self.pushButtonQuit.setIcon(QtGui.QIcon(LocationOfMySelf+'/quit.png'))
        self.pushButtonUpdate.setIcon(QtGui.QIcon(LocationOfMySelf+'/update.png'))



        self.menuFile.setTitle(_translate('MainWindow',u'Data File'))

        self.menuGeoChem.setTitle(_translate('MainWindow',u'Geochemistry'))

        self.menuStructure.setTitle(_translate('MainWindow',u'Structure'))

        self.menuSedimentary.setTitle(_translate('MainWindow', u'Sedimentary'))



        self.menuDIY.setTitle(_translate('MainWindow',u'DIY Functions'))

        self.menuHelp.setTitle(_translate('MainWindow',u'Help'))

        self.menuLanguage.setTitle(_translate('MainWindow', u'Language'))



        self.actionOpen.setText(_translate('MainWindow',u'Open Data'))
        self.actionSave.setText(_translate('MainWindow',u'Save Data'))

        self.actionTAS.setText(_translate('MainWindow',u'TAS'))
        self.actionTrace.setText(_translate('MainWindow',u'Trace'))
        self.actionRee.setText(_translate('MainWindow',u'REE'))
        self.actionPearce.setText(_translate('MainWindow',u'Pearce'))
        self.actionBivariate.setText(_translate('MainWindow',u'Bivariate'))
        self.actionHarker.setText(_translate('MainWindow',u'Harker'))

        self.actionQAPF.setText(_translate('MainWindow',u'QAPF'))

        self.actionStereo.setText(_translate('MainWindow',u'Stereo'))
        self.actionRose.setText(_translate('MainWindow',u'Rose'))
        self.actionQFL.setText(_translate('MainWindow',u'QFL'))
        self.actionQmFLt.setText(_translate('MainWindow',u'QmFLt'))
        self.actionClastic.setText(_translate('MainWindow',u'Clastic'))

        self.actionCIPW.setText(_translate('MainWindow',u'CIPW'))

        self.actionZirconCe.setText(_translate('MainWindow',u'ZirconCe'))
        self.actionZirconTiTemp.setText(_translate('MainWindow',u'ZirconTiTemp'))
        self.actionRutileZrTemp.setText(_translate('MainWindow',u'RutileZrTemp'))
        self.actionCluster.setText(_translate('MainWindow',u'Cluster'))
        self.actionAuto.setText(_translate('MainWindow', u'Auto'))
        self.actionMultiDimension.setText(_translate('MainWindow',u'MultiDimension'))

        self.actionXY.setText(_translate('MainWindow',u'X-Y plot'))
        self.actionXYZ.setText(_translate('MainWindow',u'X-Y-Z plot'))

        self.actionRbSrIsoTope.setText(_translate('MainWindow',u'Rb-Sr IsoTope'))
        self.actionSmNdIsoTope.setText(_translate('MainWindow',u'Sm-Nd IsoTope'))



        self.actionVersionCheck.setText(_translate('MainWindow',u'Version'))
        self.actionCnWeb.setText(_translate('MainWindow',u'Chinese Forum'))
        self.actionEnWeb.setText(_translate('MainWindow',u'English Forum'))
        self.actionGoGithub.setText(_translate('MainWindow',u'Github'))


        '''
        self.actionCnS.setText(_translate('MainWindow',u'Simplified Chinese'))
        self.actionCnT.setText(_translate('MainWindow', u'Traditional Chinese'))
        self.actionEn.setText(_translate('MainWindow',u'English'))
        '''

        self.actionCnS.setText(u'简体中文')
        self.actionCnT.setText(u'繁體中文')
        self.actionEn.setText(u'English')
        self.actionLoadLanguage.setText(_translate('MainWindow',u'Load Language'))


        self.ReadConfig()

        self.trans.load(LocationOfMySelf+'/'+self.Language)
        self.app.installTranslator(self.trans)
        self.retranslateUi()



    def retranslateUi(self):




        _translate = QtCore.QCoreApplication.translate

        self.talk=  _translate('MainWindow','You are using GeoPyTool ') + version +'\n'+ _translate('MainWindow','released on ') + date + '\n'



        self.pushButtonOpen.setText(_translate('MainWindow',u'Open Data'))
        self.pushButtonSave.setText(_translate('MainWindow',u'Save Data'))
        self.pushButtonSort.setText(_translate('MainWindow',u'Set Format'))
        self.pushButtonQuit.setText(_translate('MainWindow',u'Quit App'))
        self.pushButtonUpdate.setText(_translate('MainWindow', u'Check Update'))


        self.menuFile.setTitle(_translate('MainWindow', u'Data File'))

        self.menuGeoChem.setTitle(_translate('MainWindow', u'Geochemistry'))

        self.menuStructure.setTitle(_translate('MainWindow', u'Structure'))
        self.menuSedimentary.setTitle(_translate('MainWindow', u'Sedimentary'))

        self.menuDIY.setTitle(_translate('MainWindow', u'DIY Functions'))

        self.menuHelp.setTitle(_translate('MainWindow', u'Help'))
        self.menuLanguage.setTitle(_translate('MainWindow', u'Language'))

        self.actionOpen.setText(_translate('MainWindow', u'Open Data'))
        self.actionSave.setText(_translate('MainWindow', u'Save Data'))

        self.actionTAS.setText(_translate('MainWindow', u'TAS'))
        self.actionTrace.setText(_translate('MainWindow', u'Trace'))
        self.actionRee.setText(_translate('MainWindow', u'REE'))
        self.actionPearce.setText(_translate('MainWindow', u'Pearce'))
        self.actionBivariate.setText(_translate('MainWindow', u'Bivariate'))
        self.actionHarker.setText(_translate('MainWindow',u'Harker'))

        self.actionQAPF.setText(_translate('MainWindow', u'QAPF'))

        self.actionStereo.setText(_translate('MainWindow', u'Stereo'))
        self.actionRose.setText(_translate('MainWindow', u'Rose'))
        self.actionQFL.setText(_translate('MainWindow', u'QFL'))
        self.actionQmFLt.setText(_translate('MainWindow', u'QmFLt'))
        self.actionClastic.setText(_translate('MainWindow',u'Clastic'))

        self.actionCIPW.setText(_translate('MainWindow', u'CIPW'))

        self.actionZirconCe.setText(_translate('MainWindow', u'ZirconCe'))
        self.actionZirconTiTemp.setText(_translate('MainWindow', u'ZirconTiTemp'))
        self.actionRutileZrTemp.setText(_translate('MainWindow', u'RutileZrTemp'))
        self.actionCluster.setText(_translate('MainWindow', u'Cluster'))
        self.actionAuto.setText(_translate('MainWindow', u'Auto'))
        self.actionMultiDimension.setText(_translate('MainWindow',u'MultiDimension'))

        self.actionXY.setText(_translate('MainWindow', u'X-Y plot'))
        self.actionXYZ.setText(_translate('MainWindow', u'X-Y-Z plot'))

        self.actionRbSrIsoTope.setText(_translate('MainWindow',u'Rb-Sr IsoTope'))
        self.actionSmNdIsoTope.setText(_translate('MainWindow',u'Sm-Nd IsoTope'))

        self.actionVersionCheck.setText(_translate('MainWindow', u'Check Update'))
        self.actionCnWeb.setText(_translate('MainWindow', u'Chinese Forum'))
        self.actionEnWeb.setText(_translate('MainWindow', u'English Forum'))
        self.actionGoGithub.setText(_translate('MainWindow', u'Github'))


        '''
        self.actionCnS.setText(_translate('MainWindow',u'Simplified Chinese'))
        self.actionCnT.setText(_translate('MainWindow', u'Traditional Chinese'))
        self.actionEn.setText(_translate('MainWindow',u'English'))
        '''



        self.actionCnS.setText(u'简体中文')
        self.actionCnT.setText(u'繁體中文')
        self.actionEn.setText(u'English')
        self.actionLoadLanguage.setText(_translate('MainWindow',u'Load Language'))

    def resizeEvent(self, evt=None):

        w=self.width()
        h=self.height()
        '''
        if h<=360:
            h=360
            self.resize(w,h)
        if w<=640:
            w = 640
            self.resize(w, h)
        '''


        step = (w * 94 / 100) / 5
        foot=h*3/48


        #if foot<=10: foot=10

        self.tableView.setGeometry(QtCore.QRect(w/100, h/48, w*98/100, h*38/48))

        self.pushButtonOpen.setGeometry(QtCore.QRect(w/100, h*40/48, step, foot))

        self.pushButtonSave.setGeometry(QtCore.QRect(2*w/100+step, h*40/48, step, foot))

        self.pushButtonSort.setGeometry(QtCore.QRect(3*w/100+step*2, h*40/48, step, foot))

        self.pushButtonUpdate.setGeometry(QtCore.QRect(4*w/100+step*3, h*40/48, step, foot))

        self.pushButtonQuit.setGeometry(QtCore.QRect(5*w/100+step*4, h*40/48, step, foot))

    def getfile(self):
        _translate = QtCore.QCoreApplication.translate
        fileName, filetype = QFileDialog.getOpenFileName(self,_translate('MainWindow', u'Choose Data File'),
                                                         '~/',
                                                         'All Files (*);;Text Files (*.txt)')  # 设置文件扩展名过滤,注意用双分号间隔

    def goGitHub(self):
        webbrowser.open('https://github.com/GeoPyTool/GeoPyTool/wiki')

    def goCnBBS(self):
        webbrowser.open('https://zhuanlan.zhihu.com/p/30651165')

    def goEnBBS(self):
        webbrowser.open('https://github.com/GeoPyTool/GeoPyTool/issues')

    def checkVersion(self):

        #reply = QMessageBox.information(self, 'Version', self.talk)

        _translate = QtCore.QCoreApplication.translate

        url = 'https://raw.githubusercontent.com/GeoPyTool/GeoPyTool/master/geopytool/CustomClass.py'


        r= 0
        try:
            r = requests.get(url, allow_redirects=True)
            r.raise_for_status()
            NewVersion = 'self.target' + r.text.splitlines()[0]

        except requests.exceptions.ConnectionError as err:
            print(err)
            r=0
            buttonReply = QMessageBox.information(self,  _translate('MainWindow', u'NetWork Error'),_translate('MainWindow', u'Net work unavailable.'))
            NewVersion ="targetversion = '0'"

        except requests.exceptions.HTTPError as err:
            print(err)
            r=0
            buttonReply = QMessageBox.information(self,  _translate('MainWindow', u'NetWork Error'),_translate('MainWindow', u'Net work unavailable.'))
            NewVersion ="targetversion = '0'"


        exec(NewVersion)
        print('web is', self.targetversion)
        print(NewVersion)


        self.talk=  _translate('MainWindow','Version Online is ') + self.targetversion +'\n'+_translate('MainWindow','You are using GeoPyTool ') + version +'\n'+ _translate('MainWindow','released on ') + date + '\n'



        if r != 0:


            print('now is',version)
            if (version < self.targetversion):

                buttonReply = QMessageBox.question(self, _translate('MainWindow', u'Version'),
                                                   self.talk + _translate('MainWindow',
                                                                          'New version available.\n Download and update?'),
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    print('Yes clicked.')
                    self.UpDate

                    webbrowser.open('https://github.com/chinageology/GeoPyTool/blob/master/Download.md')
                else:
                    print('No clicked.')
            else:
                buttonReply = QMessageBox.information(self, _translate('MainWindow', u'Version'),
                                                      self.talk + _translate('MainWindow',
                                                                             'This is the latest version.'))

    def Update(self):
        #webbrowser.open('https://github.com/chinageology/GeoPyTool/wiki/Download')
        pip.main(['install', 'geopytool','--upgrade'])

    def ReadConfig(self):
        if(os.path.isfile('config.ini')):

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


    def WriteConfig(self,text=LocationOfMySelf+'/en'):
        try:
            with open('config.ini', 'wt') as f:
                f.write(text)
        except():
            pass


    def to_ChineseS(self):

        self.trans.load(LocationOfMySelf+'/cns')
        self.app.installTranslator(self.trans)
        self.retranslateUi()

        self.WriteConfig('Language = \'cns\'')




    def to_ChineseT(self):

        self.trans.load(LocationOfMySelf+'/cnt')
        self.app.installTranslator(self.trans)
        self.retranslateUi()

        self.WriteConfig('Language = \'cnt\'')

    def to_English(self):

        self.trans.load(LocationOfMySelf+'/en')
        self.app.installTranslator(self.trans)
        self.retranslateUi()
        self.WriteConfig('Language = \'en\'')



    def to_LoadLanguage(self):


        _translate = QtCore.QCoreApplication.translate
        fileName, filetype = QFileDialog.getOpenFileName(self,_translate('MainWindow', u'Choose Language File'),
                                                         '~/',
                                                         'Language Files (*.qm)')  # 设置文件扩展名过滤,注意用双分号间隔

        print(fileName)

        self.trans.load(fileName)
        self.app.installTranslator(self.trans)
        self.retranslateUi()


    def ErrorEvent(self):

        reply = QMessageBox.information(self,  _translate('MainWindow','Warning'),  _translate('MainWindow','Your Data mismatch this Plot.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))



    def SetUpDataFile(self):

        flag = 0
        ItemsAvalibale = self.model._df.columns.values.tolist()

        ItemsToTest = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']

        LabelList = []
        MarkerList = []
        ColorList = []
        SizeList = []
        AlphaList = []
        StyleList = []
        WidthList = []

        for i in range(len(self.model._df)):
            LabelList.append('Group1')
            MarkerList.append('o')
            ColorList.append('red')
            SizeList.append(10)
            AlphaList.append(0.6)
            StyleList.append('-')
            WidthList.append(1)

        data = {'Label': LabelList,
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
            reply = QMessageBox.information(self,  _translate('MainWindow','Ready'),
                                         _translate('MainWindow','Everything fine and no need to set up.'))

        else:
            reply = QMessageBox.information(self,  _translate('MainWindow','Ready'),
                                         _translate('MainWindow','Items added, Modify in the Table to set up details.'))


    def getDataFile(self):
        _translate = QtCore.QCoreApplication.translate
        DataFileInput, filetype = QFileDialog.getOpenFileName(self,_translate('MainWindow', u'Choose Data File'),
                                                              '~/',
                                                              'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔

        # #print(DataFileInput,filetype)

        self.DataLocation = DataFileInput

        print(self.DataLocation )


        if ('csv' in DataFileInput):
            self.raw = pd.read_csv(DataFileInput)
        elif ('xls' in DataFileInput):
            self.raw = pd.read_excel(DataFileInput)
        # #print(self.raw)

        self.model = PandasModel(self.raw)
        self.tableView.setModel(self.model)

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,_translate('MainWindow', u'Save Data File'),
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def CIPW(self):
        self.cipwpop = CIPW(df=self.model._df)

        self.cipwpop.CIPW()
        self.cipwpop.show()


    def ZirconTiTemp(self):
        self.ztpop = ZirconTiTemp(df=self.model._df)
        try:
            self.ztpop.ZirconTiTemp()
            self.ztpop.show()
        except(KeyError):
            self.ErrorEvent()

    def RutileZrTemp(self):
        self.rzpop = RutileZrTemp(df=self.model._df)
        try:
            self.rzpop.RutileZrTemp()
            self.rzpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Cluster(self):

        self.clusterpop = Cluster(df=self.model._df)
        self.clusterpop.Cluster()
        self.clusterpop.show()

        try:
            self.clusterpop.Cluster()
            self.clusterpop.show()
        except(KeyError):
            pass
            # self.ErrorEvent()

    def TAS(self):

        self.taspop = TAS(df=self.model._df)
        try:
            self.taspop.TAS()
            self.taspop.show()
        except(KeyError):
            self.ErrorEvent()



    def REE(self):
        self.reepop = REE(df=self.model._df)
        try:
            self.reepop.REE()
            self.reepop.show()
        except(KeyError):
            self.ErrorEvent()




    def Trace(self):
        self.tracepop = Trace(df=self.model._df)
        try:
            self.tracepop.Trace()
            self.tracepop.show()
        except(KeyError):
            self.ErrorEvent()

    def Pearce(self):
        self.pearcepop = Pearce(df=self.model._df)

        try:
            self.pearcepop.Pearce()
            self.pearcepop.show()
        except(KeyError):
            self.ErrorEvent()

    def Bivariate(self):
        self.bivariatepop = Bivariate(df=self.model._df)
        try:
            self.bivariatepop.Bivariate()
            self.bivariatepop.show()
        except(KeyError):
            self.ErrorEvent()


    def Harker(self):
        self.harkerpop = Harker(df=self.model._df)
        try:
            self.harkerpop.Harker()
            self.harkerpop.show()
        except(KeyError):
            self.ErrorEvent()


    def Stereo(self):
        self.stereopop = Stereo(df=self.model._df)
        try:
            self.stereopop.Stereo()
            self.stereopop.show()
        except(KeyError):
            self.ErrorEvent()

    def Rose(self):
        self.rosepop = Rose(df=self.model._df)
        try:
            self.rosepop.Rose()
            self.rosepop.show()
        except(KeyError):
            self.ErrorEvent()

    def QFL(self):
        self.qflpop = QFL(df=self.model._df)
        try:
            self.qflpop.Tri()
            self.qflpop.show()
        except(KeyError):
            self.ErrorEvent()

    def QmFLt(self):
        self.qmfltpop = QmFLt(df=self.model._df)
        try:
            self.qmfltpop.Tri()
            self.qmfltpop.show()
        except(KeyError):
            self.ErrorEvent()

    def Mud(self):
        self.mudpop = Clastic(df=self.model._df)
        try:
            self.mudpop.Tri()
            self.mudpop.show()
        except(KeyError):
            self.ErrorEvent()

    def QAPF(self):
        self.qapfpop = QAPF(df=self.model._df)
        try:
            self.qapfpop.QAPF()
            self.qapfpop.show()
        except(KeyError):
            self.ErrorEvent()


    def ZirconCe(self):
        # print('Opening a new popup window...')
        self.zirconpop = ZirconCe(df=self.model._df)
        try:
            self.zirconpop.MultiBallard()
            self.zirconpop.show()
        except(KeyError,ValueError):
            self.ErrorEvent()

    def RbSrIsoTope(self):
        self.rbsrisotopepop = IsoTope(df=self.model._df,description='Rb-Sr IsoTope diagram', xname='87Rb/86Sr',
                 yname='87Sr/86Sr', lambdaItem=1.42e-11, xlabel=r'$^{87}Rb/^{86}Sr$', ylabel=r'$^{87}Sr/^{86}Sr$')
        try:
            self.rbsrisotopepop.Magic()
            self.rbsrisotopepop.show()
        except(KeyError):
            self.ErrorEvent()

    def SmNdIsoTope(self):
        self.smndisotopepop = IsoTope(df=self.model._df,description='Sm-Nd IsoTope diagram', xname='147Sm/144Nd',
                 yname= '143Nd/144Nd', lambdaItem=6.54e-12, xlabel=r'$^{147}Sm/^{144}Nd$', ylabel=r'$^{143}Nd/^{144}Nd$')
        try:
            self.smndisotopepop.Magic()
            self.smndisotopepop.show()
        except(KeyError):
            self.ErrorEvent()


    def XY(self):
        self.xypop = XY(df=self.model._df)
        try:
            self.xypop.Magic()
            self.xypop.show()
        except(KeyError):
            self.ErrorEvent()

    def XYZ(self):
        self.xyzpop = XYZ(df=self.model._df)
        try:
            self.xyzpop.Magic()
            self.xyzpop.show()
        except(KeyError):
            self.ErrorEvent()


    def MultiDimension(self):
        self.mdpop = MultiDimension(df=self.model._df)
        try:
            self.mdpop.Magic()
            self.mdpop.show()
        except(KeyError):
            self.ErrorEvent()


    def Tri(self):
        pass

    def OldAuto(self):


        FileOutput, ok1 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'PDF Files (*.pdf)')  # 数据文件保存输出

        if (FileOutput != ''):
            pdf = matplotlib.backends.backend_pdf.PdfPages(FileOutput)

        else:
            pdf = matplotlib.backends.backend_pdf.PdfPages(self.DataLocation+'output.pdf')
            

        self.cipwsilent = CIPW(df = self.model._df)
        self.cipwsilent.CIPW()
        self.cipwsilent.QAPFsilent()
        #self.TotalResult.append(self.cipwsilent.OutPutFig)
        pdf.savefig(self.cipwsilent.OutPutFig)

        #self.ChemResult = pd.concat([self.cipwsilent.OutPutData, self.ChemResult], axis=1)




        self.tassilent = TAS(df = self.model._df)

        if (self.tassilent.Check()==True):
            self.tassilent.TAS()
            self.tassilent.GetResult()
            #self.TotalResult.append(self.tassilent.OutPutFig)

            pdf.savefig(self.tassilent.OutPutFig)

            self.ChemResult = pd.concat([self.tassilent.OutPutData, self.ChemResult], axis=1)



        self.reesilent = REE(df=self.model._df)

        if (self.reesilent.Check()==True):
            self.reesilent.REE()
            self.reesilent.GetResult()
            #self.TotalResult.append(self.reesilent.OutPutFig)

            pdf.savefig(self.reesilent.OutPutFig)

            self.ChemResult = pd.concat([self.reesilent.OutPutData, self.ChemResult], axis=1)


        self.tracesilent = Trace(df=self.model._df)

        if (self.tracesilent.Check()==True):

            self.tracesilent.Trace()
            self.tracesilent.GetResult()
            self.TotalResult.append(self.tracesilent.OutPutFig)

            pdf.savefig(self.tracesilent.OutPutFig)





        self.harkersilent = Harker(df=self.model._df)

        if (self.harkersilent.Check()==True):

            self.harkersilent.Harker()
            self.harkersilent.GetResult()
            self.TotalResult.append(self.harkersilent.OutPutFig)

            pdf.savefig(self.harkersilent.OutPutFig)





        self.pearcesilent = Pearce(df=self.model._df)

        if (self.pearcesilent.Check()==True):

            self.pearcesilent.Pearce()
            self.pearcesilent.GetResult()
            self.TotalResult.append(self.pearcesilent.OutPutFig)

            pdf.savefig(self.pearcesilent.OutPutFig)


        self.ChemResult = self.ChemResult.T.groupby(level=0).first().T

        print(self.ChemResult)

        pdf.close()




        if (FileOutput != ''):

            if ('pdf' in FileOutput):

                FileOutput = FileOutput[0:-4]

            self.ChemResult.to_csv(FileOutput+'.csv', sep=',', encoding='utf-8')

            self.cipwsilent.newdf.to_csv(FileOutput+'mole.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf1.to_csv(FileOutput+'mass.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf2.to_csv(FileOutput+'volume.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf3.to_csv(FileOutput+'calculated.csv', sep=',', encoding='utf-8')


        else:

            if ('pdf' in FileOutput):

                FileOutput = FileOutput[0:-4]

            self.ChemResult.to_csv((self.DataLocation + 'mole.csv'), sep=',', encoding='utf-8')
            self.cipwsilent.newdf1.to_csv(self.DataLocation +'mass.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf2.to_csv(self.DataLocation +'volume.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf3.to_csv(self.DataLocation +'calculated.csv', sep=',', encoding='utf-8')

    def LastAuto(self):

        self.AutoResult=pd.DataFrame()

        FileOutput, ok1 = QFileDialog.getSaveFileName(self,
                                                      '文件保存',
                                                      'C:/',
                                                      'PDF Files (*.pdf)')  # 数据文件保存输出
        if (FileOutput != ''):

            pdf = matplotlib.backends.backend_pdf.PdfPages(FileOutput)


            self.cipwsilent = CIPW(df=self.model._df)
            self.cipwsilent.CIPW()
            self.cipwsilent.QAPFsilent()
            # self.TotalResult.append(self.cipwsilent.OutPutFig)
            pdf.savefig(self.cipwsilent.OutPutFig)

            # self.AutoResult = pd.concat([self.cipwsilent.OutPutData, self.AutoResult], axis=1)

            self.tassilent = TAS(df=self.model._df)

            if (self.tassilent.Check() == True):
                self.tassilent.TAS()
                self.tassilent.GetResult()
                # self.TotalResult.append(self.tassilent.OutPutFig)

                pdf.savefig(self.tassilent.OutPutFig)

                self.AutoResult = pd.concat([self.tassilent.OutPutData, self.AutoResult], axis=1)

            self.reesilent = REE(df=self.model._df)

            if (self.reesilent.Check() == True):
                self.reesilent.REE()
                self.reesilent.GetResult()
                # self.TotalResult.append(self.reesilent.OutPutFig)

                pdf.savefig(self.reesilent.OutPutFig)

                self.AutoResult = pd.concat([self.reesilent.OutPutData, self.AutoResult], axis=1)

            self.tracesilent = Trace(df=self.model._df)

            if (self.tracesilent.Check() == True):
                self.tracesilent.Trace()
                self.tracesilent.GetResult()
                self.TotalResult.append(self.tracesilent.OutPutFig)

                pdf.savefig(self.tracesilent.OutPutFig)

            self.harkersilent = Harker(df=self.model._df)

            if (self.harkersilent.Check() == True):
                self.harkersilent.Harker()
                self.harkersilent.GetResult()
                self.TotalResult.append(self.harkersilent.OutPutFig)

                pdf.savefig(self.harkersilent.OutPutFig)

            self.pearcesilent = Pearce(df=self.model._df)

            if (self.pearcesilent.Check() == True):
                self.pearcesilent.Pearce()
                self.pearcesilent.GetResult()
                self.TotalResult.append(self.pearcesilent.OutPutFig)

                pdf.savefig(self.pearcesilent.OutPutFig)

            self.AutoResult = self.AutoResult.T.groupby(level=0).first().T

            print(self.AutoResult)

            pdf.close()

            self.AutoResult = self.AutoResult.set_index('Label')

            self.AutoResult = pd.concat([self.cipwsilent.newdf3, self.AutoResult], axis=1)







            if ('pdf' in FileOutput):
                FileOutput = FileOutput[0:-4]

            self.AutoResult.to_csv(FileOutput + '-chemical-info.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf.to_csv(FileOutput + '-cipw-mole.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf1.to_csv(FileOutput + '-cipw-mass.csv', sep=',', encoding='utf-8')
            self.cipwsilent.newdf2.to_csv(FileOutput + '-cipw-volume.csv', sep=',', encoding='utf-8')


        else:

            pass

    def Auto(self):


        TotalResult=[]

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

            if (tassilent.Check() == True):
                tassilent.TAS()
                tassilent.GetResult()
                # TotalResult.append(tassilent.OutPutFig)

                pdf.savefig(tassilent.OutPutFig)

                AutoResult = pd.concat([tassilent.OutPutData, AutoResult], axis=1)

            reesilent = REE(df=df)

            if (reesilent.Check() == True):
                reesilent.REE()
                reesilent.GetResult()
                # TotalResult.append(reesilent.OutPutFig)

                pdf.savefig(reesilent.OutPutFig)

                AutoResult = pd.concat([reesilent.OutPutData, AutoResult], axis=1)

            tracesilent = Trace(df=df)

            if (tracesilent.Check() == True):
                tracesilent.Trace()
                tracesilent.GetResult()
                TotalResult.append(tracesilent.OutPutFig)

                pdf.savefig(tracesilent.OutPutFig)

            harkersilent = Harker(df=df)

            if (harkersilent.Check() == True):
                harkersilent.Harker()
                harkersilent.GetResult()
                TotalResult.append(harkersilent.OutPutFig)

                pdf.savefig(harkersilent.OutPutFig)

            pearcesilent = Pearce(df=df)

            if (pearcesilent.Check() == True):
                pearcesilent.Pearce()
                pearcesilent.GetResult()
                TotalResult.append(pearcesilent.OutPutFig)

                pdf.savefig(pearcesilent.OutPutFig)

            AutoResult = AutoResult.T.groupby(level=0).first().T



            pdf.close()

            AutoResult = AutoResult.set_index('Label')

            AutoResult=AutoResult.drop_duplicates()

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

