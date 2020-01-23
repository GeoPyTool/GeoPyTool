from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyTrans(AppForm):
    Lines = []
    Tags = []
    description = 'Trans'
    settings_backup=pd.DataFrame()
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
        self.setWindowTitle('Trans Data')
        self._df = df

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Trans')

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
        self.setWindowTitle('Trans Result')

        self.fig = plt.figure(figsize=(12, 12))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)


        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save Current Data')
        self.reset_button = QPushButton('&Reset to Original')


        self.transpose_button = QPushButton('&Transpose')
        self.center_Geometric_button = QPushButton('&Center by Geometric Mean')
        self.center_Arithmetic_button = QPushButton('&Center by Arithmetic Mean')

        self.std_button = QPushButton('&Standard Transform')
        self.log_button = QPushButton('&Log Transform')
        self.log_ten_button = QPushButton('&Log 10 Transform')
        self.log_e_button = QPushButton('&Log e Transform')

        self.fill_NaN_button = QPushButton('&Fill Blanks With 0')
        self.remove_row_with_0_button = QPushButton('&Remove Rows With Blanks')
        self.remove_column_with_0_button = QPushButton('&Remove Columns With Blanks')


        # self.save_button.clicked.connect(self.saveDataFile)

        # self.save_button.clicked.connect(self.saveImgFile)

        self.save_button.clicked.connect(self.saveResult)
        self.reset_button.clicked.connect(self.resetResult)

        self.transpose_button.clicked.connect(self.transpose)
        self.center_Geometric_button.clicked.connect(self.center_Geometric)
        self.center_Arithmetic_button.clicked.connect(self.center_Arithmetic)
        self.std_button.clicked.connect(self.std_trans)
        self.log_button.clicked.connect(self.log_trans)
        self.log_ten_button.clicked.connect(self.log_ten_trans)
        self.log_e_button.clicked.connect(self.log_e_trans)



        self.fill_NaN_button.clicked.connect(self.fill_NaNs)
        self.remove_row_with_0_button.clicked.connect(self.remove_row_with_0)
        self.remove_column_with_0_button .clicked.connect(self.remove_column_with_0)



        self.vbox = QVBoxLayout()

        self.hbox0 =QHBoxLayout()
        self.hbox1 =QHBoxLayout()
        self.hbox2 =QHBoxLayout()

        #self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)

        for w in [self.reset_button,
                  self.save_button,]:
            self.hbox0.addWidget(w)

        for w in [self.center_Arithmetic_button,
                  self.center_Geometric_button,
                  self.std_button,
                  self.log_ten_button,
                  self.log_e_button,]:
            self.hbox1.addWidget(w)

        for w in [self.transpose_button,
                  self.fill_NaN_button,
                  self.remove_row_with_0_button,
                  self.remove_column_with_0_button]:
            self.hbox2.addWidget(w)


        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def Trans(self):

        self.fig.clear()
        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df

        #dataframe =  dataframe.dropna(axis=1,how='all')

        self.settings_backup = self._df

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsAvalibale:
            if i in ItemsToTest:
                dataframe = dataframe.drop(i, 1)
            elif( i != 'Label'):
                self.settings_backup = self.settings_backup.drop(i, 1)


        dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
        #dataframe = dataframe.dropna(axis='columns')

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

        #self.result self.settings_backup

        #self.result = self.result.merge(self.settings_backup, how='outer')

        self.result = pd.concat([self.settings_backup,self.result], axis=1)

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

    def fill_NaNs(self):
        self.result = self.result.fillna(0)
        self.tableresult = PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def transpose(self):
        self.result=self.result.T
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def remove_row_with_0(self):
        self.settings_backup = self._df
        self.settings_backup = self.settings_backup.dropna()

        #dataframe = self._df
        ItemsAvalibale = self._df.columns.values.tolist()

        ItemsToTest = ['Number', 'Tag', 'Index', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsAvalibale:
            if i in ItemsToTest:
                pass
            elif (i != 'Label'):
                self.settings_backup = self.settings_backup.drop(i, 1)
        self.result = self.result.dropna()
        self.tableresult = PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def remove_column_with_0(self):
        self.result = self.result.dropna(axis=1)
        self.tableresult = PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def center_Geometric(self):

        gmean=st.gmean(self.result.T)
        tmpresult=self.result.T/gmean
        self.result=tmpresult.T
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()


    def center_Arithmetic(self):
        mean=self.result.T.mean(numeric_only= float)
        tmpresult=self.result.T-mean
        self.result=tmpresult.T
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()


    def std_trans(self):
        mean=self.result.T.mean(numeric_only= float)
        std=self.result.T.std(numeric_only= float)
        tmpresult=(self.result.T-mean)/std
        self.result=tmpresult.T
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def log_trans(self):
        self.result=np.log(self.result)
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def log_ten_trans(self):
        self.result=np.log10(self.result)
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def log_e_trans(self):
        self.result=np.log(self.result)
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()


