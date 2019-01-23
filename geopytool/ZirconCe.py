from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class ZirconCe(QMainWindow):
    _df = pd.DataFrame()
    _changed = False



    xlabel = r'$(r_i/3+r_{Zr}/6)(r_i-r_{Zr})^2 $'
    ylabel = r'$\log_e D_{Zircon/Base}$'

    reference = 'Ballard, J. R., Palin, M. J., and Campbell, I. H., 2002, Relative oxidation states of magmas inferred from Ce(IV)/Ce(III) in zircon: application to porphyry copper deposits of northern Chile: Contributions to Mineralogy and Petrology, v. 144, no. 3, p. 347-364.'

    Elements3 = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    Elements4 = ['Th', 'U', 'Hf', 'Zr', 'Ce4']


    UsedElements3 = []
    UsedElements4 = []

    Ri3 = [1.16, 1.143, 1.126, 1.109, 1.079, 1.066, 1.053, 1.04, 1.027, 1.015, 1.004, 0.994, 0.985, 0.977]
    Ro3 = [0.84 for i in Ri3]

    Ri4 = [1.05,1.00 ,0.83 ,0.840,0.97 ]
    Ro4 = [0.84 for i in Ri4]

    ZirconZr = 497555

    x3=[]
    x4=[]

    Zircon = []
    ZirconCe=[]
    Ce3test = []
    DCe3test = []
    Ce4test = []
    DCe4test = []
    Ce4_3_Ratio = []

    xCe3 = 0.0479981
    xCe4 = 0.00788412

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Oxygen Fugacity Estimation by Ce(IV)/Ce(III) in Zircon (Ballard et al. 2002)')


        for i in range(len(self.Ri3)):
            self.x3.append((self.Ri3[i] / 3 + self.Ro3[i] / 6) * (self.Ri3[i] - self.Ro3[i]) * (self.Ri3[i] - self.Ro3[i]))

            if self.Elements3[i]=='Ce':
                self.xCe3=((self.Ri3[i] / 3 + self.Ro3[i] / 6) * (self.Ri3[i] - self.Ro3[i]) * (self.Ri3[i] - self.Ro3[i]))

        for i in range(len(self.Ri4)):
            self.x4.append((self.Ri4[i] / 3 + self.Ro4[i] / 6) * (self.Ri4[i] - self.Ro4[i]) * (self.Ri4[i] - self.Ro4[i]))
            if self.Elements3[i] == 'Ce4':
                self.xCe4=((self.Ri4[i] / 3 + self.Ro4[i] / 6) * (self.Ri4[i] - self.Ro4[i]) * (self.Ri4[i] - self.Ro4[i]))

        self._df = pd.DataFrame()
        self.raw = pd.DataFrame()

        self._df = df
        self.raw = df

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def save_plot(self):
        file_choices = 'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)'

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def create_main_frame(self):

        self.resize(1200, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig, self.axes = plt.subplots(1, 2, figsize=(12.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.1, wspace=0.1, left=0.1, bottom=0.2, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_img_button = QPushButton('&Save Figure')
        self.save_img_button.clicked.connect(self.saveImgFile)

        self.show_data_button = QPushButton('&Show Result')
        self.show_data_button.clicked.connect(self.showResult)

        self.save_data_button = QPushButton('&Save Result')
        self.save_data_button.clicked.connect(self.saveResult)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_img_button, self.show_data_button, self.save_data_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)

        self.vbox.addWidget(self.canvas)

        self.vbox.addLayout(self.hbox)

        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.textbox = QLineEdit(self)
        self.textbox.setText('Reference：' + '\n' + self.reference)
        self.statusBar().addWidget(self.textbox, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi=300)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.newdf.to_excel(DataFileOutput, encoding='utf-8')

    def showResult(self):

        self.tablepop = TableViewer(df=self.newdf, title='Zircon Ce4_3 Ratio Result')
        self.tablepop.show()

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal='triggered()'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


    def MultiBallard(self):

        self.axes[0].clear()
        self.axes[1].clear()

        self.axes[0].spines['right'].set_color('none')
        self.axes[0].spines['top'].set_color('none')

        self.axes[1].spines['right'].set_color('none')
        self.axes[1].spines['top'].set_color('none')

        self.axes[0].set_xlabel(self.xlabel)
        self.axes[0].set_ylabel(self.ylabel)
        self.axes[1].set_xlabel(self.xlabel)
        self.axes[1].set_ylabel(self.ylabel)






        self.items = self.raw.columns.values.tolist()

        self.rows = self.raw.index.values.tolist()

        DataX3=[]
        DataX4=[]

        Ybase3=[]
        Ybase4=[]


        self.Base = 0

        for i in range(len(self.raw)):
            if (self.raw.at[i, 'DataType'] == 'Base'):
                self.Base = i
                self.BaseCe = self.raw.at[i, 'Ce']
                self.BaseZr = self.raw.at[i, 'Zr']

            elif (self.raw.at[i, 'DataType'] == 'Zircon'):
                self.Zircon.append(i)


        for i in self.items:
            if i in self.Elements3:
                self.UsedElements3.append(i)
                DataX3.append(self.x3[self.Elements3.index(i)])
                Ybase3.append(self.raw.at[self.Base,i])

            elif i in self.Elements4:
                self.UsedElements4.append(i)
                DataX4.append(self.x4[self.Elements4.index(i)])
                Ybase4.append(self.raw.at[self.Base,i])




        #np.log(yi / ybase)



        print(self.rows)

        self.FittedData=[]



        print('\n DataX3 ',len(DataX3),'\n DataX4',len(DataX4))


        for i in self.rows:
            tmpy3 = []
            tmpy4 = []
            fittmpy3 = []
            fittmpy4 = []
            fitDataX3 = []
            fitDataX4 = []
            if i != self.Base:
                self.ZirconCe.append(self.raw.at[i, 'Ce'])


                for j in self.UsedElements3:
                    if len(tmpy3)<len(DataX3):
                        tmpy3.append(np.log(self.raw.at[i,j]/Ybase3[self.UsedElements3.index(j)]))
                for j in self.UsedElements4:
                    if len(tmpy4)<len(DataX4):
                        tmpy4.append(np.log(self.raw.at[i,j]/Ybase4[self.UsedElements4.index(j)]))


                print('\n y3 ', len(tmpy3), '\n y4', len(tmpy4))



                for q in self.UsedElements3:
                    if q != 'Ce':
                        fitDataX3.append(DataX3[self.UsedElements3.index(q)])
                        fittmpy3.append(tmpy3[self.UsedElements3.index(q)])

                for q in self.UsedElements4:
                    if q != 'Ce4':
                        fitDataX4.append(DataX4[self.UsedElements4.index(q)])
                        fittmpy4.append(tmpy4[self.UsedElements4.index(q)])


                print(len(fitDataX3), len(fittmpy3))
                print(len(fitDataX4), len(fittmpy4))

                tmpz3 = np.polyfit(fitDataX3, fittmpy3, 1)
                tmpz4 = np.polyfit(fitDataX4, fittmpy4, 1)



                Xline3 = np.linspace(min(fitDataX3), max(fitDataX3), 30)
                p3 = np.poly1d(tmpz3 )
                Yline3 = p3(Xline3)





                Xline4 = np.linspace(min(fitDataX4), max(fitDataX4), 30)
                p4 = np.poly1d(tmpz4 )
                Yline4 = p3(Xline4)




                self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.BaseCe)))
                self.DCe3test.append(np.power(np.e, p3(self.xCe3)))
                self.Ce4test.append(np.power(np.e, p4(self.xCe4) + np.log(self.BaseCe)))
                self.DCe4test.append(np.power(np.e, p4(self.xCe4)))



                self.axes[0].scatter(DataX3, tmpy3, s=3,color='blue', alpha=0.3, label='')
                self.axes[1].scatter(DataX4, tmpy4, s=3,color='red', alpha=0.3, label='')

                self.axes[0].plot(Xline3, Yline3, 'b-', alpha=0.3)
                self.axes[1].plot(Xline4, Yline4, 'r-', alpha=0.3)

                if i ==1:
                    for k in range(len(DataX3)):
                        self.axes[0].annotate(self.UsedElements3[k], xy=(DataX3[k], tmpy3[k]), fontsize=6, xytext=(16, 16),
                                              textcoords='offset points',
                                              ha='right', va='bottom',
                                              bbox=dict(boxstyle='round,pad=0.2', fc='blue', alpha=0.3),
                                              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
                    for k in range(len(DataX4)):
                        self.axes[1].annotate(self.UsedElements4[k], xy=(DataX4[k], tmpy4[k]), fontsize=6, xytext=(16, 16),
                                              textcoords='offset points',
                                              ha='right', va='bottom',
                                              bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=0.3),
                                              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

                tmpy3 = []
                tmpy4 = []
                fittmpy3 = []
                fittmpy4 = []
                fitDataX3 = []
                fitDataX4 = []
        self.canvas.draw()


        self.DataToWrite = [
            ['Zircon Sample Label', 'Zircon Ce4_3 Ratio', 'Melt Ce4_3 Ratio', 'DCe4', 'DCe3', 'DCe Zircon/Melt'], ]
        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], 'Label']
            ZirconTmp = (self.BaseCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                    self.ZirconCe[i] / self.DCe4test[i] - self.BaseCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[
                i]
            self.Ce4_3_Ratio.append(ZirconTmp)

            if len(self.DataToWrite) < len(DataX3):
                self.DataToWrite.append([TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.BaseCe])
        self.newdf = pd.DataFrame(self.DataToWrite)





