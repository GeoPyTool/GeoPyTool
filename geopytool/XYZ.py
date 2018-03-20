from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class XYZ(AppForm):
    Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
               u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']

    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'
    sentence=''

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

    description = 'X-Y-Z diagram'
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

    width_plot = 100.0
    height_plot = 100.0

    width_load = width_plot
    height_load = height_plot

    polygon = []
    polyline = []
    line = []

    strgons = []
    strlines = []
    strpolylines = []

    extent = 0

    Left = 0
    Right = 0
    Up = 0
    Down = 0

    FitLevel=3
    FadeGroups=100
    ShapeGroups=200


    LimSet= False

    LabelSetted = False
    ValueChoosed = True

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

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

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.3, bottom=0.3, right=0.7, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Reset)


        self.stat_button = QPushButton('&Stat')
        self.stat_button.clicked.connect(self.Stat)

        self.load_button = QPushButton('&Load')
        self.load_button.clicked.connect(self.Load)

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
        self.x_element.valueChanged.connect(self.ValueChooser)  # int

        self.x_element_label = QLabel('X')

        self.x_seter = QLineEdit(self)
        self.x_seter.textChanged[str].connect(self.LabelSeter)

        #self.x_calculator = QLineEdit(self)



        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.ValueChooser)  # int

        self.y_element_label = QLabel('Y')

        self.y_seter = QLineEdit(self)
        self.y_seter.textChanged[str].connect(self.LabelSeter)

        #self.y_calculator = QLineEdit(self)

        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Magic)  # int


        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, len(self.items) - 1)
        self.z_element.setValue(2)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.ValueChooser)  # int

        self.z_element_label = QLabel('Z')

        self.z_seter = QLineEdit(self)
        self.z_seter.textChanged[str].connect(self.LabelSeter)

        #self.z_calculator = QLineEdit(self)


        self.logz_cb = QCheckBox('&Log')
        self.logz_cb.setChecked(False)
        self.logz_cb.stateChanged.connect(self.Magic)  # int



        #
        # Layout with box sizers
        #
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.hbox6 = QHBoxLayout()
        self.hbox7 = QHBoxLayout()
        self.hbox8 = QHBoxLayout()



        for w in [self.save_button,self.stat_button, self.draw_button, self.load_button,
                  self.legend_cb, self.Normalize_cb, self.norm_slider_label, self.norm_slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

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
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)
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


    def Load(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                                         '选取文件',
                                                         '~/',
                                                         'PNG Files (*.png);;JPG Files (*.jpg);;SVG Files (*.svg)')  # 设置文件扩展名过滤,注意用双分号间隔

        print(fileName, '\t', filetype)

        if ('svg' in fileName):
            doc = minidom.parse(fileName)  # parseString also exists
            polygon_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polygon')]
            polyline_points = [path.getAttribute('points') for path in doc.getElementsByTagName('polyline')]

            svg_width = [path.getAttribute('width') for path in doc.getElementsByTagName('svg')]
            svg_height = [path.getAttribute('height') for path in doc.getElementsByTagName('svg')]

            # print(svg_width)
            # print(svg_height)

            digit = '01234567890.-'
            width = svg_width[0].replace('px', '').replace('pt', '')
            height = svg_height[0].replace('px', '').replace('pt', '')

            '''
            width=''
            for letter in svg_width[0]:
                if letter in digit:
                    width = width + letter

            #print(width)



            height=''
            for letter in svg_height[0]:
                if letter in digit:
                    height = height + letter

            #print(height)
            '''

            self.width_load = float(width)
            self.height_load = float(height)

            self.x_scale = 100.0 / float(width)
            self.y_scale = 50.0 * math.sqrt(3) / float(height)

            # print('x_scale' , self.x_scale , ' y_scale' , self.y_scale)

            soup = BeautifulSoup(open(fileName), 'lxml')

            tmpgon = soup.find_all('polygon')
            tmpline = soup.find_all('polyline')
            tmptext = soup.find_all('text')

            strgons = []
            for i in tmpgon:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polygon.attrs
                strgons.append(k['points'].split())
            gons = []
            for i in strgons:
                m = self.Read(i)
                m.append(m[0])
                gons.append(m)

            strlines = []
            for i in tmpline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polyline.attrs
                strlines.append(k['points'].split())
            lines = []
            for i in strlines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                lines.append(m)

            self.polygon = gons
            self.polyline = lines

            # print(self.polygon,'\n',self.polyline)


        elif ('png' in fileName or 'jpg' in fileName):

            self.img = mpimg.imread(fileName)
            self.flag = 1

        self.Magic()

    def Reset(self):
        self.flag = 0
        self.Magic()

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

        self.x_scale = self.width_plot / self.width_load

        self.y_scale = self.height_plot / self.height_load

        # print(self.x_scale,' and ',self.x_scale)

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
        self.axes.axis('off')

        standardnamechosen = self.StandardsName[int(self.norm_slider.value())]
        standardchosen = self.Standards[standardnamechosen]

        self.norm_slider_label.setText(standardnamechosen)



        s = [TriLine(Points=[(100, 0, 0), (0, 100, 0), (0, 0, 100), (100, 0, 0)], Sort='', Width=1, Color='black',
                     Style='-',
                     Alpha=0.3, Label='')]
        for i in s:
            self.axes.plot(i.X, i.Y, color=i.Color, linewidth=i.Width, linestyle=i.Style, alpha=i.Alpha,
                           label=i.Label)

        x = [0, 100]
        y = [0, 50 * np.sqrt(3)]

        extent = [min(x), max(x), min(y), max(y)]

        if self.flag != 0:
            self.axes.imshow(self.img, interpolation='nearest', aspect='auto', extent=extent)

        TPoints = []
        PointLabels = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y, z = 0, 0, 0
            xuse, yuse, zuse = 0, 0, 0

            x, y, z = raw.at[i, self.items[a]], raw.at[i, self.items[b]],raw.at[i, self.items[c]]


            try:
                xuse = x
                yuse = y
                zuse = z

                self.xlabel = self.items[a]
                self.ylabel = self.items[b]
                self.zlabel = self.items[c]

                if (self.Normalize_cb.isChecked()):
                    self.sentence = self.reference

                    if self.items[a] in self.Element:
                        self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen
                        xuse = xuse / standardchosen[self.items[a]]
                    if self.items[b] in self.Element:
                        self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen
                        yuse = yuse / standardchosen[self.items[b]]
                    if self.items[c] in self.Element:
                        self.zlabel = self.items[c] + ' Norm by ' + standardnamechosen
                        zuse = zuse / standardchosen[self.items[c]]

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)
                    self.xlabel = 'log10 ' + self.xlabel
                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)
                    self.ylabel = 'log10 ' + self.ylabel
                if (self.logy_cb.isChecked()):
                    zuse = math.log(y, 10)
                    self.zlabel = 'log10 ' + self.zlabel


                TPoints.append(TriPoint((xuse, yuse, zuse), Size=raw.at[i, 'Size'], Color=raw.at[i, 'Color'],
                                        Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel))

            except(ValueError):
                pass



        self.x_element_label.setText(self.xlabel)
        self.y_element_label.setText(self.ylabel)
        self.z_element_label.setText(self.zlabel)
        self.axes.annotate(self.xlabel, (-4, -3))
        self.axes.annotate(self.ylabel, (100, -3))
        self.axes.annotate(self.zlabel, (30, 90))

        for i in TPoints:
            self.axes.scatter(i.X, i.Y, marker=i.Marker, s=i.Size, color=i.Color, alpha=i.Alpha,
                              label=i.Label, edgecolors='black')

        print("Plotted")



        self.textbox.setText(self.sentence)


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0, prop=fontprop)



        if self.polygon != 0 and self.polyline != 0 and self.line != 0:

            # print('gon: ',self.polygon,' \n line:',self.polyline)

            for i in self.polygon:
                self.DrawLine(i)

            for i in self.polyline:
                self.DrawLine(i)

            for i in self.line:
                self.DrawLine(i)



                # self.DrawLine(self.polygon)
                # self.DrawLine(self.polyline)


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


        m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']
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

        self.tablepop = TabelViewer(df=StatResultDf,title='X-Y-Z Statistical Result')
        self.tablepop.show()

        self.Intro = StatResultDf

        return(StatResultDf)


