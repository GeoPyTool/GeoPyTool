from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class XYZ(AppForm,Tool):
    Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
               u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

    StandardsName = ['PM', 'OIB', 'EMORB', 'C1', 'NMORB','UCC_Rudnick & Gao2003']


    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, UCC_Rudnick & Gao2003'
    sentence=''

    NameChosen = 'PM'
    Standards = {
        'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
               'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
               'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
               'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.737, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
               'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
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
        'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                  'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                  'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                  'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                  'Yb': 3.05, 'Lu': 0.455},
        'UCC_Rudnick & Gao2003':{'K':23244.13776,'Ti':3835.794545,'P':654.6310022,'Li':24,'Be':2.1,'B':17,'N':83,'F':557,'S':62,'Cl':370,'Sc':14,'V':97,'Cr':92,
                                 'Co':17.3,'Ni':47,'Cu':28,'Zn':67,'Ga':17.5,'Ge':1.4,'As':4.8,'Se':0.09,
                                 'Br':1.6,'Rb':84,'Sr':320,'Y':21,'Zr':193,'Nb':12,'Mo':1.1,'Ru':0.34,
                                 'Pd':0.52,'Ag':53,'Cd':0.09,'In':0.056,'Sn':2.1,'Sb':0.4,'I':1.4,'Cs':4.9,
                                 'Ba':628,'La':31,'Ce':63,'Pr':7.1,'Nd':27,'Sm':4.7,'Eu':1,'Gd':4,'Tb':0.7,
                                 'Dy':3.9,'Ho':0.83,'Er':2.3,'Tm':0.3,'Yb':1.96,'Lu':0.31,'Hf':5.3,'Ta':0.9,
                                 'W':1.9,'Re':0.198,'Os':0.031,'Ir':0.022,'Pt':0.5,'Au':1.5,'Hg':0.05,'Tl':0.9,
                                 'Pb':17,'Bi':0.16,'Th':10.5,'U':2.7}}

    Lines = []
    Tags = []

    xlabel = 'x'
    ylabel = 'y'
    zlabel = 'z'

    description = 'X-Y-Z Diagram'
    unuseful = ['Name',
                'Author',
                'DataType',
                'Label',
                'Index',
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

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)

        self.FileName_Hint='XYZ'

        self.items = []

        self._df_back = df
        self._df = df
        self._given_Standard = Standard


        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        dataframe = self._df
        ItemsAvalibale = self._df.columns.values.tolist()
        ItemsToTest = ['Number', 'Tag','Type', 'Index', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
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
        self.fig = Figure((8.0,8.0), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.7, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)



        self.stat_button = QPushButton('&Stat')
        self.stat_button.clicked.connect(self.Stat)

        self.load_button = QPushButton('&Load Basemap')
        self.load_button.clicked.connect(self.Load)

        self.unload_button = QPushButton('&Unload Basemap')
        self.unload_button.clicked.connect(self.Unload)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int

        self.lda_cb = QCheckBox('&LDA')
        self.lda_cb.setChecked(False)
        self.lda_cb.stateChanged.connect(self.Magic)  # int

        self.norm_cb = QCheckBox('&Norm')
        self.norm_cb.setChecked(False)
        self.norm_cb.stateChanged.connect(self.Magic)  # int

        self.standard_slider = QSlider(Qt.Horizontal)
        self.standard_slider.setRange(0, len(self.StandardsName))

        if len(self._given_Standard) > 0:
            self.standard_slider.setValue(len(self.StandardsName))
            self.right_label = QLabel("Self Defined Standard")

        else:
            self.standard_slider.setValue(0)
            self.right_label = QLabel(self.StandardsName[int(self.standard_slider.value())])

        self.standard_slider.setTracking(True)
        self.standard_slider.setTickPosition(QSlider.TicksBothSides)
        self.standard_slider.valueChanged.connect(self.Magic)  # int
        self.left_label = QLabel('Standard')

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.ValueChooser)  # int



        self.x_seter = QLineEdit(self)
        self.x_seter.textChanged[str].connect(self.LabelSeter)

        #self.x_calculator = QLineEdit(self)



        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Magic)  # int



        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Magic)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.ValueChooser)  # int



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



        self.z_seter = QLineEdit(self)
        self.z_seter.textChanged[str].connect(self.LabelSeter)

        #self.z_calculator = QLineEdit(self)


        self.logz_cb = QCheckBox('&Log')
        self.logz_cb.setChecked(False)
        self.logz_cb.stateChanged.connect(self.Magic)  # int



        self.x_multiplier = QLineEdit(self)
        self.x_multiplier.textChanged[str].connect(self.Magic)
        self.y_multiplier = QLineEdit(self)
        self.y_multiplier.textChanged[str].connect(self.Magic)
        self.z_multiplier = QLineEdit(self)
        self.z_multiplier.textChanged[str].connect(self.Magic)

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



        for w in [self.save_button,self.stat_button, self.load_button, self.unload_button,
                  self.legend_cb,self.lda_cb,self.show_data_index_cb]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.norm_cb, self.left_label, self.standard_slider,self.right_label]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_multiplier, self.x_seter, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_multiplier, self.y_seter, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)


        for w in [self.logz_cb, self.z_multiplier, self.z_seter, self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)



        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


        w=self.width()
        h=self.height()
        self.x_seter.setFixedWidth(w/10)
        self.y_seter.setFixedWidth(w/10)
        self.z_seter.setFixedWidth(w/10)

        self.x_multiplier.setFixedWidth(w/10)
        self.y_multiplier.setFixedWidth(w/10)
        self.z_multiplier.setFixedWidth(w/10)


        #self.standard_slider.setMinimumWidth(w/5)

        #self.right_label.setFixedWidth(w/5)




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
                    width = width+letter

            #print(width)



            height=''
            for letter in svg_height[0]:
                if letter in digit:
                    height = height+letter

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

    def Unload(self):
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

        dataframe_values_only = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe_values_only = dataframe_values_only.dropna(axis='columns')
        ItemsAvalibale = dataframe_values_only.columns.values.tolist()
        data_columns = ItemsAvalibale

        df = dataframe_values_only

        numdf = (df.drop(data_columns, axis=1).join(df[data_columns].apply(pd.to_numeric, errors='coerce')))

        numdf = numdf[numdf[data_columns].notnull().all(axis=1)]

        ItemsAvalibale = numdf.columns.values.tolist()
        dataframe_values_only = numdf



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
                            #print(a)
                    except(ValueError):
                        pass
                    pass

                self.x_element.setValue(a)
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
                            #print(b)
                    except(ValueError):
                        pass
                    pass
                self.y_element.setValue(b)
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

            self.x_seter.setText(ItemsAvalibale[a])
            self.y_seter.setText(ItemsAvalibale[b])
            self.z_seter.setText(ItemsAvalibale[c])







        self.axes.clear()
        self.axes.axis('off')



        slider_value=int(self.standard_slider.value())

        if slider_value < len(self.StandardsName):
            standardnamechosen = self.StandardsName[slider_value]
            standardchosen = self.Standards[standardnamechosen]

            right_label_text=self.StandardsName[slider_value]

        elif len(self._given_Standard)<=0:
            standardnamechosen = self.StandardsName[slider_value-1]
            standardchosen = self.Standards[standardnamechosen]

            right_label_text = self.StandardsName[slider_value-1]

        else:
            standardnamechosen = "Self Defined Standard"
            standardchosen = self._given_Standard
            right_label_text = "Self Defined Standard"


        self.right_label.setText(right_label_text)


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
        PointColors = []
        XtoFit = []
        YtoFit = []
        LDA_X = []
        LDA_Label = []
        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]
        self.color_list=[]

        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']
            if target not in all_labels:
                all_labels.append(target)
                all_colors.append(color)
                all_markers.append(marker)
                all_alpha.append(alpha)
            if color not in self.color_list:
                self.color_list.append(color)


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

            if pd.isnull(dataframe.at[i, self.items[a]]) or pd.isnull(dataframe.at[i, self.items[b]]) or pd.isnull(raw.at[i, self.items[c]]):
                pass

            else:
                #x, y, z = raw.at[i, self.items[a]], raw.at[i, self.items[b]],raw.at[i, self.items[c]]

                x, y ,z  = dataframe_values_only.at[i, self.items[a]], dataframe_values_only.at[i, self.items[b]], dataframe_values_only.at[i, self.items[c]]


                try:
                    xuse = x
                    yuse = y
                    zuse = z



                    self.xlabel = self.items[a]
                    self.ylabel = self.items[b]
                    self.zlabel = self.items[c]


                    if (self.x_multiplier.text() != ''):
                        try:
                            x_string = self.x_multiplier.text()
                            x_timer = float(self.x_multiplier.text())
                            self.xlabel = self.items[a]+'*'+x_string
                            xuse=xuse*x_timer
                        except(ValueError):
                            pass

                    if (self.y_multiplier.text() != ''):
                        try:
                            y_string = self.y_multiplier.text()
                            y_timer = float(self.y_multiplier.text())
                            self.ylabel = self.items[b]+'*'+y_string
                            yuse=yuse*y_timer
                        except(ValueError):
                            pass

                    if (self.z_multiplier.text() != ''):
                        try:
                            z_string = self.z_multiplier.text()
                            z_timer = float(self.z_multiplier.text())
                            self.zlabel = self.items[c]+'*'+z_string
                            zuse=zuse*z_timer
                        except(ValueError):
                            pass

                    if (self.norm_cb.isChecked()):
                        self.sentence = self.reference

                        item_a = self.items[a]
                        item_b = self.items[b]
                        item_c = self.items[c]

                        str_to_check = ['ppm', '(', ')', '[', ']', 'wt', '\%']

                        for j in str_to_check:
                            if j in item_a:
                                item_a = item_a.replace(j, "")
                            if j in item_b:
                                item_b = item_b.replace(j, "")
                            if j in item_c:
                                item_c = item_c.replace(j, "")

                        if item_a in self.Element:
                            self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen
                            xuse = xuse / standardchosen[item_a]

                        if item_b in self.Element:
                            self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen
                            yuse = yuse / standardchosen[item_b]

                        if item_c in self.Element:
                            self.zlabel = self.items[c] + ' Norm by ' + standardnamechosen
                            zuse = zuse / standardchosen[item_c]

                    if (self.logx_cb.isChecked()):
                        xuse = math.log(x, 10)
                        newxlabel = '$log10$('+self.xlabel+')'
                    else:
                        newxlabel =  self.xlabel


                    if (self.logy_cb.isChecked()):
                        yuse = math.log(y, 10)
                        newylabel = '$log10$('+self.ylabel+')'
                    else:
                        newylabel =  self.ylabel


                    if (self.logz_cb.isChecked()):
                        zuse = math.log(y, 10)
                        newzlabel = '$log10$('+self.zlabel+')'
                    else:
                        newzlabel =  self.zlabel



                    TPoints.append(TriPoint((xuse, yuse, zuse), Size=raw.at[i, 'Size'], Color=raw.at[i, 'Color'],
                                            Alpha=raw.at[i, 'Alpha'], Marker=raw.at[i, 'Marker'], Label=TmpLabel))


                    LDA_X.append(self.LogRatioTriToBin(xuse, yuse,zuse))
                    LDA_Label.append(raw.at[i, 'Label'])

                except Exception as e:
                    self.ErrorEvent(text=repr(e))
                    # pass

        self.axes.annotate(newxlabel, xy=(0,0), xytext=(-4, -4),fontsize=6)
        self.axes.annotate(newylabel, xy=(100,0), xytext=(100, -4),fontsize=6)
        self.axes.annotate(newzlabel, xy=(50,86.7), xytext=(45, 90),fontsize=6)


        for i in range(len(TPoints)):
            self.axes.scatter(TPoints[i].X, TPoints[i].Y, marker=TPoints[i].Marker, s=TPoints[i].Size,
                              color=TPoints[i].Color, alpha=TPoints[i].Alpha,
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

        if (self.lda_cb.isChecked()):
            le = LabelEncoder()
            le.fit(LDA_Label)
            original_label = le.transform(LDA_Label)
            # print(self.result_to_fit.values.tolist())
            model = LinearDiscriminantAnalysis()
            model.fit(LDA_X, original_label)
            V_list=[]
            W_list=[]
            for i in range(len(TPoints)):
                V_list.append(TPoints[i].V)
                W_list.append(TPoints[i].W)


            xmin, xmax = min(V_list),max(V_list)
            ymin, ymax = min(W_list),max(W_list)

            self.model = model
            self.cmap_trained_data = ListedColormap(self.color_list)
            xx, yy = np.meshgrid(np.linspace(xmin, xmax, 200),
                                 np.linspace(ymin, ymax, 200))

            a1,b1,c1= self.BackLogRatioBinToTri(xmin, ymin)
            a2,b2,c2= self.BackLogRatioBinToTri(xmax, ymax)

            xnewmin,ynewmin= self.TriToBin(a1,b1,c1)
            xnewmax,ynewmax= self.TriToBin(a2,b2,c2)
            # xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]

            xplot,yplot = np.meshgrid(np.linspace(xnewmin, xnewmax, 200),
                                 np.linspace(ynewmin, ynewmax, 200))

            Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

            self.axes.contourf(xplot, yplot, Z.reshape(xx.shape), cmap=ListedColormap(self.color_list), alpha=0.2)

            # Z_proba = model.predict_proba(np.c_[xx.ravel(), yy.ravel()])
            # self.axes.pcolormesh(xx, yy, Z.reshape(xx.shape), cmap=ListedColormap(self.color_list), alpha=0.2)
            # Z = self.LDA.predict(np.c_[xx.ravel(), yy.ravel()])
            # Z = self.LDA.predict_proba(np.c_[xx.ravel(), yy.ravel()])
            # plt.pcolormesh(xx, yy, Z, cmap='red_blue_classes', norm=colors.Normalize(0., 1.), zorder=0)
            # self.axes.contourf(xx, yy, Z, cmap='hot', alpha=0.2)
            # tmpZ = Z[:, 0].reshape(xx.shape)
            # self.axes.pcolormesh(xx, yy, tmpZ, cmap=ListedColormap(self.color_list[i]),norm=colors.Normalize(0., 1.), zorder=0,alpha=0.4)
            # self.axes.contour(xx, yy, Z, [0.5], linewidths=2., colors='white')

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

        self.tablepop = TableViewer(df=StatResultDf,title='X-Y-Z Statistical Result')
        self.tablepop.show()

        self.Intro = StatResultDf

        return(StatResultDf)


