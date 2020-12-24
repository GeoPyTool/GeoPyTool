from ImportDependence import *
from CustomClass import *
#from TableViewer import TableViewer



class ZrYSrTi(AppForm):
    _df = pd.DataFrame()
    _changed = False

    title= 'Zr, Ti, Y and Sr analyses of oceanic basalts'

    xlabel = r'ld1'
    ylabel = r'ld2'

    itemstocheck = ['Zr', 'Y', 'Sr','Ti']
    reference = 'Vermeesch, P. 2006, Tectonic discrimination diagrams revisited,Geochem. Geophys. Geosyst.,7, Q06017,doi:10.1029/2005GC001092\nButler, R., and A. Woronow (1986), Discrimination among tectonic settings using trace element abundances of basalts, J. Geophys. Res., 91, 10,289–10,300.'

    ItemNames = ['IAB',
                 'MORB',
                 'OIB',]

    '''
    [[-12, 4], [-12.23, -1.37], [-18, -6.6], [-8, -6.45],],
    [[5.02, -6.28], [12.17, -12.23], [15.9, -10.93], [11.85, -16],],

    '''

    LocationAreas = [ [[5.02,-6.28], [12.17, -12.23], [11.85, -16],[5.02,-16]],
                    [[5.02, -6.28], [12.17, -12.23], [15.9, -10.93], [15.9, -5],[5.02,-5]],
                    [[15.9, -10.93], [12.17, -12.23],[11.85, -16],[15.9,-16]],
                    ]

    AreasHeadClosed = []
    SelectDic = {}
    LabelList = []
    IndexList = []
    TypeList=[]


    All_X = []
    All_Y = []

    whole_labels=[]
    SVM_labels=[]

    Ti_TiO2_ratio_mass = 47.867 / (47.867 + 32)


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
        self.legend_cb.stateChanged.connect(self.Key_Func)  # int


        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Key_Func)  # int


        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.Key_Func)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Key_Func)  # int


        self.hyperplane_cb= QCheckBox('&SVM Boundary')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Key_Func)  # int


        self.kernel_select = QSlider(Qt.Horizontal)
        self.kernel_select.setRange(0, len(self.kernel_list)-1)
        self.kernel_select.setValue(0)
        self.kernel_select.setTracking(True)
        self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        self.kernel_select.valueChanged.connect(self.Key_Func)  # int
        self.kernel_select_label = QLabel('Kernel')

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        for w in [self.load_data_button,self.save_button, self.result_button, self.save_predict_button_selected,]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.legend_cb,self.show_load_data_cb,self.show_data_index_cb,self.shape_cb,self.hyperplane_cb,self.kernel_select_label,self.kernel_select ,self.detail_cb,]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)



        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference+    '''
            Use natural logarithms instead of base 10\n
            ld1= -0.016*np.log(Zr/Ti) - 2.961*np.log(Y/Ti) + 1.500*np.log(Sr/Ti)\n    
            ld2= -1.474*np.log(Zr/Ti) + 2.143*np.log(Y/Ti) + 1.840*np.log(Sr/Ti)
            ''')

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        w=self.width()
        h=self.height() 

    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.Key_Func()


    '''
    Use natural logarithms instead of base 10\n
    ld1= -0.016*np.log(Zr/Ti) - 2.961*np.log(Y/Ti) + 1.500*np.log(Sr/Ti)\n    
    ld2= -1.474*np.log(Zr/Ti) + 2.143*np.log(Y/Ti) + 1.840*np.log(Sr/Ti)
    '''
    

    def ld1(self,Zr=1,Y=1,Sr=1,Ti=1):
        return(-0.016*np.log(Zr/Ti) - 2.961*np.log(Y/Ti) + 1.500*np.log(Sr/Ti))

    def ld2(self,Zr=1,Y=1,Sr=1,Ti=1):
        return(-1.474*np.log(Zr/Ti) + 2.143*np.log(Y/Ti) + 1.840*np.log(Sr/Ti))

    def Key_Func(self, height=12, dpi=300):
        k_s = int(self.kernel_select.value())
        self.kernel_select_label.setText(self.kernel_list[k_s])
        self.setWindowTitle(self.title)
        self.axes.clear()
        #self.axes.axis('off')
        self.FileName_Hint= self.title        
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        #self.axes.spines['right'].set_color('none')
        #self.axes.spines['top'].set_color('none')

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        self.OutPutData = pd.DataFrame()

        self.LabelList=[]
        self.IndexList=[]
        self.TypeList=[]




        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

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
        
        Zr = []
        Ti = []
        Y = []
        Sr = []
        TiO2 = []

        ItemNames = ['IAB',
                'MORB',
                'OIB',]


        Locations = [(10, -8), (8, -14), (14, -14)]
        X_offset = -6
        Y_offset = 3

        TagNumber = min(len(self.ItemNames), len(Locations))
        if (self.detail_cb.isChecked()):
            for k in range(TagNumber):
                self.axes.annotate(self.ItemNames[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)

        self.DrawLine([(5.02, -6.28), (12.17, -12.23)])
        self.DrawLine([(12.17, -12.23), (11.85, -16)])
        self.DrawLine([(12.17, -12.23), (15.9, -10.93)])


        if (self._changed):
            df =  self.CleanDataFile(self._df)

            
            XtoFit = {}
            YtoFit = {}

            SVM_X=[]
            SVM_Y=[]

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] not in PointLabels or df.at[i, 'Label'] == ''):
                    PointLabels.append(df.at[i, 'Label'])

            for i in  PointLabels:
                XtoFit[i]=[]
                YtoFit[i]=[]

            TmpPointLabels=[]

            for i in range(len(df)):
                Zr_tmp = (df.at[i, 'Zr'])
                Y_tmp = (df.at[i, 'Y'])
                Sr_tmp = (df.at[i, 'Sr'])

                if 'TiO2' in df.columns.values.tolist():
                    tmp_data = df.at[i, 'TiO2']*self.Ti_TiO2_ratio_mass*10000
                    Ti_tmp = tmp_data
                elif 'Ti' in df.columns.values.tolist():
                    Ti_tmp = df.at[i, 'Ti']
                else:
                    Ti_tmp=0

                if Ti_tmp !=0:
                    pass
                    Zr.append(Zr_tmp)
                    Y.append(Y_tmp)
                    Sr.append(Sr_tmp)
                    Ti.append(Ti_tmp)

                    xtest= self.ld1(Zr_tmp,Y_tmp,Sr_tmp,Ti_tmp)
                    ytest= self.ld2(Zr_tmp,Y_tmp,Sr_tmp,Ti_tmp)


                    Alpha = df.at[i, 'Alpha']
                    Marker = df.at[i, 'Marker']
                    Label = df.at[i, 'Label']

                    TmpLabel = ''
                    if (df.at[i, 'Label'] in TmpPointLabels or df.at[i, 'Label'] == ''):
                        TmpLabel = ''
                    else:
                        TmpPointLabels.append(df.at[i, 'Label'])
                        TmpLabel = df.at[i, 'Label']

                    TmpColor = ''
                    if (df.at[i, 'Color'] in PointColors or df.at[i, 'Color'] == ''):
                        TmpColor = ''
                    else:
                        PointColors.append(df.at[i, 'Color'])
                        TmpColor = df.at[i, 'Color']

                    XtoFit[Label].append(xtest)
                    YtoFit[Label].append(ytest)

                    SVM_X.append(xtest)
                    SVM_Y.append(ytest)

                    HitOnRegions = 0

                    self.LabelList.append(Label)

                    if 'Index' in self._df_back.columns.values:
                        self.IndexList.append(self._df_back.at[i, 'Index'])
                    else:
                        self.IndexList.append('No ' + str(int(i+1)))


                    for j in self.ItemNames:
                        if self.SelectDic[j].contains_point([xtest,ytest]):
                            HitOnRegions = 1
                            self.TypeList.append(j)
                            break
                    if HitOnRegions == 0:
                        self.TypeList.append('on line or out')

                    self.axes.scatter(xtest, ytest, marker=df.at[i, 'Marker'],
                      s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel)
                      #edgecolors='black')





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
                self.data_to_test_back= self.data_to_test
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


                            Zr_tmp_to_test = (self.data_to_test.at[i, 'Zr'])
                            Y_tmp_to_test = (self.data_to_test.at[i, 'Y'])
                            Sr_tmp_to_test = (self.data_to_test.at[i, 'Sr'])

                            if 'TiO2' in self.data_to_test.columns.values.tolist():
                                tmp_data = self.data_to_test.at[i, 'TiO2']*self.Ti_TiO2_ratio_mass*10000
                                Ti_tmp_to_test = tmp_data
                            elif  'Ti' in self.data_to_test.columns.values.tolist():
                                Ti_tmp_to_test = self.data_to_test.at[i, 'Ti']
                            else:
                                Ti_tmp_to_test = 0

                            if Ti_tmp_to_test != 0:
                                x_load_test = self.ld1(Zr_tmp_to_test,Y_tmp_to_test,Sr_tmp_to_test,Ti_tmp_to_test)
                                y_load_test = self.ld2(Zr_tmp_to_test,Y_tmp_to_test,Sr_tmp_to_test,Ti_tmp_to_test)


                                for j in self.ItemNames:
                                    if self.SelectDic[j].contains_point([x_load_test, y_load_test]):
                                        self.LabelList.append(self.data_to_test.at[i, 'Label'])
                                        self.TypeList.append(j)


                                        print(self.data_to_test.at[i, 'Label'],j)

                                        if 'Index' in self.data_to_test_back.columns.values:
                                            self.IndexList.append(self.data_to_test_back.at[i, 'Index'])
                                        else:
                                            self.IndexList.append('No '+str(int(i+1)))
                                        break

                                if (self.show_load_data_cb.isChecked()):

                                    self.axes.scatter(x_load_test,y_load_test,
                                                      marker=self.data_to_test.at[i, 'Marker'],
                                                      s=self.data_to_test.at[i, 'Size'],
                                                      color=self.data_to_test.at[i, 'Color'],
                                                      alpha=self.data_to_test.at[i, 'Alpha'],
                                                      label=tmp_label)
                                                      #edgecolors='black')


                    except Exception as e:
                        self.ErrorEvent(text=repr(e))


            if (self.legend_cb.isChecked()):
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)


            self.All_X=SVM_X
            self.All_Y=SVM_Y

            if (self.hyperplane_cb.isChecked()):
                clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)

                svm_x= SVM_X
                svm_y= SVM_Y

                print(len(svm_x),len(svm_y),len(df.index))

                xx, yy = np.meshgrid(np.arange(min(svm_x), max(svm_x), np.ptp(svm_x) / 200),
                                     np.arange(min(svm_y), max(svm_y), np.ptp(svm_y) / 200))

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





        self.OutPutTitle='Key_Func'

        self.OutPutData = pd.DataFrame(
            {'Label': self.LabelList,
             'Index':self.IndexList,
             'Type': self.TypeList,
             })

        self.OutPutFig=self.fig


    def showPredictResultSelected(self):

        k_s = int(self.kernel_select.value())
        try:
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            svm_x = self.All_X
            svm_y = self.All_Y
            le = LabelEncoder()
            le.fit(self._df.Label)
            class_label = le.transform(self._df.Label)
            svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y)], axis=1)
            svm_train = svm_train.values
            clf.fit(svm_train, self._df.Label)


            xx=[]
            yy=[]


            for i in range(len(self.data_to_test)):

                Zr_tmp = (self.data_to_test.at[i, 'Zr'])
                Y_tmp = (self.data_to_test.at[i, 'Y'])
                Sr_tmp = (self.data_to_test.at[i, 'Sr'])

                if 'TiO2' in self.data_to_test.columns.values.tolist():
                    tmp_data = self.data_to_test.at[i, 'TiO2']*self.Ti_TiO2_ratio_mass*10000
                    Ti_tmp = tmp_data
                elif  'Ti' in self.data_to_test.columns.values.tolist():
                    Ti_tmp = self.data_to_test.at[i, 'Ti']
                else:
                    Ti_tmp =0


                if Ti_tmp != 0:
                    pass
                
                    xtest= self.ld1(Zr_tmp,Y_tmp,Sr_tmp,Ti_tmp)
                    ytest= self.ld2(Zr_tmp,Y_tmp,Sr_tmp,Ti_tmp)

                    xx.append(xtest)
                    yy.append(ytest)

            Z = clf.predict(np.c_[xx.ravel(), yy])
            Z2 = clf.predict_proba(np.c_[xx.ravel(), yy])

            for i in Z2:
                print(i)

            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_


            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})],
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
        # self.OutPutData = self.OutPutData.set_index('Label')
        self.tablepop = TableViewer(df=self.OutPutData, title='Key_Func Result')
        self.tablepop.show()

