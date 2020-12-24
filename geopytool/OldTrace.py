from ImportDependence import *
from CustomClass import *

class OldTrace(AppForm):
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

    StandardsName = ['PM','OIB', 'EMORB', 'C1',  'NMORB','UCC_Rudnick & Gao2003']
    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, UCC_Rudnick & Gao2003'
    NameChosen = 'PM'
    Standards = {
        'PM': {'Cs': 0.032, 'Tl': 0.005, 'Rb': 0.635, 'Ba': 6.989, 'W': 0.02, 'Th': 0.085, 'U': 0.021, 'Nb': 0.713,
               'Ta': 0.041, 'K': 250, 'La': 0.687, 'Ce': 1.775, 'Pb': 0.185, 'Pr': 0.276, 'Mo': 0.063, 'Sr': 21.1,
               'P': 95, 'Nd': 1.354, 'F': 26, 'Sm': 0.444, 'Zr': 11.2, 'Hf': 0.309, 'Eu': 0.168, 'Sn': 0.17,
               'Sb': 0.005, 'Ti': 1300, 'Gd': 0.596, 'Tb': 0.108, 'Dy': 0.736, 'Li': 1.6, 'Y': 4.55, 'Ho': 0.164,
               'Er': 0.48, 'Tm': 0.074, 'Yb': 0.493, 'Lu': 0.074},
        'OIB': {'Cs': 0.387, 'Tl': 0.077, 'Rb': 31, 'Ba': 350, 'W': 0.56, 'Th': 4, 'U': 1.02, 'Nb': 48, 'Ta': 2.7,
                'K': 12000, 'La': 36, 'Ce': 80, 'Pb': 3.2, 'Pr': 9.7, 'Mo': 2.4, 'Sr': 660, 'P': 2700, 'Nd': 38.5,
                'F': 1150, 'Sm': 10, 'Zr': 280, 'Hf': 7.8, 'Eu': 3, 'Sn': 2.7, 'Sb': 0.03, 'Ti': 17200, 'Gd': 7.62,
                'Tb': 1.05, 'Dy': 5.6, 'Li': 5.6, 'Y': 29, 'Ho': 1.06, 'Er': 2.62, 'Tm': 0.35, 'Yb': 2.16, 'Lu': 0.3},
        'EMORB': {'Cs': 0.063, 'Tl': 0.013, 'Rb': 5.04, 'Ba': 57, 'W': 0.092, 'Th': 0.6, 'U': 0.18, 'Nb': 8.3,
                  'Ta': 0.47, 'K': 2100, 'La': 6.3, 'Ce': 15, 'Pb': 0.6, 'Pr': 2.05, 'Mo': 0.47, 'Sr': 155, 'P': 620,
                  'Nd': 9, 'F': 250, 'Sm': 2.6, 'Zr': 73, 'Hf': 2.03, 'Eu': 0.91, 'Sn': 0.8, 'Sb': 0.01, 'Ti': 6000,
                  'Gd': 2.97, 'Tb': 0.53, 'Dy': 3.55, 'Li': 3.5, 'Y': 22, 'Ho': 0.79, 'Er': 2.31, 'Tm': 0.356,
                  'Yb': 2.36, 'Lu': 0.354},
        'C1': {'Cs': 0.188, 'Tl': 0.14, 'Rb': 2.32, 'Ba': 2.41, 'W': 0.095, 'Th': 0.029, 'U': 0.008, 'Nb': 0.246,
               'Ta': 0.014, 'K': 545, 'La': 0.236, 'Ce': 0.612, 'Pb': 2.47, 'Pr': 0.095, 'Mo': 0.92, 'Sr': 7.26,
               'P': 1220, 'Nd': 0.467, 'F': 60.7, 'Sm': 0.153, 'Zr': 3.87, 'Hf': 0.1066, 'Eu': 0.058, 'Sn': 1.72,
               'Sb': 0.16, 'Ti': 445, 'Gd': 0.2055, 'Tb': 0.0364, 'Dy': 0.254, 'Li': 1.57, 'Y': 1.57, 'Ho': 0.0566,
               'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'NMORB': {'Cs': 0.007, 'Tl': 0.0014, 'Rb': 0.56, 'Ba': 6.3, 'W': 0.01, 'Th': 0.12, 'U': 0.047, 'Nb': 2.33,
                  'Ta': 0.132, 'K': 600, 'La': 2.5, 'Ce': 7.5, 'Pb': 0.3, 'Pr': 1.32, 'Mo': 0.31, 'Sr': 90, 'P': 510,
                  'Nd': 7.3, 'F': 210, 'Sm': 2.63, 'Zr': 74, 'Hf': 2.05, 'Eu': 1.02, 'Sn': 1.1, 'Sb': 0.01, 'Ti': 7600,
                  'Gd': 3.68, 'Tb': 0.67, 'Dy': 4.55, 'Li': 4.3, 'Y': 28, 'Ho': 1.01, 'Er': 2.97, 'Tm': 0.456,
                  'Yb': 3.05, 'Lu': 0.455},
        'UCC_Rudnick & Gao2003':{'K':23244.13676,'Ti':3835.794545,'P':654.6310022,'Li':24,'Be':2.1,'B':17,'N':83,'F':557,'S':62,'Cl':360,'Sc':14,'V':97,'Cr':92,
                                 'Co':17.3,'Ni':47,'Cu':28,'Zn':67,'Ga':17.5,'Ge':1.4,'As':4.8,'Se':0.09,
                                 'Br':1.6,'Rb':84,'Sr':320,'Y':21,'Zr':193,'Nb':12,'Mo':1.1,'Ru':0.34,
                                 'Pd':0.52,'Ag':53,'Cd':0.09,'In':0.056,'Sn':2.1,'Sb':0.4,'I':1.4,'Cs':4.9,
                                 'Ba':628,'La':31,'Ce':63,'Pr':7.1,'Nd':27,'Sm':4.7,'Eu':1,'Gd':4,'Tb':0.7,
                                 'Dy':3.9,'Ho':0.83,'Er':2.3,'Tm':0.3,'Yb':1.96,'Lu':0.31,'Hf':5.3,'Ta':0.9,
                                 'W':1.9,'Re':0.198,'Os':0.031,'Ir':0.022,'Pt':0.5,'Au':1.5,'Hg':0.05,'Tl':0.9,
                                 'Pb':17,'Bi':0.16,'Th':10.5,'U':2.7}}

    AllLabel = []

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Trace Standardlized Pattern Diagram')


        self.FileName_Hint='Trace'
        #self._df = df
        self._df_back =df

        self.data_to_norm = self.CleanDataFile(df)
        self._df = self.CleanDataFile(df)


        self._given_Standard = self.Standard

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Trace')

        self.AllLabel=[]

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb', u'Pr',
                        u'Mo',
                        u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb', u'Dy',
                        u'Li',
                        u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

        self.WholeData = []
        self.X0 = 1
        self.X1 = 36
        self.X_Gap = 36

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
        self.save_img_button = QPushButton('&Save Img')
        self.save_img_button.clicked.connect(self.saveImgFile)

        self.explain_button = QPushButton('&Norm Result')
        self.explain_button.clicked.connect(self.Explain)

        self.Type_cb = QCheckBox('&Cs-Lu (36 Elements)')
        self.Type_cb.setChecked(True)
        self.Type_cb.stateChanged.connect(self.Trace)  # int


        self.type_slider_left_label = QLabel('Cs-Lu (36 Elements)')
        self.type_slider_right_label= QLabel('Rb-Lu (26 Elements)')


        self.type_slider = QSlider(Qt.Horizontal)
        self.type_slider.setRange(0, 1)
        self.type_slider.setValue(0)
        self.type_slider.setTracking(True)
        self.type_slider.setTickPosition(QSlider.TicksBothSides)
        self.type_slider.valueChanged.connect(self.Trace)  # int


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Trace)  # int



        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Trace)  # int


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
        self.standard_slider.valueChanged.connect(self.Trace)  # int
        self.left_label= QLabel('Standard' )



        self.item_left_label= QLabel('Show All' )
        self.item_slider = QSlider(Qt.Horizontal)
        self.item_slider.setRange(0, len(self.AllLabel))
        self.item_slider.setTracking(True)
        self.item_slider.setTickPosition(QSlider.TicksBothSides)
        self.item_slider.valueChanged.connect(self.Trace) # int

        # Layout with box sizers
        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        for w in [self.save_img_button,self.explain_button,self.legend_cb,self.show_data_index_cb,
                  self.type_slider_left_label, self.type_slider,self.type_slider_right_label,
                  self.left_label, self.standard_slider,self.right_label]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.item_left_label,self.item_slider]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.textbox = GrowingTextEdit(self)
        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



        w=self.width()
        h=self.height()

        #setFixedWidth(w/10)

        self.type_slider.setFixedWidth(w/10)
        self.standard_slider.setMinimumWidth(w/4)
        self.right_label.setMinimumWidth(w/10)
        self.item_left_label.setFixedWidth(w/10)




    def Trace(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
              Top=6, Y0=-1,
              Y1=3, Y_Gap=5, FontSize=6,
              xLabel=r'$Trace-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):



        if (int(self.type_slider.value()) == 0):
            self.Element = [u'Cs', u'Tl', u'Rb', u'Ba', u'W', u'Th', u'U', u'Nb', u'Ta', u'K', u'La', u'Ce', u'Pb',
                            u'Pr', u'Mo',
                            u'Sr', u'P', u'Nd', u'F', u'Sm', u'Zr', u'Hf', u'Eu', u'Sn', u'Sb', u'Ti', u'Gd', u'Tb',
                            u'Dy', u'Li', u'Y', u'Ho', u'Er', u'Tm', u'Yb', u'Lu']

            CommonElements = [i for i in self.Element if i in self._df.columns]
            self.Element = CommonElements
            self.xticks = [i for i in range(1,len(CommonElements)+2)]
            self.xticklabels = CommonElements

            self.setWindowTitle('Trace Standardlized Pattern Diagram Cs-Lu '+ str(len(CommonElements)+1) +' Elements')



        else:
            self.Type_cb.setText('&Rb-Lu (26 Elements)')
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



        #raw = self.CleanDataFile(self._df)


        self.FontSize = FontSize

        PointLabels = []
        k = 0
        flag = 1


        slider_value=int(self.standard_slider.value())


        item_value=int(self.item_slider.value())

        if slider_value < len(self.StandardsName):
            standardnamechosen = self.StandardsName[slider_value]
            standardchosen = self.Standards[standardnamechosen]
            self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[slider_value])

            right_label_text=self.StandardsName[slider_value]

        elif len(self._given_Standard)<=0:
            standardnamechosen = self.StandardsName[slider_value-1]
            standardchosen = self.Standards[standardnamechosen]
            self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[slider_value-1])

            right_label_text = self.StandardsName[slider_value-1]

        else:
            standardchosen = self._given_Standard
            self.textbox.setText(self.reference + "\n You are using Self Defined Standard")
            right_label_text = "Self Defined Standard"

        self.right_label.setText(right_label_text)

        Y_bottom = 0
        Y_top = 0

        for i in range(len(raw)):
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
                    if tmp == tmp:  # to delete nan

                        self.data_to_norm.at[i, self.Element[j]] = tmp

                        tmpflag = 1
                        a = 0
                        try:
                            a = math.log(tmp, 10)
                        except(ValueError):
                            tmpflag = 0
                            pass

                        if (tmpflag == 1):
                            if Y_bottom > a: Y_bottom = a
                            if Y_top < a: Y_top = a

        self.axes.set_ylim(Y_bottom, Y_top)

        if item_value == 0:
            self.item_left_label.setText('Show All')

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

                            self.data_to_norm.at[i, self.Element[j]] = tmp

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
                                                  label=TmpLabel)
                self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                               linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

                if (self.show_data_index_cb.isChecked()):

                    if 'Index' in self._df_back.columns.values:
                        self.axes.annotate(self._df_back.at[i, 'Index'],
                                       xy=(LinesX[-1],
                                           LinesY[-1]),
                                       color=self._df.at[i, 'Color'],
                                       alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes.annotate('No' + str(i + 1),
                                           xy=(LinesX[-1],
                                               LinesY[-1]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])



        else:

            self.item_left_label.setText(self.AllLabel[item_value-1])

            for i in range(len(raw)):
                # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

                TmpLabel = ''

                LinesX = []
                LinesY = []

                if raw.at[i, 'Label'] == self.AllLabel[item_value - 1]:
                    alpha = raw.at[i, 'Alpha']
                    linewidth = raw.at[i, 'Width']
                    pointsize = raw.at[i, 'Size']
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

                                self.data_to_norm.at[i, self.Element[j]] = tmp

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
                                                      label=TmpLabel)
                    self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                                   linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

                    if (self.show_data_index_cb.isChecked()):

                        if 'Index' in self._df_back.columns.values:
                            self.axes.annotate(self._df_back.at[i, 'Index'],
                                           xy=(LinesX[-1],
                                               LinesY[-1]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
                        else:
                            self.axes.annotate('No' + str(i + 1),
                                               xy=(LinesX[-1],
                                                   LinesY[-1]),
                                               color=self._df.at[i, 'Color'],
                                               alpha=self._df.at[i, 'Alpha'])



        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)+0.5

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7) + 1

        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        self.yticks = [Location+i for i in range(count)]

        self.yticklabels = [str(np.power(10.0, (Location + i))) for i in range(count)]

        self.axes.set_yticks(self.yticks)
        self.axes.set_yticklabels(self.yticklabels, fontsize=6)




        self.axes.set_xticks(self.xticks)
        self.axes.set_xticklabels(self.xticklabels, rotation=-45, fontsize=6)



        self.canvas.draw()


        self.OutPutTitle='Trace'

        self.OutPutFig=self.fig



    def Explain(self):

        self.data_to_norm


        for i in self.data_to_norm.columns.values.tolist():
            if i in self.Element:
                self.data_to_norm = self.data_to_norm.rename(columns={i: i + '_N'})
            elif i in ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']:
                pass
            else:
                self.data_to_norm = self.data_to_norm.drop(i, 1)

        self.OutPutData = self.data_to_norm.set_index('Label')
        self.tablepop = TableViewer(df=self.OutPutData,title='Trace Element Norm Result')
        self.tablepop.show()
