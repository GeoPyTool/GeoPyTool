from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer



class Saccani(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'$Nb_N(ppm)$'
    ylabel = r'$Th_N(ppm)$'

    itemstocheck = ['Th', 'Nb']
    reference = 'Reference: Emilio Saccani.(2015).A new method of discriminating different types of post-Archean ophiolitic basalts and their tectonic significance using Th-Nb and Ce-Dy-Yb systematics. Geoscience  Frontiers(地学前缘(英文版))   6(4): 481 - 501.'

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']
    REEreference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'

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

    LocationAreas = [[[0.01, 20], [2.2, 8]],
                     [[0.01, 0.1], [0.306, 0.708]],
                     [[0.306, 0.708], [0.5,0.01]],
                     [[0.306, 0.708], [100,1000]]
                     ]

    LocationAreas=  np.log10(LocationAreas)

    AreasHeadClosed = []
    SelectDic = {}

    TypeList=[]


    def create_main_frame(self):
        self.setWindowTitle('Emilio Saccani Plot doi.org/10.1016/j.gsf.2014.03.006.')
        self.resize(800, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((12.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.2, bottom=0.2, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Saccani)  # int


        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Saccani)  # int

        self.standard_slider = QSlider(Qt.Horizontal)
        self.standard_slider.setRange(0, len(self.StandardsName)-1)
        self.standard_slider.setValue(0)
        self.left_label = QLabel('Standard')
        self.right_label = QLabel(self.StandardsName[int(self.standard_slider.value())])
        self.standard_slider.setTracking(True)
        self.standard_slider.setTickPosition(QSlider.TicksBothSides)
        self.standard_slider.valueChanged.connect(self.Saccani)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.legend_cb,self.show_data_index_cb,self.left_label ,self.standard_slider,self.right_label]:
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

        self.standard_slider.setMinimumWidth(w/4)
        self.right_label.setMinimumWidth(w/10)


    def Saccani(self):
        self.axes.clear()
        
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')
        self.axes.set_xticks([-2,-1,0,1,2])
        self.axes.set_xticklabels([0.01,0.1,1,10,100])
        self.axes.set_xlim(left=-2, right=2,)

        self.axes.set_yticks([-2,-1,0,1,2,3])
        self.axes.set_yticklabels([0.01,0.1,1,10,100,1000])
        self.axes.set_ylim(bottom=-2,top=3)

        for i in self.LocationAreas:
            self.DrawLine(i)

        self.Check()
        PointLabels = []
        x = []
        y = []

        slider_value=int(self.standard_slider.value())

        if slider_value < len(self.StandardsName):
            standardnamechosen = self.StandardsName[slider_value]
            standardchosen = self.Standards[standardnamechosen]
            self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[slider_value])

            self.right_label.setText(self.StandardsName[slider_value])

        if (self._changed):
            df =  self.CleanDataFile(self._df)


            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']



                x.append(df.at[i, 'Nb']/standardchosen['Nb'])
                y.append(df.at[i, 'Th']/standardchosen['Th'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))


                self.axes.scatter(np.log10(df.at[i, 'Nb']/standardchosen['Nb']), np.log10(df.at[i, 'Th']/standardchosen['Th']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel)






            if (self.legend_cb.isChecked()):
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

            if (self.show_data_index_cb.isChecked()):

                if 'Index' in self._df.columns.values:

                    for i in range(len(self._df)):
                        self.axes.annotate(self._df.at[i, 'Index'],
                                           xy=(np.log10(df.at[i, 'Nb']/standardchosen['Nb']),
                                               np.log10(df.at[i, 'Th']/standardchosen['Th'])),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
                else:
                    for i in range(len(self._df)):
                        self.axes.annotate('No' + str(i + 1),
                                           xy=(np.log10(df.at[i, 'Nb']/standardchosen['Nb']),
                                               np.log10(df.at[i, 'Th']/standardchosen['Th'])),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
            self.canvas.draw()




        self.OutPutTitle='Saccani'

        self.OutPutData = pd.DataFrame(
            {'Label': self.LabelList,
             'RockType': self.TypeList
             })

        self.OutPutFig=self.fig

