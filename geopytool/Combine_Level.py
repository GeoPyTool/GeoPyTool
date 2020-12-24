from ImportDependence import *
from CustomClass import *


class MyCombine_transverse(AppForm):
    Lines = []
    Tags = []
    description = 'Combine_transverse'
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
        self.setWindowTitle('Combine_transverse Data')
        self.result = df

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Combine_transverse')

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
        self.setWindowTitle('Combine_transverse Result')

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

        #self.undo_button = QPushButton('&Undo')

        self.fillNaN_button = QPushButton('&Fill Blanks with 0')
        self.RemoveNaNColumns_button = QPushButton('&Remove Columns with Blank')
        self.RemoveNaNRows_button = QPushButton('&Remove Rows with Blank')



        # self.save_button.clicked.connect(self.saveDataFile)

        # self.save_button.clicked.connect(self.saveImgFile)

        self.save_button.clicked.connect(self.saveResult)
        self.reset_button.clicked.connect(self.resetResult)
        # self.undo_button.clicked.connect(self.undoResult)

        self.fillNaN_button.clicked.connect(self.fillNaN)
        self.RemoveNaNColumns_button.clicked.connect(self.RemoveNaNColumns)
        self.RemoveNaNRows_button.clicked.connect(self.RemoveNaNRows)


        self.vbox = QVBoxLayout()

        self.hbox =QHBoxLayout()

        #self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)

        self.hbox.addWidget(self.save_button)
        self.hbox.addWidget(self.reset_button)
        # self.vbox.addWidget(self.undo_button)

        self.hbox.addWidget(self.fillNaN_button)
        self.hbox.addWidget(self.RemoveNaNColumns_button)
        self.hbox.addWidget(self.RemoveNaNRows_button)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def Combine_transverse(self):

        self.fig.clear()
        self.WholeData = []
        ItemsAvalibale = self.result.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self.result = self.result.set_index('Label')

        self.originalresult= self.result
        self.lastresult = self.result

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




    def resetResult(self):
        self.result=self.originalresult
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()


    def undoResult(self):
        self.result = self.lastresult
        self.result = PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def fillNaN(self):
        self.lastresult = self.result
        self.result=self.result.fillna(0)
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def RemoveNaNColumns(self):
        self.lastresult = self.result
        self.result = self.result.dropna(axis='columns')
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

    def RemoveNaNRows(self):
        self.lastresult = self.result
        self.result = self.result.dropna(axis='index')
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()
