from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyDist(AppForm):

    #Distance_Type = ['hsim_Distance', 'close_distance','euclidean','chebyshev','cosine','correlation','braycurtis','canberra','cityblock','dice','hamming','jaccard','kulsinski','matching','rogerstanimoto','russellrao','sokalmichener','sokalsneath','sqeuclidean','yule']
    Distance_Type = ['Hsim_Distance', 'Close_Distance', 'Euclidean' ,'Chebyshev','Cosine','Correlation',]

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

        self.WholeResult={}
        self.Lines = []
        self.Tags = []
        self.whole_labels = []
        self.description = 'Dist'
        self.settings_backup = pd.DataFrame()


        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Dist Calculation')
        self._df = df

        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Dist')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)

        self.create_main_frame()

        ItemsAvalibale = self._df.columns.values.tolist()
        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            if target not in self.whole_labels:
                self.whole_labels.append(target)

        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')
        self.result = self._df
        self.result = self.result.dropna(axis=1,how='all')
        self.settings_backup = self._df

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsAvalibale:
            if i in ItemsToTest:
                self.result =  self.result.drop(i, 1)
            elif( i != 'Label'):
                self.settings_backup = self.settings_backup.drop(i, 1)

        self.result = self.result.apply(pd.to_numeric, errors='coerce')
        self.result = self.result.dropna(axis='columns')
        self.originalresult = self.result

        self.tabelresult=PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)

        self.show()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('Dist Result')

        self.fig = plt.figure(figsize=(12, 12))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)


        self.distance_slider = QSlider(Qt.Horizontal)
        self.distance_slider.setRange(0, len(self.Distance_Type)-1)
        self.distance_slider.setTracking(True)
        self.distance_slider.setTickPosition(QSlider.TicksBothSides)
        self.distance_slider.valueChanged.connect(self.Dist)  # int
        self.distance_slider_label= QLabel('Euclidean' ) #

        w=self.width()
        h=self.height()
        self.distance_slider.setFixedWidth(w / 2)
        self.distance_slider_label.setFixedWidth(w / 5)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save Current Data')
        self.reset_button = QPushButton('&Reset to Original')



        # self.save_button.clicked.connect(self.saveDataFile)

        # self.save_button.clicked.connect(self.saveImgFile)

        self.save_button.clicked.connect(self.saveResult)
        self.reset_button.clicked.connect(self.resetResult)

        self.vbox = QVBoxLayout()

        self.hbox =QHBoxLayout()

        #self.vbox.addWidget(self.canvas)
        self.vbox.addWidget(self.tableView)

        self.hbox.addWidget(self.distance_slider_label)
        self.hbox.addWidget(self.distance_slider)
        self.hbox.addWidget(self.reset_button)
        self.hbox.addWidget(self.save_button)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def Dist(self):
        self.WholeResult={}

        slider_value = int(self.distance_slider.value())
        self.distance_slider_label.setText(self.Distance_Type[slider_value])

        #print(self.whole_labels)
        comb_labels = list(combinations(self.whole_labels, 2))
        #print(comb_labels)


        for i in comb_labels:

            tmp_result=[]

            #print(i)
            tmp_a= self.originalresult[self.originalresult.index == i[0]]
            tmp_b= self.originalresult[self.originalresult.index == i[1]]

            tmp_team = list(product(tmp_a.values.tolist(), tmp_b.values.tolist()))

            for m in tmp_team:
                if slider_value == 0:
                    tmp_result.append(self.Hsim_Distance(m[0], m[1]))
                elif slider_value == 1:
                    tmp_result.append(self.Close_Distance(m[0], m[1]))
                elif slider_value == 2: tmp_result.append(distance.euclidean(m[0], m[1]))
                elif slider_value == 3: tmp_result.append(distance.chebyshev(m[0], m[1]))
                elif slider_value == 4: tmp_result.append(distance.cosine(m[0], m[1]))
                elif slider_value == 5: tmp_result.append(distance.correlation(m[0], m[1]))
                elif slider_value == 6: tmp_result.append(distance.braycurtis(m[0], m[1]))
                elif slider_value == 7: tmp_result.append(distance.canberra(m[0], m[1]))
                elif slider_value == 8: tmp_result.append(distance.cityblock(m[0], m[1]))
                elif slider_value == 9: tmp_result.append(distance.dice(m[0], m[1]))
                elif slider_value == 10: tmp_result.append(distance.hamming(m[0], m[1]))
                elif slider_value == 11: tmp_result.append(distance.jaccard(m[0], m[1]))
                elif slider_value == 12: tmp_result.append(distance.kulsinski(m[0], m[1]))
                elif slider_value == 13: tmp_result.append(distance.matching(m[0], m[1]))
                elif slider_value == 14: tmp_result.append(distance.rogerstanimoto(m[0], m[1]))
                elif slider_value == 15: tmp_result.append(distance.russellrao(m[0], m[1]))
                elif slider_value == 16: tmp_result.append(distance.sokalmichener(m[0], m[1]))
                elif slider_value == 17: tmp_result.append(distance.sokalsneath(m[0], m[1]))
                elif slider_value == 18: tmp_result.append(distance.sqeuclidean(m[0], m[1]))
                elif slider_value == 19: tmp_result.append(distance.yule(m[0], m[1]))


                    #print(tmp_result)

            self.WholeResult[str(i[0])+'_'+str(i[1])]=tmp_result

        #print(self.WholeResult)

        #self.result=pd.DataFrame.from_dict(self.WholeResult, orient='index')
        self.result=pd.DataFrame.from_dict(self.WholeResult, orient='index')

        self.result.index.names = ['Label']

        Distance_Chosen= self.Distance_Type[slider_value]
        Columns_List=[]

        for i in range(len(self.result.columns)):
            if i ==0:
                Columns_List.append(Distance_Chosen)
            else:
                Columns_List.append('')

        self.result.columns = Columns_List
        print(self.result.columns.values)


        #print(self.result)
        #self.result.index.name = 'Distance'
        #self.result.reset_index()
        #print(self.result)
        self.tabelresult = PandasModel(self.result)
        self.tableView.setModel(self.tabelresult)
        self.show()
        pass

    def resetResult(self):
        self.result=self.originalresult
        self.tableresult=PandasModel(self.result)
        self.tableView.setModel(self.tableresult)
        self.show()

