from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyThreeD(AppForm):
    Lines = []
    Tags = []
    description = 'ThreeD'
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

    PureColors=['Reds','Greens','Blues','Greys','Oranges','Purples']
    PureColor=['red','green','blue','grey','yellow','c']

    def __init__(self, parent=None,  DataFiles =[pd.DataFrame()],DataLocation='DataLocation'):
        QMainWindow.__init__(self, parent)


        self.FileName_Hint='3D'


        self.DataFiles = DataFiles
        self.DataLocation = DataLocation
        self.Labels = self.getFileName(self.DataLocation)
        print(self.DataLocation)
        print(self.Labels)
        self.setWindowTitle('ThreeD Data Visualization')


        self.items = []
        if (len(self.DataFiles) > 0):
            self._changed = True
            # print('DataFrame recieved to ThreeD')

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('ThreeD Data Visualization')

        self.fig = plt.figure(figsize=(12, 8))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = Axes3D(self.fig, elev=-150, azim=110)
        #self.axes = self.fig.add_subplot(111)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.ThreeD)  # int

        self.log_cb = QCheckBox('&Log')
        self.log_cb.setChecked(True)
        self.log_cb.stateChanged.connect(self.ThreeD)  # int


        self.cb_list=[]

        self.setter_list=[]


        for i in range(min(len(self.PureColors),len(self.Labels))):

            tmp_cb = QCheckBox(self.Labels[i])
            tmp_cb.setChecked(True)
            self.cb_list.append(tmp_cb)

            tmp_setter = QLineEdit(self)
            tmp_setter.setText('Alpha 0-1')
            self.setter_list.append(tmp_setter)


        w = self.width()
        for i in self.cb_list:
            i.setFixedWidth(w / 8)
            i.stateChanged.connect(self.ThreeD)  # int

        for i in self.setter_list:
            i.setFixedWidth(w / 8)
            i.textChanged[str].connect(self.ThreeD)  # int

        self.save_img_button = QPushButton('&Save Image')
        self.save_img_button.clicked.connect(self.saveImgFile)
        #self.save_img_button.clicked.connect(self.exportScene)

        self.vbox = QVBoxLayout()
        self.hbox1 =QHBoxLayout()
        self.hbox2 =QHBoxLayout()
        self.hbox3 =QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.hbox1.addWidget(self.log_cb)
        self.hbox1.addWidget(self.legend_cb)
        self.hbox1.addWidget(self.save_img_button)

        for i in self.cb_list:
            self.hbox2.addWidget(i)

        for i in self.setter_list:
            self.hbox3.addWidget(i)

        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def ThreeD(self):

        self.axes.clear()
        self.WholeData = []

        all_matshow =[]


        for k in self.cb_list:
            if k.isChecked():
                text= k.text()
                #print(text)

                for i in range(len(self.DataFiles)):
                    ItemsAvalibale = self.DataFiles[i].columns.values.tolist()
                    if 'Label' in ItemsAvalibale:
                        self.DataFiles[i] = self.DataFiles[i].set_index('Label')
                    dataframe = self.DataFiles[i]
                    dataframe = dataframe.dropna(axis=1, how='all')
                    ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                                   'Style', 'Width']
                    for j in ItemsToTest:
                        if j in ItemsAvalibale:
                            dataframe = dataframe.drop(j, 1)

                    dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
                    dataframe = dataframe.dropna(axis='columns')
                    dataframe = pd.DataFrame(dataframe.values)

                    self.result = dataframe

                    self.originalresult = self.result

                    self.result = pd.DataFrame(self.result.values.flatten())

                    a, b = self.originalresult.shape

                    m = list(i for i in range(a))
                    n = list(i for i in range(b))

                    location_list = list(product(m, n))

                    x = []
                    y = []

                    for k in location_list:
                        x.append(k[0])
                        y.append(k[1])

                    if (self.log_cb.isChecked()):
                        zs = np.log10(self.result.values)
                    else:
                        zs = self.result.values

                    # print(type(zs),zs.shape)
                    zs = np.matrix(zs)
                    #print(type(zs), zs.shape)

                    #print(self.PureColors[i], self.Labels[i])

                    alpha = 0.3

                    try:
                        tmp_alpha = float(self.setter_list[i].text())
                        if 0 <= tmp_alpha <= 1:
                            alpha = tmp_alpha
                    except:
                        pass

                    if (text==self.Labels[i]):
                        self.axes.matshow(zs, aspect='auto', origin='lower', cmap=self.PureColors[i], alpha=alpha)
                        #self.axes.imshow(zs, interpolation='nearest',aspect='auto', origin='lower', cmap=self.PureColors[i], alpha=alpha)
                        #tmp_matshow= plt.matshow(zs, aspect='auto', origin='lower', cmap=self.PureColors[i], alpha=alpha)
                        #all_matshow.append(tmp_matshow)

                        self.axes.scatter(xs=x, ys=y, zs=zs,  marker='o', s=0.5,c=self.PureColor[i],label=self.Labels[i],alpha=alpha)

                        #self.axes.scatter(-1,-1,  marker= 'o', s=20,c=self.PureColor[i],alpha= 1, label=self.Labels[i])
                        #self.axes.set_xlim(left=0)
                        #self.axes.set_ylim(bottom=0)

                        #self.axes.plot_surface(x, y, zs,color=self.PureColor[i],label=self.Labels[i],alpha=alpha)

        scatter_proxy=[]
        for i in range(min(len(self.PureColors),len(self.Labels))):
            tmp_line = matplotlib.lines.Line2D([0], [0], linestyle="none", c=self.PureColor[i], marker='o')
            scatter_proxy.append(tmp_line)

        if (self.legend_cb.isChecked()):
            #self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)
            self.axes.legend(scatter_proxy, self.Labels[0:min(len(self.PureColors),len(self.Labels))], numpoints=1)

        self.canvas.draw()
        self.show()





