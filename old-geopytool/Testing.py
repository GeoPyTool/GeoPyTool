from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class Testing(AppForm):
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

    description = 'X-Y diagram'
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

    Xleft,Xright,Ydown,Yup=0,0,0,0

    LimSet= False

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
        self.main_frame = QWidget()
        self.dpi = 128

        self.view = pg.PlotWidget()


        self.view.setParent(self.main_frame)


        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.Reset)

        self.load_button = QPushButton('&Load')
        #self.load_button.clicked.connect(self.Load)


        self.fit_cb= QCheckBox('&PolyFit')
        self.fit_cb.setChecked(False)
        self.fit_cb.stateChanged.connect(self.Magic)  # int

        self.fit_label = QLabel('Exp')
        self.fit_seter = QLineEdit(self)
        self.fit_seter.textChanged[str].connect(self.FitChanged)


        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Magic)  # int

        self.shape_label = QLabel('Step')
        self.shape_seter = QLineEdit(self)
        self.shape_seter.textChanged[str].connect(self.ShapeChanged)



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

        #self.x_calculator = QLineEdit(self)



        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Magic)  # int

        self.y_element_label = QLabel('Y')

        #self.y_calculator = QLineEdit(self)


        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Magic)  # int


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

        for w in [self.fit_cb,self.fit_label, self.fit_seter,self.shape_cb,self.shape_label,self.shape_seter]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.save_button, self.draw_button, self.load_button,self.Normalize_cb, self.norm_slider_label, self.norm_slider]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)





        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.view)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

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

            self.width_load = float(width)
            self.height_load = float(height)

            soup = BeautifulSoup(open(fileName), 'lxml')

            tmpgon = soup.find_all('polygon')
            tmppolyline = soup.find_all('polyline')
            tmptext = soup.find_all('text')
            tmpline = soup.find_all('line')

            tmppath = soup.find_all('path')

            self.strgons = []
            for i in tmpgon:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polygon.attrs
                self.strgons.append(k['points'].split())

            self.strpolylines = []
            for i in tmppolyline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.polyline.attrs
                self.strpolylines.append(k['points'].split())

            self.strlines = []
            for i in tmpline:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.line.attrs
                a = str(k['x1']) + ',' + str(k['y1']) + ' ' + str(k['x2']) + ',' + str(k['y2'])
                self.strlines.append(a.split())

            self.strpath = []
            for i in tmppath:
                a = (str(i)).replace('\n', '').replace('\t', '')
                m = BeautifulSoup(a, 'lxml')
                k = m.path.attrs
                self.strpath.append(k['d'].split())

            # print(self.strpath)



            self.polygon = []
            for i in self.strgons:
                m = self.Read(i)
                m.append(m[0])
                self.polygon.append(m)

            self.polyline = []
            for i in self.strpolylines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                self.polyline.append(m)

            self.line = []
            for i in self.strlines:
                m = self.Read(i)
                # print('i: ',i,'\n m:',m)
                self.line.append(m)


        elif ('png' in fileName or 'jpg' in fileName):

            self.img = mpimg.imread(fileName)
            self.flag = 1

        self.Magic()

    def Reset(self):
        self.flag = 0
        self.Magic()

    def FitChanged(self, text):
        w = 'Fit' + text
        self.fit_label.setText(w)
        self.fit_label.adjustSize()

        try:
            self.FitLevel = float(text)
        except:
            pass

        self.Magic()


    def ShapeChanged(self, text):
        w = 'Shape' + text
        self.shape_label.setText(w)
        self.shape_label.adjustSize()

        try:
            self.ShapeGroups = int(text)
        except:
            pass

        self.Magic()

    def GetASequence(self, head=0, tail= 200, count=10):

        tail = self.ShapeGroups

        if count > 0:
            result = np.arange(head, tail, (tail - head) / count)
        else:
            result = np.arange(head, tail, (tail - head) / 10)

        return (result)

    def Magic(self):


        self.view.clear()
        self.view.addLegend()
        self.ax = self.view.getAxis('bottom')
        self.ay = self.view.getAxis('left')
        self.WholeData = []

        self.x_scale = self.width_plot / self.width_load

        self.y_scale = self.height_plot / self.height_load

        # print(self.x_scale,' and ',self.x_scale)

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        self.x_element_label.setText(self.items[a])
        self.y_element_label.setText(self.items[b])


        if (self.Left != self.Right) and (self.Down != self.Up) and abs(self.Left) + abs(self.Right) + abs(
                self.Down) + abs(self.Up) != 0:
            self.extent = [self.Left, self.Right, self.Down, self.Up]
        elif (self.Left == self.Right and abs(self.Left) + abs(self.Right) != 0):
            reply = QMessageBox.warning(self, 'Warning', 'You set same value to Left and Right limits.')
            self.extent = 0

        elif (self.Down == self.Up and abs(self.Down) + abs(self.Up) != 0):
            reply = QMessageBox.warning(self, 'Warning', 'You set same value to Up and Down limits.')
            self.extent = 0
        else:
            self.extent = 0

        standardnamechosen = self.StandardsName[int(self.norm_slider.value())]
        standardchosen = self.Standards[standardnamechosen]

        self.norm_slider_label.setText(standardnamechosen)


        PointLabels = []
        XtoFit = []
        YtoFit = []
        Colors=[]
        Alphas=[]
        Markers=[]
        Names=[]

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
            xuse, yuse = 0, 0

            x, y = raw.at[i, self.items[a]], raw.at[i, self.items[b]]


            try:
                xuse = x
                yuse = y

                self.xlabel = self.items[a]
                self.ylabel = self.items[b]

                if (self.Normalize_cb.isChecked()):

                    self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen


                    self.x_element_label.setText(self.xlabel)

                    self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen


                    self.y_element_label.setText(self.ylabel)

                    if self.items[a] in self.Element:
                        xuse = xuse / standardchosen[self.items[a]]

                    if self.items[b] in self.Element:
                        yuse = yuse / standardchosen[self.items[b]]

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)
                    self.xlabel = '$log10$ ' + self.xlabel


                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.ylabel = '$log10$ ' + self.ylabel

                XtoFit.append(xuse)
                YtoFit.append(yuse)
                Colors.append(raw.at[i, 'Color'])
                Alphas.append(raw.at[i, 'Alpha'])
                Names.append(raw.at[i, 'Label'])
                Markers.append(raw.at[i, 'Marker'])


            except(ValueError):
                pass


        #self.Xleft, self.Xright, self.Ydown, self.Yup = min(XtoFit), max(XtoFit), min(YtoFit), max(YtoFit)

        z = np.polyfit(YtoFit, XtoFit,self.FitLevel)

        Yline = np.linspace(min(YtoFit), max(YtoFit), 30)

        #Yline = np.linspace(self.Ydown,self.Yup, 30)

        p = np.poly1d(z)
        Xline = p(Yline)

        print(z)
        self.reference=str(z)
        self.textbox.setText('x=f(y) Polyfitting parameter：' + '\n' + self.reference)


        xmin, xmax = min(XtoFit), max(XtoFit)
        ymin, ymax = min(YtoFit), max(YtoFit)

        xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]

        command = '''xx, yy = np.mgrid[xmin:xmax:''' + str(self.ShapeGroups) + '''j, ymin:ymax:''' + str(
            self.ShapeGroups) + '''j]'''
        exec(command)

        positions = np.vstack([xx.ravel(), yy.ravel()])
        values = np.vstack([raw[self.items[a]], raw[self.items[b]]])
        kernel = st.gaussian_kde(values)
        f = np.reshape(kernel(positions).T, xx.shape)
        data = f
        img = pg.ImageItem(data)

        TargetWidth = img.width()
        TargetHeight = img.height()

        OriginalWidth = abs(xmax - xmin)
        OriginalHeight = abs(ymax - ymin)

        xscale = TargetWidth / OriginalWidth
        yscale = TargetHeight / OriginalHeight

        XtoFitUsed = []
        YtoFitUsed = []

        XlineUsed = []
        YlineUsed = []

        for i in range(len(XtoFit)):
            XtoFitUsed.append((XtoFit[i] - xmin) * xscale)
            YtoFitUsed.append((YtoFit[i] - ymin) * yscale)

        for i in range(len(Xline)):
            XlineUsed.append((Xline[i] - xmin) * xscale)
            YlineUsed.append((Yline[i] - ymin) * yscale)

        Xoriginal = np.arange(xmin, xmax, (xmax - xmin) / 10)
        Yoriginal = np.arange(ymin, ymax, (ymax - ymin) / 10)

        XonPlot = self.GetASequence()
        YonPlot = self.GetASequence()

        XonStick = []
        YonStick = []

        for i in range(len(XonPlot)):
            XonStick.append([XonPlot[i], Xoriginal[i]])
            YonStick.append([YonPlot[i], Yoriginal[i]])
            pass

        self.ax.setTicks([XonStick])
        self.ay.setTicks([YonStick])



        self.view.plot(XtoFitUsed, YtoFitUsed, pen=None, symbol=Markers[i], symbolPen=None, symbolSize=3,
                  symbolBrush=(100, 255, 255, 48), name= PointLabels)

        if (self.fit_cb.isChecked()):
            #self.axes.plot(Xline, Yline, 'b-')
            self.view.plot(XlineUsed, YlineUsed, pen='b')

            pass


        if (self.shape_cb.isChecked()):

            ## generate empty curves
            curves = []

            levels = np.linspace(data.min(), data.max(), 10)
            for i in range(len(levels)):
                v = levels[i]
                ## generate isocurve with automatic color selection
                c = pg.IsocurveItem(level=v, pen=(i, len(levels) * 1.5))
                c.setParentItem(img)  ## make sure isocurve is always correctly displayed over image
                c.setZValue(10)
                curves.append(c)

            imgLevels = (data.min(), data.max() * 2)

            img.setImage(data, levels=imgLevels)

            img.setScaledMode()

            for c in curves:
                c.setData(data)

            self.view.addItem(img)
            pass




