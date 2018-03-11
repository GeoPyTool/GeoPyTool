from geopytool.ImportDependence import *
from geopytool.CustomClass import *
from geopytool.TabelViewer import TabelViewer

class IsoTope(AppForm):


    reference = 'Ludwig, K. R. (2003). "Isoplot, rev. 3.75. A geochronological toolkit for microsoft excel."  5: 1-75.'
    sentence = ''

    Lines = []
    Tags = []

    xlabel = 'x'
    ylabel = 'y'

    description = 'IsoTope diagram'
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


    FitLevel=1


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

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int


        self.fit_cb= QCheckBox('&PolyFit')
        self.fit_cb.setChecked(False)
        self.fit_cb.stateChanged.connect(self.Magic)  # int

        self.fit_label = QLabel('Fit Exp is')
        self.fit_seter = QLineEdit(self)
        self.fit_seter.textChanged[str].connect(self.FitChanged)



        self.lambda_label = QLabel('Lambda is')
        self.lambda_seter = QLineEdit(self)
        self.lambda_seter.textChanged[str].connect(self.Magic)



        self.fit_slider_label = QLabel('y= f(x)')
        self.fit_slider = QSlider(Qt.Vertical)
        self.fit_slider.setRange(0, 1)
        self.fit_slider.setValue(0)
        self.fit_slider.setTracking(True)
        self.fit_slider.setTickPosition(QSlider.TicksBothSides)
        self.fit_slider.valueChanged.connect(self.Magic)  # int



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


        #
        # Layout with box sizers
        #
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()


        for w in [self.save_button,self.draw_button,
                  self.legend_cb]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)


        for w in [self.fit_slider_label ,self.fit_slider,self.fit_cb,self.fit_label, self.fit_seter]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)


        for w in [self.x_element_label,self.x_seter, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.y_element_label,self.y_seter, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)


        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)




    def Reset(self):
        self.flag = 0
        self.Magic()


    def FitChanged(self, text):
        w = 'Fit Exp is' + text
        self.fit_label.setText(w)
        self.fit_label.adjustSize()

        try:
            self.FitLevel = float(text)
        except:
            pass

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

        raw = self._df



        if self.LabelSetted == True:
            if(self.x_seter.text()!=''):
                a = int(self.x_seter.text())
            else:
                a = int(self.x_element.value())


            if (self.y_seter.text() != ''):
                b = int(self.y_seter.text())
            else:
                b = int(self.y_element.value())

        if self.ValueChoosed == True:
            a = int(self.x_element.value())
            b = int(self.y_element.value())



        self.axes.clear()



        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])

        PointLabels = []


        XtoFit = []
        YtoFit = []


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

                self.sentence = self.reference


                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel, edgecolors='black')

                XtoFit.append(xuse)
                YtoFit.append(yuse)

            except(ValueError):
                pass

        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)

        self.x_element_label.setText(self.xlabel)
        self.y_element_label.setText(self.ylabel)


        if self.LimSet==False:
            self.Xleft, self.Xright, self.Ydown, self.Yup = min(XtoFit), max(XtoFit), min(YtoFit), max(YtoFit)





        #Yline = np.linspace(min(YtoFit), max(YtoFit), 30)




        if(int(self.fit_slider.value())== 0):
            Xline = np.linspace(self.Xleft, self.Xright, 30)
            z = np.polyfit(XtoFit, YtoFit, self.FitLevel)
            self.fit_slider_label.setText('y= f(x)')
            p = np.poly1d(z)
            Yline = p(Xline)
            formular='y= f(x)'


        elif(int(self.fit_slider.value())== 1):
            Yline = np.linspace(self.Ydown, self.Yup, 30)
            z = np.polyfit(YtoFit, XtoFit, self.FitLevel)
            self.fit_slider_label.setText('x= f(y)')
            p = np.poly1d(z)
            Xline = p(Yline)
            formular='x= f(y)'




        self.textbox.setText(formular+' Polyfitting parameter：' + '\n' +str(z)+'\n\n'+ self.sentence)



        if (self.fit_cb.isChecked()):
            self.axes.plot(Xline, Yline, 'b-')


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        self.canvas.draw()



        return(dict)

    def relation(self,data1=np.ndarray,data2=np.ndarray):
        data=array([data1,data2])
        dict={'cov':cov(data,bias=1),'corrcoef':corrcoef(data)}
        return(dict)
