from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class Trace(AppForm):
    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
              30, 31, 32, 33, 34, 35, 36, 37]
    xticklabels = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr', u'Mo',
                   u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
                   u'Li',
                   u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']


    itemstocheck = ['Cs', 'Tl', 'Rb', 'Ba', 'W', 'Th', '', 'Nb', 'Ta', 'K', 'La', 'Ce', 'Pb', 'Pr', 'Mo',
                   'Sr', 'P', 'Nd', 'F', 'Sm', 'Zr', 'Hf', 'E', 'Sn', 'Sb', 'Ti', 'Gd', 'Tb', 'Dy',
                   'Li',
                   'Y', 'Ho', 'Er', 'Tm', 'Yb', 'L']

    StandardsName = ['OIB', 'EMORB', 'C1', 'PM', 'NMORB']
    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.'

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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Trace Standardlized Pattern Diagram')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Trace')

        self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr',
                        u'Mo',
                        u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
                        u'Li',
                        u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

        self.WholeData = []
        self.X0 = 1
        self.X1 = 37
        self.X_Gap = 37

        self.create_main_frame()
        self.create_status_bar()


    def Check(self):

        row = self._df.index.tolist()
        col = self._df.columns.tolist()
        itemstocheck = self.itemstocheck
        checklist = list((set(itemstocheck).union(set(col))) ^ (set(itemstocheck) ^ set(col)))
        if len(checklist) > 1 :
            self.OutPutCheck = True
        else:
            self.OutPutCheck = False
        return(self.OutPutCheck)



    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.8, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        #self.axes.axis('off')

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        #self.result_button = QPushButton('&Result')
        #self.result_button.clicked.connect(self.Trace)

        self.Type_cb = QCheckBox('&CS-Lu (37 Elements)')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Trace)  # int

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Trace)  # int


        self.standard = QSlider(Qt.Horizontal)
        self.standard.setRange(0, 4)
        self.standard.setValue(0)
        self.standard.setTracking(True)
        self.standard.setTickPosition(QSlider.TicksBothSides)
        self.standard.valueChanged.connect(self.Trace)  # int

        self.standard_label = QLabel('Standard: ' + self.StandardsName[int(self.standard.value())])


        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.Type_cb,
                  self.legend_cb, self.standard_label, self.standard]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[int(self.standard.value())])
        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


    def Trace(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
              Top=6, Y0=-1,
              Y1=3, Y_Gap=5, FontSize=12,
              xLabel=r'$Trace-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        if (self.Type_cb.isChecked()):
            self.Type_cb.setText('&CS-Lu (37 Elements)')
            self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                            u'Pr', u'Mo',
                            u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb',
                            u'Dy', u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            CommonElements = [i for i in self.Element if i in self._df.columns]
            self.Element = CommonElements
            self.xticks = [i for i in range(1,len(CommonElements)+2)]
            self.xticklabels = CommonElements

            self.setWindowTitle('Trace Standardlized Pattern Diagram CS-Lu '+ str(len(CommonElements)+1) +' Elements')



        else:
            self.Type_cb.setText('&Rb-Lu (27 Elements)')
            self.Element = [u'Rb', u'Ba', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pr', u'Sr', u'P', u'Nd',
                            u'Zr', u'Hf',
                            u'Sm', u'Eu', u'Ti', u'Tb', u'Dy', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            CommonElements = [i for i in self.Element if i in self._df.columns]
            self.Element = CommonElements
            self.xticks = [i for i in range(1,len(CommonElements)+2)]
            self.xticklabels = CommonElements

            self.setWindowTitle('Trace Standardlized Pattern Diagram Rb-Lu '+ str(len(CommonElements)+1) +' Elements')


        self.axes.clear()
        #self.axes.axis('off')

        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')

        self.WholeData = []

        raw = self._df

        self.FontSize = FontSize

        PointLabels = []
        k = 0
        flag = 1

        standardnamechosen = self.StandardsName[int(self.standard.value())]
        standardchosen = self.Standards[standardnamechosen]

        self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[int(self.standard.value())])

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            LinesX = []
            LinesY = []

            for j in range(len(CommonElements)):

                flag = 1

                tmp = 1

                if CommonElements[j] in raw.columns:
                    tmp = raw.at[i, CommonElements[j]] / standardchosen[CommonElements[j]]

                elif CommonElements[j] == 'K' and 'K2O' in raw.columns:
                    tmp = raw.at[i, 'K2O'] * (
                        2 * 39.0983 / 94.1956) * 10000 / standardchosen[
                        CommonElements[j]]

                elif CommonElements[j] == 'Ti' and 'TiO2' in raw.columns:
                    tmp = raw.at[i, 'TiO2'] * (
                        47.867 / 79.865) * 10000 / standardchosen[
                        CommonElements[j]]

                else:
                    flag = 0

                if flag == 1:
                    if tmp==tmp:# to delete nan
                        tmpflag = 1
                        a=0
                        try:
                            a=math.log(tmp, 10)
                        except(ValueError):
                            tmpflag=0
                            pass

                        if(tmpflag==1):

                            LinesY.append(a)
                            LinesX.append(j + 1)

                            self.WholeData.append(math.log(tmp, 10))

                            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                                TmpLabel = ''
                            else:
                                PointLabels.append(raw.at[i, 'Label'])
                                TmpLabel = raw.at[i, 'Label']

                            self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                              s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                              label=TmpLabel, edgecolors='black')
            self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                           linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)



        self.standard_label.setText('Standard: ' + self.StandardsName[int(self.standard.value())])



        self.yticks = [Location+i for i in range(count)]

        self.yticklabels = [str(np.power(10.0, (Location + i))) for i in range(count)]

        self.axes.set_yticks(self.yticks)
        self.axes.set_yticklabels(self.yticklabels)




        self.axes.set_xticks(self.xticks)
        self.axes.set_xticklabels(self.xticklabels)


        self.canvas.draw()


        self.OutPutTitle='Trace'

        self.OutPutFig=self.fig