from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class REE(AppForm):

    reference = 'Reference: Sun, S. S., and Mcdonough, W. F., 1989, UCC_Rudnick & Gao2003'
    xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    xticklabels = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    itemstocheck = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']



    LREE = ['La', 'Ce', 'Pr', 'Nd']
    MREE = ['Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho']
    HREE = [ 'Er', 'Tm', 'Yb', 'Lu']

    BinLREE=['La', 'Ce', 'Pr', 'Nd','Sm', 'Eu']
    BinHREE=['Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']

    StandardsName = ['C1 Chondrite Sun and McDonough,1989', 'Chondrite Taylor and McLennan,1985',
                     'Chondrite Haskin et al.,1966', 'Chondrite Nakamura,1977', 'MORB Sun and McDonough,1989','UCC_Rudnick & Gao2003']

    # RefName=['Sun, S. S., and Mcdonough, W. F., 1989, Chemical and isotopic systematics of oceanic basalts: implications for mantle composition and processes: Geological Society London Special Publications, v. 42, no. 1, p. 313-345.',]

    NameChosen = 'C1 Chondrite Sun and McDonough,1989'
    Standards = {
        'C1 Chondrite Sun and McDonough,1989': {'La': 0.237, 'Ce': 0.612, 'Pr': 0.095, 'Nd': 0.467, 'Sm': 0.153,
                                                'Eu': 0.058, 'Gd': 0.2055, 'Tb': 0.0374, 'Dy': 0.254, 'Ho': 0.0566,
                                                'Er': 0.1655, 'Tm': 0.0255, 'Yb': 0.17, 'Lu': 0.0254},
        'Chondrite Taylor and McLennan,1985': {'La': 0.367, 'Ce': 0.957, 'Pr': 0.137, 'Nd': 0.711, 'Sm': 0.231,
                                               'Eu': 0.087, 'Gd': 0.306, 'Tb': 0.058, 'Dy': 0.381, 'Ho': 0.0851,
                                               'Er': 0.249, 'Tm': 0.0356, 'Yb': 0.248, 'Lu': 0.0381},
        'Chondrite Haskin et al.,1966': {'La': 0.32, 'Ce': 0.787, 'Pr': 0.112, 'Nd': 0.58, 'Sm': 0.185, 'Eu': 0.071,
                                         'Gd': 0.256, 'Tb': 0.05, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                         'Yb': 0.186, 'Lu': 0.034},
        'Chondrite Nakamura,1977': {'La': 0.33, 'Ce': 0.865, 'Pr': 0.112, 'Nd': 0.63, 'Sm': 0.203, 'Eu': 0.077,
                                    'Gd': 0.276, 'Tb': 0.047, 'Dy': 0.343, 'Ho': 0.07, 'Er': 0.225, 'Tm': 0.03,
                                    'Yb': 0.22,
                                    'Lu': 0.034},
        'MORB Sun and McDonough,1989': {'La': 2.5, 'Ce': 7.5, 'Pr': 1.32, 'Nd': 7.3, 'Sm': 2.63, 'Eu': 1.02, 'Gd': 3.68,
                                        'Tb': 0.67, 'Dy': 4.55, 'Ho': 1.052, 'Er': 2.97, 'Tm': 0.46, 'Yb': 3.05,
                                        'Lu': 0.46},
        'UCC_Rudnick & Gao2003':{'Li':24,'Be':2.1,'B':17,'N':83,'F':557,'S':62,'Cl':370,'Sc':14,'V':97,'Cr':92,
                                 'Co':17.3,'Ni':47,'Cu':28,'Zn':67,'Ga':17.5,'Ge':1.4,'As':4.8,'Se':0.09,
                                 'Br':1.6,'Rb':84,'Sr':320,'Y':21,'Zr':193,'Nb':12,'Mo':1.1,'Ru':0.34,
                                 'Pd':0.52,'Ag':53,'Cd':0.09,'In':0.056,'Sn':2.1,'Sb':0.4,'I':1.4,'Cs':4.9,
                                 'Ba':628,'La':31,'Ce':63,'Pr':7.1,'Nd':27,'Sm':4.7,'Eu':1,'Gd':4,'Tb':0.7,
                                 'Dy':3.9,'Ho':0.83,'Er':2.3,'Tm':0.3,'Yb':1.96,'Lu':0.31,'Hf':5.3,'Ta':0.9,
                                 'W':1.9,'Re':0.198,'Os':0.031,'Ir':0.022,'Pt':0.5,'Au':1.5,'Hg':0.05,'Tl':0.9,
                                 'Pb':17,'Bi':0.16,'Th':10.5,'U':2.7}}

    LabelList=[]
    algebraDeltaEuList = []
    geometricDeltaEuList = []



    LaPrDeltaCeList = []
    LaNdDeltaCeList = []

    LaYbList=[]
    LaSmList=[]
    GdYbList=[]

    LREEList=[]
    MREEList=[]
    HREEList=[]

    BinLREEList = []
    BinHREEList = []
    L_HREEList=[]

    ALLREEList=[]
    AllAlpha = []
    AllWidth = []
    AllSize = []

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('REE Standardlized Pattern Diagram')

        #self._df = df



        self._df_back= df


        self.FileName_Hint='REE'

        self.OutPutData = pd.DataFrame()
        self.LabelList=[]
        self.algebraDeltaEuList=[]
        self.geometricDeltaEuList=[]
        self.LaPrDeltaCeList=[]
        self.LaNdDeltaCeList=[]
        self.LaSmList=[]
        self.LaYbList=[]
        self.GdYbList=[]
        self.LREEList=[]
        self.MREEList=[]
        self.HREEList=[]
        self.ALLREEList=[]
        self.BinHREEList=[]
        self.BinLREEList=[]
        self.L_HREEList=[]

        self.data_to_norm = self.CleanDataFile(df)


        self._df = self.CleanDataFile(df)


        self.AllLabel=[]

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        #self._given_Standard = Standard

        self._given_Standard = self.Standard

        if (len(df) > 0):
            self._changed = True
            # #print('DataFrame recieved to REE')

        self.Element = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
        self.WholeData = []
        self.X0 = 1
        self.X1 = 15
        self.X_Gap = 15

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
        self.resize(800, 600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
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

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.REE)  # int



        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.REE)  # int


        self.standard_slider = QSlider(Qt.Horizontal)
        self.standard_slider.setRange(0, len(self.StandardsName))

        if len(self._given_Standard) > 0:
            self.standard_slider.setValue(len(self.StandardsName))
            self.standard_right_label = QLabel("Self Defined Standard")

        else:

            self.standard_slider.setValue(0)
            self.standard_right_label = QLabel(self.StandardsName[int(self.standard_slider.value())])


        self.standard_slider.setTracking(True)
        self.standard_slider.setTickPosition(QSlider.TicksBothSides)
        self.standard_slider.valueChanged.connect(self.REE)  # int
        self.standard_left_label= QLabel('Standard')


        self.item_left_label= QLabel('Show All' )
        self.item_slider = QSlider(Qt.Horizontal)
        self.item_slider.setRange(0, len(self.AllLabel))
        self.item_slider.setTracking(True)
        self.item_slider.setTickPosition(QSlider.TicksBothSides)
        self.item_slider.valueChanged.connect(self.REE)  # int



        #
        # Layout with box sizers
        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        for w in [self.save_img_button, self.explain_button, self.legend_cb,self.show_data_index_cb,self.standard_left_label, self.standard_slider, self.standard_right_label]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [ self.item_left_label,self.item_slider]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.textbox = GrowingTextEdit(self)
        #self.textbox.setText(self.reference+"\nStandard Chosen: "+self.StandardsName[int(self.standard_slider.value())])
        self.vbox.addWidget(self.textbox)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


        w=self.width()
        h=self.height()

        #setFixedWidth(w/10)

        self.standard_slider.setMinimumWidth(w/4)
        self.standard_right_label.setFixedWidth(w/2)
        self.item_left_label.setMinimumWidth(w/4)
        #self.item_left_label.setMinimumWidth(w/5)

        self.item_left_label.setFixedWidth(w/10)

    def REE(self, Left=0, Right=16, X0=1, X1=15, X_Gap=15, Base=-1,
            Top=6, Y0=-1,
            Y1=3, Y_Gap=5, FontSize=12,
            xLabel=r'$REE-Standardlized-Pattern$', yLabel='', width=12, height=12, dpi=300):

        self.axes.clear()
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        self.WholeData = []
        self.OutPutData = pd.DataFrame()
        self.LabelList=[]
        self.algebraDeltaEuList=[]
        self.geometricDeltaEuList=[]
        self.LaPrDeltaCeList=[]
        self.LaNdDeltaCeList=[]
        self.LaSmList=[]
        self.LaYbList=[]
        self.GdYbList=[]
        self.LREEList=[]
        self.MREEList=[]
        self.HREEList=[]
        self.ALLREEList=[]
        self.BinHREEList=[]
        self.BinLREEList=[]
        self.L_HREEList=[]

        self.AllAlpha=[]
        self.AllWidth = []
        self.AllSize = []

        #raw = self._df


        raw = self.CleanDataFile(self._df)

        self.FontSize = FontSize

        PointLabels = []
        k = 0


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

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''
            LinesX = []
            LinesY = []
            TmpEu = raw.at[i, 'Eu'] / standardchosen['Eu']
            TmpSm = raw.at[i, 'Sm'] / standardchosen['Sm']
            TmpGd = raw.at[i, 'Gd'] / standardchosen['Gd']
            TmpCe = raw.at[i, 'Ce'] / standardchosen['Ce']
            TmpLa = raw.at[i, 'La'] / standardchosen['La']
            TmpPr = raw.at[i, 'Pr'] / standardchosen['Pr']
            TmpNd = raw.at[i, 'Nd'] / standardchosen['Nd']
            TmpYb = raw.at[i, 'Yb'] / standardchosen['Yb']

            algebraEu = 2*TmpEu/(TmpSm+TmpGd)
            geometricEu = TmpEu/np.power((TmpSm*TmpGd),0.5)

            firstCe=2*TmpCe/(TmpLa+TmpPr)
            secondCe=3*TmpCe/(2*TmpLa+TmpNd)

            LaYb=TmpLa/TmpYb
            LaSm=TmpLa/TmpSm
            GdYb=TmpGd/TmpYb


            tmpLREEResult = 0
            tmpMREEResult = 0
            tmpHREEResult = 0
            tmpWholeResult = 0
            tmpBinLREE=0
            tmpBinHREE=0

            for j in self.Element:

                if j in self.LREE:
                    tmpLREEResult += raw.at[i, j]
                elif j in self.MREE:
                    tmpMREEResult += raw.at[i, j]
                elif j in self.HREE:
                    tmpHREEResult += raw.at[i, j]

                if j in self.BinLREE:
                    tmpBinLREE += raw.at[i, j]
                elif j in self.BinHREE:
                    tmpBinHREE += raw.at[i, j]

                tmpWholeResult+= raw.at[i, j]



            self.LabelList.append(raw.at[i, 'Label'])
            self.algebraDeltaEuList.append( algebraEu )
            self.geometricDeltaEuList.append( geometricEu )
            self.LaPrDeltaCeList.append(firstCe)
            self.LaNdDeltaCeList.append(secondCe)
            self.LaSmList.append(LaSm)
            self.LaYbList.append(LaYb)
            self.GdYbList.append(GdYb)
            self.LREEList.append( tmpLREEResult )
            self.MREEList.append( tmpMREEResult )
            self.HREEList.append( tmpHREEResult )
            self.ALLREEList.append( tmpWholeResult )
            self.BinHREEList.append(tmpBinHREE)
            self.BinLREEList.append(tmpBinLREE)
            self.L_HREEList.append(tmpBinLREE/tmpBinHREE)

            '''
            for i in self.data_to_norm.columns.values.tolist():
                if i not in self.Element:
                    self.data_to_norm = self.data_to_norm.drop(i, 1)            
            '''

            Y_bottom=0
            Y_top=0

            for j in range(len(self.Element)):
                tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]
                self.data_to_norm.at[i, self.Element[j]] = tmp
                tmpflag = 1
                a = 0
                try:
                    a = math.log(tmp, 10)
                except(ValueError):
                    tmpflag = 0
                    pass
                if (tmpflag == 1):
                    if Y_bottom >a:Y_bottom =a
                    if Y_top<a:Y_top=a

            self.axes.set_ylim(Y_bottom, Y_top+1)

            if item_value == 0:
                self.item_left_label.setText('Show All')
                for j in range(len(self.Element)):
                    tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]
                    self.data_to_norm.at[i, self.Element[j]] = tmp
                    tmpflag = 1
                    a = 0
                    try:
                        a = math.log(tmp, 10)
                    except(ValueError):
                        tmpflag = 0
                        pass
                    if (tmpflag == 1):
                        if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                            self.WholeData.append(math.log(tmp, 10))
                            TmpLabel = ''
                        else:
                            PointLabels.append(raw.at[i, 'Label'])
                            TmpLabel = raw.at[i, 'Label']

                        LinesY.append(a)
                        LinesX.append(j + 1)
                        self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                          s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                          label=TmpLabel)
                self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=raw.at[i, 'Width'],
                               linestyle=raw.at[i, 'Style'], alpha=raw.at[i, 'Alpha'])

                if (self.show_data_index_cb.isChecked()):

                    if 'Index' in self._df_back.columns.values:
                        self.axes.annotate(self._df_back.at[i, 'Index'],
                                           xy=(LinesX[-1], LinesY[-1]),
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

                for j in range(len(self.Element)):
                    tmp = raw.at[i, self.Element[j]] / standardchosen[self.Element[j]]
                    self.data_to_norm.at[i, self.Element[j]] = tmp
                    tmpflag = 1
                    a = 0
                    try:
                        a = math.log(tmp, 10)
                    except(ValueError):
                        tmpflag = 0
                        pass
                    if (tmpflag == 1):
                        if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                            TmpLabel = ''
                        else:
                            PointLabels.append(raw.at[i, 'Label'])
                            TmpLabel = raw.at[i, 'Label']
                        alpha= raw.at[i, 'Alpha']
                        linewidth= raw.at[i, 'Width']
                        pointsize= raw.at[i, 'Size']

                        if raw.at[i, 'Label'] == self.AllLabel[item_value - 1]:
                            LinesY.append(a)
                            LinesX.append(j + 1)
                            self.WholeData.append(math.log(tmp, 10))
                            self.axes.scatter(j + 1, math.log(tmp, 10), marker=raw.at[i, 'Marker'],
                                              s=pointsize, color=raw.at[i, 'Color'], alpha=alpha,
                                              label=TmpLabel)
                        self.axes.plot(LinesX, LinesY, color=raw.at[i, 'Color'], linewidth=linewidth,linestyle=raw.at[i, 'Style'], alpha=alpha)

                print(LinesX,LinesY)

                if (self.show_data_index_cb.isChecked()):

                    if len(LinesX) > 0 and len(LinesY) > 0:
                        if 'Index' in self._df_back.columns.values:
                            self.axes.annotate(self._df_back.at[i, 'Index'],
                                               xy=(LinesX[-1], LinesY[-1]),
                                               color=self._df.at[i, 'Color'],
                                               alpha=self._df.at[i, 'Alpha'])
                        else:
                            self.axes.annotate('No' + str(i + 1),
                                               xy=(LinesX[-1], LinesY[-1]),
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




        self.standard_right_label.setText(right_label_text)


        self.yticks = [Location+i for i in range(count)]
        self.yticklabels = [str(np.power(10.0, (Location + i))) for i in range(count)]

        self.axes.set_yticks(self.yticks)
        self.axes.set_yticklabels(self.yticklabels, fontsize=6)


        #self.axes.set_yscale('log')

        self.axes.set_xticks(self.xticks)
        self.axes.set_xticklabels(self.xticklabels, rotation=-45, fontsize=6)






        self.canvas.draw()




        self.OutPutTitle='REE'

        #print(len(self.algebraDeltaEuList))

        self.OutPutData = pd.DataFrame(
            {'Label': self.LabelList,
             'Eu/Eu*(algebra)': self.algebraDeltaEuList,
             'Eu/Eu*(square)': self.geometricDeltaEuList,

             'Ce/Ce*(LaPr)': self.LaPrDeltaCeList,
             'Ce/Ce*(LaNd)': self.LaNdDeltaCeList,

             '(La/Sm)N':self.LaSmList,
             '(La/Yb)N':self.LaYbList,
             '(Gd/Yb)N':self.GdYbList,

             'trisection LREE': self.LREEList,
             'trisection MREE': self.MREEList,
             'trisection HREE': self.HREEList,
             'bisection LREE': self.BinLREEList,
             'bisection HREE': self.BinHREEList,
             'LREE/HREE':self.L_HREEList,

             'ALLREE': self.ALLREEList
             })

        #print('middle ',len(self.OutPutData['Eu/Eu*(algebra)']))


        '''
        self.LaPrDeltaCeList.append(firstCe)
        self.LaNdDeltaCeList.append(secondCe)
        '''

        self.OutPutFig=self.fig



    def Explain(self):

        self.data_to_norm


        for i in self.data_to_norm.columns.values.tolist():
            if i in self.Element:
                self.data_to_norm = self.data_to_norm.rename(columns = {i : i+'_N'})
            #elif i in ['Label','Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha','Style', 'Width']: pass
            elif i in ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha','Style', 'Width']: pass
            else:
                self.data_to_norm = self.data_to_norm.drop(i, 1)

        #print('last',len(self.OutPutData['Eu/Eu*(algebra)']))

        df = pd.concat([self.data_to_norm,self.OutPutData], axis=1).set_index('Label')
        self.tablepop = TableViewer(df=df,title='REE Norm Result')
        self.tablepop.show()
