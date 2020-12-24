from ImportDependence import *
from CustomClass import *


class MyTwoD_Grey(AppForm):
    Lines = []
    Tags = []
    FileName_Hint=''
    description = 'TwoD'
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



    def __init__(self, parent=None,  DataFiles =[pd.DataFrame()],DataLocation='DataLocation'):
        QMainWindow.__init__(self, parent)
        self.FileName_Hint=''
        self.DataFiles = DataFiles
        self.DataLocation = DataLocation
        self.Labels = self.getFileName(self.DataLocation)
        self.setWindowTitle('TwoD Data Visualization')


        self.items = []
        if (len(self.DataFiles) > 0):
            self._changed = True
            # print('DataFrame recieved to TwoD')

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('TwoD Data Visualization')

        self.fig = plt.figure(figsize=(12, 8))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        #self.axes = Axes3D(self.fig, elev=-150, azim=110)
        self.axes = self.fig.add_subplot(111)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.log_cb = QCheckBox('&Log')
        self.log_cb.setChecked(True)
        self.log_cb.stateChanged.connect(self.TwoD)  # int

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TwoD)  # int

        self.y_flip_cb = QCheckBox('&Flip Y')
        self.y_flip_cb.setChecked(False)
        self.y_flip_cb.stateChanged.connect(self.TwoD)  # int

        self.x_flip_cb = QCheckBox('&Flip X')
        self.x_flip_cb.setChecked(False)
        self.x_flip_cb.stateChanged.connect(self.TwoD)  # int


        self.cb_list=[]

        self.setter_list=[]


        for i in range(len(self.Labels)):

            tmp_cb = QCheckBox(self.Labels[i])
            tmp_cb.setChecked(True)
            self.cb_list.append(tmp_cb)

            tmp_setter = QLineEdit(self)
            tmp_setter.setText('Alpha 0-1')
            self.setter_list.append(tmp_setter)


        w = self.width()
        for i in self.cb_list:
            i.setFixedWidth(w / 8)
            i.stateChanged.connect(self.TwoD)  # int

        for i in self.setter_list:
            i.setFixedWidth(w / 8)
            i.textChanged[str].connect(self.TwoD)  # int

        self.save_img_button = QPushButton('&Save Image')
        self.save_img_button.clicked.connect(self.saveImgFile)
        #self.save_img_button.clicked.connect(self.exportScene)

        self.vbox = QVBoxLayout()
        self.hbox1 =QHBoxLayout()
        self.hbox2 =QHBoxLayout()
        self.hbox3 =QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.hbox1.addWidget(self.legend_cb)
        self.hbox1.addWidget(self.log_cb)
        self.hbox1.addWidget(self.x_flip_cb)
        self.hbox1.addWidget(self.y_flip_cb)
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



    def TwoD(self):

        self.FileName_Hint=''
        self.axes.clear()
        self.WholeData = []

        all_matshow =[]

        for k in self.cb_list:
            if k.isChecked():

                text= k.text()



                self.FileName_Hint+=text
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

                    if (self.log_cb.isChecked()):
                        zs = np.log10(dataframe.values)
                    else:
                        zs = dataframe.values




                    # print(type(zs),zs.shape)
                    zs = np.matrix(zs)
                    #print(type(zs), zs.shape)

                    #print( self.Labels[i])

                    alpha = 1

                    try:
                        tmp_alpha = float(self.setter_list[i].text())
                        if 0 <= tmp_alpha <= 1:
                            alpha = tmp_alpha
                    except:
                        pass

                    if (text==self.Labels[i]):
                        #self.axes.matshow(zs, aspect='auto', origin='lower', cmap=self.PureColors[i], alpha=alpha)

                        #m = mean(zs)
                        #new_zs = zs/m
                        #print(new_zs)

                        self.axes.imshow(zs, interpolation='nearest',aspect='auto', origin='lower', cmap= 'Greys', alpha=alpha)


                        #tmp_matshow= plt.matshow(zs, aspect='auto', origin='lower', cmap=self.PureColors[i], alpha=alpha)
                        #all_matshow.append(tmp_matshow)
                        #print(self.PureColor[i])
                        self.axes.scatter(-1,-1,  marker= 'o', s=20,c='grey',alpha= 1, label=self.Labels[i],edgecolors='black')
                        self.axes.set_xlim(left=0)
                        self.axes.set_ylim(bottom=0)




        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        #x_max,y_max= 0,0
        xlim=self.axes.get_xlim()
        ylim=self.axes.get_ylim()


        print(xlim,ylim )

        if (self.x_flip_cb.isChecked()):
            self.axes.set_xlim(max(xlim),min(xlim))
        else:
            self.axes.set_xlim(min(xlim), max(xlim))

        if (self.y_flip_cb.isChecked()):
            self.axes.set_ylim(max(ylim),min(ylim))
        else:
            self.axes.set_ylim(min(ylim),max(ylim))

        self.canvas.draw()
        self.show()

    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/'+self.FileName_Hint,
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi=300)
            #self.canvas.print_raw(ImgFileOutput, dpi=300)




