from geopytool.ImportDependence import *
from geopytool.CustomClass import *
from geopytool.TabelViewer import TabelViewer

class RbSrIsoTope(AppForm):


    reference = 'Ludwig, K. R. (2003). "Isoplot, rev. 3.75. A geochronological toolkit for microsoft excel."  5: 1-75.'
    sentence = ''

    Lines = []
    Tags = []

    xlabel = r'$^{87}Rb/^{86}Sr$'
    ylabel = r'$^{87}Sr/^{86}Sr$'

    description = 'Rb Sr IsoTope diagram'
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


        self.resize(800, 600)

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


        #
        self.hbox0 = QHBoxLayout()


        for w in [self.save_button,self.draw_button,
                  self.legend_cb]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox0)


        self.textbox = GrowingTextEdit(self)

        self.vbox.addWidget(self.textbox)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)




    def Reset(self):
        self.flag = 0
        self.Magic()



    def Magic(self):

        self.WholeData = []

        raw = self._df

        self.axes.clear()



        self.axes.set_xlabel(self.xlabel)

        self.axes.set_ylabel(self.ylabel)

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

            x, y = raw.at[i, '87Rb/86Sr'], raw.at[i, '87Sr/86Sr']



            try:
                xuse = x
                yuse = y

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



        Xline = np.linspace(min(XtoFit), max(XtoFit), 30)
        z = np.polyfit(XtoFit, YtoFit, self.FitLevel)
        p = np.poly1d(z)
        Yline = p(Xline)
        formular='y= f(x)'


        print(z)

        k= z[0]
        b= z[1]
        t = 0

        deltaRb = 1.42 / np.power(10, 11)
        deltaRb = 1.42e-11

        t = np.log(k + 1) / deltaRb

        tma=t/np.power(10,6)




        self.textbox.setText('Age = '+ str(tma)+'\n'+' Ma'+'Initial 87Sr/86Sr = '+ str(b) +'\n\n'+ self.sentence)


        self.axes.plot(Xline, Yline, 'b-')


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        self.canvas.draw()



        return(dict)

    def relation(self,data1=np.ndarray,data2=np.ndarray):
        data=array([data1,data2])
        dict={'cov':cov(data,bias=1),'corrcoef':corrcoef(data)}
        return(dict)
