from ImportDependence import *
from CustomClass import *

class Rose(AppForm):
    reference = 'Zhou, J. B., Zeng, Z. X., and Yuan, J. R., 2003, THE DESIGN AND DEVELOPMENT OF THE SOFTWARE STRUCKIT FOR STRUCTURAL GEOLOGY: Journal of Changchun University of Science & Technology, v. 33, no. 3, p. 276-281.'

    _df = pd.DataFrame()
    _changed = False

    xlabel = r''
    ylabel = r''

    Gap = 10

    MultipleRoseName = 'Dip'

    SingleRoseName = ['Dip']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Rose Map')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Rose')

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
        #self.axes.set_xlim(-90, 450)
        #self.axes.set_ylim(0, 90)




        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Rose)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Rose)  # int

        self.Type_cb = QCheckBox('&Wulf')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Rose)  # int

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        self.Rose_cb = QCheckBox('&Single Rose')
        self.Rose_cb.setChecked(True)
        self.Rose_cb.stateChanged.connect(self.Rose)  # int

        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
        else:
            self.Rose_cb.setText('Multiple Rose')

        slider_label = QLabel('Step:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 30)
        self.slider.setValue(5)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Rose)  # int

        self.ChooseItems = ['Strike', 'Dip', 'Dip-Angle']
        self.chooser_label = QLabel('Dip')
        self.chooser = QSlider(Qt.Horizontal)
        self.chooser.setRange(1, 3)
        self.chooser.setValue(2)
        self.chooser.setTracking(True)
        self.chooser.setTickPosition(QSlider.TicksBothSides)
        self.chooser.valueChanged.connect(self.Rose)  # int

        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.Type_cb, self.Rose_cb,
                  self.legend_cb, slider_label, self.slider, self.chooser, self.chooser_label]:
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

            if (self.Type_cb.isChecked()):
                self.Type_cb.setText('Wulf')
                b.append(self.eqan(i))
            else:
                self.Type_cb.setText('Schmidt')
                b.append(self.eqar(i))

        return (a, b)


    def singlerose(self, Width=1, Color=['red']):
        '''
        draw the rose map of single sample with different items~
        '''
        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        Name = self.SingleRoseName

        self.axes.clear()
        # self.axes.set_xlim(-90, 450)
        # self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        self.raw = self._df

        real_max = []

        for k in range(len(Name)):

            Data = []
            S = []
            R = []
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])

            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())
            count = []

            for i in range(len(t)):
                tmp_count = 0
                for j in S:
                    if i < len(t) - 1:
                        if t[i] < j <= t[i + 1]:
                            tmp_count += 1
                count.append(tmp_count)

            count_max = max(count)
            real_max.append(count_max)

        maxuse = max(real_max)

        for k in range(len(Name)):
            Data = []
            S = []
            R = []
            for i in range(len(self.raw)):
                S.append(self.raw.at[i, Name[k]])

            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())
            count = []

            for i in range(len(t)):
                tmp_count = 0
                for j in S:
                    if i < len(t) - 1:
                        if t[i] < j <= t[i + 1]:
                            tmp_count += 1
                count.append(tmp_count)
            s = np.linspace(0, 360, 360 / self.Gap + 1)
            t = tuple(s.tolist())

            R_factor = 90 / maxuse

            for i in count:
                TMP = 90 - i * R_factor
                R.append(TMP)

            m, n = self.Trans(t, R)
            self.axes.plot(m, n, color=Color[k], linewidth=1, alpha=0.6, marker='')
            self.axes.fill(m, n, Color=Color[k], Alpha=0.6, )

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]


        list2= list1


        print(maxuse + 1)

        try:
            list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1.0) / 7.0))]
        except(ValueError):
            pass
        list2.reverse()
        self.axes.set_rgrids(list1, list2)

        #self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])



        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.5, 1), loc=2, borderaxespad=0, prop=fontprop)

    def multirose(self, Width=1, Name='Dip'):
        '''
        draw the rose map of multiple samples~
        '''

        Name = self.MultipleRoseName

        self.axes.clear()
        # self.axes.set_xlim(-90, 450)
        # self.axes.set_ylim(0, 90)

        titles = list('NWSE')

        titles = ['N', '330', '300', 'W', '240', '210', 'S', '150', '120', 'E', '60', '30']
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)

        self.angles = np.array([90., 120., 150., 180., 210., 240., 270., 300., 330.,
                                360., 30., 60.])
        self.axes.set_thetagrids(self.angles, labels=titles, fontsize=14)

        self.raw = self._df

        real_max = []

        S = []
        R = []
        Color = []
        Label = []
        Whole = {}

        for i in range(len(self.raw)):
            S.append(self.raw.at[i, Name])

            if self.raw.at[i, 'Color'] not in Color and self.raw.at[i, 'Color'] != '':
                Color.append(self.raw.at[i, 'Color'])
            if self.raw.at[i, 'Label'] not in Label and self.raw.at[i, 'Label'] != '':
                Label.append(self.raw.at[i, 'Label'])

        Whole = ({k: [] for k in Label})

        WholeCount = ({k: [] for k in Label})

        for i in range(len(self.raw)):
            for k in Label:
                if self.raw.at[i, 'Label'] == k:
                    Whole[k].append(self.raw.at[i, Name])

        t = tuple(np.linspace(0, 360, 360 / self.Gap + 1).tolist())
        real_max = 0

        for j in range(len(Label)):

            for i in range(len(t)):
                tmp_count = 0
                for u in Whole[Label[j]]:
                    if i < len(t) - 1:
                        if t[i] < u <= t[i + 1]:
                            tmp_count += 1
                real_max = max(real_max, tmp_count)
                WholeCount[Label[j]].append(tmp_count)

        maxuse = real_max
        R_factor = 90 / maxuse

        for j in range(len(Label)):

            R = []
            for i in WholeCount[Label[j]]:
                TMP = 90 - i * R_factor
                R.append(TMP)

            m, n = self.Trans(t, R)
            self.axes.plot(m, n, color=Color[j], linewidth=1, alpha=0.6, marker='', label=Label[j])
            self.axes.fill(m, n, Color=Color[j], Alpha=0.6)

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
            list1 = [self.eqan(x) for x in range(15, 90, 15)]
        else:
            self.Type_cb.setText('Schmidt')
            list1 = [self.eqar(x) for x in range(15, 90, 15)]

        list2= list1

        try:
            list2 = [str(x) for x in range(0, int(maxuse + 1), int((maxuse + 1) / 7))]
        except(ValueError):
            pass


        list2.reverse()

        self.axes.set_rgrids(list1, list2)

        #self.axes.set_thetagrids(range(360 + 90, 0 + 90, -15), [str(x) for x in range(0, 360, 15)])

        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.5, 1), loc=2, borderaxespad=0, prop=fontprop)

    def Rose(self):

        self.Gap = self.slider.value()

        self.chooser_label.setText(self.ChooseItems[self.chooser.value() - 1])

        self.MultipleRoseName = self.ChooseItems[self.chooser.value() - 1]

        self.SingleRoseName = [(self.ChooseItems[self.chooser.value() - 1])]

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('Wulf')
        else:
            self.Type_cb.setText('Schmidt')

        if (self.Rose_cb.isChecked()):
            self.Rose_cb.setText('Single Rose')
            self.singlerose()
        else:
            self.Rose_cb.setText('Multiple Rose')
            self.multirose()

        self.canvas.draw()
