from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyQDA(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'QDA'
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
    data_to_test=pd.DataFrame()
    text_result = ''
    whole_labels=[]
    QDA = QuadraticDiscriminantAnalysis
    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df

        self._df_back = df


        self.FileName_Hint='QDA'


        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to QDA')

        self.settings_backup = self._df
        ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha', 
                       'Style', 'Width']
        for i in self._df.columns.values.tolist():
            if i not in ItemsToTest:
                self.settings_backup = self.settings_backup.drop(i, 1)
        #print(self.settings_backup)


        self.result_to_fit= self.Slim(self._df)

        self.QDA = QuadraticDiscriminantAnalysis(n_components=len(self.result_to_fit)-1)

        le = LabelEncoder()
        le.fit(self.result_to_fit.index)
        original_label = le.transform(self.result_to_fit.index)

        #print(self.result_to_fit.columns.values.tolist())

        try:
            self.QDA.fit(self.result_to_fit.values,original_label)
            self.comp = (self.QDA.scalings_)
            self.n = len(self.comp)

        except Exception as e:
            self.ErrorEvent(text=repr(e))
        self.create_main_frame()

    def create_main_frame(self):

        self.resize(800, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)

        self.setWindowTitle('Quadratic Discriminant Analysis')

        self.fig = plt.figure(figsize=(12, 6))
        #self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.3, bottom=0.3, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Key_Func)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Key_Func)  # int

        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Key_Func)  # int

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_picture_button.clicked.connect(self.saveImgFile)

        self.save_result_button = QPushButton('&Show QDA Result')
        self.save_result_button.clicked.connect(self.showResult)

        self.save_Para_button = QPushButton('&Show QDA Para')
        self.save_Para_button.clicked.connect(self.showPara)

        self.save_predict_button = QPushButton('&Show Predict Result')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Add Data to Test')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        self.kernel_select = QSlider(Qt.Horizontal)
        self.kernel_select.setRange(0, len(self.kernel_list)-1)
        self.kernel_select.setValue(0)
        self.kernel_select.setTracking(True)
        self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        self.kernel_select.valueChanged.connect(self.Key_Func)  # int
        self.kernel_select_label = QLabel('Kernel')

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)

        for w in [self.legend_cb, self.show_load_data_cb, self.show_data_index_cb, self.shape_cb, self.hyperplane_cb,self.kernel_select_label,self.kernel_select ]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.load_data_button, self.save_picture_button, self.save_result_button, self.save_Para_button, self.save_predict_button]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)

        self.axes = self.fig.add_subplot(111)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        #self.show()



    def Key_Func(self):

        a = 0
        b = 1

        k_s = int(self.kernel_select.value())

        self.axes.clear()

        le = LabelEncoder()
        le.fit(self.result_to_fit.index)
        original_label = le.transform(self.result_to_fit.index)

        #print(self.result_to_fit.columns.values.tolist())


        self.QDA.fit(self.result_to_fit.values, original_label)
        self.comp = (self.QDA.scalings_)
        self.n = len(self.comp)
        self.qda_result = self.QDA.fit_transform(self.result_to_fit.values, original_label)
        #self.qda_result = self.QDA.transform(self.result_to_fit.values)

        #self.text_result='N Components :' + str(n)+'N Components :' + str(comp)+ '\nExplained Variance Ratio :' + str(evr)+'\nExplained Variance :' + str(ev)


        title=[]
        for i in range(len(self.comp)):
            title.append('Components No.'+ str(i+1))

        self.nvs = zip(title, self.comp)
        self.compdict = dict((title, self.comp) for title, self.comp in self.nvs)

        self.Para=pd.DataFrame(self.compdict)

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        self.color_list=[]

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
            if color not in self.color_list:
                self.color_list.append(color)

        self.whole_labels = all_labels

        if(len(self.data_to_test)>0):

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

                #print(self.data_to_test)

                test_labels=[]
                test_colors=[]
                test_markers=[]
                test_alpha=[]


                for i in range(len(self.data_to_test)):
                    target = self.data_to_test.at[i, 'Label']
                    color = self.data_to_test.at[i, 'Color']
                    marker = self.data_to_test.at[i, 'Marker']
                    alpha = self.data_to_test.at[i, 'Alpha']

                    if target not in test_labels and target not in all_labels:
                        test_labels.append(target)
                        test_colors.append(color)
                        test_markers.append(marker)
                        test_alpha.append(alpha)


                self.whole_labels = self.whole_labels +test_labels

                self.data_to_test_to_fit= self.Slim(self.data_to_test)


                self.load_settings_backup = self.data_to_test
                Load_ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 
                               'Alpha', 'Style', 'Width']
                for i in self.data_to_test.columns.values.tolist():
                    if i not in Load_ItemsToTest:
                        self.load_settings_backup = self.load_settings_backup .drop(i, 1)

                #print(self.data_to_test_to_fit)
                #print(self.data_to_test_to_fit.shape)

                try:
                    self.qda_data_to_test = self.QDA.transform(self.data_to_test_to_fit)


                    self.load_result = pd.concat([self.load_settings_backup, pd.DataFrame(self.qda_data_to_test)], axis=1)

                    for i in range(len(test_labels)):

                        if (self.show_load_data_cb.isChecked()):
                            self.axes.scatter(self.qda_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a],
                                              self.qda_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b],
                                              color=test_colors[i],
                                              marker=test_markers[i],
                                              label=test_labels[i],
                                              alpha=test_alpha[i])


                            '''
                            if (self.shape_cb.isChecked()):
                                pass
                                XtoFit = self.qda_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a]
                                YtoFit = self.qda_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b]

                                xmin, xmax = min(XtoFit), max(XtoFit)
                                ymin, ymax = min(YtoFit), max(YtoFit)

                                DensityColorMap = 'Blues'
                                DensityAlpha = 0.1

                                DensityLineColor = test_colors[i]
                                DensityLineAlpha = 0.1
                                # Peform the kernel density estimate
                                xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                                positions = np.vstack([xx.ravel(), yy.ravel()])
                                values = np.vstack([XtoFit, YtoFit])
                                kernelstatus = True
                                try:
                                    st.gaussian_kde(values)
                                except Exception as e:
                                    self.ErrorEvent(text=repr(e))
                                    kernelstatus = False
                                if kernelstatus == True:
                                    kernel = st.gaussian_kde(values)
                                    f = np.reshape(kernel(positions).T, xx.shape)
                                    # Contourf plot
                                    cfset = self.axes.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
                                    # Contour plot
                                    cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                                    # Label plot
                                    self.axes.clabel(cset, inline=1, fontsize=10)                            
                            '''
                except Exception as e:
                    self.ErrorEvent(text=repr(e))

            else:
                self.ErrorEvent(text=missing)


        #self.kernel_select_label.setText(self.kernel_list[k_s])
        self.axes.set_xlabel("function "+str(a))

        self.axes.set_ylabel("function "+str(b))


        self.begin_result = pd.concat([self.settings_backup, pd.DataFrame(self.qda_result)], axis=1)

        for i in range(len(all_labels)):
            self.axes.scatter(self.qda_result[self.result_to_fit.index == all_labels[i], a],
                              self.qda_result[self.result_to_fit.index == all_labels[i], b],
                              color=all_colors[i],
                              marker=all_markers[i],
                              label=all_labels[i],
                              alpha=all_alpha[i])

            if (self.shape_cb.isChecked()):
                pass
                XtoFit = self.qda_result[self.result_to_fit.index == all_labels[i], a]
                YtoFit = self.qda_result[self.result_to_fit.index == all_labels[i], b]

                xmin, xmax = min(XtoFit), max(XtoFit)
                ymin, ymax = min(YtoFit), max(YtoFit)

                DensityColorMap = 'Greys'
                DensityAlpha = 0.1

                DensityLineColor = all_colors[i]
                DensityLineAlpha = 0.3
                # Peform the kernel density estimate
                xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                positions = np.vstack([xx.ravel(), yy.ravel()])
                values = np.vstack([XtoFit, YtoFit])
                kernelstatus = True
                try:
                    st.gaussian_kde(values)
                except Exception as e:
                    self.ErrorEvent(text=repr(e))
                    kernelstatus = False

                if kernelstatus == True:
                    kernel = st.gaussian_kde(values)
                    f = np.reshape(kernel(positions).T, xx.shape)
                    # Contourf plot
                    cfset = self.axes.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
                    # Contour plot
                    cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                    # Label plot
                    # self.axes.clabel(cset, inline=1, fontsize=10)

        if (self.show_data_index_cb.isChecked()):
            for i in range(len(self.qda_result)):
                    if 'Index' in self._df.columns.values:

                        self.axes.text(self.qda_result[i, a], self.qda_result[i, b], self._df_back.at[i, 'Index'], size=self._df.at[i, 'Size'], zorder=1, color=self._df.at[i, 'Color'],
                                   alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes.text(self.qda_result[i, a], self.qda_result[i, b], 'No'+str(i+1), size=self._df.at[i, 'Size'], zorder=1, color=self._df.at[i, 'Color'],
                                   alpha=self._df.at[i, 'Alpha'])

        if (self.hyperplane_cb.isChecked()):
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            svm_x = self.qda_result[:, a]
            svm_y = self.qda_result[:, b]
            xx, yy = np.meshgrid(np.arange(min(svm_x), max(svm_x), np.ptp(svm_x) / 500),
                                 np.arange(min(svm_y), max(svm_y), np.ptp(svm_y) / 500))

            le = LabelEncoder()
            le.fit(self.result_to_fit.index)
            class_label = le.transform(self.result_to_fit.index)
            svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y)], axis=1)

            svm_train = svm_train.values
            clf.fit(svm_train, class_label)
            Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)
            self.axes.contourf(xx, yy, Z,cmap=ListedColormap(self.color_list), alpha=0.2)


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)



        self.result = pd.concat([self.begin_result , self.load_result], sort=False, axis=0).set_index('Label')
        self.canvas.draw()

    def showPredictResult(self):


        k_s = int(self.kernel_select.value())

        try:
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            clf.fit(self.qda_result, self.result_to_fit.index)
            Z = clf.predict(np.c_[self.qda_data_to_test])

            Z2 = clf.predict_proba(np.c_[self.qda_data_to_test])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_

            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})], 
                axis=1).set_index('Label')
            #print(predict_result)

            #self.predictpop = TableViewer(df=predict_result, title='SVM Predict Result with All Items')
            self.predictpop = TableViewer(df=predict_result,
                                          title=self.description + ' SVM Predict Result with All Items')
            self.predictpop.show()

            '''
            DataFileOutput, ok2 = QFileDialog.getSaveFileName(self, '文件保存', 'C:/', 'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出
            if (DataFileOutput != ''):
                if ('csv' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-4]
                    predict_result.to_csv(DataFileOutput, sep=', ', encoding='utf-8')
                    # self.result.to_csv(DataFileOutput + '.csv', sep=', ', encoding='utf-8')
                elif ('xlsx' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-5]
                    predict_result.to_excel(DataFileOutput, encoding='utf-8')
                    # self.result.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')


            '''

        except Exception as e:
            msg = 'You need to load another data to run SVM.\n '
            self.ErrorEvent(text= msg +repr(e) )

    def Distance_Calculation(self):

        print(self.whole_labels)
        distance_result={}

        #distance_result[self.whole_labels[i]] = []

        print(distance_result)

        for i in range(len(self.whole_labels)):
            #print(self.whole_labels[i], self.qda_result[self.result_to_fit.index == self.whole_labels[i]][0])
            print( self.whole_labels[i], len(self.qda_result[self.result_to_fit.index == self.whole_labels[i]]))

            pass


        '''
        for i in range(len(self.whole_labels)):
            for j in range(len(self.whole_labels)):
                if i ==j:
                    pass
                else:
                    distance_result[self.whole_labels[i] + ' to ' + self.whole_labels[j]] = []

                    self.qda_result[self.result_to_fit.index == self.whole_labels[i]]

                    self.qda_result[self.result_to_fit.index == self.whole_labels[j]]

                    for m in range(len(self.qda_result[self.result_to_fit.index == self.whole_labels[i]])):
                        for n in range(len(self.qda_result[self.result_to_fit.index == self.whole_labels[j]])):
                            pass

                            self.qda_result[self.result_to_fit.index == self.whole_labels[i]][m]

                            #tmp_dist= self.Hsim_Distance(self.qda_result[self.result_to_fit.index == self.whole_labels[i]][m], self.qda_result[self.result_to_fit.index == self.whole_labels[j]][n])
                            #print(tmp_dist)
                            #distance_result[self.whole_labels[i] + ' to ' + self.whole_labels[j]].append(tmp_dist)
            pass
        
        '''


        #print(self.qda_result)

        try:
            self.qda_data_to_test[self.data_to_test_to_fit.index == self.whole_labels[0], 0]
        except Exception as e:
            pass
            # self.ErrorEvent(text=repr(e))
