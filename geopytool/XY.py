from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer

class XY(AppForm):
    Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
               u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
               u'Li',
               u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']


    StandardsName = ['PM', 'OIB', 'EMORB', 'C1', 'NMORB','UCC_Rudnick & Gao2003']


    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, UCC_Rudnick & Gao2003'
    sentence =''

    ContainNan = False
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
        'UCC_Rudnick & Gao2003':{'Li':24,'Be':2.1,'B':17,'N':83,'F':557,'S':62,'Cl':370,'Sc':14,'V':97,'Cr':92,
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

    description = 'X-Y Diagram'
    unuseful = ['Name',
                'Mineral',
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

    FitLevel=1
    FadeGroups=100
    ShapeGroups=200

    LabelSetted = False
    ValueChoosed = True
    FlagLoaded=False
    TypeLoaded=''

    whole_labels=[]

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)


        self.FileName_Hint='XY'


        self.items = []
        self.a_index= 0
        self.b_index= 1


        self.raw = df
        self._df = df
        self._df_back=df
        self._given_Standard = Standard

        self.All_X=[]
        self.All_Y=[]

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')


        self.rawitems = self.raw.columns.values.tolist()



        dataframe = self._df
        ItemsAvalibale = self._df.columns.values.tolist()
        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width','Label']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)


        dataframe_values_only = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe_values_only = dataframe_values_only.dropna(axis='columns')


        ItemsAvalibale = dataframe_values_only.columns.values.tolist()

        data_columns= ItemsAvalibale

        df= dataframe_values_only

        numdf = (df.drop(data_columns, axis=1).join(df[data_columns].apply(pd.to_numeric, errors='coerce')))

        numdf = numdf[numdf[data_columns].notnull().all(axis=1)]

        ItemsAvalibale = numdf.columns.values.tolist()
        dataframe_values_only=numdf

        self.items = dataframe_values_only.columns.values.tolist()

        #print(self.items)
        self.dataframe_values_only=dataframe_values_only

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

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.13, bottom=0.2, right=0.7, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.load_data_button = QPushButton('&Add Data to Compare')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        self.save_plot_button = QPushButton('&Save IMG')
        self.save_plot_button .clicked.connect(self.saveImgFile)

        self.stat_button = QPushButton('&Show Stat')
        self.stat_button.clicked.connect(self.Stat)


        self.load_img_button = QPushButton('&Load Basemap')
        self.load_img_button.clicked.connect(self.Load)

        self.unload_img_button = QPushButton('&Unload Basemap')
        self.unload_img_button.clicked.connect(self.Unload)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int



        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Magic)  # int


        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Magic)  # int


        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Magic)  # int


        self.fit_cb= QCheckBox('&PolyFit')
        self.fit_cb.setChecked(False)
        self.fit_cb.stateChanged.connect(self.Magic)  # int




        self.fit_seter = QLineEdit(self)
        self.fit_seter.textChanged[str].connect(self.FitChanged)



        self.fit_slider_label = QLabel('y= f(x) EXP')
        self.fit_slider = QSlider(Qt.Vertical)
        self.fit_slider.setRange(0, 1)
        self.fit_slider.setValue(0)
        self.fit_slider.setTracking(True)
        self.fit_slider.setTickPosition(QSlider.TicksBothSides)
        self.fit_slider.valueChanged.connect(self.Magic)  # int


        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Magic)  # int

        #self.shape_label = QLabel('Step')
        #self.shape_seter = QLineEdit(self)
        #self.shape_seter.textChanged[str].connect(self.ShapeChanged)



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
        self.left_label= QLabel('Standard' )



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




        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Magic)  # int


        self.save_predict_button_selected = QPushButton('&Predict Selected')
        self.save_predict_button_selected.clicked.connect(self.showPredictResultSelected)

        self.save_predict_button = QPushButton('&Predict All')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Add Data to Compare')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        self.width_size_seter_label = QLabel('SVG Width')
        self.width_size_seter = QLineEdit(self)

        self.width_size_seter.textChanged[str].connect(self.WChanged)

        self.height_size_seter_label = QLabel('SVG Height')
        self.height_size_seter = QLineEdit(self)

        self.height_size_seter.textChanged[str].connect(self.HChanged)

        self.Left_size_seter_label = QLabel('PNG Left')
        self.Left_size_seter = QLineEdit(self)

        self.Left_size_seter.textChanged[str].connect(self.LeftChanged)

        self.Right_size_seter_label = QLabel('PNG Right')
        self.Right_size_seter = QLineEdit(self)

        self.Right_size_seter.textChanged[str].connect(self.RightChanged)

        self.Up_size_seter_label = QLabel('PNG Top')
        self.Up_size_seter = QLineEdit(self)

        self.Up_size_seter.textChanged[str].connect(self.UpChanged)

        self.Down_size_seter_label = QLabel('PNG Bottom')
        self.Down_size_seter = QLineEdit(self)

        self.Down_size_seter.textChanged[str].connect(self.DownChanged)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()

        w=self.width()
        h=self.height()

        #self.load_data_button.setFixedWidth(w/4)


        self.kernel_select = QSlider(Qt.Horizontal)
        self.kernel_select.setRange(0, len(self.kernel_list)-1)
        self.kernel_select.setValue(0)
        self.kernel_select.setTracking(True)
        self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        self.kernel_select.valueChanged.connect(self.Magic)  # int
        self.kernel_select_label = QLabel('Kernel')

        for w in [self.save_plot_button ,self.stat_button,self.load_data_button,self.save_predict_button,self.save_predict_button_selected]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)


        for w in [self.legend_cb,self.show_load_data_cb,self.show_data_index_cb, self.norm_cb,self.shape_cb,self.hyperplane_cb,self.kernel_select_label,self.kernel_select]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)


        for w in [self.left_label, self.standard_slider,self.right_label,self.fit_cb,self.fit_slider,self.fit_slider_label ,self.fit_seter]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)


        for w in [self.logx_cb,self.x_seter, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb,self.y_seter, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)


        for w in [self.load_img_button, self.width_size_seter_label, self.width_size_seter, self.height_size_seter_label,
                  self.height_size_seter]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignLeft)



        for w in [self.unload_img_button,self.Left_size_seter_label, self.Left_size_seter,
                  self.Right_size_seter_label,  self.Right_size_seter,self.Down_size_seter_label, self.Down_size_seter,
                  self.Up_size_seter_label ,self.Up_size_seter]:
            self.hbox5.addWidget(w)
            self.hbox5.setAlignment(w, Qt.AlignLeft)



        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.vbox.addLayout(self.hbox5)

        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)





        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        w=self.width()
        h=self.height()

        self.x_seter.setFixedWidth(w/10)
        self.y_seter.setFixedWidth(w/10)

        '''
        self.save_plot_button.setFixedWidth(w/10)
        self.stat_button.setFixedWidth(w/10)
        self.load_data_button.setFixedWidth(w/4)
        self.save_predict_button_selected.setFixedWidth(w/4)
        self.save_predict_button.setFixedWidth(w/4)
        '''

        self.standard_slider.setFixedWidth(w/5)

        self.right_label.setFixedWidth(w/5)

        self.fit_seter.setFixedWidth(w/20)

        self.load_img_button.setFixedWidth(w/5)
        self.unload_img_button.setFixedWidth(w/5)

        self.width_size_seter_label.setFixedWidth(w/10)
        self.height_size_seter_label.setFixedWidth(w/10)

        self.width_size_seter.setMinimumWidth(w/20)
        self.height_size_seter.setMinimumWidth(w/20)

        self.Right_size_seter_label.setFixedWidth(w/10)
        self.Left_size_seter_label.setFixedWidth(w/10)
        self.Up_size_seter_label.setFixedWidth(w/10)
        self.Down_size_seter_label.setFixedWidth(w/10)

        self.Right_size_seter.setFixedWidth(w/20)
        self.Left_size_seter.setFixedWidth(w/20)
        self.Up_size_seter.setFixedWidth(w/20)
        self.Down_size_seter.setFixedWidth(w/20)


    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.Magic()


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

        #print(fileName, '\t', filetype)


        if len(fileName)>0:
            self.FlagLoaded= True

        if ('svg' in fileName):

            self.TypeLoaded='svg'
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

            self.TypeLoaded='png'

            self.img = mpimg.imread(fileName)
            self.flag = 1


        self.Magic()

    def Unload(self):
        self.flag = 0

        self.FlagLoaded = False
        self.TypeLoaded = ''

        self.Magic()

    def WChanged(self, text):
        try:
            self.width_plot = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.x_scale = self.width_plot / self.width_load

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

        self.Magic()

    def HChanged(self, text):

        try:
            self.height_plot = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.y_scale = self.height_plot / self.height_load

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

        self.Magic()

    # text_location= [path.getAttribute('transform') for path in doc.getElementsByTagName('text')]
    '''
    tmppolygon_points=[]
    for i in polygon_points:
        tmppolygon_points.append(i.split())

    polygon=[]
    for i in tmppolygon_points:
        for l in range(len(i)):
            a=float((i[l].split(','))[0])
            b=float((i[l].split(','))[1])

            polygon.append([a,b])
    '''

    def LeftChanged(self, text):
        try:
            self.Left = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.Magic()

    def RightChanged(self, text):
        try:
            self.Right = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.Magic()

    def UpChanged(self, text):

        try:
            self.Up = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.Magic()

    def DownChanged(self, text):

        try:
            self.Down = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.Magic()

    def FitChanged(self, text):
        try:
            self.FitLevel = float(text)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.Magic()

    def ShapeChanged(self, text):
        w = 'Shape' + text
        self.shape_label.setText(w)
        self.shape_label.adjustSize()

        try:
            self.ShapeGroups = int(text)

        except Exception as e:
            self.ErrorEvent(text=repr(e))

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

        k_s = int(self.kernel_select.value())
        self.kernel_select_label.setText(self.kernel_list[k_s])


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


        dataframe_values_only = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe_values_only = dataframe_values_only.dropna(axis='columns')
        ItemsAvalibale = dataframe_values_only.columns.values.tolist()
        data_columns= ItemsAvalibale

        df= dataframe_values_only

        numdf = (df.drop(data_columns, axis=1).join(df[data_columns].apply(pd.to_numeric, errors='coerce')))

        numdf = numdf[numdf[data_columns].notnull().all(axis=1)]

        ItemsAvalibale = numdf.columns.values.tolist()
        dataframe_values_only=numdf



        a = int(self.x_element.value())
        b = int(self.y_element.value())



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

                    except Exception as e:
                        self.ErrorEvent(text=repr(e))
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
                    except Exception as e:
                        self.ErrorEvent(text=repr(e))
                        pass
                    pass
                self.y_element.setValue(b)
            else:
                b = int(self.y_element.value())


            if b> len(ItemsAvalibale)-1:
                b = int(self.y_element.value())
            if a> len(ItemsAvalibale)-1:
                a = int(self.x_element.value())


        if self.ValueChoosed == True:
            a = int(self.x_element.value())
            b = int(self.y_element.value())

            self.x_seter.setText(ItemsAvalibale[a])
            self.y_seter.setText(ItemsAvalibale[b])

        self.a_index= a
        self.b_index= b


        self.axes.clear()

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


        if self.flag != 0:
            if self.extent != 0:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto', extent=self.extent)
            else:
                self.axes.imshow(self.img, interpolation='nearest', aspect='auto')

        self.axes.set_xlabel(ItemsAvalibale[a])

        self.axes.set_ylabel(ItemsAvalibale[b])

        PointLabels = []
        PointColors = []
        XtoFit = []
        YtoFit = []

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

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

        self.whole_labels = all_labels


        df = self.CleanDataFile(self._df)

        for i in range(len(df)):
            TmpLabel = ''
            if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(df.at[i, 'Label'])
                TmpLabel = df.at[i, 'Label']

            TmpColor = ''
            if (df.at[i, 'Color'] in PointColors or df.at[i, 'Color'] == ''):
                TmpColor = ''
            else:
                PointColors.append(df.at[i, 'Color'])
                TmpColor = df.at[i, 'Color']

            x, y = dataframe_values_only.at[i, self.items[a]], dataframe_values_only.at[i, self.items[b]]

            try:
                xuse = x
                yuse = y

                self.xlabel = self.items[a]
                self.ylabel = self.items[b]

                if (self.norm_cb.isChecked()):

                    self.sentence = self.reference
                    #print(self.items[a] , self.items[a] in self.Element)

                    item_a =self.items[a]
                    item_b =self.items[b]

                    str_to_check=['ppm','(',')','[',']','wt','\%']

                    for j in str_to_check:
                        if j in item_a:
                            item_a=item_a.replace(j, "")
                        if j in item_b:
                            item_b=item_b.replace(j, "")

                    if item_a in self.Element:
                        self.xlabel = self.items[a] + ' Norm by ' + standardnamechosen
                        xuse = xuse / standardchosen[item_a]

                    if item_b in self.Element:
                        self.ylabel = self.items[b] + ' Norm by ' + standardnamechosen
                        yuse = yuse / standardchosen[item_b]

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)
                    newxlabel = '$log10$( ' + self.xlabel + ')'

                    self.axes.set_xlabel(newxlabel)
                else:

                    self.axes.set_xlabel(self.xlabel)

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    newylabel = '$log10$( ' + self.ylabel + ')'

                    self.axes.set_ylabel(newylabel)
                else:
                    self.axes.set_ylabel(self.ylabel)

                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel)
                '''

                if raw.at[i, 'Color'] == 'w' or raw.at[i, 'Color'] =='White':
                    self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel, edgecolors='black')
                else:
                    self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                      s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                      label=TmpLabel,
                                      edgecolors='white')
                '''

                XtoFit.append(xuse)
                YtoFit.append(yuse)

            except Exception as e:
                self.ErrorEvent(text=repr(e))
                #pass





        #Yline = np.linspace(min(YtoFit), max(YtoFit), 30)


        ResultStr=''
        BoxResultStr=''
        Paralist=[]

        #print(XtoFit, '\n', YtoFit)

        if len(XtoFit) != len(YtoFit):

            reply = QMessageBox.information(self, 'Warning','Your Data X and Y have different length!')

            pass

        fitstatus = True

        if (int(self.fit_slider.value()) == 0):
            if len(XtoFit)>0:
                Xline = np.linspace(min(XtoFit), max(XtoFit), 30)
                try:
                    np.polyfit(XtoFit, YtoFit, self.FitLevel)
                except Exception as e:
                    self.ErrorEvent(text=repr(e))
                    fitstatus = False


                if (fitstatus == True):
                    try:
                        opt, cov = np.polyfit(XtoFit, YtoFit, self.FitLevel, cov=True)
                        self.fit_slider_label.setText('y= f(x) EXP')
                        p = np.poly1d(opt)
                        Yline = p(Xline)
                        formular = 'y= f(x):'
                        sigma = np.sqrt(np.diag(cov))


                        N = len(XtoFit)
                        F = N - 2
                        MSWD = 1 + 2 * np.sqrt(2 / F)
                        MSWDerr = np.sqrt(2 / F)

                        for i in range(int(self.FitLevel + 1)):
                            Paralist.append([opt[i], sigma[i]])

                            if int(self.fit_slider.value()) == 0:

                                if (self.FitLevel - i == 0):
                                    ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i]) + '+'
                                    BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + '\n'

                                else:
                                    ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i]) + '$x^' + str(
                                        self.FitLevel - i) + '$' + '+'
                                    BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + 'x^' + str(
                                        self.FitLevel - i) + '+\n'


                            elif (int(self.fit_slider.value()) == 1):

                                if (self.FitLevel - i == 0):
                                    ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i]) + '+'
                                    BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + '+\n'



                                else:
                                    ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i]) + '$y^' + str(
                                        self.FitLevel - i) + '$' + '+'
                                    BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + 'y^' + str(
                                        self.FitLevel - i) + '+\n'

                                pass

                            pass

                        self.textbox.setText(formular + '\n' + BoxResultStr + '\n MSWD(±2σ)' + str(MSWD) + '±' + str(
                            2 * MSWDerr) + '\n' + self.sentence)

                        if (self.fit_cb.isChecked()):
                            self.axes.plot(Xline, Yline, 'b-')

                    except Exception as e:
                        self.ErrorEvent(text=repr(e))

        elif (int(self.fit_slider.value()) == 1):

            if len(YtoFit) > 0:

                Yline = np.linspace(min(YtoFit), max(YtoFit), 30)

                try:
                    np.polyfit(YtoFit, XtoFit, self.FitLevel, cov=True)
                except(ValueError, TypeError):
                    fitstatus = False
                    pass

                if (fitstatus == True):
                    opt, cov = np.polyfit(YtoFit, XtoFit, self.FitLevel, cov=True)
                    self.fit_slider_label.setText('x= f(x) EXP')
                    p = np.poly1d(opt)
                    Xline = p(Yline)
                    formular = 'x= f(y):'
                    sigma = np.sqrt(np.diag(cov))

                    N=len(XtoFit)
                    F=N-2
                    MSWD=1+2*np.sqrt(2/F)
                    MSWDerr=np.sqrt(2/F)

                    for i in range(int(self.FitLevel + 1)):
                        Paralist.append([opt[i], sigma[i]])


                        if int(self.fit_slider.value()) == 0:

                            if (self.FitLevel - i == 0):
                                ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i])+'+'
                                BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + '\n'

                            else:
                                ResultStr = ResultStr+ str(opt[i])+'$\pm$'+str(sigma[i])+'$x^'+str(self.FitLevel-i)+'$'+'+'
                                BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + 'x^' + str(
                                self.FitLevel - i) +  '+\n'



                        elif (int(self.fit_slider.value()) == 1):

                            if (self.FitLevel-i==0):
                                ResultStr = ResultStr + str(opt[i]) + '$\pm$' + str(sigma[i])+'+'
                                BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + '+\n'



                            else:
                                ResultStr = ResultStr+ str(opt[i])+'$\pm$'+str(sigma[i])+'$y^'+str(self.FitLevel-i)+'$'+'+'
                                BoxResultStr = BoxResultStr + str(opt[i]) + '±' + str(sigma[i]) + 'y^' + str(
                                self.FitLevel - i) +  '+\n'


                            pass

                        pass

                    self.textbox.setText(formular +'\n'+ BoxResultStr+ '\n MSWD(±2σ)'+str(MSWD)+'±'+str(2*MSWDerr)+'\n' + self.sentence)

                    if (self.fit_cb.isChecked()):
                        self.axes.plot(Xline, Yline, 'b-')

        XtoFit_dic = {}
        YtoFit_dic = {}

        for i in PointLabels:
            XtoFit_dic[i] = []
            YtoFit_dic[i] = []

        for i in range(len(df)):
            Alpha = df.at[i, 'Alpha']
            Marker = df.at[i, 'Marker']
            Label = df.at[i, 'Label']

            xtest = self.dataframe_values_only.at[i, self.items[a]]
            ytest = self.dataframe_values_only.at[i, self.items[b]]

            XtoFit_dic[Label].append(xtest)
            YtoFit_dic[Label].append(ytest)

        if (self.shape_cb.isChecked()):
            for i in PointLabels:

                if XtoFit_dic[i] != YtoFit_dic[i]:
                    xmin, xmax = min(XtoFit_dic[i]), max(XtoFit_dic[i])
                    ymin, ymax = min(YtoFit_dic[i]), max(YtoFit_dic[i])

                    DensityColorMap = 'Greys'
                    DensityAlpha = 0.1

                    DensityLineColor = PointColors[PointLabels.index(i)]
                    DensityLineAlpha = 0.3

                    # Peform the kernel density estimate
                    xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                    # print(self.ShapeGroups)
                    # command='''xx, yy = np.mgrid[xmin:xmax:'''+str(self.ShapeGroups)+ '''j, ymin:ymax:''' +str(self.ShapeGroups)+'''j]'''
                    # exec(command)
                    # print(xx, yy)
                    positions = np.vstack([xx.ravel(), yy.ravel()])
                    values = np.vstack([XtoFit_dic[i], YtoFit_dic[i]])
                    kernelstatus = True
                    try:
                        st.gaussian_kde(values)
                    except Exception as e:
                        self.ErrorEvent(text=repr(e))
                        kernelstatus = False
                    if kernelstatus == True:
                        kernel = st.gaussian_kde(values)
                        f = np.reshape(kernel(positions).T, xx.shape)
                        # Contourf plot
                        cfset = self.axes.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
                        ## Or kernel density estimate plot instead of the contourf plot
                        # self.axes.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
                        # Contour plot
                        cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                        # Label plot
                        #self.axes.clabel(cset, inline=1, fontsize=10)


        if (len(self.data_to_test) > 0):

            contained = True
            missing = 'Miss setting infor:'

            for i in ['Label', 'Color', 'Marker', 'Alpha']:
                if i not in self.data_to_test.columns.values.tolist():
                    contained = False
                    missing = missing + '\n' + i

            if contained == True:
                for i in self.data_to_test.columns.values.tolist():
                    if i not in self._df.columns.values.tolist():
                        self.data_to_test = self.data_to_test.drop(columns=i)

                # print(self.data_to_test)

                test_labels = []
                test_colors = []
                test_markers = []
                test_alpha = []

                for i in range(len(self.data_to_test)):

                    # print(self.data_to_test.at[i, 'Label'])
                    target = self.data_to_test.at[i, 'Label']
                    color = self.data_to_test.at[i, 'Color']
                    marker = self.data_to_test.at[i, 'Marker']
                    alpha = self.data_to_test.at[i, 'Alpha']

                    if target not in test_labels and target not in all_labels:
                        test_labels.append(target)
                        test_colors.append(color)
                        test_markers.append(marker)
                        test_alpha.append(alpha)

                self.whole_labels = self.whole_labels + test_labels

                self.data_to_test_to_fit = self.Slim(self.data_to_test)

                self.load_settings_backup = self.data_to_test
                Load_ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size',
                                    'Alpha',
                                    'Style', 'Width']
                for i in self.data_to_test.columns.values.tolist():
                    if i not in Load_ItemsToTest:
                        self.load_settings_backup = self.load_settings_backup.drop(i, 1)

                print(self.load_settings_backup ,self.data_to_test)

                print(self.load_settings_backup.shape ,self.data_to_test.shape)


                #self.load_result = pd.concat([self.load_settings_backup, pd.DataFrame(self.data_to_test_to_fit)], axis=1)
            try:
                for i in range(len(self.data_to_test)):

                    target = self.data_to_test.at[i, 'Label']
                    if target not in all_labels:
                        all_labels.append(target)
                        tmp_label = self.data_to_test.at[i, 'Label']
                    else:
                        tmp_label=''


                    x_load_test = self.data_to_test.at[i, self.items[a]]
                    y_load_test = self.data_to_test.at[i, self.items[b]]

                    if (self.show_load_data_cb.isChecked()):

                        self.axes.scatter(x_load_test, y_load_test,
                                          marker=self.data_to_test.at[i, 'Marker'],
                                          s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                          alpha=self.data_to_test.at[i, 'Alpha'],
                                          label=tmp_label)

                        '''
                        if raw.at[i, 'Color'] == 'w' or raw.at[i, 'Color'] == 'White':
                            self.axes.scatter(x_load_test, y_load_test,
                                              marker=self.data_to_test.at[i, 'Marker'],
                                              s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                              alpha=self.data_to_test.at[i, 'Alpha'],
                                              label=tmp_label,
                                              edgecolors='black')
                        else:
                            self.axes.scatter(x_load_test, y_load_test,
                                              marker=self.data_to_test.at[i, 'Marker'],
                                              s=self.data_to_test.at[i, 'Size'], color=self.data_to_test.at[i, 'Color'],
                                              alpha=self.data_to_test.at[i, 'Alpha'],
                                              label=tmp_label,
                                              edgecolors='white')
                                              
                        '''



            except Exception as e:
                self.ErrorEvent(text=repr(e))



        if (self.TypeLoaded=='svg'):

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


        self.All_X=XtoFit
        self.All_Y=YtoFit
        if (self.hyperplane_cb.isChecked()):


            if XtoFit != YtoFit:
                clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
                svm_x = XtoFit
                svm_y = YtoFit
                xx, yy = np.meshgrid(np.arange( min(svm_x), max(svm_x), np.ptp(svm_x) / 500),
                                            np.arange( min(svm_y), max(svm_y), np.ptp(svm_y) / 500))

                le = LabelEncoder()
                le.fit(self._df.Label)
                print(len(self._df.Label),self._df.Label)

                class_label=le.transform(self._df.Label)
                svm_train= pd.concat([pd.DataFrame(svm_x),pd.DataFrame(svm_y)], axis=1)

                svm_train=svm_train.values
                clf.fit(svm_train,class_label)
                Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
                Z = Z.reshape(xx.shape)
                self.axes.contourf(xx, yy, Z, cmap='hot', alpha=0.2)

        if (self.show_data_index_cb.isChecked()):

            if 'Index' in self._df_back.columns.values:

                for i in range(len(self._df)):
                    self.axes.annotate(self._df_back.at[i, 'Index'],
                                       xy=(self.All_X[i],
                                           self.All_Y[i]),
                                       color=self._df.at[i, 'Color'],
                                       alpha=self._df.at[i, 'Alpha'])

            else:
                for i in range(len(self._df)):
                        self.axes.annotate('No' + str(i+1),
                                           xy=(self.All_X[i],
                                               self.All_Y[i]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        self.canvas.draw()


    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.Magic()

    def showPredictResultSelected(self):

        k_s = int(self.kernel_select.value())
        try:
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            svm_x = self.All_X
            svm_y = self.All_Y

            le = LabelEncoder()
            le.fit(self._df.Label)
            class_label = le.transform(self._df.Label)
            svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y)], axis=1)
            svm_train = svm_train.values
            clf.fit(svm_train, self._df.Label)
            xx = self.data_to_test_to_fit[self.items[self.a_index]]
            yy = self.data_to_test_to_fit[self.items[self.b_index]]

            Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

            Z2 = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_


            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})],
                axis=1).set_index('Label')
            print(predict_result)


            self.predictpop = TableViewer(df=predict_result, title='SVM Predict Result With '+ self.items[self.a_index]+','+self.items[self.b_index])
            self.predictpop.show()

            '''
            DataFileOutput, ok2 = QFileDialog.getSaveFileName(self, '文件保存', 'C:/',  'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出
            if (DataFileOutput != ''):
                if ('csv' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-4]
                    predict_result.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                    # self.result.to_csv(DataFileOutput + '.csv', sep=',', encoding='utf-8')
                elif ('xlsx' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-5]
                    predict_result.to_excel(DataFileOutput, encoding='utf-8')
                    # self.result.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')
            '''


        except Exception as e:
            msg = 'You need to load another data to run SVM.\n '
            self.ErrorEvent(text= msg +repr(e) )


    def showPredictResult(self):
        k_s = int(self.kernel_select.value())
        try:
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            le = LabelEncoder()
            le.fit(self._df.Label)
            df_values = self.Slim(self._df)

            clf.fit(df_values, self._df.Label)
            Z = clf.predict(np.c_[self.data_to_test_to_fit])
            Z2 = clf.predict_proba(np.c_[self.data_to_test_to_fit])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_

            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})],
                axis=1).set_index('Label')
            print(predict_result)

            self.predictAllpop = TableViewer(df=predict_result, title='SVM Predict Result with All Items')
            self.predictAllpop.show()


        except Exception as e:
            msg = 'You need to load another data to run SVM.\n '
            self.ErrorEvent(text= msg +repr(e) )



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
            StatResultDict[i] = self.stateval(df[i].values)
        StdSortedList = sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std'])
        StdSortedList.reverse()
        StatResultDf = pd.DataFrame.from_dict(StatResultDict, orient='index')
        StatResultDf['Items']=StatResultDf.index.tolist()
        self.tablepop = TableViewer(df=StatResultDf,title='Statistical Result')
        self.tablepop.show()
        self.Intro = StatResultDf
        return(StatResultDf)


