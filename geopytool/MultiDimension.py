from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MultiDimension(AppForm):
    Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
               u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']

    NameChosen = 'OIB'
    Standards = {
        'OIB': {'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                'K': 12000, 'La': 37, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200, 'Gd': 7.62,
                'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3},
        'EMORB': {'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                  'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155, 'P': 620,
                  'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                  'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                  'Yb': 2.37, 'Lu': 0.354},
        'C1': {'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
               'Ta': 0.014, 'K': 545, 'La': 0.237, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
               'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
               'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
               'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
               'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
               'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
               'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.737, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
               'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
        'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                  'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                  'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                  'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                  'Yb': 3.05, 'Lu': 0.455}, }

    Lines = []
    Tags = []

    xlabel = 'x'
    ylabel = 'y'
    zlabel = 'z'

    description = 'MultiDimension diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']

    LabelSetted = False
    ValueChoosed = True


    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)


        print(os.path.dirname(__file__))

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        dataframe = self._df
        ItemsAvalibale = self._df.columns.values.tolist()
        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width', 'Label']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        dataframe_values_only = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe_values_only = dataframe_values_only.dropna(axis='columns')

        ItemsAvalibale = dataframe_values_only.columns.values.tolist()

        data_columns = ItemsAvalibale

        df = dataframe_values_only

        numdf = (df.drop(data_columns, axis=1).join(df[data_columns].apply(pd.to_numeric, errors='coerce')))

        numdf = numdf[numdf[data_columns].notnull().all(axis=1)]

        ItemsAvalibale = numdf.columns.values.tolist()
        dataframe_values_only = numdf

        self.items = dataframe_values_only.columns.values.tolist()

        print(self.items)


        self.create_main_frame()
        self.create_status_bar()

        self.polygon = 0
        self.polyline = 0

        self.flag = 0

    def create_main_frame(self):

        self.resize(800, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.1, wspace=0.1,left=0.1, bottom=0.2, right=0.9, top=0.9)


        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = Axes3D(self.fig, elev=-150, azim=110)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)


        self.result_button = QPushButton('&Result')
        self.result_button.clicked.connect(self.Stat)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int



        self.Normalize_cb = QCheckBox('&Normalize')
        self.Normalize_cb.setChecked(False)
        self.Normalize_cb.stateChanged.connect(self.Magic)  # int

        self.norm_slider_label = QLabel('Standard:' + self.NameChosen)
        self.norm_slider = QSlider(Qt.Horizontal)
        self.norm_slider.setRange(0, 4)
        self.norm_slider.setValue(0)
        self.norm_slider.setTracking(True)
        self.norm_slider.setTickPosition(QSlider.TicksBothSides)
        self.norm_slider.valueChanged.connect(self.Magic)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Magic)  # int
        self.x_element_label = QLabel('X')
        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int
        self.x_seter = QLineEdit(self)
        self.x_seter.textChanged[str].connect(self.LabelSeter)



        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Magic)  # int
        self.y_element_label = QLabel('Y')
        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Magic)  # int
        self.y_seter = QLineEdit(self)
        self.y_seter.textChanged[str].connect(self.LabelSeter)



        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, len(self.items) - 1)
        self.z_element.setValue(2)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.Magic)  # int
        self.z_element_label = QLabel('Z')
        self.logz_cb = QCheckBox('&Log')
        self.logz_cb.setChecked(False)
        self.logz_cb.stateChanged.connect(self.Magic)  # int
        self.z_seter = QLineEdit(self)
        self.z_seter.textChanged[str].connect(self.LabelSeter)


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        self.hbox.addWidget(self.canvas)

        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()





        for w in [self.save_button,self.result_button, self.legend_cb,self.Normalize_cb, self.norm_slider_label, self.norm_slider]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)




        for w in [self.logx_cb, self.x_element_label,self.x_seter, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label,self.y_seter, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logz_cb, self.z_element_label,self.z_seter, self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)




        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def LabelSeter(self):
        self.LabelSetted = True
        self.ValueChoosed = False
        self.Magic()

    def ValueChooser(self):
        self.LabelSetted = False
        self.ValueChoosed = True
        self.Magic()


    def Magic(self):

        self.WholeData = []


        raw = self._df



        dataframe = self._df
        ItemsAvalibale = self._df.columns.values.tolist()
        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width','Label']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        ItemsAvalibale = dataframe.columns.values.tolist()





        a = int(self.x_element.value())
        b = int(self.y_element.value())
        c = int(self.z_element.value())

        if self.LabelSetted == True:
            if(self.x_seter.text()!=''):
                try:
                    a = int(self.x_seter.text())
                except(ValueError):
                    atmp=self.x_seter.text()
                    try:
                        if atmp in ItemsAvalibale:
                            a= ItemsAvalibale.index(atmp)
                            print(a)
                    except(ValueError):
                        pass
                    pass
            else:
                a = int(self.x_element.value())


            if (self.y_seter.text() != ''):
                try:
                    b = int(self.y_seter.text())
                except(ValueError):
                    btmp=self.y_seter.text()
                    try:
                        if btmp in ItemsAvalibale:
                            b= ItemsAvalibale.index(btmp)
                            print(b)
                    except(ValueError):
                        pass
                    pass
            else:
                b = int(self.y_element.value())

            if (self.z_seter.text() != ''):
                try:
                    c = int(self.z_seter.text())
                except(ValueError):
                    ctmp=self.z_seter.text()
                    try:
                        if ctmp in ItemsAvalibale:
                            c= ItemsAvalibale.index(ctmp)
                            print(c)
                    except(ValueError):
                        pass
                    pass
            else:
                c = int(self.z_element.value())


            if a> len(ItemsAvalibale)-1:
                a = int(self.x_element.value())
            if b> len(ItemsAvalibale)-1:
                b = int(self.y_element.value())
            if c> len(ItemsAvalibale)-1:
                c = int(self.z_element.value())




        if self.ValueChoosed == True:
            a = int(self.x_element.value())
            b = int(self.y_element.value())
            c = int(self.z_element.value())



        self.axes.clear()


        standardnamechosen = self.StandardsName[int(self.norm_slider.value())]
        standardchosen = self.Standards[standardnamechosen]

        self.norm_slider_label.setText(standardnamechosen)

        if self.flag != 0:
            if self.extent != 0:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto', extent=self.extent)
            else:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto')

        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])


        self.axes.set_zlabel(self.items[c])
        self.z_element_label.setText(self.items[c])

        PointLabels = []

        x_to_plot=[]
        y_to_plot=[]
        z_to_plot=[]
        label_to_plot=[]
        color_to_plot=[]
        size_to_plot=[]
        alpha_to_plot=[]
        marker_to_plot=[]


        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y , z= 0, 0, 0
            xuse, yuse,zuse = 0, 0, 0

            x, y , z= raw.at[i, self.items[a]], raw.at[i, self.items[b]],raw.at[i, self.items[c]]

            marker = raw.at[i, 'Marker']
            s = raw.at[i, 'Size']
            color = raw.at[i, 'Color']
            alpha = raw.at[i, 'Alpha']
            label = TmpLabel

            try:
                xuse = x
                yuse = y
                zuse = z

                self.xlabel = self.items[a]
                self.ylabel = self.items[b]
                self.zlabel = self.items[c]

                if (self.Normalize_cb.isChecked()):


                    if self.items[a] in self.Element:
                        xuse = xuse / standardchosen[self.items[a]]

                        self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen

                        self.axes.set_xlabel(self.xlabel)
                        self.x_element_label.setText(self.xlabel)

                    if self.items[b] in self.Element:
                        yuse = yuse / standardchosen[self.items[b]]

                        self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen

                        self.axes.set_ylabel(self.ylabel)
                        self.y_element_label.setText(self.ylabel)

                    if self.items[c] in self.Element:
                        zuse = zuse / standardchosen[self.items[c]]
                        self.zlabel = self.items[c] + ' Norm by ' + standardnamechosen

                        self.axes.set_zlabel(self.zlabel)
                        self.z_element_label.setText(self.zlabel)

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)
                    self.xlabel = '$log10$ ' + self.xlabel

                    self.axes.set_xlabel(self.xlabel)

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.ylabel = '$log10$ ' + self.ylabel

                    self.axes.set_ylabel(self.ylabel)

                if (self.logz_cb.isChecked()):
                    zuse = math.log(z, 10)

                    self.zlabel = '$log10$ ' + self.zlabel

                    self.axes.set_zlabel(self.zlabel)


                x_to_plot.append(xuse)
                y_to_plot.append(yuse)
                z_to_plot.append(zuse)
                label_to_plot.append(label)
                color_to_plot.append(color)
                size_to_plot.append(s)
                alpha_to_plot.append(alpha)
                marker_to_plot.append(marker)

            except(ValueError):
                pass


        for i in range(len(x_to_plot)):
            self.axes.scatter(x_to_plot[i], y_to_plot[i], z_to_plot[i], marker=marker_to_plot[i], s=size_to_plot[i],
                              color=color_to_plot[i], alpha=alpha_to_plot[i], label=label_to_plot[i], edgecolors='black')

        if (self.legend_cb.isChecked()):
            self.axes.legend(loc=2,prop=fontprop)


        self.canvas.draw()



    def stateval(self,data=np.ndarray):
        dict={'mean':mean(data),'ptp':ptp(data),'var':var(data),'std':std(data),'cv':mean(data)/std(data)}

        return(dict)

    def relation(self,data1=np.ndarray,data2=np.ndarray):
        data=array([data1,data2])
        dict={'cov':cov(data,bias=1),'corrcoef':corrcoef(data)}
        return(dict)

    def Stat(self):

        df=self._df


        # m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']
        m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author','Name','Type','Ref']
        for i in m:
            if i in df.columns.values:
                df = df.drop(i, 1)
        df.set_index('Label', inplace=True)

        items = df.columns.values
        index = df.index.values

        StatResultDict = {}

        for i in items:
            StatResultDict[i] = self.stateval(df[i])

        StdSortedList = sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std'])

        StdSortedList.reverse()

        for k in sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std']):
            print("%s=%s" % (k, StatResultDict[k]))

        StatResultDf = pd.DataFrame.from_dict(StatResultDict, orient='index')
        StatResultDf['Items']=StatResultDf.index.tolist()

        self.tablepop = TableViewer(df=StatResultDf,title='MultiDimensional Statistical Result')
        self.tablepop.show()


        self.Intro = StatResultDf

        return(StatResultDf)