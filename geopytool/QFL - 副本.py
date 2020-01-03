from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class QFL(AppForm, Tool):
    reference = 'Refrence: Dickinson, W. R., Beard, L. S., Brakenridge, G. R., Erjavec, J. L., Ferguson, R. C., Inman, K. F., Knepp, R. A., Lindberg, F. A., and Ryberg, P. T., 1983, Provenance of North American Phanerozoic sandstones in relation to tectonic setting: Geological Society of America Bulletin, v. 94, no. 2, p. 222.'

    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Q', u'F', u'L']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',
              u'Recycled \n Orogenic',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc']
    Locations = [(8.5, 1.5, 90),
                 (28.5, 1.5, 70),
                 (58.5, 1.5, 40),
                 (18, 22, 70),
                 (35, 30, 35),
                 (15, 60, 15),
                 (11, 80, 9)]
    Offset = [(-80, 2),
              (-80, 2),
              (-80, 2),
              (-20, -5),
              (-20, -8),
              (-60, -2),
              (-40, -5)]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Q-F-L')

        self._df_back = df
        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df
        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

    def create_main_frame(self):
        self.resize(1000,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

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
        self.draw_button.clicked.connect(self.Tri)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Tri)  # int

        self.Tag_cb = QCheckBox('&Tag')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.Tri)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Tri)  # int
        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.legend_cb,self.show_data_index_cb , self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        self.vbox.addWidget(self.textbox)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-10, 140)
        self.axes.set_ylim(-10, 100)

        # self.axes.spines['right'].set_color('none')
        # self.axes.spines['top'].set_color('none')
        # self.axes.spines['bottom'].set_color('none')
        # self.axes.spines['left'].set_color('none')



        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=9, )

        a = [TriLine(Points=[(85, 15, 0), (0, 3, 97)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),
             TriLine(Points=[(45, 0, 55), (0, 75, 25)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),
             TriLine(Points=[(50, 50, 0), (0, 75, 25)], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T0 = (85, 15, 0)
        T1 = (0, 3, 97)
        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (87, 0, 13)
        T3 = (0, 63, 37)
        T5 = (45, 0, 55)
        T6 = (0, 75, 25)

        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        b = [TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),
             TriLine(Points=[T7, (0, 63, 37)], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label='')]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        y = 3 * np.sqrt(3) * (82 - 7.5 - np.sqrt(15)) / (18 * np.sqrt(3) - 1.5)
        z = 82 - np.power(15, 0.5)
        x = 100 - y - z

        p0 = (85, 15, 0)
        p1 = (0, 3, 97)
        p2 = (18, 0, 82)
        p3 = (0, 36, 64)

        p4 = self.TriCross(A=[p0, p1], B=[p2, p3])

        c = [TriLine(Points=[(18, 0, 82), p4], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label='')]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        p, q = self.TriFill(P=[(100, 0, 0), (85, 15, 0), (0, 3, 97), (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p, q, Color='blue', Alpha=0.13, )

        ap0 = (85, 15, 0)
        ap1 = (0, 3, 97)
        ap2 = (0, 75, 25)
        ap3 = (45, 0, 55)

        ap4 = self.TriCross(A=[ap0, ap1], B=[ap2, ap3])

        m, n = self.TriFill(P=[(0, 75, 25), (0, 3, 97), ap4], Color='red', Alpha=0.13)

        self.axes.fill(m, n, Color='red', Alpha=0.13, )

        raw = self._df

        #raw = self.Slim(self._df)

        PointLabels = []
        TPoints = []

        print(raw.columns)
        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']
            TPoints.append(TriPoint((raw.at[i, 'F'], raw.at[i, 'L'], raw.at[i, 'Q']), Size=raw.at[i, 'Size'],
                                    Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                    Label=TmpLabel))

        for i in range(len(TPoints)):
            self.axes.scatter(TPoints[i].X, TPoints[i].Y, marker=TPoints[i].Marker, s=TPoints[i].Size, color=TPoints[i].Color, alpha=TPoints[i].Alpha,
                              label=TPoints[i].Label)


            if (self.show_data_index_cb.isChecked()):

                if 'Index' in self._df_back.columns.values:

                    self.axes.annotate(str(self._df_back.at[i, 'Index']),
                                       xy=(TPoints[i].X,
                                           TPoints[i].Y),
                                       color=self._df.at[i, 'Color'],
                                       alpha=self._df.at[i, 'Alpha'])
                else:
                    self.axes.annotate('No' + str(i + 1),
                                       xy=(TPoints[i].X,
                                           TPoints[i].Y),
                                       color=self._df.at[i, 'Color'],
                                       alpha=self._df.at[i, 'Alpha'])


        if (self.Tag_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=i.FontSize, color='grey', alpha=0.8)

        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, prop=fontprop)




        self.canvas.draw()

