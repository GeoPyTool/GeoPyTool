from geopytool.ImportDependence import *
from geopytool.CustomClass import *

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
    reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'
    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Tags = []

    Label = [u'Q', u'A', u'P', u'F']
    LabelPosition = [(48, 50 * np.sqrt(3) + 2),
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

                 (93, 5, 2),
                 (83, 15, 2),
                 (53, 53, 2),
                 (15, 83, 2),
                 (5, 93, 2),

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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to DualTri')

        self.raw = self._df
        self.create_main_frame()
        self.create_status_bar()

        TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (35, 65, 0)], Sort='',
                Width=1, Color='black', Style='-',
                Alpha=0.7, Label='')

        for i in range(len(self.LabelPosition)):
            plt.annotate(self.Label[i], xy=(self.LabelPosition[i]), xycoords='data', xytext=(0, 0),
                         textcoords='offset points',
                         fontsize=16, )

    def create_main_frame(self):
        self.resize(600, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((12, 12), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)

        # 8 * np.sqrt(3)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        #self.result_button = QPushButton('&Result')
        #self.result_button.clicked.connect(self.Explain)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.QAPF)  # int





        self.slider_label = QLabel('Plutonic')
        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(0, 1)
        self.slider.setValue(0)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.QAPF)  # int

        '''
        self.Tag_cb = QCheckBox('&Plutonic')
        self.Tag_cb.setChecked(True)
        self.Tag_cb.stateChanged.connect(self.QAPF)  # int
        if (self.Tag_cb.isChecked()):
            self.Tag_cb.setText('&Plutonic')
        else:
            self.Tag_cb.setText('&Volcanic')
        '''


        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.QAPF)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button,  self.detail_cb, self.legend_cb,self.slider_label,self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)


        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference+'\n'+self.infotext)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def QAPF(self):

        self.axes.clear()
        self.axes.axis('off')
        self.Tags = []

        self.axes.set_xlim(-10, 110)
        self.axes.set_ylim(-105 * np.sqrt(3) / 2, 105 * np.sqrt(3) / 2)

        s = [TriLine(Points=[(100, 0, 0), (0, 0, 100), (0, 100, 0), (0, 0, -100), (100, 0, 0), (0, 100, 0)], Sort='',
                     Width=1, Color='black', Style='-',
                     Alpha=0.7, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        if (int(self.slider.value()) == 0):

            self.Labels = ['quartzolite',

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

            self.Locations = [(5, 5, 95),

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

                              (93, 5, 2),
                              (83, 15, 2),
                              (53, 53, 2),
                              (15, 83, 2),
                              (5, 93, 2),

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

            self.Offset = [(-30, 0),

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
            self.slider_label.setText('Plutonic')
            self.setWindowTitle('QAPF modal classification of plutonic rocks')

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
            self.Labels = ['rhyolite',

                           'alkali\nfeldspar\rhyolite',

                           'dacite',

                           'quartz\nalkali\nfeldspar\ntrachyte',
                           'quartz\ntrachyte',
                           'quartz\nlatite',
                           'basalt\nandesite',

                           'alkali\nfeldspar\ntrachyte',
                           'trachyte',
                           'latite',

                           'foid-bearing\nalkali\nfeldspar\ntrachyte',
                           'foid-bearing\ntrachyte',
                           'foid-bearing\nlatite',

                           'phonolite',
                           'tephritic\nphonolite',
                           ' phonolitic\nbasanite\n(olivine > 10%)\nphonolitic\ntephrite\n(olivine < 10%)',
                           ' basanite\n(olivine > 10%)\ntephrite\n(olivine < 10%)',
                           'phonolitic\nfoidite',
                           'tephritic\nfoidite',
                           'foidoite']

            self.Locations = [(35, 15, 50),

                              (45, 5, 50),

                              (20, 50, 30),

                              (85, 5, 10),
                              (75, 15, 10),
                              (45, 45, 10),
                              (15, 75, 10),

                              (93, 5, 2),
                              (83, 15, 2),
                              (53, 53, 2),

                              (95, 3, -8),
                              (75, 23, -8),
                              (49, 49, -8),

                              (63, 7, -30),
                              (50, 20, -30),
                              (20, 50, -30),
                              (7, 63, -30),
                              (16, 8, -76),
                              (8, 16, -76),
                              (4, 4, -92)]

            self.Offset = [(-20, 0),

                           (-70, 30),

                           (0, 0),

                           (-70, 15),
                           (-10, 0),
                           (-40, 0),
                           (-30, -5),

                           (-80, 5),
                           (0, 0),
                           (-40, 0),

                           (-80, -15),
                           (-40, 0),
                           (-40, 0),

                           (-80, 0),
                           (-40, 0),
                           (-40, 0),
                           (60, 0),
                           (-40, 20),
                           (0, 20),
                           (-20, 0)]
            self.slider_label.setText('Volcanic')

            self.setWindowTitle('QAPF modal classification of volcanic rocks')


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
                                 Location=self.TriToBin(self.Locations[i][0], self.Locations[i][1],
                                                        self.Locations[i][2]),
                                 X_offset=self.Offset[i][0], Y_offset=self.Offset[i][1]))

        if (self.detail_cb.isChecked()):
            for i in self.Tags:
                self.axes.annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

        raw = self._df
        PointLabels = []
        TPoints = []

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

            if (q != 0 and q != ''):
                TPoints.append(TriPoint((a, p, q), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))
            else:
                TPoints.append(TriPoint((a, p, 0 - f), Size=raw.at[i, 'Size'],
                                        Color=raw.at[i, 'Color'], Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'],
                                        Label=TmpLabel))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')



        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()
