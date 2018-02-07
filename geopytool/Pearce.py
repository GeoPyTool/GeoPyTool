from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class Pearce(AppForm):
    reference = 'Pearce, J. A., Harris, N. B. W., and Tindle, A. G., 1984, Trace Element Discrimination Diagrams for the Tectonic Interpretation of Granitic Rocks: Journal of Petrology, v. 25, no. 4, p. 956-983.'
    Lines = []
    Tags = []
    description = 'Pearce diagram (after Julian A. Pearce et al., 1984).\n syn-COLG: syn-collision granites\n VAG: volcanic arc granites\n WPG: within plate granites\n ORG: ocean ridge granites '
    text = [u'0.1', u'1', u'10', u'100', u'1000', u'10000', u'100000', u'1000000', u'10000000']

    Condation0 = {'BaseLines': [[(2, 80), (55, 300)],
                                [(55, 300), (400, 2000)],
                                [(55, 300), (51.5, 8)],
                                [(51.5, 8), (50, 1)],
                                [(51.5, 8), (2000, 400)], ],
                  'xLabel': r'Y+Nb (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(1, 3), (1, 1), (2.4, 2.4), (3, 1)],
                  'Frame': [[(0, 0), (0, 4)],
                            [(0, 0), (4, 0)],],

                  'BaseY': [[(0, 1), (-0.1, 1)],
                            [(0, 2), (-0.1, 2)],
                            [(0, 3), (-0.1, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)],
                            [(3, 0), (3, -0.1)], ]

                  }

    Condation1 = {'BaseLines': [[(0.5, 140), (6, 200)],
                                [(6, 200), (50, 2000)],
                                [(6, 200), (6, 8)],
                                [(6, 8), (6, 1)],
                                [(6, 8), (200, 400)], ],
                  'xLabel': r'Yb+Ta (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 3), (0.5, 1), (1.5, 2.4), (2, 1)],
                  'Frame': [[(-1, 0), (-1, 3)],
                            [(-1, 0), (3, 0)],],

                  'BaseY': [[(-1, 1), (-1.1, 1)],
                            [(-1, 2), (-1.1, 2)],
                            [(-1, 3), (-1.1, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(-1, 0), (-1, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)], ]
                  }

    Condation2 = {'BaseLines': [[(1, 2000), (50, 10)],
                                [(40, 1), (50, 10)],
                                [(50, 10), (1000, 100)],
                                [(25, 25), (1000, 400)], ],
                  'xLabel': r'Y (PPM)',
                  'yLabel': r'Nb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 1.5), (0.5, 2), (2, 2), (2, 1)],
                  'Frame': [[(-0.5, 0), (-0.5, 3)],
                            [(-0.5, 0), (3, 0)],],

                  'BaseY': [[(-0.5, 1), (-0.6, 1)],
                            [(-0.5, 2), (-0.6, 2)],
                            [(-0.5, 3), (-0.6, 3)],],

                  'BaseX': [[(0, 0), (0, -0.1)],
                            [(1, 0), (1, -0.1)],
                            [(2, 0), (2, -0.1)],]

                  }

    Condation3 = {'BaseLines': [[(0.55, 20), (3, 2)],
                                [(0.1, 0.35), (3, 2)],
                                [(3, 2), (5, 1)],
                                [(5, 0.05), (5, 1)],
                                [(5, 1), (100, 7)],
                                [(3, 2), (100, 20)], ],
                  'xLabel': r'Yb (PPM)',
                  'yLabel': r'Ta (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(-0.5, 0.1), (-0.5, -1), (0.7, 1), (2, 0.5)],
                  'Frame': [[(-1, -1.5), (-1, 2)],
                            [(-1, -1.5), (2, -1.5)],],

                  'BaseY': [[(-1, 0), (-1.1, 0)],
                            [(-1, 1), (-1.1, 1)],
                            [(-1, 2), (-1.1, 2)],],

                  'BaseX': [[(-1, -1.5), (-1, -1.6)],
                            [(0, -1.5), (0, -1.6)],
                            [(1, -1.5), (1, -1.6)],
                            [(2, -1.5), (2, -1.6)], ]
                  }

    condation = [Condation0, Condation1, Condation2, Condation3]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(
            'Pearce diagram (after Julian A. Pearce et al., 1984).\n syn-COLG: syn-collision granites\n VAG: volcanic arc granites\n WPG: within plate granites\n ORG: ocean ridge granites ')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Pearce')

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

        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Pearce)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Pearce)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Pearce)  # int

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.Pearce)  # int

        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 3)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.Pearce)  # int

        self.standard_label = QLabel('Type')

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button,
                  self.legend_cb, self.slider_label, self.slider, self.detail_cb, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Pearce(self):

        self.WholeData = []

        raw = self._df

        a = int(self.standard.value())

        self.axes.clear()
        self.axes.axis('off')

        self.axes.set_xlabel(self.condation[a]['xLabel'])
        self.axes.set_ylabel(self.condation[a]['yLabel'])


        s=[]
        for i in self.condation[a]['Frame']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            s.append((i[1][0]/2,i[1][1]/2))


        self.axes.annotate(self.condation[a]['xLabel'], s[1], xycoords='data', xytext=(-2, -50),
                           textcoords='offset points',
                           fontsize=9, color='grey', alpha=0.8)
        self.axes.annotate(self.condation[a]['yLabel'], s[0], xycoords='data', xytext=(-50, -2),
                           textcoords='offset points',rotation=90,
                           fontsize=9, color='grey', alpha=0.8)



        for i in self.condation[a]['BaseX']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            if (type(i[0][0])== int):
                self.axes.annotate(str(int(np.power(10, np.float32(i[0][0])))), i[1], xycoords='data', xytext=(-2,-10),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)

        for i in self.condation[a]['BaseY']:
            self.DrawLine(i, color='black', linewidth=0.8, alpha=0.5)
            if (type(i[0][1]) == int):
                self.axes.annotate(str(int(np.power(10, np.float32(i[0][1])))), i[1], xycoords='data', xytext=(-15,-10),
                               textcoords='offset points',
                               fontsize=9, color='grey', alpha=0.8)


        BaseLines = self.condation[a]['BaseLines']

        for i in BaseLines:
            self.DrawLogLine(l=i)
        PointLabels = []

        self.Tags = []

        for i in range(len(self.condation[a]['Labels'])):
            self.Tags.append(Tag(Label=self.condation[a]['Labels'][i], Location=self.condation[a]['Locations'][i]))

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0

            if (a == 0):
                x, y = (raw.at[i, 'Y'] + raw.at[i, 'Nb']), raw.at[i, 'Rb']
            elif (a == 1):
                x, y = (raw.at[i, 'Yb'] + raw.at[i, 'Ta']), raw.at[i, 'Rb']
            elif (a == 2):
                x, y = raw.at[i, 'Y'], raw.at[i, 'Nb']
            elif (a == 3):
                x, y = raw.at[i, 'Yb'], raw.at[i, 'Ta']

            self.axes.scatter(math.log(x, 10), math.log(y, 10), marker=raw.at[i, 'Marker'],
                              s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                              label=TmpLabel, edgecolors='black')

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7)

        if (self.legend_cb.isChecked()):
            a = int(self.slider.value())
            self.axes.legend(loc=a, prop=fontprop)

        if (self.detail_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

        self.canvas.draw()
