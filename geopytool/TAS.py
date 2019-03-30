from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer


class TAS(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'

    itemstocheck = ['SiO2', 'K2O', 'Na2O']
    reference = 'Reference: Maitre, R. W. L., Streckeisen, A., Zanettin, B., Bas, M. J. L., Bonin, B., and Bateman, P., 2004, Igneous Rocks: A Classification and Glossary of Terms: Cambridge University Press, v. -1, no. 70, p. 93–120.'

    ItemNames = ['Foidolite',
                 'Peridotgabbro',
                 'Foid Gabbro',
                 'Foid Monzodiorite',
                 'Foid Monzosyenite',
                 'Foid Syenite',
                 'Gabbro Bs',
                 'Gabbro Ba',
                 'Monzogabbro',
                 'Monzodiorite',
                 'Monzonite',
                 'Syenite',
                 'Quartz Monzonite',
                 'Gabbroic Diorite',
                 'Diorite',
                 'Granodiorite',
                 'Granite',
                 'Quartzolite',
                 ]

    LocationAreas = [[[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]],
                     [[41, 0], [41, 3], [45, 3], [45, 0]],
                     [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]],
                     [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]],
                     [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]],
                     [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]],
                     [[45, 0], [45, 2], [52, 5], [52, 0]],
                     [[45, 2], [45, 5], [52, 5]],
                     [[45, 5], [49.4, 7.3], [52, 5]],
                     [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]],
                     [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]],
                     [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]],
                     [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]],
                     [[52, 0], [52, 5], [57, 5.9], [57, 0]],
                     [[57, 0], [57, 5.9], [63, 7], [63, 0]],
                     [[63, 0], [63, 7], [69, 8], [77.3, 0]],
                     [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]],
                     [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]],
                     ]

    AreasHeadClosed = []
    SelectDic = {}

    TypeList=[]

    RittmanList=[]

    All_X = []
    All_Y = []

    whole_labels=[]
    SVM_labels=[]

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
        self.legend_cb.stateChanged.connect(self.TAS)  # int


        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.TAS)  # int

        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.TAS)  # int

        self.irvine_cb = QCheckBox('&Irvine')
        self.irvine_cb.setChecked(True)
        self.irvine_cb.stateChanged.connect(self.TAS)  # int


        self.riedman_cb = QCheckBox('&Rittman')
        self.riedman_cb.setChecked(True)
        self.riedman_cb.stateChanged.connect(self.TAS)  # int


        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.TAS)  # int


        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.TAS)  # int


        self.slider_left_label = QLabel('Volcanic')
        self.slider_right_label = QLabel('Plutonic')

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1)
        self.slider.setValue(0)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        self.kernel_select = QSlider(Qt.Horizontal)
        self.kernel_select.setRange(0, len(self.kernel_list)-1)
        self.kernel_select.setValue(0)
        self.kernel_select.setTracking(True)
        self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        self.kernel_select.valueChanged.connect(self.TAS)  # int
        self.kernel_select_label = QLabel('Kernel')

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        for w in [self.load_data_button,self.save_button, self.result_button, self.save_predict_button_selected,self.slider_left_label, self.slider,self.slider_right_label]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.legend_cb,self.show_load_data_cb,self.show_data_index_cb,self.shape_cb,self.hyperplane_cb,self.kernel_select_label,self.kernel_select ,self.tag_cb,self.irvine_cb ]:
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


        self.slider_left_label.setFixedWidth(w/10)

        self.slider.setFixedWidth(w/10)

        self.slider_right_label.setFixedWidth(w/10)

    def Irvine(self,x, a = 39.0, b = 3.9492, c = -2.1111, d = 0.86096, e = -0.15188, f = 0.012030, g = -(3.3539 / 10000)):

        return(a+ b*np.power(x,1) +c*np.power(x,2) +d*np.power(x,3) +e*np.power(x,4) +f*np.power(x,5) +g*np.power(x,6))
        pass

    def Rittman(self,x=46,r_1=3.3,r_2=0):
        y_1= r_1*np.sqrt(x-43)
        y_2= r_2*np.sqrt(x-43)
        return(y_1,y_2)


    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
        self.TAS()


    def TAS(self, Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
            Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xlabel=r'$SiO_2 wt\%$', ylabel=r'$Na_2O + K_2O wt\%$', width=12,
            height=12, dpi=300):



        k_s = int(self.kernel_select.value())
        self.kernel_select_label.setText(self.kernel_list[k_s])


        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Plutonic (Wilson et al. 1989)')
        self.axes.clear()
        #self.axes.axis('off')

        self.FileName_Hint='TAS'
        
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')


        self.axes.set_xticks([30,40,50,60,70,80,90])
        self.axes.set_xticklabels([30,40,50,60,70,80,90])

        self.axes.set_yticks([0, 5, 10, 15, 20])
        self.axes.set_yticklabels([0, 5, 10, 15, 20])

        self.axes.set_ylim(bottom=0)



        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]


        self.OutPutData = pd.DataFrame()
        self.LabelList=[]
        self.IndexList=[]
        self.TypeList=[]
        self.RittmanList=[]



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


        YIrvine= np.arange(0,10.2,0.1)
        XIrvine= self.Irvine(YIrvine)


        PointLabels = []
        PointColors = []
        x = []
        y = []
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 5.2), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        X_offset = -6
        Y_offset = 3

        if (int(self.slider.value())==0):
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'S/N/L']
            title = 'TAS (total alkali–silica) diagram Volcanic (after Wilson et al. 1989).'
            description = '\n' \
                          'F: Foidite, Ph: Phonolite, Pc Pocrobasalt, U1: Tephrite (ol < 10%) Basanite(ol > 10%), U2: Phonotephrite, U3: Tephriphonolite,\n' \
                          'Ba: alkalic basalt,Bs: subalkalic baslt, S1: Trachybasalt, S2: Basaltic Trachyandesite, S3: Trachyandesite,\n' \
                          'O1: Basaltic Andesite, O2: Andesite, O3 Dacite, T: Trachyte , Td: Trachydacite , R: Rhyolite, Q: Silexite \n' \
                          'S/N/L: Sodalitite/Nephelinolith/Leucitolith'
            self.setWindowTitle(title)
            self.textbox.setText(self.reference+description)




        else:
            Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3',
                      u'T',
                      u'Td', u'R', u'Q', u'T/U/I']
            title = 'TAS (total alkali–silica) diagram Plutonic (after Wilson et al. 1989).'
            description = '\n' \
                          'F: Foidolite, Ph: Foid Syenite, Pc: Peridotgabbro, U1: Foid Gabbro, U2: Foid Monzodiorite, U3: Foid Monzosyenite,\n' \
                          'Ba: alkalic gabbro,Bs: subalkalic gabbro, S1: Monzogabbro, S2: Monzodiorite, S3: Monzonite,\n' \
                          'O1: Gabbroic Diorite, O2: Diorite, O3: Graodiorite, T: Syenite , Td: Quartz Monzonite , R: Granite, Q: Quartzolite \n' \
                          'T/U/I: Tawite/Urtite/Italite'


            self.setWindowTitle(title)
            self.textbox.setText(self.reference+description)


        TagNumber = min(len(Labels), len(Locations))
        if (self.tag_cb.isChecked()):
            for k in range(TagNumber):
                self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                                   textcoords='offset points',
                                   fontsize=9, color='grey', alpha=0.8)

        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])

        # self.DrawLine([(41.75, 1), (52.5, 5)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])

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
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = df.at[i, 'Label']

                xtest=df.at[i, 'SiO2']
                ytest=df.at[i, 'Na2O'] + df.at[i, 'K2O']



                for j in self.ItemNames:
                    if self.SelectDic[j].contains_point([xtest,ytest]):

                        self.LabelList.append(Label)
                        self.TypeList.append(j)

                        self.RittmanList.append(round( ytest**2/(xtest-43) + 0.001, 2))

                        if 'Index' in self._df_back.columns.values:
                            self.IndexList.append(self._df_back.at[i, 'Index'])
                        else:
                            self.IndexList.append('No ' + str(i))
                        break
                    pass


                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel)
                  #edgecolors='black')


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
                ytest=df.at[i, 'Na2O'] + df.at[i, 'K2O']

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


            if (self.irvine_cb.isChecked()):
                self.axes.plot(XIrvine, YIrvine,color= 'black', linewidth=1,
                           linestyle=':', alpha=0.6,label='Irvine, Barragar 1971\n')



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

                            x_load_test = self.data_to_test.at[i, 'SiO2']
                            y_load_test = self.data_to_test.at[i, 'Na2O'] + self.data_to_test.at[i, 'K2O']



                            for j in self.ItemNames:
                                if self.SelectDic[j].contains_point([x_load_test, y_load_test]):
                                    self.LabelList.append(self.data_to_test.at[i, 'Label'])
                                    self.TypeList.append(j)


                                    print(self.data_to_test.at[i, 'Label'],j)
                                    self.RittmanList.append(round(y_load_test ** 2 / (x_load_test - 43) + 0.001, 2))

                                    if 'Index' in self.data_to_test_back.columns.values:
                                        self.IndexList.append(self.data_to_test_back.at[i, 'Index'])
                                    else:
                                        self.IndexList.append('No '+str(i))
                                    break

                            if (self.show_load_data_cb.isChecked()):

                                self.axes.scatter(self.data_to_test.at[i, 'SiO2'], (
                                        self.data_to_test.at[i, 'Na2O'] + self.data_to_test.at[i, 'K2O']),
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





        self.OutPutTitle='TAS'

        self.OutPutData = pd.DataFrame(
            {'Label': self.LabelList,
             'Index':self.IndexList,
             'RockType': self.TypeList,
             'Rittman Index': self.RittmanList
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
            xx = self.data_to_test['SiO2']
            yy=[]
            for k in range(len(self.data_to_test)):
                tmp =self.data_to_test.at[k, 'Na2O'] + self.data_to_test.at[k,'K2O']
                yy.append(tmp)
                pass

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

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData,title='TAS Result')
        self.tablepop.show()