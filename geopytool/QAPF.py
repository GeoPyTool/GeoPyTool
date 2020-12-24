from ImportDependence import *
from CustomClass import *

LocationOfMySelf=os.path.dirname(__file__)

print(LocationOfMySelf,'Import Denpendence')

fpath = LocationOfMySelf+('/wqy.ttf')

font = ft2font.FT2Font(fpath)
fprop = font_manager.FontProperties(fname=fpath)

ttfFontProp = ttfFontProperty(font)
fontprop = font_manager.FontProperties(family='sans-serif',
                            #name=ap.fontprop.name,
                            size=9,
                            fname=ttfFontProp.fname,
                            stretch=ttfFontProp.stretch,
                            style=ttfFontProp.style,
                            variant=ttfFontProp.variant,
                            weight=ttfFontProp.weight)

plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 'truetype'
plt.rcParams['axes.unicode_minus']=False

class QAPF(AppForm, Tool):

    infotext ='Q = quartz, A = alkali feldspar, P = plagioclase and F = feldspathoid.\nOnly for rocks in which the mafic mineral content, M, is greater than 90%.'

    exptext='''
            1a: quartzolite,
            1b: quartz-rich granitoid,		
            2: alkali feldspar granite,
            3a: (syeno granite),
            3b: (monzo granite),
            4: granodiorite,
            5: tonalite,		
            6*: quartz alkali feldspar syenite,
            7*: quartz syenite,
            8*: quartz monzonite,
            9*: quartz monzodiorite quartz monzogabbro,
            10*: quartz diorite quartz gabbro  quartz anorthosite,		
            6: alkali feldspar syenite,
            7: syenite,
            8: monzonite,
            9: monzodiorite monzogabbro,
            10: diorite gabbro anorthosite,		
            6\': foid-bearing alkali feldspar syenite,
            7\': foid-bearing syenite,
            8\': foid-bearing monzonite,
            9\': foid-bearing monzodiorite foid-bearing monzogabbro,
            10\': foid-bearing diorite foid-bearing gabbro foid-bearing anorthosite,		
            11: foid syenite,
            12: foid monzosyenite,
            13: foid monzodiorite foid monzogabbro,
            14: foid diorite foid gabbro,
            15: foidolite
            '''


    #infotext = infotext + exptext


    reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Q', u'A', u'P', u'F']
    LabelPosition = [(48, 50 * np.sqrt(3) + 1),
                     (-6, -1),
                     (104, -1),
                     (49, -50 * np.sqrt(3) - 4)]

    Labels = ['quartzolite',

              'quartz-rich\ngranitoid',

              'granite',

              'alkali\nfeldspar\ngranite',
              '(syeno\ngranite)',
              '(monzo\ngranite)',
              'granodiorite',
              'tonalite',

              'quartz\nalkali\nfeldspar\nsyenite',
              'quartz\nsyenite',
              'quartz\nmonzonite',
              'quartz\nmonzodiorite\nquartz\nmonzogabbro',
              'quartz\ndiorite\nquartz gabbro\n quartz\nanorthosite',

              'alkali\nfeldspar\nsyenite',
              'syenite',
              'monzonite',
              'monzodiorite\nmonzogabbro',
              'diorite\ngabbro\nanorthosite',

              'foid-bearing\nalkali\nfeldspar\nsyenite',
              'foid-bearing\nsyenite',
              'foid-bearing\nmonzonite',
              'foid-bearing\nmonzodiorite\nfoid-bearing\nmonzogabbro',
              'foid-bearing\ndiorite\nfoid-bearing gabbro\nfoid-bearing\nanorthosite',

              'foid\nsyenite',
              'foid\nmonzosyenite',
              'foid\nmonzodiorite\nfoid\nmonzogabbro',
              'foid\ndiorite\nfoid\ngabbro',
              'foidolite']

    Locations = [(5, 5, 95),

                 (10, 10, 80),

                 (35, 15, 50),

                 (45, 5, 50),
                 (45, 25, 30),
                 (35, 35, 30),
                 (25, 45, 30),
                 (5, 45, 50),

                 (85, 5, 10),
                 (75, 15, 10),
                 (45, 45, 10),
                 (15, 75, 10),
                 (5, 85, 10),

                 (93, 5, 1),
                 (83, 15, 1),
                 (53, 53, 1),
                 (15, 83, 1),
                 (5, 93, 1),

                 (95, 3, -8),
                 (75, 23, -8),
                 (49, 49, -8),
                 (23, 75, -8),
                 (3, 95, -8),

                 (63, 7, -30),
                 (50, 20, -30),
                 (20, 50, -30),
                 (7, 63, -30),
                 (10, 10, -80)]

    Offset = [(-30, 0),

              (-30, 0),

              (-20, 0),

              (-70, 30),
              (-50, 30),
              (-30, 0),
              (0, 0),
              (30, 20),

              (-70, 15),
              (-10, 0),
              (-40, 0),
              (-50, -5),
              (30, 15),

              (-80, 5),
              (0, 0),
              (-40, 0),
              (-50, -5),
              (60, 5),

              (-80, -15),
              (-40, 0),
              (-40, 0),
              (-20, -15),
              (50, -30),

              (-80, 0),
              (-40, 0),
              (-40, 0),
              (60, 0),
              (-30, 0)]

    LocationAreas0 = [[[50.0, 86.60254037844386], [45.0, 77.94228634059948], [55.0, 77.94228634059948]],
                         [[45.0, 77.94228634059948], [30.0, 51.96152422706631], [70.0, 51.96152422706631],
                          [55.0, 77.94228634059948]],
                         [[30.0, 51.96152422706631], [10.0, 17.32050807568877], [18.0, 17.32050807568877],
                          [34.0, 51.96152422706631]],
                         [[34.0, 51.96152422706631], [18.0, 17.32050807568877], [38.0, 17.32050807568877],
                          [44.0, 51.96152422706631]],
                         [[44.0, 51.96152422706631], [38.0, 17.32050807568877], [62.0, 17.32050807568877],
                          [56.0, 51.96152422706631]],
                         [[56.0, 51.96152422706631], [62.0, 17.32050807568877], [82.0, 17.32050807568877],
                          [66.0, 51.96152422706631]],
                         [[66.0, 51.96152422706631], [82.0, 17.32050807568877], [90.0, 17.32050807568877],
                          [70.0, 51.96152422706631]],
                         [[10.0, 17.32050807568877], [2.5, 4.330127018922193], [12.0, 4.330127018922193],
                          [18.0, 17.32050807568877]],
                         [[18.0, 17.32050807568877], [12.0, 4.330127018922193], [35.75, 4.330127018922193],
                          [38.0, 17.32050807568877]],
                         [[38.0, 17.32050807568877], [35.75, 4.330127018922193], [64.25, 4.330127018922193],
                          [62.0, 17.32050807568877]],
                         [[62.0, 17.32050807568877], [64.25, 4.330127018922193], [88.34951456310678, 4.204006814487566],
                          [82.0, 17.32050807568877]],
                         [[88.34951456310678, 4.204006814487566], [82.0, 17.32050807568877], [97.5, 4.330127018922193],
                          [90.0, 17.32050807568877]],
                         [[2.5, 4.330127018922193], [0.0, 0.0], [10.0, 0.0], [11.650485436893202, 4.204006814487566]],
                         [[11.650485436893202, 4.204006814487566], [10.0, 0.0], [35.0, 0.0],
                          [35.75, 4.330127018922193]],
                         [[35.75, 4.330127018922193], [35.0, 0.0], [65.0, 0.0], [64.25, 4.330127018922193]],
                         [[64.25, 4.330127018922193], [65.0, 0.0], [90.0, 0.0], [88.34951456310678, 4.204006814487566]],
                         [[88.34951456310678, 4.204006814487566], [90.0, 0.0], [100.0, 0.0], [97.5, 4.330127018922193]],
                         [[0.0, 0.0], [5.0, -8.660254037844386], [14.0, -8.660254037844386], [10.0, 0.0]],
                         [[10.0, 0.0], [14.0, -8.660254037844386], [36.42857142857143, -8.247860988423225],
                          [35.0, 0.0]],
                         [[35.0, 0.0], [36.42857142857143, -8.247860988423225], [63.57142857142858, -8.247860988423225],
                          [65.0, 0.0]],
                         [[65.0, 0.0], [63.57142857142858, -8.247860988423225], [86.0, -8.660254037844386],
                          [90.0, 0.0]],
                         [[90.0, 0.0], [86.0, -8.660254037844386], [95.0, -8.660254037844386], [100.0, 0.0]],
                         [[5.0, -8.660254037844386], [30.0, -51.96152422706631], [34.0, -51.96152422706631],
                          [14.0, -8.660254037844386]],
                         [[14.0, -8.660254037844386], [34.0, -51.96152422706631], [50.0, -51.96152422706631],
                          [50.0, -8.660254037844386]],
                         [[50.0, -8.660254037844386], [50.0, -51.96152422706631], [66.0, -51.96152422706631],
                          [86.0, -8.660254037844386]],
                         [[86.0, -8.660254037844386], [66.0, -51.96152422706631], [70.0, -51.96152422706631],
                          [95.0, -8.660254037844386]],
                         [[30.0, -51.96152422706631], [50.0, -86.60254037844386], [70.0, -51.96152422706631]]]

    ItemNames0 = [
        '1a: quartzolite',
        '1b: quartz-rich granitoid',
        '2: alkali feldspar granite',
        '3a: (syeno granite)',
        '3b: (monzo granite)',
        '4: granodiorite',
        '5: tonalite',
        '6*: quartz alkali feldspar syenite',
        '7*: quartz syenite',
        '8*: quartz monzonite',
        '9*: quartz monzodiorite quartz monzogabbro',
        '10*: quartz diorite quartz gabbro  quartz anorthosite',
        '6: alkali feldspar syenite',
        '7: syenite',
        '8: monzonite',
        '9: monzodiorite monzogabbro',
        '10: diorite gabbro anorthosite',
        '6\': foid-bearing alkali feldspar syenite',
        '7\': foid-bearing syenite',
        '8\': foid-bearing monzonite',
        '9\': foid-bearing monzodiorite foid-bearing monzogabbro',
        '10\': foid-bearing diorite foid-bearing gabbro foid-bearing anorthosite',
        '11: foid syenite',
        '12: foid monzosyenite',
        '13: foid monzodiorite foid monzogabbro',
        '14: foid diorite foid gabbro',
        '15: foidolite'
    ]

    LocationAreas1 = [
        [[30.0, 51.96152422706631], [10.0, 17.32050807568877], [38.0, 17.32050807568877], [44.0, 51.96152422706631]],
        [[44.0, 51.96152422706631], [38.0, 17.32050807568877], [62.0, 17.32050807568877], [56.0, 51.96152422706631]],
        [[56.0, 51.96152422706631], [62.0, 17.32050807568877], [90.0, 17.32050807568877], [70.0, 51.96152422706631]],
        [[10.0, 17.32050807568877], [2.5, 4.330127018922193], [12.0, 4.330127018922193], [18.0, 17.32050807568877]],
        [[18.0, 17.32050807568877], [12.0, 4.330127018922193], [35.75, 4.330127018922193], [38.0, 17.32050807568877]],
        [[38.0, 17.32050807568877], [35.75, 4.330127018922193], [64.25, 4.330127018922193], [62.0, 17.32050807568877]],
        [[62.0, 17.32050807568877], [65.0, 0.0], [100.0, 0.0], [90.0, 17.32050807568877]],
        [[2.5, 4.330127018922193], [0.0, 0.0], [10.0, 0.0], [11.650485436893202, 4.204006814487566]],
        [[11.650485436893202, 4.204006814487566], [10.0, 0.0], [35.0, 0.0], [35.75, 4.330127018922193]],
        [[35.75, 4.330127018922193], [35.0, 0.0], [65.0, 0.0], [64.25, 4.330127018922193]],
        [[0.0, 0.0], [5.0, -8.660254037844386], [14.0, -8.660254037844386], [10.0, 0.0]],
        [[10.0, 0.0], [14.0, -8.660254037844386], [36.42857142857143, -8.247860988423225], [35.0, 0.0]],
        [[35.0, 0.0], [36.42857142857143, -8.247860988423225], [63.57142857142858, -8.247860988423225], [65.0, 0.0]],
        [[65.0, 0.0], [63.57142857142858, -8.247860988423225], [95.0, -8.660254037844386], [100.0, 0.0]],
        [[5.0, -8.660254037844386], [30.0, -51.96152422706631], [34.0, -51.96152422706631], [14.0, -8.660254037844386]],
        [[14.0, -8.660254037844386], [34.0, -51.96152422706631], [50.0, -51.96152422706631],
         [50.0, -8.660254037844386]],
        [[50.0, -8.660254037844386], [50.0, -51.96152422706631], [66.0, -51.96152422706631],
         [86.0, -8.660254037844386]],
        [[86.0, -8.660254037844386], [66.0, -51.96152422706631], [70.0, -51.96152422706631],
         [95.0, -8.660254037844386]],
        [[30.0, -51.96152422706631], [45.0, -77.94228634059948], [50.0, -77.94228634059948],
         [50.0, -51.96152422706631]],
        [[50.0, -51.96152422706631], [50.0, -77.94228634059948], [55.0, -77.94228634059948],
         [70.0, -51.96152422706631]],
        [[45.0, -77.94228634059948], [50.0, -86.60254037844386], [55.0, -77.94228634059948]]]

    ItemNames1 = [
        '1:alkali feldspar rhyolite',
        '2:rhyolite',
        '3:dacite',
        '4:quartz alkali feldspar trachyte',
        '5:quartz trachyte',
        '6:quartz latite',
        '7:basalt andesite',
        '8:alkali feldspar trachyte',
        '9:trachyte',
        '10:latite',
        '11:foid-bearing alkali feldspar trachyte',
        '12:foid-bearing trachyte',
        '13:foid-bearing latite',
        '7:basalt andesite',
        '14:phonolite',
        '15:tephritic phonolite',
        '16:phonolitic basanite (olivine > 10%) phonolitic tephrite (olivine < 10%)',
        '17:basanite (olivine > 10%) tephrite (olivine < 10%)',
        '18:phonolitic foidite',
        '19:tephritic foidite',
        '20:foidoite',
    ]

    AreasHeadClosed = []
    SelectDic0 = {}
    SelectDic1 = {}

    AllLabel = []
    IndexList = []
    LabelList = []
    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)


        self.FileName_Hint='QAPF'
        self._df = df
        self._df_back = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to DualTri')

        self.raw = self._df
        self.create_main_frame()
        self.create_status_bar()

        self.AllLabel = []

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        for i in range(len(self.LocationAreas0)):
            tmpi = self.LocationAreas0[i] + [self.LocationAreas0[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic0[self.ItemNames0[i]] = tmppath

        for i in range(len(self.LocationAreas1)):
            tmpi = self.LocationAreas1[i] + [self.LocationAreas1[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic1[self.ItemNames1[i]] = tmppath


        TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (35, 65, 0)], Sort='',
                Width=1, Color='black', Style='-',
                Alpha=0.7, Label='')

        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

    def create_main_frame(self):
        self.resize(800, 1000)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((12, 11), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)

        # 8 * np.sqrt(3)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.result_button = QPushButton('&Classification Result')
        self.result_button.clicked.connect(self.Explain)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.QAPF)  # int

        self.slider_left_label = QLabel('Plutonic')
        self.slider_right_label = QLabel('Volcanic')


        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1)
        self.slider.setValue(0)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.QAPF)  # int


        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.QAPF)  # int



        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.QAPF)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.result_button, self.show_data_index_cb , self.detail_cb, self.legend_cb,self.slider_left_label,self.slider,self.slider_right_label]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)



        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



        w=self.width()
        h=self.height()

        #setFixedWidth(w/10)

        self.slider.setMinimumWidth(w/10)
        self.slider_left_label.setMinimumWidth(w/10)
        self.slider_right_label.setMinimumWidth(w/10)


    def QAPF(self):

        self.axes.clear()
        self.axes.axis('off')
        self.Tags = []

        raw = self._df

        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)



        if (int(self.slider.value()) == 0):
            s = [
                TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (0, 100, 0)], Sort='',
                        Width=1, Color='black', Style='-',
                        Alpha=0.7, Label='')]
            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)
            self.Labels = ['1a',

                           '1b',

                           '2',
                           '3a',
                           '3b',
                           '4',
                           '5',

                           '6*',
                           '7*',
                           '8*',
                           '9*',
                           '10*',

                           '6',
                           '7',
                           '8',
                           '9',
                           '10',

                           '6\'',
                           '7\'',
                           '8\'',
                           '9\'',
                           '10\'',

                           '11',
                           '12',
                           '13',
                           '14',
                           '15']
            self.Locations = [(50,80),

                              (50,65),

                              (22,33),
                              (32,33),
                              (50,33),
                              (66,33),
                              (76,33),

                              (10, 10),
                              (26, 10),
                              (50, 10),
                              (74, 10),
                              (88, 10),

                              (6, 1),
                              (24, 1),
                              (50, 1),
                              (76, 1),
                              (90, 1),

                              (6, -5),
                              (24, -5),
                              (50, -5),
                              (76, -5),
                              (90, -5),

                              (18, -30),
                              (40, -30),
                              (60, -30),
                              (78, -30),
                              (50, -60)]


            self.setWindowTitle('QAPF modal classification of plutonic rocks')

            self.exptext='''
                1a: quartzolite,
                1b: quartz-rich granitoid,		
                2: alkali feldspar granite,
                3a: (syeno granite),
                3b: (monzo granite),
                4: granodiorite,
                5: tonalite,		
                6*: quartz alkali feldspar syenite,
                7*: quartz syenite,
                8*: quartz monzonite,
                9*: quartz monzodiorite quartz monzogabbro,
                10*: quartz diorite quartz gabbro  quartz anorthosite,		
                6: alkali feldspar syenite,
                7: syenite,
                8: monzonite,
                9: monzodiorite monzogabbro,
                10: diorite gabbro anorthosite,		
                6\': foid-bearing alkali feldspar syenite,
                7\': foid-bearing syenite,
                8\': foid-bearing monzonite,
                9\': foid-bearing monzodiorite foid-bearing monzogabbro,
                10\': foid-bearing diorite foid-bearing gabbro foid-bearing anorthosite,		
                11: foid syenite,
                12: foid monzosyenite,
                13: foid monzodiorite foid monzogabbro,
                14: foid diorite foid gabbro,
                15: foidolite
                '''

            self.textbox.setText(self.reference + '\n' + self.infotext+ '\n' + self.exptext)


            D1 = (0, 0, 100)
            L1 = [(10, 0, 90), (0, 10, 90)]
            L2 = [(40, 0, 60), (0, 40, 60)]
            L3 = [(80, 0, 20), (0, 80, 20)]

            L4 = [(95, 0, 5), (0, 95, 5)]

            SL1 = [D1, (90, 10, 0)]
            SL2 = [D1, (65, 35, 0)]
            SL3 = [D1, (35, 65, 0)]
            SL4 = [D1, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL21 = self.TriCross(SL2, L2)
            CL22 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L2)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL21 = [CL21, CL22]
            NSL22 = [CL22, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, (10, 90, 0)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            D2 = (0, 0, -100)
            L2 = [(40, 0, -60), (0, 40, -60)]
            L3 = [(90, 0, -10), (0, 90, -10)]

            SL1 = [D2, (90, 10, 0)]
            SL2 = [D2, (65, 35, 0)]
            SL3 = [D2, (35, 65, 0)]
            SL4 = [D2, (10, 90, 0)]

            SL5 = [(20, 20, -60), (45, 45, -10)]

            CL1 = self.TriCross(SL1, L2)
            CL2 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L3)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL2 = [CL2, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, (10, 90, 0)]

            s = [
                TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=SL5, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label=''),
                TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                        Label='')]
            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)


        else:

            s = [
                TriLine(Points=[ (35, 65, 0),(100, 0, 0), (0, 0, 100), (0, 100, 0),(0, 0, -100), (100, 0, 0)], Sort='',
                        Width=1, Color='black', Style='-',
                        Alpha=0.7, Label='')]
            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)


            self.Labels = ['1',
                           '2',
                           '3',

                           '4',
                           '5',
                           '6',
                           '7',

                           '8',
                           '9',
                           '10',

                           '11',
                           '12',
                           '13',

                           '14',
                           '15',
                           '16',
                           '17',

                           '18',
                           '19',
                           '20']

            self.Locations = [(22,33),
                              (42,33),
                              (65,33),

                              (10, 10),
                              (25, 10),
                              (50, 10),
                              (80, 10),

                              (6, 1),
                              (24, 1),
                              (50, 1),

                              (6, -5),
                              (24, -5),
                              (50, -5),

                              (18, -30),
                              (40, -30),
                              (60, -30),
                              (78, -30),


                              (40, -63),
                              (55, -63),
                              (48, -82)]


            self.setWindowTitle('QAPF modal classification of volcanic rocks')



            self.exptext='''
                1:alkali feldspar rhyolite,
                2:rhyolite,
                3:dacite,
                4:quartz alkali feldspar trachyte,
                5:quartz trachyte,
                6:quartz latite,
                7:basalt andesite,
                8:alkali feldspar trachyte,
                9:trachyte,
                10:latite,
                11:foid-bearing alkali feldspar trachyte,
                12:foid-bearing trachyte,
                13:foid-bearing latite,
                14:phonolite,
                15:tephritic phonolite,
                16:phonolitic basanite (olivine > 10%) phonolitic tephrite (olivine < 10%),
                17:basanite (olivine > 10%) tephrite (olivine < 10%),
                18:phonolitic foidite,
                19:tephritic foidite,
                20:foidoite,         
                '''

            self.textbox.setText(self.reference + '\n' + self.infotext+ '\n' + self.exptext)


            D = (0, 0, 100)
            L1 = [(10, 0, 90), (0, 10, 90)]
            L2 = [(40, 0, 60), (0, 40, 60)]
            L3 = [(80, 0, 20), (0, 80, 20)]

            L4 = [(95, 0, 5), (0, 95, 5)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''), ]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            SL1 = [D, (90, 10, 0)]
            SL2 = [D, (65, 35, 0)]
            SL3 = [D, (35, 65, 0)]
            SL4 = [D, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL21 = self.TriCross(SL2, L2)
            CL22 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L2)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            TL4 = self.TriCross(SL3, L4)

            NL4 = [(95, 0, 5), TL4]

            NSL1 = [CL1, (90, 10, 0)]
            NSL21 = [CL21, CL22]
            NSL22 = [CL22, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, CL42]

            s = [TriLine(Points=NL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL21, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL22, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='--', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            D = (0, 0, -100)
            L1 = [(10, 0, -90), (0, 10, -90)]
            L2 = [(40, 0, -60), (0, 40, -60)]
            L3 = [(90, 0, -10), (0, 90, -10)]

            SL5 = [(5, 5, -90), (45, 45, -10)]

            s = [TriLine(Points=L1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=L3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),
                 TriLine(Points=SL5, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

            SL1 = [D, (90, 10, 0)]
            SL2 = [D, (65, 35, 0)]
            SL3 = [D, (35, 65, 0)]
            SL4 = [D, (10, 90, 0)]

            CL1 = self.TriCross(SL1, L2)
            CL2 = self.TriCross(SL2, L3)
            CL3 = self.TriCross(SL3, L3)
            CL41 = self.TriCross(SL4, L2)
            CL42 = self.TriCross(SL4, L3)

            NSL1 = [CL1, (90, 10, 0)]
            NSL2 = [CL2, (65, 35, 0)]
            NSL3 = [CL3, (35, 65, 0)]
            NSL4 = [CL41, CL42]

            s = [TriLine(Points=NSL1, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL2, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL3, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label=''),

                 TriLine(Points=NSL4, Sort='', Width=1, Color='black', Style='-', Alpha=0.7,
                         Label='')]

            for i in s:
                self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                               label=i.Label)

        for i in range(len(self.LabelPosition)):
            self.axes.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                               textcoords='offset points',
                               fontsize=8, )




        for i in range(len(self.Labels)):
            self.Tags.append(Tag(Label=self.Labels[i],
                                 Location=(self.Locations[i][0], self.Locations[i][1]),
                                 ))

        if (self.detail_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location,
                                   fontsize=6, color='grey', alpha=0.8)



        #raw = self.CleanDataFile(self._df)


        PointLabels = []
        TPoints = []
        self.IndexList = []
        self.LabelList = []
        self.TypeList = []

        print(raw.columns.values)

        for i in range(len(raw)):

            if 'A (Volume)' in raw.columns.values:
                q = raw.at[i, 'Q (Volume)']
                f = raw.at[i, 'F (Volume)']
                a = raw.at[i, 'A (Volume)']
                p = raw.at[i, 'P (Volume)']
            elif 'A' in raw.columns.values:
                q = raw.at[i, 'Q']
                f = raw.at[i, 'F']
                a = raw.at[i, 'A']
                p = raw.at[i, 'P']


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



            if (q != 0 and q != ''):
                TPoints.append(TriPoint((a, p, q), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))


                xa,ya = self.TriToBin(a, p, q)

            else:
                TPoints.append(TriPoint((a, p, 0 - f), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))



                xa,ya = self.TriToBin(a, p, 0 - f)



            if (int(self.slider.value()) == 0):
                HitOnRegions = 0
                for j in self.ItemNames0:
                    if self.SelectDic0[j].contains_point([xa, ya]):
                        self.TypeList.append(j)
                        HitOnRegions = 1
                        break
                if HitOnRegions == 0:
                    self.TypeList.append('on line or out')
            else:
                HitOnRegions = 0
                for j in self.ItemNames1:
                    if self.SelectDic1[j].contains_point([xa, ya]):
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




        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()

        #self.OutPutFig=self.fig

        self.OutPutTitle = 'QAPF'

        print(len(self.LabelList), len(self.IndexList), len(self.TypeList))

        self.OutPutData = pd.DataFrame({'Label': self.LabelList,
                                        'Index': self.IndexList,
                                        'Type': self.TypeList,
                                        })

    def Explain(self):

        # self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData, title='QPAF Result')
        self.tablepop.show()