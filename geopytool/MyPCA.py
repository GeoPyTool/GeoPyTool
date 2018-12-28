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

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to PCA')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('PCA Result')

        self.fig = plt.figure(figsize=(12, 12))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)


        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.reset_button = QPushButton('&Reset to Original')

        self.pca_button = QPushButton('&Run PCA')
        self.save_button = QPushButton('&Save Current Data')

        self.reset_button.clicked.connect(self.resetResult)
        self.pca_button.clicked.connect(self.PCA_func)
        self.save_button.clicked.connect(self.saveResult)

        self.explained_variance_ratio_label = QLabel('Explained Variance Ratio')
        self.explained_variance_label = QLabel('Explained Variance')

        self.n_components_label = QLabel('Components Numbers')
        self.components_label = QLabel('Components')

        self.vbox = QVBoxLayout()

        self.hbox =QHBoxLayout()

        self.vbox.addWidget(self.tableView)
        self.vbox.addWidget(self.explained_variance_ratio_label)
        self.vbox.addWidget(self.explained_variance_label)
        self.vbox.addWidget(self.n_components_label)
        self.vbox.addWidget(self.components_label)


        self.hbox.addWidget(self.pca_button)
        self.hbox.addWidget(self.reset_button)
        self.hbox.addWidget(self.save_button)


        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def prePCA(self):

        self.fig.clear()
        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df

        dataframe =  dataframe.dropna(axis=1,how='all')



        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe = dataframe.dropna(axis='columns')



        self.result=dataframe
        self.originalresult=self.result
        self.tabelresult=PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)
        self.show()

    def resetResult(self):
        self.result=self.originalresult
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
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


        pca=PCA(n_components='mle')
        try:
            pca.fit(self.result)
            evr = (pca.explained_variance_ratio_)
            ev = (pca.explained_variance_)
            n = (pca.n_components_)
            comp = (pca.components_)

            self.explained_variance_ratio_label.setText('Explained Variance Ratio :' + str(evr))
            self.explained_variance_label.setText('Explained Variance :' + str(ev))
            self.n_components_label.setText('N Components :' + str(n))
            self.components_label.setText('N Components :' + str(comp))

        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.explained_variance_ratio_label.adjustSize()
        self.explained_variance_label.adjustSize()
        self.n_components_label.adjustSize()
        self.components_label.adjustSize()




        pass