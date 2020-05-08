from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class Stereo(AppForm):

    reference = 'Zhou, J. B., Zeng, Z. X., and Yuan, J. R., 2003, THE DESIGN AND DEVELOPMENT OF THE SOFTWARE STRUCKIT FOR STRUCTURAL GEOLOGY: Journal of Changchun University of Science & Technology, v. 33, no. 3, p. 276-281.'

    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Stereo Net Projection')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Stereo')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.resize(1000,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111, projection='polar')
        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Stereo)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Stereo)  # int

        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.Stereo)  # int

        self.shape_slider_left_label = QLabel('Line')
        self.shape_slider_right_label = QLabel('Point')
        self.shape_slider = QSlider(Qt.Horizontal)
        self.shape_slider.setRange(0, 1)
        self.shape_slider.setValue(0)
        self.shape_slider.setTracking(True)
        self.shape_slider.setTickPosition(QSlider.TicksBothSides)
        self.shape_slider.valueChanged.connect(self.Stereo)  # int


        self.type_slider_left_label = QLabel('Wulff')
        self.type_slider_right_label = QLabel('Schmidt')
        self.type_slider = QSlider(Qt.Horizontal)
        self.type_slider.setRange(0, 1)
        self.type_slider.setValue(0)
        self.type_slider.setTracking(True)
        self.type_slider.setTickPosition(QSlider.TicksBothSides)
        self.type_slider.valueChanged.connect(self.Stereo)  # int





        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()


        for w in [self.save_button,self.legend_cb, self.shape_slider_left_label, self.shape_slider, self.shape_slider_right_label,
                  self.type_slider_left_label,self.type_slider,self.type_slider_right_label]:
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

        w=self.width()
        h=self.height()

        self.shape_slider.setFixedWidth(w/20)
        self.type_slider.setFixedWidth(w/20)






    def eqar(self, A):
        return (2 ** .5) * 90 * np.sin(np.pi * (90. - A) / (2. * 180.))

    def eqan(self, A):
        return 90 * np.tan(np.pi * (90. - A) / (2. * 180.))

    def getangular(self, A, B, C):
        a = np.radians(A)
        b = np.radians(B)
        c = np.radians(C)
        result = np.arctan((np.tan(a)) * np.cos(np.abs(b - c)))
        result = np.rad2deg(result)
        return result

    def Trans(self, S=(0, 100, 110), D=(0, 30, 40)):
        a = []
        b = []

        for i in S:
            a.append(np.radians(90 - i))
        for i in D:
            b.append(self.eqar(i))

        return (a, b)

    def lines(self, Width=1, Color='k'):
        '''
        read the Excel, then draw the wulf net and Plot points, job done~
        '''
        self.axes.clear()

        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        raw = self._df

        Data = []
        Labels = []


        if (int(self.type_slider.value()) == 0):
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append([raw.at[i, 'Dip'], raw.at[i, 'Dip-Angle'], raw.at[i, 'Color'],
                         raw.at[i, 'Width'], raw.at[i, 'Alpha'], raw.at[i, 'Label']])
            Dip = raw.at[i, 'Dip']
            Dip_Angle = raw.at[i, 'Dip-Angle']

            Label = raw.at[i, 'Label']
            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ''

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, 'Width']
            Color = raw.at[i, 'Color']
            Alpha = raw.at[i, 'Alpha']
            Marker = raw.at[i, 'Marker']
            Size = raw.at[i, 'Size']

            if (Color not in Setting or Color != ''):
                Width = raw.at[i, 'Width']
                Color = raw.at[i, 'Color']
                Alpha = raw.at[i, 'Alpha']
                Marker = raw.at[i, 'Marker']
                Size = raw.at[i, 'Size']

                Setting = [Width, Color, Alpha, Marker, Size]
            r = np.arange(Dip - 90, Dip + 91, 1)
            BearR = [np.radians(-A + 90) for A in r]

            if (int(self.type_slider.value()) == 0):
                Line = (self.eqan(self.getangular(Dip_Angle, Dip, r)))
            else:
                Line = (self.eqar(self.getangular(Dip_Angle, Dip, r)))

            self.axes.plot(BearR, Line, color=Color, linewidth=Width, alpha=Alpha, label=Label)

        # self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])

        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.5, 1), loc=2, borderaxespad=0, prop=fontprop)

    def points(self, Width=1, Color='k'):
        '''
        read the Excel, then draw the schmidt net and Plot points, job done~
        '''
        self.axes.clear()

        # self.axes.set_xlim(-90, 450)
        self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        raw = self._df

        Data = []
        Labels = []


        if (int(self.type_slider.value()) == 0):
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            list1 = [self.eqar(x) for x in range(15, 90, 15)]
        list2 = [str(x) for x in range(15, 90, 15)]
        self.axes.set_rgrids(list1, list2)

        for i in range(len(raw)):
            Data.append(
                [raw.at[i, 'Dip'], raw.at[i, 'Dip-Angle'], raw.at[i, 'Color'],
                 raw.at[i, 'Width'], raw.at[i, 'Alpha'], raw.at[i, 'Marker'], raw.at[i, 'Label']])
            Dip = raw.at[i, 'Dip']
            Dip_Angle = raw.at[i, 'Dip-Angle']

            Label = raw.at[i, 'Label']

            if (Label not in Labels):
                Labels.append(Label)
            else:
                Label = ''

            Width = 1
            Color = 'red'
            Alpha = 0.8
            Marker = 'o'
            Size = 50

            Setting = [Width, Color, Alpha, Marker, Size]

            Width = raw.at[i, 'Width']
            Color = raw.at[i, 'Color']
            Alpha = raw.at[i, 'Alpha']
            Marker = raw.at[i, 'Marker']
            Size = raw.at[i, 'Size']

            if (Color not in Setting or Color != ''):
                Width = raw.at[i, 'Width']
                Color = raw.at[i, 'Color']
                Alpha = raw.at[i, 'Alpha']
                Marker = raw.at[i, 'Marker']
                Size = raw.at[i, 'Size']

                Setting = [Width, Color, Alpha, Marker, Size]

            if (int(self.type_slider.value()) == 0):
                self.axes.scatter(np.radians(90 - Dip), self.eqan(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')
            else:
                self.axes.scatter(np.radians(90 - Dip), self.eqar(Dip_Angle), marker=Marker, s=Size, color=Color,
                                  alpha=Alpha,
                                  label=Label, edgecolors='black')

        # plt.plot(120, 30, color='K', linewidth=4, alpha=Alpha, marker='o')
        # self.axes.thetagrids(range(360 + 90, 0 + 90, -30), [str(x) for x in range(0, 360, 30)])
        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.5, 1), loc=2, borderaxespad=0, prop=fontprop)


    def Stereo(self):
        self.Label = [u'N', u'S', u'W', u'E']
        self.LabelPosition = []

        if (int(self.shape_slider.value()) == 0):
            self.lines()
        else:
            self.points()

        self.canvas.draw()



