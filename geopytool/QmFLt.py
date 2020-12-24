from ImportDependence import *
from CustomClass import *

class QmFLt(AppForm, Tool):
    reference = 'Refrence: Dickinson, W. R., Beard, L. S., Brakenridge, G. R., Erjavec, J. L., Ferguson, R. C., Inman, K. F., Knepp, R. A., Lindberg, F. A., and Ryberg, P. T., 1983, Provenance of North American Phanerozoic sandstones in relation to tectonic setting: Geological Society of America Bulletin, v. 94, no. 2, p. 222.'

    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Qm', u'F', u'Lt']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
                     (-6, -1),
                     (104, -1)]

    Labels = [u'Craton \n Interior',
              u'Transitional \n Continental',
              u'Basement \n Uplift',

              u'Mixed',
              u'Dissected \n Arc',
              u'Transitional \n Arc',
              u'Undissected \n Arc',

              u'Quartzose \n Recycled',
              u'Transitional \n Recycled',
              u'Lithic \n Recycled']
    Locations = [(15, 5, 90),
                 (30, 8, 62),
                 (60, 10, 30),

                 (30, 25, 45),
                 (40, 20, 40),
                 (40, 40, 20),
                 (20, 70, 10),

                 (10, 3, 60),
                 (10, 50, 40),
                 (10, 80, 10)]

    Offset = [(-66, 2),
              (-108, 2),
              (-95, 2),

              (-10, +10),
              (-10, -25),
              (-40, -20),
              (-30, -35),

              (+68, -28),
              (+50, -2),
              (+52, -15)]

    LocationAreas = [
        [[50.0, 86.60254037844386], [40.0, 69.28203230275508], [49.825, 63.60956590796702], [55.5, 77.07626093681503]],
        [[40.0, 69.28203230275508], [28.5, 49.363448015713], [40.780921907809216, 42.16256065419889],
         [49.825, 63.60956590796702]],
        [[28.5, 49.363448015713], [0.0, 0.0], [23.0, 0.0], [40.780921907809216, 42.16256065419889]],
        [[47.53, 58.17958662623859], [40.780921907809216, 42.16256065419889], [69.44694469446945, 25.35975979878824]],
        [[40.780921907809216, 42.16256065419889], [31.08, 19.15648193171178], [69.44694469446945, 25.35975979878824]],
        [[31.08, 19.15648193171178], [23.0, 0.0], [53.0, 0.0], [79.60000000000001, 10.911920087683928],
         [69.44694469446945, 25.35975979878824]],
        [[53.0, 0.0], [87.0, 0.0], [79.60000000000001, 10.911920087683928]],
        [[55.5, 77.07626093681503], [47.53, 58.17958662623859], [57.82421757824217, 43.002521299805245],
         [70.79207920792079, 50.58960279532859]],
        [[57.82421757824217, 43.002521299805245], [69.44694469446945, 25.35975979878824], [84.0, 27.712812921102035],
         [70.79207920792079, 50.58960279532859]],
        [[69.44694469446945, 25.35975979878824],  [87.0, 0.0], [100.0, 0.0],[84.0, 27.712812921102035]]
        ]

    ItemNames = [u'Craton Interior',
              u'Transitional Continental',
              u'Basement Uplift',

              u'Mixed',
              u'Dissected Arc',
              u'Transitional Arc',
              u'Undissected Arc',

              u'Quartzose Recycled',
              u'Transitional Recycled',
              u'Lithic Recycled']

    AreasHeadClosed = []
    SelectDic = {}
    AllLabel = []
    IndexList = []
    LabelList = []
    TypeList = []


    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Qm-F-lt')

        self._df_back = df
        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Tri')

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df

        self.AllLabel = []

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        for i in range(len(self.LocationAreas)):
            tmpi = self.LocationAreas[i] + [self.LocationAreas[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic[self.ItemNames[i]] = tmppath

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

        self.result_button = QPushButton('&Classification Result')
        self.result_button.clicked.connect(self.Explain)

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

        for w in [self.save_button,self.result_button, self.draw_button, self.legend_cb,self.show_data_index_cb, self.Tag_cb]:
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

        a = [TriLine(Points=[(77, 23, 0), (0, 11, 89)], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label='')]

        for i in a:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T0 = (77, 23, 0)
        T1 = (0, 11, 89)
        T2 = (43, 0, 57)
        T3 = (0, 87, 13)

        T4 = self.TriCross(A=[T0, T1], B=[T2, T3])

        T2 = (43, 0, 57)
        T3 = (0, 87, 13)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)

        T7 = self.TriCross(A=[T2, T3], B=[T5, T6])

        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T5 = (82, 0, 18)
        T6 = (0, 68, 32)

        T8 = self.TriCross(A=[T0, T1], B=[T5, T6])

        b = [TriLine(Points=[T4, T2], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T4, T7], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T7, T3], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T8, T7], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T7, (0, 68, 32)], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label=''), ]

        for i in b:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T9 = (13, 87, 0)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T0 = (77, 23, 0)
        T1 = (0, 11, 89)

        T12 = self.TriCross(A=[T10, T11], B=[T0, T1])

        c = [TriLine(Points=[T9, T12], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                     Label=''), ]

        for i in c:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        p, q = self.TriFill(P=[(100, 0, 0), T0, T1, (0, 0, 100)], Color='blue', Alpha=0.13)

        self.axes.fill(p, q, Color='blue', Alpha=0.13, )

        m, n = self.TriFill(P=[T12, T11, (0, 100, 0), T1], Color='red', Alpha=0.13)

        self.axes.fill(m, n, Color='red', Alpha=0.13, )

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T13 = (47, 53, 0)
        T14 = (0, 82, 18)

        T15 = self.TriCross(A=[T10, T11], B=[T13, T14])

        k = [TriLine(Points=[T15, T13], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''),

             TriLine(Points=[T15, T14], Sort='', Width=1, Color='black', Style=':', Alpha=0.7,
                     Label=''), ]

        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T10 = (20, 0, 80)
        T16 = (0, 40, 60)

        T17 = self.TriCross(A=[T10, T16], B=[T0, T1])

        k = [TriLine(Points=[T17, T10], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]

        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T10 = (20, 0, 80)
        T11 = (13, 87, 0)
        T18 = (0, 42, 59)
        T19 = (84, 0, 16)

        T20 = self.TriCross(A=[T10, T11], B=[T18, T19])

        k = [TriLine(Points=[T18, T20], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        T21 = (0, 71, 29)
        T22 = (58, 42, 0)

        T23 = self.TriCross(A=[T10, T11], B=[T21, T22])

        k = [TriLine(Points=[T23, T21], Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                     Label=''), ]
        for i in k:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        raw = self._df

        #raw = self.CleanDataFile(self._df)


        PointLabels = []
        TPoints = []

        self.IndexList = []
        self.LabelList = []
        self.TypeList = []

        for i in range(len(raw)):
            TmpLabel = ''
            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            self.LabelList.append(raw.at[i, 'Label'])
            if 'Index' in raw.columns.values:
                self.IndexList.append(raw.at[i, 'Index'])
            else:
                self.IndexList.append('No ' + str(int(i+1)))

            TPoints.append(TriPoint((raw.at[i, 'F'], raw.at[i, 'Lt'], raw.at[i, 'Qm']), Size=raw.at[i, 'Size'],
                                    Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                    Label=TmpLabel))

            xa,ya = self.TriToBin(raw.at[i, 'F'], raw.at[i, 'Lt'], raw.at[i, 'Qm'])
            HitOnRegions = 0
            for j in self.ItemNames:
                if self.SelectDic[j].contains_point([xa, ya]):
                    self.TypeList.append(j)
                    HitOnRegions = 1
                    break
            if HitOnRegions == 0:
                self.TypeList.append('on line or out')

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

        #self.OutPutFig=self.fig

        self.OutPutTitle = 'QmFLt'

        print(len(self.LabelList), len(self.IndexList), len(self.TypeList))



        self.OutPutData = pd.DataFrame({'Label': self.LabelList,
                                        'Index': self.IndexList,
                                        'Type': self.TypeList,
                                        })





    def Explain(self):

        # self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData, title='QmFLt Result')
        self.tablepop.show()