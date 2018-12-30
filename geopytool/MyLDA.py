from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyLDA(AppForm):
    Lines = []
    Tags = []
    description = 'LDA'
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
        self.setWindowTitle('LDA Data')
        self._df = df

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to LDA')

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
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)


        self.setWindowTitle('LDA Result')

        self.fig = plt.figure(figsize=(12, 6))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.reset_button = QPushButton('&Reset to Original')

        self.LDA_button = QPushButton('&Run LDA')
        self.save_button = QPushButton('&Save Current Data')

        self.reset_button.clicked.connect(self.resetResult)
        self.LDA_button.clicked.connect(self.LDA_func)
        self.save_button.clicked.connect(self.saveResult)

        self.explained_variance_ratio_label = QLabel('Explained Variance Ratio')
        self.explained_variance_label = QLabel('Explained Variance')

        self.n_components_label = QLabel('Components Numbers')
        self.components_label = QLabel('Components')

        self.vbox = QVBoxLayout()

        self.hbox =QHBoxLayout()


        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)
        #self.vbox.addWidget(self.explained_variance_ratio_label)
        #self.vbox.addWidget(self.explained_variance_label)
        #self.vbox.addWidget(self.n_components_label)
        self.vbox.addWidget(self.components_label)


        self.hbox.addWidget(self.LDA_button)
        self.hbox.addWidget(self.reset_button)
        self.hbox.addWidget(self.save_button)


        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def preLDA(self):


        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df


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


    def LDA_func(self):

        # self.fig.clear()

        self.axes.clear()
        lda=LinearDiscriminantAnalysis(n_components=2)
        X=self.result.apply(pd.to_numeric, errors='coerce')
        Y=self.result.index
        y=[]
        for i in Y:
            if i==Y[0]:
                y.append(1)
            else:
                y.append(0)
        try:
            #lda.fit(X,Y)
            lda.fit(self.result.values, self.result.index)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        X_new = lda.fit(self.result.values,self.result.index).transform(self.result.values)


        print(X_new.shape)
        print(y)
        #self.axes.scatter(X_new[:, 0], X_new[:, 1], marker='o', c=y)

        self.canvas.draw()
        self.show()

