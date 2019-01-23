from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer



class IsoTope(AppForm):


    reference = 'Ludwig, K. R. (2003). "Isoplot, rev. 3.75. A geochronological toolkit for microsoft excel."  5: 1-75.'
    sentence = ''

    Lines = []
    Tags = []

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


    description = 'Rb-Sr IsoTope diagram'
    xname='87Rb/86Sr'
    yname='87Sr/86Sr'
    lambdaItem = 1.42e-11
    xlabel = r'$^{87}Rb/^{86}Sr$'
    ylabel = r'$^{87}Sr/^{86}Sr$'


    def __init__(self, parent=None, df=pd.DataFrame(), description='Rb-Sr IsoTope diagram', xname='87Rb/86Sr',
                 yname='87Sr/86Sr', lambdaItem=1.42e-11, xlabel=r'$^{87}Rb/^{86}Sr$', ylabel=r'$^{87}Sr/^{86}Sr$'):

        QMainWindow.__init__(self, parent)

        self.items = []

        self.description = description
        self.xname = xname
        self.yname = yname
        self.lambdaItem = lambdaItem
        self.xlabel = xlabel
        self.ylabel = ylabel

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Magic')

        self.setWindowTitle(self.description)
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

            x, y = raw.at[i, self.xname], raw.at[i, self.yname]



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

        opt, cov = np.polyfit(XtoFit, YtoFit, self.FitLevel, cov=True)
        p = np.poly1d(opt)


        Yline = p(Xline)


        sigma = np.sqrt(np.diag(cov))
        a, aerr, b, berr = opt[0], sigma[0], opt[1], sigma[1]

        lambdaItem = self.lambdaItem

        t = np.log(a + 1) / lambdaItem

        tma=t/np.power(10,6)
        terr=1/(a+1)*aerr/ lambdaItem/ np.power(10, 6)

        N=len(XtoFit)
        F=N-2
        MSWD=1+2*np.sqrt(2/F)
        MSWDerr=np.sqrt(2/F)


        self.textbox.setText('Age(±2σ) = '+ str(tma)+' Ma ±'+str(2*terr)+'\n Initial '+ self.yname +' (±2σ)= '+ str(b)+'±'+str(2*berr) +'\n MSWD(±2σ)= '+ str(MSWD)+'±'+str(2*MSWDerr)+'\n\n'+ self.sentence)

        self.axes.plot(Xline, Yline, color='grey', linestyle='-', alpha=0.5)


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        self.canvas.draw()



        return(dict)

