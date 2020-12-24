from ImportDependence import *
from CustomClass import *
#from TableViewer import TableViewer


class K2OSiO2(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$K_2O wt\%$'

    itemstocheck = ['SiO2', 'K2O']
    reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'

    AreasHeadClosed = []
    SelectDic = {}

    TypeList=[]

    All_X = []
    All_Y = []

    whole_labels=[]
    SVM_labels=[]



    LocationAreas = [ [ [45,100],[45, 0.945], [48, 1.2], [68, 2.9], [85, 4.345],[85,100]],
                   [ [45, 0.945],  [48, 1.2], [68, 2.9], [85, 4.345],[85, 1.965],[68, 1.2], [48, 0.3],[45, 0.16499999999999998]],
                    [[45, 0.16499999999999998], [48, 0.3], [68, 1.2], [85, 1.965],[85,0],[45,0],]
                     ]

    ItemNames = ['High K',
                 'Medium K',
                 'Low K',
                 ]

    def create_main_frame(self):
        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls


        self.load_data_button = QPushButton('&Add Data to Compare')
        self.load_data_button.clicked.connect(self.loadDataToTest)


        self.save_button = QPushButton('&Save Img')
        self.save_button.clicked.connect(self.saveImgFile)

        self.result_button = QPushButton('&Classification Result')
        self.result_button.clicked.connect(self.Explain)


        self.save_predict_button_selected = QPushButton('&Predict Result')
        self.save_predict_button_selected.clicked.connect(self.showPredictResultSelected)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.K2OSiO2)  # int


        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.K2OSiO2)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.K2OSiO2)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.K2OSiO2)  # int


        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.K2OSiO2)  # int


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        for w in [self.load_data_button,self.save_button, self.result_button, self.save_predict_button_selected]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.legend_cb,self.show_load_data_cb,self.show_data_index_cb,self.shape_cb,self.hyperplane_cb]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)



        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        w=self.width()
        h=self.height()



    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.K2OSiO2()


    def K2OSiO2(self, Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
            Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xlabel=r'$SiO_2 wt\%$', ylabel=r'$K_2O wt\%$', width=12,
            height=12, dpi=300):
        self.setWindowTitle('K2OSiO2  diagram ')
        self.axes.clear()
        #self.axes.axis('off')
        
        
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')

        '''
        self.axes.set_xticks([30,40,50,60,70,80,90])
        self.axes.set_xticklabels([30,40,50,60,70,80,90])

        self.axes.set_yticks([0, 5, 10, 15, 20])
        self.axes.set_yticklabels([0, 5, 10, 15, 20])

        self.axes.set_ylim(bottom=0)

        '''

        self.OutPutData = pd.DataFrame()

        self.LabelList = []
        self.IndexList = []
        self.TypeList = []

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        self.AllLabel = []


        for i in range(len(self.LocationAreas)):
            tmpi = self.LocationAreas[i] + [
                self.LocationAreas[i][0]]  # Here is to add the beginning point to the region
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic[self.ItemNames[i]] = tmppath

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

            if target not in self.SVM_labels:
                self.SVM_labels.append(target)
            if target not in all_labels:
                all_labels.append(target)
                all_colors.append(color)
                all_markers.append(marker)
                all_alpha.append(alpha)

        self.whole_labels = all_labels

        PointLabels = []
        PointColors = []
        x = []
        y = []


        title = 'K2O-SiO2diagram'
        self.setWindowTitle(title)
        self.textbox.setText(self.reference)


        k_1=(2.9-1.2)/(68-48)
        y_1= 1.2+ (85-48)*k_1
        y_0= 1.2+ (45-48)*k_1
        self.DrawLine([(45, y_0),(48, 1.2), (68,2.9),(85,y_1)])

        k_2=(1.2-0.3)/(68-48)
        y_2= 0.3+ (85-48)*k_2
        y_3= 0.3+ (45-48)*k_2
        self.DrawLine([(45, y_3),(48, 0.3), (68, 1.2),(85,y_2)])
        Labels=['High K','Medium K','Low K']
        Locations=[(80,5),(80,3),(80,1)]
        X_offset, Y_offset=0,0

        for k in range(len(Labels)):
            self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                               textcoords='offset points',
                               fontsize=9, color='grey', alpha=0.8)

        self.Check()

        if self.OutPutCheck==True:
            pass

        if (self._changed):
            df =  self.CleanDataFile(self._df)

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']


                TmpColor = ''
                if (df.at[i, 'Color'] in PointColors or df.at[i, 'Color'] == ''):
                    TmpColor = ''
                else:
                    PointColors.append(df.at[i, 'Color'])
                    TmpColor = df.at[i, 'Color']



                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = df.at[i, 'Label']

                xtest=df.at[i, 'SiO2']
                ytest=df.at[i, 'K2O']

                HitOnRegions = 0

                self.LabelList.append(Label)

                if 'Index' in self._df_back.columns.values:
                    self.IndexList.append(self._df_back.at[i, 'Index'])
                else:
                    self.IndexList.append('No ' + str(i + 1))


                for j in self.ItemNames:
                    if self.SelectDic[j].contains_point([xtest, ytest]):
                        HitOnRegions = 1
                        self.TypeList.append(j)
                        break
                if HitOnRegions == 0:
                    self.TypeList.append('on line or out')


                self.axes.scatter(df.at[i, 'SiO2'], df.at[i, 'K2O'], marker=df.at[i, 'Marker'],
                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel)




            XtoFit = {}
            YtoFit = {}

            SVM_X=[]
            SVM_Y=[]

            for i in  PointLabels:
                XtoFit[i]=[]
                YtoFit[i]=[]


            for i in range(len(df)):
                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = df.at[i, 'Label']

                xtest=df.at[i, 'SiO2']
                ytest=df.at[i, 'K2O']

                XtoFit[Label].append(xtest)
                YtoFit[Label].append(ytest)

                SVM_X.append(xtest)
                SVM_Y.append(ytest)

            if (self.shape_cb.isChecked()):
                for i in PointLabels:

                    if XtoFit[i] != YtoFit[i]:
                        xmin, xmax = min(XtoFit[i]), max(XtoFit[i])
                        ymin, ymax = min(YtoFit[i]), max(YtoFit[i])

                        DensityColorMap = 'Greys'
                        DensityAlpha = 0.1

                        DensityLineColor = PointColors[PointLabels.index(i)]
                        DensityLineAlpha = 0.3

                        # Peform the kernel density estimate
                        xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                        # print(self.ShapeGroups)
                        # command='''xx, yy = np.mgrid[xmin:xmax:'''+str(self.ShapeGroups)+ '''j, ymin:ymax:''' +str(self.ShapeGroups)+'''j]'''
                        # exec(command)
                        # print(xx, yy)
                        positions = np.vstack([xx.ravel(), yy.ravel()])
                        values = np.vstack([XtoFit[i], YtoFit[i]])
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
                            ## Or kernel density estimate plot instead of the contourf plot
                            # self.axes.imshow(np.rot90(f), cmap='Blues', extent=[xmin, xmax, ymin, ymax])
                            # Contour plot
                            cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                            # Label plot
                            #self.axes.clabel(cset, inline=1, fontsize=10)




            if (len(self.data_to_test) > 0):

                contained = True
                missing = 'Miss setting infor:'

                for i in ['Label', 'Color', 'Marker', 'Alpha']:
                    if i not in self.data_to_test.columns.values.tolist():
                        contained = False
                        missing = missing + '\n' + i

                if contained == True:
                    for i in self.data_to_test.columns.values.tolist():
                        if i not in self._df.columns.values.tolist():
                            self.data_to_test = self.data_to_test.drop(columns=i)

                    # print(self.data_to_test)

                    test_labels = []
                    test_colors = []
                    test_markers = []
                    test_alpha = []

                    for i in range(len(self.data_to_test)):

                        # print(self.data_to_test.at[i, 'Label'])
                        target = self.data_to_test.at[i, 'Label']
                        color = self.data_to_test.at[i, 'Color']
                        marker = self.data_to_test.at[i, 'Marker']
                        alpha = self.data_to_test.at[i, 'Alpha']

                        if target not in test_labels and target not in all_labels:
                            test_labels.append(target)
                            test_colors.append(color)
                            test_markers.append(marker)
                            test_alpha.append(alpha)

                    self.whole_labels = self.whole_labels + test_labels


                    self.load_settings_backup = self.data_to_test
                    Load_ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color',
                                        'Size',
                                        'Alpha',
                                        'Style', 'Width']
                    for i in self.data_to_test.columns.values.tolist():
                        if i not in Load_ItemsToTest:
                            self.load_settings_backup = self.load_settings_backup.drop(i, 1)

                    print(self.load_settings_backup, self.data_to_test)

                    print(self.load_settings_backup.shape, self.data_to_test.shape)


                    try:

                        for i in range(len(self.data_to_test)):

                            target = self.data_to_test.at[i, 'Label']
                            if target not in all_labels:
                                all_labels.append(target)
                                tmp_label = self.data_to_test.at[i, 'Label']
                            else:
                                tmp_label=''

                            x_load_test = self.data_to_test.at[i, 'SiO2']
                            y_load_test = self.data_to_test.at[i, 'K2O']

                            for j in self.ItemNames:
                                if self.SelectDic[j].contains_point([x_load_test, y_load_test]):
                                    self.LabelList.append(self.data_to_test.at[i, 'Label'])
                                    self.TypeList.append(j)
                                    break
                                pass

                            if (self.show_load_data_cb.isChecked()):

                                self.axes.scatter(self.data_to_test.at[i, 'SiO2'],self.data_to_test.at[i, 'K2O'],
                                                  marker=self.data_to_test.at[i, 'Marker'],
                                                  s=self.data_to_test.at[i, 'Size'],
                                                  color=self.data_to_test.at[i, 'Color'],
                                                  alpha=self.data_to_test.at[i, 'Alpha'],
                                                  label=tmp_label)




                    except Exception as e:
                        self.ErrorEvent(text=repr(e))


            if (self.legend_cb.isChecked()):
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


            self.All_X=SVM_X
            self.All_Y=SVM_Y

            if (self.hyperplane_cb.isChecked()):
                clf = svm.SVC(C=1.0, kernel='linear',probability= True)

                svm_x= SVM_X
                svm_y= SVM_Y

                print(len(svm_x),len(svm_y),len(df.index))

                xx, yy = np.meshgrid(np.arange(min(svm_x), max(svm_x), np.ptp(svm_x) / 500),
                                     np.arange(min(svm_y), max(svm_y), np.ptp(svm_y) / 500))

                le = LabelEncoder()
                le.fit(self._df.Label)
                class_label = le.transform(self._df.Label)
                svm_train= pd.concat([pd.DataFrame(svm_x),pd.DataFrame(svm_y)], axis=1)
                svm_train=svm_train.values
                clf.fit(svm_train,class_label)
                Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
                Z = Z.reshape(xx.shape)
                self.axes.contourf(xx, yy, Z, cmap='hot', alpha=0.2)


            if (self.show_data_index_cb.isChecked()):

                if 'Index' in self._df.columns.values:

                    for i in range(len(self._df)):
                        self.axes.annotate(self._df.at[i, 'Index'],
                                           xy=(self.All_X[i],
                                               self.All_Y[i]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
                else:
                    for i in range(len(self._df)):
                        self.axes.annotate('No' + str(i + 1),
                                           xy=(self.All_X[i],
                                               self.All_Y[i]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
            self.canvas.draw()





        self.OutPutTitle='K2OSiO2'

        self.OutPutData = pd.DataFrame(
            {'Label': self.LabelList,
             'Type': self.TypeList
             })

        #self.OutPutFig=self.fig


    def showPredictResultSelected(self):
        try:
            clf = svm.SVC(C=1.0, kernel='linear',probability= True)
            svm_x = self.All_X
            svm_y = self.All_Y

            le = LabelEncoder()
            le.fit(self._df.Label)
            class_label = le.transform(self._df.Label)
            svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y)], axis=1)
            svm_train = svm_train.values
            clf.fit(svm_train, self._df.Label)
            xx = self.data_to_test['SiO2']
            yy=[]
            for k in range(len(self.data_to_test)):
                tmp =self.data_to_test.at[k, 'Na2O'] + self.data_to_test.at[k,'K2O']
                yy.append(tmp)
                pass

            Z = clf.predict(np.c_[xx.ravel(), yy])
            Z2 = clf.predict_proba(np.c_[xx.ravel(), yy])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = self.SVM_labels
            predict_result = pd.concat(
                [self.load_settings_backup['Label'], pd.DataFrame({'SVM Classification': Z}), proba_df],
                axis=1).set_index('Label')
            print(predict_result)

            self.predictpop = TableViewer(df=predict_result, title='SVM Predict Result')
            self.predictpop.show()

            '''
            DataFileOutput, ok2 = QFileDialog.getSaveFileName(self, '文件保存', 'C:/',  'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出
            if (DataFileOutput != ''):
                if ('csv' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-4]
                    predict_result.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                    # self.result.to_csv(DataFileOutput + '.csv', sep=',', encoding='utf-8')
                elif ('xlsx' in DataFileOutput):
                    # DataFileOutput = DataFileOutput[0:-5]
                    predict_result.to_excel(DataFileOutput, encoding='utf-8')
                    # self.result.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')


            '''

        except Exception as e:
            msg = 'You need to load another data to run SVM.\n '
            self.ErrorEvent(text= msg +repr(e) )




    def Explain(self):

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData,title='K2OSiO2 Result')
        self.tablepop.show()