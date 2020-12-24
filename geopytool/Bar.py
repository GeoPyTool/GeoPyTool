from ImportDependence import *
from CustomClass import *
#from TableViewer import TableViewer

class Bar(AppForm):

    xlabel = 'x'
    items = []
    description = 'Bar Chart'
    LabelSetted = True
    ValueChoosed = False
    single_LabelSetted = True
    single_ValueChoosed = False
    switched = False
    LabelList = []

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)
        self.FileName_Hint= self.title
        self.a_index= 0
        self.b_index= 0
        self.raw = df
        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')
        self.items = self._df.columns.values.tolist()
        for k in self.items:
            if "Type" in k:
                self.a_index = self.items.index(k)
        self.create_main_frame()
        self.create_status_bar()


    def create_main_frame(self):

        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((10, 8.0), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.33, bottom=0.2, right=0.7, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.save_plot_button = QPushButton('&Save IMG')
        self.save_plot_button .clicked.connect(self.saveImgFile)

        self.switch_button = QPushButton('&Switch to 2D')
        self.switch_button.clicked.connect(self.switch)

        self.color_cb = QCheckBox('&Color')
        self.color_cb.setChecked(False)
        self.color_cb.stateChanged.connect(self.Magic)  # int

        self.style_cb = QCheckBox('&Direction')
        self.style_cb.setChecked(False)
        self.style_cb.stateChanged.connect(self.Magic)  # int

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int



        self.LabelList=[]
        for i in range(len(self.raw)):
            Label = self.raw.at[i,'Label']
            if Label not in self.LabelList:
                self.LabelList.append(Label)

        self.hbox = QHBoxLayout()

        for w in [self.switch_button, self.save_plot_button,self.color_cb,self.style_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        if ( self.switched== False):

            self.selecter = QLineEdit(self)
            self.selecter.textChanged[str].connect(self.LabelSeter)

            self.element = QSlider(Qt.Horizontal)
            self.element.setRange(0, len(self.items) - 1)
            self.element.setValue(self.a_index)
            self.element.setTracking(True)
            self.element.setTickPosition(QSlider.TicksBothSides)
            self.element.valueChanged.connect(self.ValueChooser)  # int

            self.switch_button.setText('&Switch to Single Group')
            self.hbox0 = QHBoxLayout()
            for w in [self.selecter, self.element]:
                self.hbox0.addWidget(w)
                self.hbox0.setAlignment(w, Qt.AlignVCenter)
        else:
            self.single_selecter = QLineEdit(self)
            self.single_selecter.textChanged[str].connect(self.single_LabelSeter)

            self.single_element = QSlider(Qt.Horizontal)
            self.single_element.setRange(0, len(self.LabelList) - 1)
            self.single_element.setValue(self.b_index)
            self.single_element.setTracking(True)
            self.single_element.setTickPosition(QSlider.TicksBothSides)
            self.single_element.valueChanged.connect(self.single_ValueChooser)  # int
            self.switch_button.setText('&Switch to All Groups')
            self.hbox0 = QHBoxLayout()
            for w in [self.single_selecter, self.single_element]:
                self.hbox0.addWidget(w)
                self.hbox0.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox0)
        self.textbox = GrowingTextEdit(self)
        self.vbox.addWidget(self.textbox)
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def switch(self):
        self.switched = not(self.switched)
        self.create_main_frame()
        self.Magic()

    def LabelSeter(self):
        self.LabelSetted = True
        self.ValueChoosed = False
        self.Magic()

    def ValueChooser(self):
        self.LabelSetted = False
        self.ValueChoosed = True
        self.Magic()

    def single_LabelSeter(self):
        self.single_LabelSetted = True
        self.single_ValueChoosed = False
        self.Magic()

    def single_ValueChooser(self):
        self.single_LabelSetted = False
        self.single_ValueChoosed = True
        self.Magic()

    def Magic(self):
        self.WholeData = []

        # print(self.x_scale,' and ',self.x_scale)
        raw = self._df
        dataframe = self._df

        ItemsAvalibale = self._df.columns.values.tolist()

        if (self.switched == False):
            a = int(self.element.value())
        else:
            b = int(self.single_element.value())

        self.axes.clear()
        #self.axes.set_xlabel(ItemsAvalibale[a])

        if (self.switched == False):
            self.axes.clear()
            if self.LabelSetted == True:
                if(self.selecter.text()!=''):
                    try:
                        a = int(self.selecter.text())
                    except(ValueError):
                        atmp=self.selecter.text()
                        try:
                            if atmp in ItemsAvalibale:
                                a= ItemsAvalibale.index(atmp)
                                #print(a)

                        except Exception as e:
                            self.ErrorEvent(text=repr(e))
                            pass
                        pass

                    self.element.setValue(a)
                else:
                    a = int(self.element.value())

                if a> len(ItemsAvalibale)-1:
                    a = int(self.element.value())

            if self.ValueChoosed == True:
                a = int(self.element.value())

                self.selecter.setText(ItemsAvalibale[a])

            AllTypes=[]
            AllCounters=[]

            for i in range(len(self.raw)):

                x= self.raw.at[i, self.items[a]]

                if x not in AllTypes:
                    AllTypes.append(x)
                else:
                    pass

            for j in AllTypes:
                tmpCounter = 0
                for i in range(len(self.raw)):
                    x = self.raw.at[i, self.items[a]]
                    if x != j:
                        pass
                    else:
                        tmpCounter = tmpCounter + 1
                AllCounters.append(tmpCounter)


            print(AllTypes,'\n',AllCounters)

            if (self.color_cb.isChecked()):
                if(self.style_cb.isChecked()):
                    self.axes.bar(AllTypes,AllCounters)
                else:
                    self.axes.barh(AllTypes,AllCounters)
            else:

                if(self.style_cb.isChecked()):
                    self.axes.bar(AllTypes, AllCounters, color='gray')
                else:
                    self.axes.barh(AllTypes, AllCounters, color='gray')

            self.title='Bar Chart'


            # autopct='%1.1f%%'显示比列，格式化显示一位小数，固定写法
        else:
            self.axes.clear()
            single_TypeList=[]
            single_Counters=[]


            if self.single_LabelSetted == True:
                if(self.single_selecter.text()!=''):
                    try:
                        b = int(self.single_selecter.text())
                    except(ValueError):
                        btmp=self.single_selecter.text()
                        try:
                            if btmp in self.LabelList:
                                b= self.LabelList.index(btmp)
                                #print(a)

                        except Exception as e:
                            self.ErrorEvent(text=repr(e))
                            pass

                    self.single_element.setValue(b)
                else:
                    b = int(self.single_element.value())

                if b> len(self.LabelList)-1:
                    b = int(self.single_element.value())

            if self.single_ValueChoosed == True:
                b = int(self.single_element.value())

                self.single_selecter.setText(self.LabelList[b])

            for i in range(len(raw)):
                if self.raw.at[i, 'Type'] not in single_TypeList and self.raw.at[i, 'Label'] == self.LabelList[b]:
                    single_TypeList.append(self.raw.at[i, 'Type'])
                else:
                    pass

            print(len(self.LabelList),len(single_TypeList))

            for j in single_TypeList:
                tmpCounter = 0
                for i in range(len(self.raw)):
                    x = self.raw.at[i, 'Type']
                    if x != j:
                        pass
                    else:
                        tmpCounter = tmpCounter + 1
                single_Counters.append(tmpCounter)

            #print(len(single_TypeList),len(single_Counters))

            self.title='Bar Chart of '+ self.LabelList[b]
            if (self.color_cb.isChecked()):

                if(self.style_cb.isChecked()):
                    self.axes.bar(single_TypeList, single_Counters, )
                else:
                    self.axes.barh(single_TypeList,single_Counters, )
            else:
                if (self.style_cb.isChecked()):
                    self.axes.bar(single_TypeList, single_Counters, color='gray')
                else:
                    self.axes.barh(single_TypeList, single_Counters, color='gray')


            # autopct='%1.1f%%'显示比列，格式化显示一位小数，固定写法
        '''
        except Exception as e:
        self.ErrorEvent(text=repr(e))
        if (self.legend_cb.isChecked()):
        #self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)
        self.axes.legend(bbox_to_anchor=(1.3, 1),loc='upper left', borderaxespad=1, prop=fontprop)
        '''
        # pass



        self.setWindowTitle(self.title)
        self.FileName_Hint= self.title
        self.canvas.draw()

