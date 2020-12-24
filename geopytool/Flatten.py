from ImportDependence import *
from CustomClass import *


class MyFlatten(AppForm):
    Lines = []
    Tags = []
    description = 'Flatten'
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
            # print('DataFrame recieved to Flatten')

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
        self.setWindowTitle('Flatten 2-d Data to 1-d list')

        # self.fig = plt.figure(figsize=(12, 12))
        # self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.main_frame)


        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        self.flatten_button = QPushButton('&Flatten')
        self.reset_button = QPushButton('&Reset')
        self.save_button = QPushButton('&Save')

        self.flatten_button.clicked.connect(self.flattenResult)
        self.reset_button.clicked.connect(self.resetResult)
        self.save_button.clicked.connect(self.saveResult)


        self.vbox = QVBoxLayout()

        #self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)





        self.hbox =QHBoxLayout()

        #self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)

        self.hbox.addWidget(self.flatten_button)
        self.hbox.addWidget(self.reset_button)
        self.hbox.addWidget(self.save_button)





        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def Flatten(self):

        # self.fig.clear()
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
        # self.canvas.draw()
        self.show()

    def flattenResult(self):
        self.result=pd.DataFrame(self.result.values.flatten())

        #print(self.originalresult.shape)

        a,b =self.originalresult.shape

        m=list(i for i in range(a))
        n=list(i for i in range(b))

        location_list= list(product(m,n))
        #print(location_list)

        self.tabelresult=PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)
        self.show()


    def resetResult(self):
        self.result=self.originalresult
        self.tabelresult=PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)
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