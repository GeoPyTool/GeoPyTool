from ImportDependence import *
from CustomClass import *


class MySta(AppForm):
    Lines = []
    Tags = []
    description = 'Sta'
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
        self.setWindowTitle('Statistics Result')
        self._df = df

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Sta')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('Statistics Result')
        self.fig = plt.figure(figsize=(12, 8))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.05, bottom=0.1, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Sta)  # int

        self.save_button = QPushButton('&Save Result')
        self.save_img_button = QPushButton('&Save Image')

        # self.save_button.clicked.connect(self.saveDataFile)
        #

        self.save_button.clicked.connect(self.saveResult)
        self.save_img_button.clicked.connect(self.saveImgFile)




        self.vbox = QVBoxLayout()

        self.hbox =QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)

        self.hbox.addWidget(self.legend_cb)
        self.hbox.addWidget(self.save_img_button)
        self.hbox.addWidget(self.save_button)


        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        w=self.width()
        h=self.height()

        self.tableView.setFixedHeight(h/3)

    def Sta(self):

        self.fig.clear()
        self.axes.clear()
        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()
        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')
        dataframe = self._df
        dataframe =  dataframe.dropna(axis=1,how='all')
        self.settings_backup = self._df
        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
        for i in ItemsAvalibale:
            if i in ItemsToTest:
                dataframe = dataframe.drop(i, 1)
            elif( i != 'Label'):
                self.settings_backup = self.settings_backup.drop(i, 1)

        #if 'Label' in self.settings_backup.columns.values.tolist(): self.settings_backup = self.settings_backup.set_index('Label')
        dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe = dataframe.dropna(axis='columns')



        StatResultDict = {}

        rows_to_plot=[]
        color_to_plot=[]
        alpha_to_plot=[]
        label_to_plot=[]

        for index, row in dataframe.iterrows():
            StatResultDict[index] = self.stateval(row)
            target = self.raw.loc[(self.raw['Label'] == index)]
            target =target.to_dict()
            color = list(target['Color'].values())[0]
            alpha = list(target['Alpha'].values())[0]

            rows_to_plot.append(row)
            label_to_plot.append(index)
            color_to_plot.append(color)
            alpha_to_plot.append(alpha)


            #plt.hist(row,  density=True, facecolor= color, alpha= alpha, label= index)

        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        plt.hist(rows_to_plot, density=True, color=color_to_plot, alpha=0.6, label= label_to_plot)

        if (self.legend_cb.isChecked()):
            plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0, prop=fontprop)


        StdSortedList = sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std'])
        StdSortedList.reverse()
        StatResultDf = pd.DataFrame.from_dict(StatResultDict, orient='index')

        self.result = pd.concat([self.settings_backup,StatResultDf], axis=1,sort=False)



        StatResultDf['Items'] = StatResultDf.index.tolist()
        self.tabelresult = PandasModel(StatResultDf)
        #self.tabelresult = PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)
        self.canvas.draw()
        self.show()

        #print(self.settings_backup)
        #self.tablepop = TableViewer(df=self.settings_backup,title='Setting Backup')
        #self.tablepop.show()



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



