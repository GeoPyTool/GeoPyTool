from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyPCA(AppForm):
    Lines = []
    Tags = []
    description = 'PCA'
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



    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('PCA Data')
        self._df = df

        self.text_result=''

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to PCA')

        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            #self._df = self._df.set_index('Label')
            dataframe = self._df.set_index('Label')

        dataframe =  dataframe.dropna(axis=1,how='all')

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe = dataframe.dropna(axis='columns')



        self.result_to_fit=dataframe


        pca=PCA(n_components='mle')

        pca.fit(self.result_to_fit.values)
        self.evr = (pca.explained_variance_ratio_)
        self.ev = (pca.explained_variance_)
        self.n = (pca.n_components_)
        self.comp = (pca.components_)


        self.create_main_frame()

    def create_main_frame(self):

        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)

        self.setWindowTitle('PCA Result')

        self.fig = plt.figure(figsize=(12, 6))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)


        #self.axes = self.fig.add_subplot(111)
        self.axes = Axes3D(self.fig, elev=-150, azim=110)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.PCA_func)  # int

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_result_button = QPushButton('&Save PCA Result')
        self.save_picture_button.clicked.connect(self.saveImgFile)
        self.save_result_button.clicked.connect(self.saveResult)



        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, self.n - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.PCA_func)  # int
        self.x_element_label = QLabel('component')

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, self.n - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.PCA_func)  # int
        self.y_element_label = QLabel('component')

        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, self.n - 1)
        self.z_element.setValue(2)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.PCA_func)  # int
        self.z_element_label = QLabel('component')

        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()


        for w in [self.x_element_label,self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.y_element_label,self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        for w in [self.z_element_label,self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.hbox.addWidget(self.legend_cb)
        self.hbox.addWidget(self.save_picture_button)
        self.hbox.addWidget(self.save_result_button)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        self.show()


    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-4]

                self.result.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                # self.result.to_csv(DataFileOutput + '.csv', sep=',', encoding='utf-8')

            elif ('xlsx' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-5]

                self.result.to_excel(DataFileOutput, encoding='utf-8')

                # self.result.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')



    def PCA_func(self):

        a = int(self.x_element.value())
        b = int(self.y_element.value())
        c = int(self.z_element.value())

        self.axes.clear()
        pca=PCA(n_components='mle')

        pca.fit(self.result_to_fit.values)
        self.evr = (pca.explained_variance_ratio_)
        self.ev = (pca.explained_variance_)
        self.n = (pca.n_components_)
        self.comp = (pca.components_)

        #self.text_result='N Components :' + str(n)+'N Components :' + str(comp)+ '\nExplained Variance Ratio :' + str(evr)+'\nExplained Variance :' + str(ev)


        title=[]
        for i in range(len(self.comp)):
            title.append('Components No.'+ str(i+1))

        self.nvs = zip(title, self.comp)
        self.compdict = dict((title, self.comp) for title, self.comp in self.nvs)

        self.result=pd.DataFrame(self.compdict)


        pca_result = pca.fit_transform(self.result_to_fit)

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        for i in range(len(self._df)):
            target =self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

            if target not in all_labels:
                all_labels.append(target)
                all_colors.append(color)
                all_markers.append(marker)
                all_alpha.append(alpha)


        for i in range(len(all_labels)):

            self.axes.scatter(pca_result[self.result_to_fit.index == all_labels[i] , a],
                              pca_result[self.result_to_fit.index == all_labels[i] , b],
                              pca_result[self.result_to_fit.index == all_labels[i] , c],
                              color = all_colors[i],
                              marker = all_markers[i],
                              label=all_labels[i],
                              alpha = all_alpha[i])


        self.axes.set_xlabel("component no."+str(a+1))
        self.x_element_label.setText("component no."+str(a+1))

        self.axes.set_ylabel("component no."+str(b+1))
        self.y_element_label.setText("component no."+str(b+1))

        self.axes.set_zlabel("component no."+str(c+1))
        self.z_element_label.setText("component no."+str(c+1))

        if (self.legend_cb.isChecked()):
            self.axes.legend(loc=2,prop=fontprop)

        self.canvas.draw()

