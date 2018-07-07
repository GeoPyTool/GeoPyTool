#!/usr/bin/python3
# coding:utf-8

from geopytool.ImportDependence import *
from geopytool.CustomClass import *


LocationOfMySelf=os.path.dirname(__file__)

#print(LocationOfMySelf,' init')


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
from geopytool.HarkerDIY import HarkerDIY

#from geopytool.Magic import Magic

from geopytool.Clastic import Clastic
from geopytool.CIA import CIA

from geopytool.IsoTope import IsoTope

from geopytool.KArIsoTope import KArIsoTope

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
from geopytool.ZirconCeOld import ZirconCeOld
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
    raw = pd.DataFrame(index=[], columns=[])  # raw is initialized as a blank DataFrame
    Standard = {}# Standard is initialized as a blank Dict
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

        self.setAcceptDrops(True)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('MainWindow', u'GeoPyTool'))
        self.setWindowIcon(QIcon(LocationOfMySelf+'/geopytool.png'))
        self.talk=  _translate('MainWindow','You are using GeoPyTool ') + version +'\n'+  _translate('MainWindow','released on ') + date

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

        self.actionClose = QtWidgets.QAction(QIcon(LocationOfMySelf+'/close.png'), u'Close',self)
        self.actionClose.setObjectName('actionClose')
        self.actionClose.setShortcut('Ctrl+T')

        #self.actionSet = QtWidgets.QAction(QIcon(LocationOfMySelf + '/set.png'), u'Set', self)
        #self.actionSet.setObjectName('actionSet')
        #self.actionSet.setShortcut('Ctrl+F')

        self.actionSave = QtWidgets.QAction(QIcon(LocationOfMySelf+'/save.png'), u'Save',self)
        self.actionSave.setObjectName('actionSave')
        self.actionSave.setShortcut('Ctrl+S')

        self.actionQuit = QtWidgets.QAction(QIcon(LocationOfMySelf+'/quit.png'), u'Quit',self)
        self.actionQuit.setObjectName('actionQuit')
        self.actionQuit.setShortcut('Ctrl+Q')






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

        self.actionHarkerDIY = QtWidgets.QAction(QIcon(LocationOfMySelf+'/spider.png'),u'HarkerDIY',self)
        self.actionHarkerDIY.setObjectName('actionHarkerDIY')


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

        self.actionZirconCeOld = QtWidgets.QAction(QIcon(LocationOfMySelf+'/calc.png'),u'ZirconCeOld',self)
        self.actionZirconCeOld.setObjectName('actionZirconCeOldOld')

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

        self.actionCIA = QtWidgets.QAction(QIcon(LocationOfMySelf+'/mud.png'),u'CIA and ICV',self)
        self.actionCIA.setObjectName("actionCIA")

        self.actionXY = QtWidgets.QAction(QIcon(LocationOfMySelf+'/xy.png'), u'X-Y',self)
        self.actionXY.setObjectName('actionXY')

        self.actionXYZ = QtWidgets.QAction(QIcon(LocationOfMySelf+'/triangular.png'),u'Ternary',self)
        self.actionXYZ.setObjectName('actionXYZ')

        self.actionRbSrIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf+'/magic.png'),u'Rb-Sr IsoTope',self)
        self.actionRbSrIsoTope.setObjectName('actionRbSrIsoTope')

        self.actionSmNdIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf+'/magic.png'),u'Sm-Nd IsoTope',self)
        self.actionSmNdIsoTope.setObjectName('actionSmNdIsoTope')


        self.actionKArIsoTope = QtWidgets.QAction(QIcon(LocationOfMySelf+'/magic.png'),u'K-Ar IsoTope',self)
        self.actionKArIsoTope.setObjectName('actionKArIsoTope')


        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionClose)
        #self.menuFile.addAction(self.actionSet)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)



        self.menuGeoChem.addAction(self.actionAuto)
        self.menuGeoChem.addAction(self.actionTAS)
        self.menuGeoChem.addAction(self.actionTrace)
        self.menuGeoChem.addAction(self.actionRee)
        self.menuGeoChem.addAction(self.actionPearce)
        self.menuGeoChem.addAction(self.actionHarker)
        #self.menuGeoChem.addAction(self.actionHarkerDIY)
        #self.menuGeoChem.addAction(self.actionBivariate)
        self.menuGeoChem.addAction(self.actionCIPW)
        self.menuGeoChem.addAction(self.actionQAPF)





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
        #self.menuGeoCalc.addAction(self.actionKArIsoTope)



        self.menuAdditional.addAction(self.actionXY)
        self.menuAdditional.addAction(self.actionXYZ)
        self.menuAdditional.addAction(self.actionCluster)
        self.menuAdditional.addAction(self.actionMultiDimension)




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

        self.menubar.addAction(self.menuGeoCalc.menuAction())
        self.menubar.addSeparator()

        self.menubar.addAction(self.menuAdditional.menuAction())
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
        self.actionHarkerDIY.triggered.connect(self.HarkerDIY)
        self.actionQAPF.triggered.connect(self.QAPF)

        self.actionStereo.triggered.connect(self.Stereo)
        self.actionRose.triggered.connect(self.Rose)
        self.actionQFL.triggered.connect(self.QFL)
        self.actionQmFLt.triggered.connect(self.QmFLt)

        self.actionClastic.triggered.connect(self.Clastic)
        self.actionCIA.triggered.connect(self.CIA)

        self.actionCIPW.triggered.connect(self.CIPW)
        self.actionZirconCe.triggered.connect(self.ZirconCe)
        self.actionZirconCeOld.triggered.connect(self.ZirconCeOld)
        self.actionZirconTiTemp.triggered.connect(self.ZirconTiTemp)
        self.actionRutileZrTemp.triggered.connect(self.RutileZrTemp)
        self.actionCluster.triggered.connect(self.Cluster)
        self.actionAuto.triggered.connect(self.Auto)


        self.actionMultiDimension.triggered.connect(self.MultiDimension)

        self.actionOpen.triggered.connect(self.getDataFile)
        self.actionClose.triggered.connect(self.clearDataFile)
        #self.actionSet.triggered.connect(self.SetUpDataFile)
        self.actionSave.triggered.connect(self.saveDataFile)
        self.actionQuit.triggered.connect(qApp.quit)

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
        self.actionKArIsoTope.triggered.connect(self.KArIsoTope)


        self.ReadConfig()
        self.trans.load(LocationOfMySelf+'/'+self.Language)
        self.app.installTranslator(self.trans)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.talk=  _translate('MainWindow','You are using GeoPyTool ') + version +'\n'+ _translate('MainWindow','released on ') + date + '\n'

        self.menuFile.setTitle(_translate('MainWindow', u'Data File'))
        self.menuGeoChem.setTitle(_translate('MainWindow', u'Geochemistry'))
        self.menuGeoCalc.setTitle(_translate('MainWindow',u'Calculation'))
        self.menuStructure.setTitle(_translate('MainWindow', u'Structure'))
        self.menuSedimentary.setTitle(_translate('MainWindow', u'Sedimentary'))
        self.menuAdditional.setTitle(_translate('MainWindow', u'Additional Functions'))
        self.menuHelp.setTitle(_translate('MainWindow', u'Help'))
        self.menuLanguage.setTitle(_translate('MainWindow', u'Language'))

        self.actionOpen.setText(_translate('MainWindow', u'Open Data'))
        self.actionClose.setText(_translate('MainWindow', u'Close Data'))
        #self.actionSet.setText(_translate('MainWindow', u'Set Format'))
        self.actionSave.setText(_translate('MainWindow', u'Save Data'))
        self.actionQuit.setText(_translate('MainWindow', u'Quit App'))

        self.actionAuto.setText('1-1 '+_translate('MainWindow', u'Auto'))
        self.actionTAS.setText('1-2 '+ _translate('MainWindow',u'TAS'))
        self.actionTrace.setText('1-3 '+_translate('MainWindow',u'Trace'))
        self.actionRee.setText('1-4 '+_translate('MainWindow',u'REE'))
        self.actionPearce.setText('1-5 '+_translate('MainWindow',u'Pearce'))
        self.actionHarker.setText('1-6 '+_translate('MainWindow',u'Harker'))
        self.actionCIPW.setText('1-7 '+_translate('MainWindow',u'CIPW'))
        self.actionQAPF.setText('1-8 '+_translate('MainWindow',u'QAPF'))
        #self.actionBivariate.setText(_translate('MainWindow',u'Bivariate'))
        #self.actionHarkerDIY.setText(_translate('MainWindow',u'HarkerDIY'))

        self.actionStereo.setText('2-1 '+_translate('MainWindow',u'Stereo'))
        self.actionRose.setText('2-2 '+_translate('MainWindow',u'Rose'))

        self.actionQFL.setText('3-1 '+_translate('MainWindow',u'QFL'))
        self.actionQmFLt.setText('3-2 '+_translate('MainWindow',u'QmFLt'))
        self.actionClastic.setText('3-3 '+_translate('MainWindow',u'Clastic'))
        self.actionCIA.setText('3-4 '+ _translate('MainWindow',u'CIA and ICV'))

        self.actionZirconCe.setText('4-1 '+ _translate('MainWindow',u'ZirconCe'))
        self.actionZirconCeOld.setText('4-2 '+ _translate('MainWindow', u'ZirconCeOld'))
        self.actionZirconTiTemp.setText('4-3 '+ _translate('MainWindow',u'ZirconTiTemp'))
        self.actionRutileZrTemp.setText('4-4 '+_translate('MainWindow',u'RutileZrTemp'))
        self.actionRbSrIsoTope.setText('4-5 '+_translate('MainWindow',u'Rb-Sr IsoTope'))
        self.actionSmNdIsoTope.setText('4-6 '+_translate('MainWindow',u'Sm-Nd IsoTope'))
        #self.actionKArIsoTope.setText(_translate('MainWindow',u'K-Ar IsoTope'))

        self.actionXY.setText('5-1 '+_translate('MainWindow',u'X-Y plot'))
        self.actionXYZ.setText('5-2 '+_translate('MainWindow',u'X-Y-Z plot'))
        self.actionCluster.setText('5-3 '+_translate('MainWindow',u'Cluster'))
        self.actionMultiDimension.setText('5-4 '+_translate('MainWindow',u'MultiDimension'))

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


    def getfile(self):
        _translate = QtCore.QCoreApplication.translate
        fileName, filetype = QFileDialog.getOpenFileName(self,_translate('MainWindow', u'Choose Data File'),
                                                         '~/',
                                                         'All Files (*);;Text Files (*.txt)')  # 设置文件扩展名过滤,注意用双分号间隔

    def goGitHub(self):
        webbrowser.open('https://github.com/GeoPyTool/GeoPyTool')

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
                    #qApp.quit
                    #pip.main(['install', 'geopytool', '--upgrade --no-cache-dir'])


                    #self.UpDate

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

    def ErrorEvent(self,text=''):

        if(text==''):
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Plot.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))
        else:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                      'Your Data mismatch this Plot.\n Error infor is:') + text)

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

    def clearDataFile(self):
        self.raw = pd.DataFrame()
        self.model = PandasModel(self.raw)
        self.tableView.setModel(self.model)


    def getDataFile(self,CleanOrNot=True):
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


        if len(self.raw)>0:

            self.model = PandasModel(self.raw)

            print(self.model._df)


            self.tableView.setModel(self.model)

            self.model = PandasModel(self.raw)

            print(self.model._df)

            flag = 0
            ItemsAvalibale = self.model._df.columns.values.tolist()
            ItemsToTest = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
            for i in ItemsToTest:
                if i not in ItemsAvalibale:
                    # print(i)
                    flag = flag + 1

            if flag == 0:
                pass
                #reply = QMessageBox.information(self, _translate('MainWindow', 'Ready'), _translate('MainWindow', 'Everything fine and no need to set up.'))

            else:

                self.SetUpDataFile()

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)


        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,_translate('MainWindow', u'Save Data File'),
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        dftosave = self.model._df




        #self.model._df.reset_index(drop=True)


        if (DataFileOutput != ''):


            if ('csv' in DataFileOutput):
                dftosave.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):

                dftosave.to_excel(DataFileOutput, encoding='utf-8')




    def TAS(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.taspop = TAS(df=self.model._df)




            try:
                self.taspop.TAS()
                self.taspop.show()


            except Exception as e:
                self.ErrorEvent(text=repr(e))

            '''
                print('Error is ',e)
            except:
                
                self.ErrorEvent()
            '''


    def REE(self):

        print('self.model._df length: ',len(self.model._df))


        if len(self.Standard)>0:
            print('self.Standard length: ', len(self.Standard))

        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):

            self.reepop = REE(df=self.model._df,Standard=self.Standard)

            try:
                self.reepop.REE()
                self.reepop.show()

            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Trace(self):

        print('self.model._df length: ',len(self.model._df))



        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.tracepop = Trace(df=self.model._df,Standard=self.Standard)
            try:
                self.tracepop.Trace()
                self.tracepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Pearce(self):

        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.pearcepop = Pearce(df=self.model._df)

            try:
                self.pearcepop.Pearce()
                self.pearcepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Bivariate(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.bivariatepop = Bivariate(df=self.model._df)
            try:
                self.bivariatepop.Bivariate()
                self.bivariatepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Harker(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.harkerpop = Harker(df=self.model._df)
            try:
                self.harkerpop.Harker()
                self.harkerpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def HarkerDIY(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()
        if (len(self.model._df) > 0):
            self.harkerdiypop = HarkerDIY(df=self.model._df)
            try:
                self.harkerdiypop.Magic()
                self.harkerdiypop.show()
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

        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rzpop = RutileZrTemp(df=self.model._df)
            try:
                self.rzpop.RutileZrTemp()
                self.rzpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Cluster(self):
        print('self.model._df length: ',len(self.model._df))


        if (len(self.model._df)<=0):
            self.getDataFile()
            pass

        if (len(self.model._df) > 0):
            self.clusterpop = Cluster(df=self.model._df)
            self.clusterpop.Cluster()

    def Stereo(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.stereopop = Stereo(df=self.model._df)

            try:
                self.stereopop.Stereo()
                self.stereopop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Rose(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rosepop = Rose(df=self.model._df)
            try:
                self.rosepop.Rose()
                self.rosepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QFL(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.qflpop = QFL(df=self.model._df)
            try:
                self.qflpop.Tri()
                self.qflpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QmFLt(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.qmfltpop = QmFLt(df=self.model._df)
            try:
                self.qmfltpop.Tri()
                self.qmfltpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def Clastic(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.clusterpop = Clastic(df=self.model._df)
            try:
                self.clusterpop.Tri()
                self.clusterpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def CIA(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.ciapop = CIA(df=self.model._df)

            try:
                self.ciapop.CIA()
                self.ciapop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def QAPF(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()



        if (len(self.model._df) > 0):
            ItemsAvalibale = self.model._df.columns.values.tolist()
            if 'Q' in  ItemsAvalibale and 'A' in  ItemsAvalibale and 'P' in  ItemsAvalibale and 'F' in ItemsAvalibale:
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
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
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
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile(CleanOrNot=False)
        # print('Opening a new popup window...')

        if (len(self.model._df) > 0):
            self.zirconoldpop = ZirconCeOld(df=self.model._df)
            try:
                self.zirconoldpop.MultiBallard()
                self.zirconoldpop.show()
            except(KeyError,ValueError,TypeError):
                self.ErrorEvent()

    def RbSrIsoTope(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.rbsrisotopepop = IsoTope(df=self.model._df,description='Rb-Sr IsoTope diagram', xname='87Rb/86Sr',
                 yname='87Sr/86Sr', lambdaItem=1.42e-11, xlabel=r'$^{87}Rb/^{86}Sr$', ylabel=r'$^{87}Sr/^{86}Sr$')
            try:
                self.rbsrisotopepop.Magic()
                self.rbsrisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def SmNdIsoTope(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.smndisotopepop = IsoTope(df=self.model._df,description='Sm-Nd IsoTope diagram', xname='147Sm/144Nd',
                 yname= '143Nd/144Nd', lambdaItem=6.54e-12, xlabel=r'$^{147}Sm/^{144}Nd$', ylabel=r'$^{143}Nd/^{144}Nd$')
            try:
                self.smndisotopepop.Magic()
                self.smndisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def KArIsoTope(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.karisotopepop = KArIsoTope(df=self.model._df)
            try:
                self.karisotopepop.Magic()
                self.karisotopepop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def XY(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.xypop = XY(df=self.model._df,Standard=self.Standard)
            try:
                self.xypop.Magic()
                self.xypop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))

    def XYZ(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.xyzpop = XYZ(df=self.model._df,Standard=self.Standard)
            try:
                self.xyzpop.Magic()
                self.xyzpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))


    def MultiDimension(self):
        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
            self.mdpop = MultiDimension(df=self.model._df)
            try:
                self.mdpop.Magic()
                self.mdpop.show()
            except Exception as e:
                self.ErrorEvent(text=repr(e))


    def Tri(self):
        pass

    def Auto(self):

        print('self.model._df length: ',len(self.model._df))
        if (len(self.model._df)<=0):
            self.getDataFile()

        if (len(self.model._df) > 0):
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

                reesilent = REE(df=df,Standard=self.Standard)

                if (reesilent.Check() == True):
                    reesilent.REE()
                    reesilent.GetResult()
                    # TotalResult.append(reesilent.OutPutFig)

                    pdf.savefig(reesilent.OutPutFig)

                    AutoResult = pd.concat([reesilent.OutPutData, AutoResult], axis=1)

                tracesilent = Trace(df=df,Standard=self.Standard)

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

