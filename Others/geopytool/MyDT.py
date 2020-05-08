from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyDT(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'DecisionTree'
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
    data_to_test =pd.DataFrame()
    switched = True
    text_result = ''
    whole_labels=[]
    clf = tree.DecisionTreeClassifier()
    #pca = DecisionTree(n_components=3)
    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df
        self._df_back = df

        self.FileName_Hint='Decision Tree'

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to DecisionTree')



        self.settings_backup = self._df
        ItemsToTest = ['Label','Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']
        for i in self._df.columns.values.tolist():
            if i not in ItemsToTest:
                self.settings_backup = self.settings_backup.drop(i, 1)
        #print(self.settings_backup)


        self.result_to_fit= self.Slim(self._df)


        #print(self.result_to_fit)
        #print(self.result_to_fit.shape)

        #self.pca=DecisionTree(n_components='mle')

        try:
            self.clf.fit(self.result_to_fit.values,self._df.Label)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(1200,800)
        self.main_frame = QWidget()
        self.dpi = 960
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.setWindowTitle('Decision Tree Classifier')
        self.fig = plt.figure(figsize=(12, 6))
        #self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Key_Func)  # int

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_picture_button.clicked.connect(self.saveImgFile)

        self.save_result_button = QPushButton('&Show DecisionTree Result')
        self.save_result_button.clicked.connect(self.showResult)

        self.save_Para_button = QPushButton('&Show DecisionTree Para')
        self.save_Para_button.clicked.connect(self.showPara)

        self.save_predict_button = QPushButton('&Show Predict Result')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Load Data')
        self.load_data_button.clicked.connect(self.loadDataToTest)



        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()


        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)

        for w in [self.show_load_data_cb, ]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.load_data_button, self.save_picture_button, self.save_result_button, self.save_Para_button, self.save_predict_button]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)


        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)



        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
        self.axes = self.fig.add_subplot(111)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        #self.show()

    def switch(self):
        self.switched = not(self.switched)
        self.create_main_frame()
        self.Key_Func()

    def Key_Func(self):

        self.axes.clear()
        self.clf.fit(self.result_to_fit.values,self._df.Label)


        self.Para=pd.DataFrame()

        self.data_to_test_to_fit=pd.DataFrame()


        if(len(self.data_to_test)>0):

            self.data_to_test_to_fit = self.Slim(self.data_to_test)

            contained = True
            missing = 'Miss setting infor:'

            for i in ['Label', 'Color', 'Marker', 'Alpha']:
                if i not in self.data_to_test.columns.values.tolist():
                    contained = False
                    missing = missing +'\n' + i

            if contained == True:
                for i in self.data_to_test.columns.values.tolist():
                    if i not in self._df.columns.values.tolist():
                        self.data_to_test=self.data_to_test.drop(columns=i)



                self.clf.predict(self.data_to_test_to_fit)
                self.clf.predict_proba(self.data_to_test_to_fit)



        if (self.legend_cb.isChecked()):

            if (self.switched == False):
                    self.axes.legend(loc=2, prop=fontprop)
            else:
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


        #self.result = pd.concat([self.begin_result , self.load_result], axis=0,sort=False).set_index('Label')

        tree.plot_tree(self.clf, max_depth=6, filled = True)
        self.canvas.draw()


    def showPredictResult(self):
        if(len(self.data_to_test)>0):
            Z = self.clf.predict(np.c_[ self.data_to_test_to_fit])
            Z2 = self.clf.predict_proba(np.c_[ self.data_to_test_to_fit])
            proba_df=pd.DataFrame(Z2)
            proba_df.columns = self.clf.classes_

            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i]) + 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'Decision Tree Classification': Z}),
                 pd.DataFrame({'Confidence probability': proba_list}),proba_df],
                axis=1).set_index('Label')
            print(predict_result)

            self.predictpop = TableViewer(df=predict_result, title=self.description +' Decision Tree Predict Result with All Items')
            self.predictpop.show()

