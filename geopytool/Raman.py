from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer


class Raman(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'Raman Shift'
    ylabel = r'Raman Scatter Relative Strenth'

    itemstocheck = ['Shift', 'Strenth']
    reference = 'Yu, Q.-Y., Bagas, L., Yang, P.-H., Zhang, D., GeoPyTool: a cross-platform software solution for common geological calculations and plots, Geoscience Frontiers (2018), doi: 10.1016/j.gsf.2018.08.001..'

    xmin=0
    xmax=0
    Alpha=0.6

    PureColor = ['black', 'grey','red', 'green', 'blue', 'yellow', 'c']

    def __init__(self, parent=None, df=pd.DataFrame(),filename= '/'):
        QWidget.__init__(self, parent)


        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')
        self.FileName_Hint = ''
        self._df = df
        self.filename= filename

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')


        self.create_main_frame()
        self.create_status_bar()



    def create_main_frame(self):
        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.8, top=0.9)
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


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Raman)  # int


        self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        self.show_load_data_cb.setChecked(True)
        self.show_load_data_cb.stateChanged.connect(self.Raman)  # int

        self.show_data_peak_cb = QCheckBox('&Show Data Peak')
        self.show_data_peak_cb.setChecked(True)
        self.show_data_peak_cb.stateChanged.connect(self.Raman)  # int

        self.seter_alpha_label = QLabel('Alpha')
        self.seter_alpha = QLineEdit(self)
        self.seter_alpha.textChanged[str].connect(self.Raman)


        self.seter_label = QLabel('Threshold')
        self.seter = QLineEdit(self)
        self.seter.textChanged[str].connect(self.Raman)


        self.seter_Left_label = QLabel('Left')
        self.seter_Left = QLineEdit(self)
        self.seter_Left.textChanged[str].connect(self.Raman)
        self.seter_Right_label = QLabel('Right')
        self.seter_Right = QLineEdit(self)
        self.seter_Right.textChanged[str].connect(self.Raman)


        self.seter_Bottom_label = QLabel('Bottom')
        self.seter_Bottom = QLineEdit(self)
        self.seter_Bottom.textChanged[str].connect(self.Raman)
        self.seter_Top_label = QLabel('Top')
        self.seter_Top = QLineEdit(self)
        self.seter_Top.textChanged[str].connect(self.Raman)


        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()

        for w in [self.legend_cb,self.show_load_data_cb,self.show_data_peak_cb,self.seter_label,self.seter,self.seter_alpha_label,self.seter_alpha]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        for w in [self.load_data_button,self.save_button,self.seter_Left_label ,self.seter_Left,self.seter_Right_label ,self.seter_Right,self.seter_Bottom_label ,self.seter_Bottom,self.seter_Top_label ,self.seter_Top]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox1)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        w=self.width()
        h=self.height()

        self.seter.setFixedWidth(w / 20)
        self.seter_alpha.setFixedWidth(w / 20)
        self.seter_Left_label.setFixedWidth(w / 20)
        self.seter_Left.setFixedWidth(w / 20)
        self.seter_Right_label.setFixedWidth(w / 20)
        self.seter_Right.setFixedWidth(w / 20)
        self.seter_Bottom_label.setFixedWidth(w / 20)
        self.seter_Bottom.setFixedWidth(w / 20)
        self.seter_Top_label.setFixedWidth(w / 20)
        self.seter_Top.setFixedWidth(w / 20)


    def Raman(self):
        self.setWindowTitle('Raman  diagram ')
        self.axes.clear()
        #self.axes.axis('off')
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        ##self.axes.spines['top'].set_color('none')

        title = 'Raman Scatter Strenth / Shift'
        self.setWindowTitle(title)
        self.textbox.setText(self.reference)

        self.xmin=min(self._df.Shift)
        self.xmax=max(self._df.Shift)

        try:
            alpha = float(self.seter_alpha.text())
            # if( type(left) == int or type(left)== float or type(left)== np.float ):pass
            if 0<= alpha<=1:
                self.Alpha=alpha
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))




        self.axes.plot(self._df.Shift,self._df.Strength,label=self.getFileName([self.filename]),color=self.PureColor[0],alpha = self.Alpha)

        #print(sorted(self._df.Strength))



        if self.show_data_peak_cb.isChecked():
            try:
                threshold = float(self.seter.text())
                if 0< threshold <=1:
                    indexes, _ = find_peaks(self._df.Strength, prominence=max(self._df.Strength) * threshold)
                else:
                    indexes, _ = find_peaks(self._df.Strength,prominence=max(self._df.Strength) *0.03)
            except Exception as e:
                indexes, _ = find_peaks(self._df.Strength,prominence=max(self._df.Strength) *0.03)
            for i in indexes:
                pass
                self.axes.annotate(str(int(np.round(self._df.Shift[i]))), xy=(self._df.Shift[i], self._df.Strength[i]),rotation=45,color=self.PureColor[0],alpha = self.Alpha,fontsize=6, xytext=(16, 16),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.2', fc=self.PureColor[0], alpha=0.1),
                                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                self.axes.scatter(self._df.Shift[i], self._df.Strength[i],color=self.PureColor[0],alpha = self.Alpha)



        if (len(self.data_to_test) > 0):
            print('Loaded')

            for i in range(len(self.data_to_test)):

                if self.show_load_data_cb.isChecked():
                    self.axes.plot(self.data_to_test[i].Shift, self.data_to_test[i].Strength, label=self.getFileName([self.data_to_test_location[i]]),color=self.PureColor[i+1],alpha = self.Alpha)

                    self.xmin = min(self.xmin,min(self.data_to_test[i].Shift))
                    self.xmax = max(self.xmax,max(self.data_to_test[i].Shift))

                    if self.show_data_peak_cb.isChecked():
                        try:
                            threshold = float(self.seter.text())
                            if 0 < threshold <= 1:
                                load_indexes, _ = find_peaks(self.data_to_test[i].Strength, prominence=max(self.data_to_test[i].Strength) * threshold)
                            else:
                                load_indexes, _ = find_peaks(self.data_to_test[i].Strength, prominence=max(self.data_to_test[i].Strength) * 0.03)
                        except Exception as e:
                            load_indexes, _ = find_peaks(self.data_to_test[i].Strength, prominence=max(self.data_to_test[i].Strength) * 0.03)
                        for j in load_indexes:
                            pass
                            self.axes.annotate(str(int(np.round(self.data_to_test[i].Shift[j]))),
                                               xy=(self.data_to_test[i].Shift[j], self.data_to_test[i].Strength[j]),rotation=45, color=self.PureColor[i+1],
                                               alpha=self.Alpha, fontsize=6, xytext=(16, 16),
                                               textcoords='offset points',
                                               ha='right', va='bottom',
                                               bbox=dict(boxstyle='round,pad=0.2', fc=self.PureColor[i+1], alpha=0.1),
                                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                            self.axes.scatter(self.data_to_test[i].Shift[j], self.data_to_test[i].Strength[j], color= self.PureColor[i+1],
                                              alpha=self.Alpha)



        self.axes.set_xlim(left=self.xmin,right=self.xmax)


        try:
            left = float(self.seter_Left.text())
            # if( type(left) == int or type(left)== float or type(left)== np.float ):pass
            self.axes.set_xlim(left=left)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))

        try:
            right = float(self.seter_Right.text())
            self.axes.set_xlim(right=right)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))

        try:
            Bottom = float(self.seter_Bottom.text())
            # if( type(Bottom) == int or type(Bottom)== float or type(Bottom)== np.float ):pass
            self.axes.set_ylim(bottom=Bottom)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))

        try:
            Top = float(self.seter_Top.text())
            self.axes.set_ylim(top=Top)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()



    def loadDataToTest(self):
        TMP =self.getDataFiles()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
            self.data_to_test_location=TMP[1]
        self.Raman()

    def showPredictResultSelected(self):
        pass



    def Explain(self):

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData,title='Raman Result')
        self.tablepop.show()