from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class REE(AppForm):
    reference = 'Print the reference here.'

    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    xticklabels = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    LREE = ['La', 'Ce', 'Pr', 'Nd']
    MREE = ['Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho']
    HREE = [ 'Er', 'Tm', 'Yb', 'Lu']

    StandardsName = ['C1 Chondrite Sun and McDonough,1989', 'Chondrite Taylor and McLennan,1985',
                     'Chondrite Haskin et al.,1966', 'Chondrite Nakamura,1977', 'MORB Sun and McDonough,1989']

    # RefName=['Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.',]

    NameChosen = 'C1 Chondrite Sun and McDonough,1989'
    Standards = {
        'C1 Chondrite Sun and McDonough,1989': {'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
                                                'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
                                                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'Chondrite Taylor and McLennan,1985': {'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
                                               'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
                                               'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381},
        'Chondrite Haskin et al.,1966': {'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185, 'Eu': 0.071,
                                         'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                         'Yb': 0.186, 'Lu': 0.034},
        'Chondrite Nakamura,1977': {'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203, 'Eu': 0.077,
                                    'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                    'Yb': 0.22,
                                    'Lu': 0.034},
        'MORB Sun and McDonough,1989': {'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63, 'Eu': 1.02, 'Gd': 3.68,
                                        'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052, 'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05,
                                        'Lu': 0.46}}

    LabelList=[]
    algebraDeltaEuList = []
    geometricDeltaEuList = []
    LREEList=[]
    MREEList=[]
    HREEList=[]
    ALLREEList=[]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('REE Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to REE')

        self.Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 15
        self.X_Gap = 15

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        self.axes.axis('off')

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.REE)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.REE)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.REE)  # int

        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 4)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.REE)  # int

        self.standard_label = QLabel('Standard: ' + self.StandardsName[int(self.standard.value())])
        self.reference = self.StandardsName[int(self.standard.value())]+'Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, self.slider_label, self.slider, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def REE(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
            Top=6, Y0=-1,
            Y1=3, Y_Gap=5, FontSize=12,
            xLabel=r'$REE-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        self.axes.clear()

        self.axes.axis('off')

        self.WholeData = []

        raw = self._df

        self.FontSize = FontSize

        PointLabels = []
        k = 0

        standardnamechosen = self.StandardsName[int(self.standard.value())]
        standardchosen = self.Standards[standardnamechosen]

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            LinesX = []
            LinesY = []

            TmpEu = raw.at[i, 'Eu'] / standardchosen['Eu']
            TmpSm = raw.at[i, 'Sm'] / standardchosen['Sm']
            TmpGd = raw.at[i, 'Gd'] / standardchosen['Gd']

            algebraEu = 2*TmpEu/(TmpSm+TmpGd)
            geometricEu = TmpEu/np.power((TmpSm*TmpGd),0.5)


            tmpLREEResult = 0
            tmpMREEResult = 0
            tmpHREEResult = 0
            tmpWholeResult = 0

            for j in self.Element:

                if j in self.LREE:
                    tmpLREEResult += raw.at[i, j]
                elif j in self.MREE:
                    tmpMREEResult += raw.at[i, j]
                elif j in self.HREE:
                    tmpHREEResult += raw.at[i, j]

                tmpWholeResult+= raw.at[i, j]



            self.LabelList.append(raw.at[i, 'Label'])
            self.algebraDeltaEuList.append( algebraEu )
            self.geometricDeltaEuList.append( geometricEu )
            self.LREEList.append( tmpLREEResult )
            self.MREEList.append( tmpMREEResult )
            self.HREEList.append( tmpHREEResult )
            self.ALLREEList.append( tmpWholeResult )



            for j in range(len(self.Element)):
                tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]

                tmpflag = 1
                a = 0
                try:
                    a = math.log(tmp, 10)
                except(ValueError):
                    tmpflag = 0
                    pass

                if (tmpflag == 1):

                    LinesY.append(a)
                    LinesX.append(j + 1)

                    self.WholeData.append(math.log(tmp, 10))

                    if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        PointLabels.append(raw.at[i, 'Label'])
                        TmpLabel = raw.at[i, 'Label']

                    self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel, edgecolors='black')

            self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                           linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        self.DrawLine([(0, Location), (16, Location)], color='black', linewidth=0.8, alpha=0.8)

        self.DrawLine([(0, Location), (0, Head + (Head - Tale) / 5)], color='black', linewidth=0.8, alpha=0.8)

        self.standard_label.setText('Standard: ' + self.StandardsName[int(self.standard.value())])

        for i in range(count):
            self.DrawLine([(0, round(Location + i)), ((Head - Tale) / 50, round(Location + i))], color='black',
                          linewidth=0.8, alpha=0.8)

            self.axes.annotate(str(np.power(10.0, (Location + i))), ((Head - Tale) / 50, round(Location + i)),
                               xycoords='data', xytext=(-15, 0),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8, rotation=90)

        for i in range(min(len(self.xticks), len(self.xticklabels))):
            self.DrawLine([(self.xticks[i], Location), (self.xticks[i], Location + (Head - Tale) / 50)], color='black',
                          linewidth=0.8, alpha=0.8)
            self.axes.annotate(self.xticklabels[i], (self.xticks[i], Location), xycoords='data', xytext=(-5, -10),
                               textcoords='offset points',
                               fontsize=8, color='black', alpha=0.8)



        self.canvas.draw()


        self.WholeResult = self.Explain()


    def Explain(self):
        self.Intro = pd.DataFrame(
            {'Label': self.LabelList,
             'algebraDeltaEu': self.algebraDeltaEuList,
             'geometricDeltaEu': self.geometricDeltaEuList,
             'LREE': self.LREEList,
             'MREE': self.MREEList,
             'HREE': self.HREEList,
             'ALLREE': self.ALLREEList
             })

        #self.Intro = self.Intro.set_index('Label')

        self.tablepop = TabelViewer(df=self.Intro,title='REE Result')
        self.tablepop.show()

        return(self.Intro)
