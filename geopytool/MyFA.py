from ImportDependence import *
from CustomClass import *


class MyFA(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'FA'
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
    switched = True
    text_result = ''
    whole_labels=[]
    fa = FactorAnalysis()
    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df

        self._df_back = df


        self.FileName_Hint='FA'


        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to FA')

        self.settings_backup = self._df
        ItemsToTest = ['Label','Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']
        for i in self._df.columns.values.tolist():
            if i not in ItemsToTest:
                self.settings_backup = self.settings_backup.drop(i, 1)
        print(self.settings_backup)


        self.result_to_fit= self.Slim(self._df)


        #print(self.result_to_fit.columns.values.tolist())

        try:
            self.fa.fit(self.result_to_fit.values)
            self.comp = (self.fa.components_)
            self.n = len(self.comp)

        except Exception as e:
            self.ErrorEvent(text=repr(e))
        self.create_main_frame()

    def create_main_frame(self):

        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)

        self.setWindowTitle('Factor Analysis')

        self.fig = plt.figure(figsize=(12, 6))
        #self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.2, bottom=0.3, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Key_Func)  # int

        self.lda_cb = QCheckBox('&LDA')
        self.lda_cb.setChecked(False)
        self.lda_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Key_Func)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Key_Func)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Key_Func)  # int


        self.hyperplane_cb= QCheckBox('&SVM')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Key_Func)  # int

        self.line_cb= QCheckBox('&Boundary Line')
        self.line_cb.setChecked(False)
        self.line_cb.stateChanged.connect(self.Key_Func)  # int

        self.run_MLP_button = QPushButton('&Run MLP')
        self.run_MLP_button.clicked.connect(self.runMLP)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_picture_button.clicked.connect(self.saveImgFile)

        self.save_result_button = QPushButton('&Show FA Result')
        self.save_result_button.clicked.connect(self.showResult)

        self.save_Para_button = QPushButton('&Show FA Para')
        self.save_Para_button.clicked.connect(self.showPara)

        self.save_predict_button = QPushButton('&Show Predict Result')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Load Data')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        self.switch_button = QPushButton('&Switch to 2D')
        self.switch_button.clicked.connect(self.switch)


        self.kernel_select = QSlider(Qt.Horizontal)
        self.kernel_select.setRange(0, len(self.kernel_list)-1)
        self.kernel_select.setValue(0)
        self.kernel_select.setTracking(True)
        self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        self.kernel_select.valueChanged.connect(self.Key_Func)  # int
        self.kernel_select_label = QLabel('Kernel')


        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, self.n - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Key_Func)  # int
        self.x_element_label = QLabel('component')

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, self.n - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Key_Func)  # int
        self.y_element_label = QLabel('component')

        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, self.n - 1)
        self.z_element.setValue(2)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.Key_Func)  # int
        self.z_element_label = QLabel('component')

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)

        for w in [self.switch_button,self.legend_cb, self.show_load_data_cb, self.show_data_index_cb, self.shape_cb, self.lda_cb ,self.hyperplane_cb,self.line_cb,self.kernel_select_label,self.kernel_select,self.run_MLP_button]:
            self.hbox0.addWidget(w)
            self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [ self.load_data_button, self.save_picture_button, self.save_result_button, self.save_Para_button, self.save_predict_button]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)
        for w in [self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)
        for w in [self.z_element_label,self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)

        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)


        if ( self.switched== False):

            self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.3, bottom=0.3, right=0.7, top=0.9)
            self.switch_button.setText('&Switch to 2D')
            self.axes = Axes3D(self.fig, elev=-150, azim=110)
            self.vbox.addLayout(self.hbox4)
        else:

            self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
            self.switch_button.setText('&Switch to 3D')
            self.axes = self.fig.add_subplot(111)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        #self.show()

    def switch(self):
        self.switched = not(self.switched)
        self.create_main_frame()
        self.Key_Func()


    def Key_Func(self):

        a = int(self.x_element.value())
        b = int(self.y_element.value())
        c = int(self.z_element.value())

        k_s = int(self.kernel_select.value())

        self.axes.clear()

        self.fa.fit(self.result_to_fit.values)
        self.comp = (self.fa.components_)


        #self.text_result='N Components :' + str(n)+'N Components :' + str(comp)+ '\nExplained Variance Ratio :' + str(evr)+'\nExplained Variance :' + str(ev)


        title=[]
        for i in range(len(self.comp)):
            title.append('Components No.'+ str(i+1))

        self.nvs = zip(title, self.comp)
        self.compdict = dict((title, self.comp) for title, self.comp in self.nvs)

        self.Para=pd.DataFrame(self.compdict)



        self.trained_result = self.fa.fit_transform(self.result_to_fit.values)

        self.comp = (self.fa.components_)
        #self.n = (self.fa.n_components_)

        self.n = len(self.comp)

        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]
        LDA_X=[]
        LDA_Label=[]

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

            LDA_X.append([self.trained_result[i, a],
                          self.trained_result[i, b]])
            LDA_Label.append(self._df.at[i, 'Label'])


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
                Load_ItemsToTest = ['Number', 'Tag', 'Type', 'Index', 'Name', 'Author', 'DataType', 'Marker', 'Color',
                                    'Size',
                                    'Alpha',
                                    'Style', 'Width']

                for i in self.data_to_test.columns.values.tolist():
                    if i not in Load_ItemsToTest:
                        self.load_settings_backup = self.load_settings_backup .drop(i, 1)

                #print(self.data_to_test_to_fit)
                #print(self.data_to_test_to_fit.shape)

                try:
                    self.trained_data_to_test = self.fa.transform(self.data_to_test_to_fit)


                    self.load_result = pd.concat([self.load_settings_backup,pd.DataFrame(self.trained_data_to_test)], axis=1)

                    for i in range(len(test_labels)):

                        if (self.show_load_data_cb.isChecked()):
                            if (self.switched == False):
                                self.axes.scatter(self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a],
                                                  self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b],
                                                  self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], c],
                                                  color=test_colors[i],
                                                  marker=test_markers[i],
                                                  label=test_labels[i],
                                                  alpha=test_alpha[i])

                            else:
                                self.axes.scatter(self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a],
                                                  self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b],
                                                  color=test_colors[i],
                                                  marker=test_markers[i],
                                                  label=test_labels[i],
                                                  alpha=test_alpha[i])


                                '''
                                if (self.shape_cb.isChecked()):
                                    pass
                                    XtoFit = self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a]
                                    YtoFit = self.trained_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b]
    
                                    xmin, xmax = min(XtoFit), max(XtoFit)
                                    ymin, ymax = min(YtoFit), max(YtoFit)
    
                                    DensityColorMap = 'Blues'
                                    DensityAlpha = 0.1
    
                                    DensityLineColor = test_colors[i]
                                    DensityLineAlpha = 0.1
                                    # Peform the kernel density estimate
                                    xx, yy = np.mgrid[xmin:xmax:2048j, ymin:ymax:2048j]
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


        self.kernel_select_label.setText(self.kernel_list[k_s])
        self.axes.set_xlabel("component no."+str(a+1))
        self.x_element_label.setText("component no."+str(a+1))

        self.axes.set_ylabel("component no."+str(b+1))
        self.y_element_label.setText("component no."+str(b+1))


        self.begin_result = pd.concat([self.settings_backup,pd.DataFrame(self.trained_result)], axis=1)

        for i in range(len(all_labels)):
            if (self.switched == False):

                self.axes.scatter(self.trained_result[self.result_to_fit.index == all_labels[i], a],
                                  self.trained_result[self.result_to_fit.index == all_labels[i], b],
                                  self.trained_result[self.result_to_fit.index == all_labels[i], c],
                                  color=all_colors[i],
                                  marker=all_markers[i],
                                  label=all_labels[i],
                                  alpha=all_alpha[i])

                self.axes.set_zlabel("component no." + str(c + 1))
                self.z_element_label.setText("component no." + str(c + 1))



            else:

                self.axes.scatter(self.trained_result[self.result_to_fit.index == all_labels[i], a],
                                  self.trained_result[self.result_to_fit.index == all_labels[i], b],
                                  color=all_colors[i],
                                  marker=all_markers[i],
                                  label=all_labels[i],
                                  alpha=all_alpha[i])



                if (self.shape_cb.isChecked()):
                    pass
                    XtoFit = self.trained_result[self.result_to_fit.index == all_labels[i], a]
                    YtoFit = self.trained_result[self.result_to_fit.index == all_labels[i], b]

                    xmin, xmax = min(XtoFit), max(XtoFit)
                    ymin, ymax = min(YtoFit), max(YtoFit)

                    DensityColorMap = 'Greys'
                    DensityAlpha = 0.1

                    DensityLineColor = all_colors[i]
                    DensityLineAlpha = 0.3
                    # Peform the kernel density estimate
                    xx, yy = np.mgrid[xmin:xmax:2048j, ymin:ymax:2048j]
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
                        if (self.legend_cb.isChecked()):
                            self.axes.clabel(cset, inline=1, fontsize=10)


        if (self.show_data_index_cb.isChecked()):
            for i in range(len(self.trained_result)):
                if (self.switched == True):

                    if 'Index' in self._df_back.columns.values:
                        self.axes.annotate(self._df_back.at[i, 'Index'],
                                           xy=(self.trained_result[i, a],
                                               self.trained_result[i, b]),
                                           color=self._df.at[i, 'Color'],
                                           alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes.annotate('No'+str(i+1),
                                       xy=(self.trained_result[i, a],
                                        self.trained_result[i, b]),
                                       color=self._df.at[i,'Color'],
                                       alpha=self._df.at[i,'Alpha'])
                else:

                    if 'Index' in self._df.columns.values:

                        self.axes.text(self.trained_result[i, a], self.trained_result[i, b],self.trained_result[i, c], self._df_back.at[i, 'Index'], size=self._df.at[i,'Size'], zorder=1,color=self._df.at[i,'Color'],
                                   alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes.text(self.trained_result[i, a], self.trained_result[i, b],self.trained_result[i, c], 'No'+str(i+1), size=self._df.at[i,'Size'], zorder=1,color=self._df.at[i,'Color'],
                                   alpha=self._df.at[i, 'Alpha'])




        if (self.hyperplane_cb.isChecked()):

            if (self.switched == False):
                clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability = True)
                svm_x = self.trained_result[:, a]
                svm_y = self.trained_result[:, b]
                svm_z = self.trained_result[:, c]
                xx, yy = np.meshgrid(np.arange( min(svm_x), max(svm_x), np.ptp(svm_x) / 100),
                                         np.arange( min(svm_y), max(svm_y), np.ptp(svm_y) / 100))

                xmin, xmax = self.axes.get_xlim()
                ymin, ymax = self.axes.get_ylim()
                xx, yy = np.mgrid[xmin:xmax:2048j, ymin:ymax:2048j]

                le = LabelEncoder()
                le.fit(self.result_to_fit.index)
                class_label = le.transform(self.result_to_fit.index)
                svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y), pd.DataFrame(svm_z)], axis=1)

                svm_train = svm_train.values

                if k_s==0:
                    # The equation of the separating plane is given by all x so that np.dot(svc.coef_[0], x) + b = 0.
                    zz = lambda x, y: (-clf.intercept_[0] - clf.coef_[0][0] * x - clf.coef_[0][1] * y) / clf.coef_[0][2]
                    clf.fit(svm_train, class_label)
                    self.axes.plot_surface(xx, yy, zz(xx,yy).reshape(xx.shape), color= 'grey', alpha=0.5)

            else:
                clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s],probability= True)
                svm_x = self.trained_result[:, a]
                svm_y = self.trained_result[:, b]


                xx, yy = np.meshgrid(np.arange( min(svm_x), max(svm_x), np.ptp(svm_x) / 100),
                                         np.arange( min(svm_y), max(svm_y), np.ptp(svm_y) / 100))

                xmin, xmax = self.axes.get_xlim()
                ymin, ymax = self.axes.get_ylim()
                xx, yy = np.mgrid[xmin:xmax:2048j, ymin:ymax:2048j]

                le = LabelEncoder()
                le.fit(self.result_to_fit.index)
                class_label=le.transform(self.result_to_fit.index)
                svm_train= pd.concat([pd.DataFrame(svm_x),pd.DataFrame(svm_y)], axis=1)

                svm_train=svm_train.values
                clf.fit(svm_train,class_label)
                Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
                Z = Z.reshape(xx.shape)
                #self.axes.contourf(xx, yy, Z, cmap=ListedColormap(self.color_list), alpha=0.2)

                CS = self.axes.contourf(xx, yy, Z.reshape(xx.shape), levels=len(self.color_list) + 1,
                                        cmap=ListedColormap(self.color_list), alpha=0.2)
                CS2 = self.axes.contour(CS, levels=CS.levels[::len(self.color_list)], colors='k', origin='lower',
                                        alpha=0)
                if (self.line_cb.isChecked()):
                    for l in CS2.allsegs:
                        if len(l) > 0:
                            a = np.array(l[0])
                            print(a)
                            x = a[:, 0]
                            y = a[:, 1]

                            self.axes.plot(x, y, color='red', alpha=0.3)
                            #self.axes.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='k', alpha=0.3)

                self.axes.set_xlim(xmin, xmax)
                self.axes.set_ylim(ymin, ymax)


        if (self.legend_cb.isChecked()):

            if (self.switched == False):
                    self.axes.legend(loc=2, prop=fontprop)
            else:
                self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)



        self.result = pd.concat([self.begin_result , self.load_result],sort=False, axis=0).set_index('Label')

        if (self.lda_cb.isChecked()):
            le = LabelEncoder()
            le.fit(LDA_Label)
            original_label = le.transform(LDA_Label)
            # print(self.result_to_fit.values.tolist())
            model = LinearDiscriminantAnalysis()
            model.fit(LDA_X, original_label)
            xmin, xmax = self.axes.get_xlim()
            ymin, ymax = self.axes.get_ylim()
            self.model = model
            self.cmap_trained_data = ListedColormap(self.color_list)
            #xx, yy = np.meshgrid(np.linspace(xmin, xmax, 200), np.linspace(ymin, ymax, 200))

            xx, yy = np.mgrid[xmin:xmax:2048j, ymin:ymax:2048j]
            Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
            #self.axes.contourf(xx, yy, Z.reshape(xx.shape), cmap=ListedColormap(self.color_list), alpha=0.2)

            CS = self.axes.contourf(xx, yy, Z.reshape(xx.shape), levels=len(self.color_list) + 1,
                                    cmap=ListedColormap(self.color_list), alpha=0.2)
            CS2 = self.axes.contour(CS, levels=CS.levels[::len(self.color_list)], colors='k', origin='lower',
                                    alpha=0)
            if (self.line_cb.isChecked()):
                for l in CS2.allsegs:
                    if len(l) > 0:
                        a = np.array(l[0])
                        print(a)
                        x = a[:, 0]
                        y = a[:, 1]
                        self.axes.plot(x, y, color='blue', alpha=0.3)
                        #self.axes.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='k', alpha=0.3)

            self.axes.set_xlim(xmin, xmax)
            self.axes.set_ylim(ymin, ymax)


        self.canvas.draw()

    def showPredictResult(self):


        k_s = int(self.kernel_select.value())

        try:
            clf = svm.SVC(C=1.0, kernel=self.kernel_list[k_s], probability=True)
            clf.fit(self.trained_result, self.result_to_fit.index)
            Z = clf.predict(np.c_[self.trained_data_to_test])

            Z2 = clf.predict_proba(np.c_[self.trained_data_to_test])
            proba_df = pd.DataFrame(Z2)
            proba_df.columns = clf.classes_

            proba_list = []
            for i in range(len(proba_df)):
                proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
            predict_result = pd.concat(
                [self.data_to_test['Label'], pd.DataFrame({'SVM Classification': Z}),
                 pd.DataFrame({'Confidence probability': proba_list}),proba_df],
                axis=1).set_index('Label')
            print(predict_result)

            #self.predictpop = TableViewer(df=predict_result, title='SVM Predict Result with All Items')
            self.predictpop = TableViewer(df=predict_result,
                                          title=self.description + ' SVM Predict Result with All Items')
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


    # def runMLP(self):
    #
    #     n = len(self.trained_result)
    #
    #     # n 是FA后得到的训练集的样本数
    #     # 用训练集中样本的维度作为输入层神经元个数
    #     # 用训练集中样本的类别标签数作为输出层神经元个数
    #     # m 是根据上面参考文献得到的经验公式，作为隐藏神经元层数
    #
    #     m = int((4 * n**2 + 3)/(n** 2 - 8))
    #     input_size = len(self.trained_result.T)
    #     output_size = len(set(self.result_to_fit.index))
    #     alpha= 2 # 2-10
    #
    #     # if (2<=m<=10):
    #     #     alpha = m  # 2-10
    #     # else:
    #     #     alpha = 5
    #     # n_h 是得到的隐藏层的每一层神经元个数
    #     n_h= int(n/(alpha*(input_size+output_size)))
    #
    #
    #     hidden_layer_tuple=(n_h,) * m
    #
    #     self.MLP = MLPClassifier(solver='lbfgs', alpha=1e-5,
    #                              hidden_layer_sizes=hidden_layer_tuple,
    #                              random_state=1)
    #
    #     try:
    #         self.MLP.fit(self.trained_result,self.result_to_fit.index )
    #         self.coefs_ = self.MLP.coefs_
    #         self.intercepts_ = self.MLP.intercepts_
    #         self.MLP_params = self.MLP.get_params(deep=True)
    #
    #     except Exception as e:
    #         self.ErrorEvent(text=repr(e))
    #
    #     Z = self.MLP.predict(self.trained_data_to_test)
    #
    #     Z2 = self.MLP.predict_proba(self.trained_data_to_test)
    #     proba_df = pd.DataFrame(Z2)
    #     proba_df.columns = self.MLP.classes_
    #
    #     proba_list = []
    #     for i in range(len(proba_df)):
    #         proba_list.append(round(max(proba_df.iloc[i]) + 0.001, 2))
    #     predict_result = pd.concat(
    #         [self.data_to_test['Label'], pd.DataFrame({'Classification': Z}),
    #          pd.DataFrame({'Confidence probability': proba_list})],
    #         axis=1)
    #     # print(predict_result)
    #
    #     self.predictpop = TableViewer(df=predict_result,
    #                                   title=self.description + 'Predict Result with All Items')
    #     self.predictpop.show()



    def Distance_Calculation(self):

        print(self.whole_labels)
        distance_result={}

        #distance_result[self.whole_labels[i]] = []

        print(distance_result)

        for i in range(len(self.whole_labels)):
            #print(self.whole_labels[i], self.trained_result[self.result_to_fit.index == self.whole_labels[i]][0])
            print( self.whole_labels[i], len(self.trained_result[self.result_to_fit.index == self.whole_labels[i]]))

            pass


        '''
        for i in range(len(self.whole_labels)):
            for j in range(len(self.whole_labels)):
                if i ==j:
                    pass
                else:
                    distance_result[self.whole_labels[i] + ' to ' + self.whole_labels[j]] = []

                    self.trained_result[self.result_to_fit.index == self.whole_labels[i]]

                    self.trained_result[self.result_to_fit.index == self.whole_labels[j]]

                    for m in range(len(self.trained_result[self.result_to_fit.index == self.whole_labels[i]])):
                        for n in range(len(self.trained_result[self.result_to_fit.index == self.whole_labels[j]])):
                            pass

                            self.trained_result[self.result_to_fit.index == self.whole_labels[i]][m]

                            #tmp_dist= self.Hsim_Distance(self.trained_result[self.result_to_fit.index == self.whole_labels[i]][m],self.trained_result[self.result_to_fit.index == self.whole_labels[j]][n])
                            #print(tmp_dist)
                            #distance_result[self.whole_labels[i] + ' to ' + self.whole_labels[j]].append(tmp_dist)
            pass
        
        '''


        #print(self.trained_result)

        try:
            self.trained_data_to_test[self.data_to_test_to_fit.index == self.whole_labels[0], 0]
        except Exception as e:
            pass
            # self.ErrorEvent(text=repr(e))
