from ImportDependence import *
from CustomClass import *



class Clastic(AppForm, Tool):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []
    reference = 'Reference: Figure 1-A from Flemming, B.W., 2000. A revised textural classification of gravel-free muddy sediments on the basis of ternary diagrams. Continental Shelf Research, 20(10): 1125-1137.'

    Label = [u'Clay', u'Sand', u'Silt']
    LabelPosition = [(45, 50 * np.sqrt(3) + 2),
                     (-15, -5),
                     (104, -5)]

    Labels = [u'Y',
              u'SY',
              u'TY',
              u'YS',
              u'STY',
              u'YT',
              u'S',
              u'TS',
              u'ST',
              u'T',
              '20',
              '40',
              '60',
              '80',

              '80',
              '60',
              '40',
              '20',

              '80',
              '60',
              '40',
              '20', ]

    Locations = [(10, 10, 80),
                 (40, 10, 50),
                 (10, 40, 50),
                 (50, 10, 40),
                 (30, 30, 30),
                 (10, 50, 40),
                 (80, 10, 10),
                 (60, 30, 10),
                 (40, 50, 10),
                 (10, 80, 10),

                 (20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 20, 80),
                 (0, 40, 60),
                 (0, 60, 40),
                 (0, 80, 20),
                 ]
    Offset = [(0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0),

              (-18, 0),
              (-18, 0),
              (-18, 0),
              (-18, 0),

              (0, -18),
              (0, -18),
              (0, -18),
              (0, -18),

              (0, 0),
              (0, 0),
              (0, 0),
              (0, 0), ]


    LocationAreas =  [  [  [50.0, 86.60254037844386], [37.5, 64.9519052838329], [62.5, 64.9519052838329]   ] ,
                        [  [37.5, 64.9519052838329], [25.0, 43.30127018922193], [40.0, 34.64101615137754], [50.0, 51.96152422706631], [50.0, 64.9519052838329]   ] ,
                        [  [50.0, 64.9519052838329], [50.0, 51.96152422706631], [60.0, 34.64101615137754], [75.0, 43.30127018922193], [62.5, 64.9519052838329]   ] ,
                        [  [25.0, 43.30127018922193], [12.5, 21.650635094610966], [18.75, 10.825317547305483], [30.0, 17.32050807568877], [40.0, 34.64101615137754]   ] ,
                        [  [50.0, 51.96152422706631], [30.0, 17.32050807568877], [70.0, 17.32050807568877]   ] ,
                        [  [60.0, 34.64101615137754], [70.0, 17.32050807568877], [81.25, 10.825317547305483], [87.5, 21.650635094610966], [75.0, 43.30127018922193]   ] ,
                        [  [12.5, 21.650635094610966], [0.0, 0.0], [25.0, 0.0]   ] ,
                        [  [30.0, 17.32050807568877], [18.75, 10.825317547305483], [25.0, 0.0], [50.0, 0.0], [50.0, 17.32050807568877]   ] ,
                        [  [50.0, 17.32050807568877], [50.0, 0.0], [75.0, 0.0], [81.25, 10.825317547305483], [70.0, 17.32050807568877]   ] ,
                        [  [87.5, 21.650635094610966], [75.0, 0.0], [100.0, 0.0]]
                     ]


    ItemNames = [u'Clay',
              u'SY',
              u'TY',
              u'YS',
              u'STY',
              u'YT',
              u'S',
              u'TS',
              u'ST',
              u'T',]


    ItemNames = [u'Clay',
              u'Sand Clay',
              u'Silt Clay',
              u'Clay Sand',
              u'Sand Silt Clay',
              u'Clay Silt',
              u'Sand',
              u'Silt Sand',
              u'Sand Silt',
              u'Silt',]

    AreasHeadClosed = []
    SelectDic = {}
    AllLabel = []
    IndexList = []
    LabelList = []
    TypeList = []

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Sand-Silt-Clay')
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
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.7, top=0.9)

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

        self.InternalLine_cb = QCheckBox('&Internal Line')
        self.InternalLine_cb.setChecked(True)
        self.InternalLine_cb.stateChanged.connect(self.Tri)  # int


        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Tri)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button,self.result_button, self.draw_button, self.legend_cb,self.show_data_index_cb ,self.InternalLine_cb, self.Tag_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Tri(self):

        self.axes.clear()
        self.axes.axis('off')
        self.axes.set_xlim(-15, 140)
        self.axes.set_ylim(-10, 100)

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
        # 20间隔点坐标：
        Gap20 = [(20, 0, 80),
                 (40, 0, 60),
                 (60, 0, 40),
                 (80, 0, 20),

                 (20, 80, 0),
                 (40, 60, 0),
                 (60, 40, 0),
                 (80, 20, 0),

                 (0, 80, 20),
                 (0, 60, 40),
                 (0, 40, 60),
                 (0, 20, 80)]

        # 二等分点坐标：
        Gap50 = [(50, 0, 50),
                 (40, 20, 40),

                 (0, 50, 50),
                 (20, 40, 40),

                 (50, 50, 0),
                 (40, 40, 20), ]

        # 四等分点坐标：
        Gap25 = [(25, 0, 75),
                 (0, 25, 75),

                 (75, 0, 25),
                 (75, 25, 0),

                 (25, 75, 0),
                 (0, 75, 25), ]

        # 中心三角坐标：
        Middle = [(20, 20, 60),
                  (60, 20, 20),
                  (20, 60, 20), ]

        # 中心三角垂直链接四等分线坐标：
        Other = [(12.5, 12.5, 75),
                 (75, 12.5, 12.5),
                 (12.5, 75, 12.5), ]


        tmp = []
        # 中心三角绘制
        tmp.append(
            TriLine(Points=[Middle[0], Middle[1], Middle[2], Middle[0]], Sort='', Width=1, Color='black', Style='-',
                    Alpha=0.7,
                    Label=''))

        # 二等分和四等分线条绘制
        for i in range(len(Gap50)):

            if i % 2 == 0:
                tmp.append(
                    TriLine(Points=[Gap50[i], Gap50[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))
                tmp.append(
                    TriLine(Points=[Gap25[i], Gap25[i + 1]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                            Label=''))

        # 中心外延线条绘制
        for i in range(len(Middle)):
            tmp.append(TriLine(Points=[Middle[i], Other[i]], Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                               Label=''))

        if (self.InternalLine_cb.isChecked()):
            # 20网格线条绘制
            for i in range(len(Gap20)):
                if i <= len(Gap20) - 5:
                    tmp.append(
                        TriLine(Points=[Gap20[i], Gap20[i + 4]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                                Label=''))
                else:
                    tmp.append(
                        TriLine(Points=[Gap20[i], Gap20[-1 - i]], Sort='', Width=0.5, Color='grey', Style='-', Alpha=0.5,
                                Label=''))

        for i in tmp:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        raw = self._df
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


            TPoints.append(TriPoint((raw.at[i, 'Sand'], raw.at[i, 'Silt'], raw.at[i, 'Clay']), Size=raw.at[i, 'Size'],
                                    Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                    Label=TmpLabel))



            xa,ya = self.TriToBin(raw.at[i, 'Sand'], raw.at[i, 'Silt'], raw.at[i, 'Clay'])

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
                              label=TPoints[i].Label, edgecolors='black')


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


        self.OutPutFig=self.fig

        self.OutPutTitle = 'Clastic'


        print(len(self.LabelList), len(self.IndexList), len(self.TypeList))



        self.OutPutData = pd.DataFrame({'Label': self.LabelList,
                                        'Index': self.IndexList,
                                        'Type': self.TypeList,
                                        })      




    def Explain(self):

        # self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData, title='Clastic Result')
        self.tablepop.show()
