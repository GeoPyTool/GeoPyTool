from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer

class Pie(AppForm):

    xlabel = 'x'
    items = []

    description = 'Pie Chart'
    LabelSetted = True
    ValueChoosed = False

    def __init__(self, parent=None, df=pd.DataFrame(),Standard={}):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.description)
        self.FileName_Hint='Pie'
        self.a_index= 0
        self.raw = df
        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')
        dataframe = self._df

        self.items = self._df.columns.values.tolist()


        for k in self.items:
            if "Type" in k:
                self.a_index = self.items.index(k)
        self.create_main_frame()
        self.create_status_bar()
        self.axes.set_xlabel(self.items[self.a_index])

    def create_main_frame(self):

        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((10, 8.0), dpi=self.dpi)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.13, bottom=0.2, right=0.7, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.save_plot_button = QPushButton('&Save IMG')
        self.save_plot_button .clicked.connect(self.saveImgFile)

        self.color_cb = QCheckBox('&Color')
        self.color_cb.setChecked(False)
        self.color_cb.stateChanged.connect(self.Magic)  # int

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Magic)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(self.a_index)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.ValueChooser)  # int

        self.x_seter = QLineEdit(self)
        self.x_seter.textChanged[str].connect(self.LabelSeter)

        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()

        w=self.width()
        h=self.height()

        self.x_seter.setFixedWidth(w/10)

        for w in [self.save_plot_button,self.legend_cb,self.color_cb,]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        for w in [self.x_seter, self.x_element]:
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

        w=self.width()
        h=self.height()

        self.x_seter.setFixedWidth(w/10)

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

        # print(self.x_scale,' and ',self.x_scale)
        raw = self._df
        dataframe = self._df

        ItemsAvalibale = self._df.columns.values.tolist()


        a = int(self.x_element.value())

        self.axes.clear()
        self.axes.set_xlabel(ItemsAvalibale[a])


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



            if a> len(ItemsAvalibale)-1:
                a = int(self.x_element.value())


        if self.ValueChoosed == True:
            a = int(self.x_element.value())

            self.x_seter.setText(ItemsAvalibale[a])


        AllTypes=[]
        AllCounters=[]

        for i in range(len(self.raw)):

            x= self.raw.at[i, self.items[a]]

            try:
                if x not in AllTypes:
                    AllTypes.append(x)
                else:
                    pass

                self.xlabel = self.items[a]
                self.axes.set_xlabel(self.xlabel)
            except Exception as e:
                self.ErrorEvent(text=repr(e))
                #pass

        for j in AllTypes:
            tmpCounter = 0
            for i in range(len(self.raw)):
                x = self.raw.at[i, self.items[a]]
                if x != j:
                    tmpCounter = 1
                else:
                    tmpCounter = tmpCounter + 1
            AllCounters.append(tmpCounter)
        #print(len(AllTypes),len(AllCounters))


        if (self.color_cb.isChecked()):
            self.axes.pie(AllCounters, labels=AllTypes, autopct='%1.1f%%')
        else:
            _, _, autotexts =self.axes.pie(AllCounters, labels=AllTypes, autopct='%1.1f%%', colors = ['%f' % (i/float(len(AllTypes))) for i in range(len(AllTypes))])
            for autotext in autotexts:
                autotext.set_color('white')

        # autopct='%1.1f%%'显示比列，格式化显示一位小数，固定写法

        if (self.legend_cb.isChecked()):
            #self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)
            self.axes.legend(bbox_to_anchor=(1.3, 1),loc='upper left', borderaxespad=1, prop=fontprop)

        self.canvas.draw()

