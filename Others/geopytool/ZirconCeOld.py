from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class ZirconCeOld(QMainWindow):
    _df = pd.DataFrame()
    _changed = False

    ylabel = r'Ln D $Zircon/Rock%$'
    reference = 'Ballard, J. R., Palin, M. J., and Campbell, I. H., 2002, Relative oxidation states of magmas inferred from Ce(IV)/Ce(III) in zircon: application to porphyry copper deposits of northern Chile: Contributions to Mineralogy and Petrology, v. 144, no. 3, p. 347-364.'

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Oxygen Fugacity Estimation by Ce(IV)/Ce(III) in Zircon (Ballard et al. 2002)')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

        self.raw = self._df

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()



        self.Base = 0
        self.Zircon = []
        self.Elements = []
        self.Elements3 = []
        self.Elements3_Plot_Only = []
        self.Elements4 = []
        self.x = []
        self.x3 = []
        self.x3_Plot_Only = []
        self.x4 = []
        self.y = []
        self.y3 = []
        self.y3_Plot_Only = []
        self.y4 = []
        self.z3 = []
        self.z4 = []
        self.xCe3 = []
        self.yCe3 = []
        self.xCe4 = []
        self.yCe4 = []
        self.Ce3test = []
        self.DCe3test = []
        self.Ce4test = []
        self.DCe4test = []
        self.Ce4_3_Ratio = []

        self.ZirconCe = []

        self.DataToWrite = [['First', 'Second', 'Third']]

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
        self.fig ,self.axes= plt.subplots(1, 2, figsize=(12.0, 12.0),dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.1, wspace=0.1,left=0.1, bottom=0.2, right=0.9, top=0.9)
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

        self.tablepop = TableViewer(df=self.newdf,title='Zircon Ce Result')
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

        xlabel = r'$(r_i/3+r_{Zr}/6)(r_i-r_{Zr})^2 $'
        ylabel = r'$\log_e D_{Zircon/Rock}$'

        self.axes[0].clear()
        self.axes[1].clear()

        self.axes[0].spines['right'].set_color('none')
        self.axes[0].spines['top'].set_color('none')

        self.axes[1].spines['right'].set_color('none')
        self.axes[1].spines['top'].set_color('none')

        self.axes[0].set_xlabel(xlabel)
        self.axes[0].set_ylabel(ylabel)
        self.axes[1].set_xlabel(xlabel)
        self.axes[1].set_ylabel(ylabel)


        self.raw = self._df

        self.RockCe = self.raw.at[4, 'Ce']

        self.a = self.raw.index.values.tolist()
        self.b = self.raw.columns.values.tolist()



        self.Base = 0
        self.Zircon = []
        self.Elements = []
        self.Elements3 = []
        self.Elements3_Plot_Only = []
        self.Elements4 = []
        self.x = []
        self.x3 = []
        self.x3_Plot_Only = []
        self.x4 = []
        self.y = []
        self.y3 = []
        self.y3_Plot_Only = []
        self.y4 = []
        self.z3 = []
        self.z4 = []
        self.xCe3 = []
        self.yCe3 = []
        self.xCe4 = []
        self.yCe4 = []
        self.Ce3test = []
        self.DCe3test = []
        self.Ce4test = []
        self.DCe4test = []
        self.Ce4_3_Ratio = []

        self.ZirconCe = []

        for i in range(len(self.raw)):
            if (self.raw.at[i, 'DataType'] == 'Base'):
                self.Base = i
            elif (self.raw.at[i, 'DataType'] == 'Zircon'):
                self.Zircon.append(i)

        for j in self.b:
            if (j == 'Ce'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.xCe3.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
            elif (j == 'Ce4'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 4):
                    self.xCe4.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))

            elif (self.raw.at[1, j] == 'yes'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements3.append(j)

                elif (self.raw.at[0, j] == 4):
                    self.x4.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements4.append(j)
                    self.Elements.append(j)

            elif (self.raw.at[1, j] == 'no'):
                ri = self.raw.at[2, j]
                ro = self.raw.at[3, j]
                if (self.raw.at[0, j] == 3):
                    self.x3_Plot_Only.append((ri / 3 + ro / 6) * (ri - ro) * (ri - ro))
                    self.Elements3_Plot_Only.append(j)
                    self.Elements.append(j)

        for i in self.Zircon:
            self.ZirconCe.append(self.raw.at[i, 'Ce'])
            tmpy3 = []
            tmpy4 = []
            tmpy3_Plot_Only = []

            for j in self.b:
                if (j == 'Ce'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe3.append(ytemp)
                elif (j == 'Ce4'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    self.yCe4.append(ytemp)
                elif (self.raw.at[1, j] == 'yes'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3.append(ytemp)

                    elif (self.raw.at[0, j] == 4):
                        tmpy4.append(ytemp)
                elif (self.raw.at[1, j] == 'no'):
                    ybase = self.raw.at[self.Base, j]
                    yi = self.raw.at[i, j]
                    ytemp = np.log(yi / ybase)
                    if (self.raw.at[0, j] == 3):
                        tmpy3_Plot_Only.append(ytemp)
            self.y3.append(tmpy3)
            self.y4.append(tmpy4)
            self.y3_Plot_Only.append(tmpy3_Plot_Only)

        for k in range(len(self.y3)):

            tmpz3 = np.polyfit(self.x3, self.y3[k], 1)
            self.z3.append(tmpz3)

            for i in range(len(self.x3)):
                x, y = self.x3[i], self.y3[k][i]

                self.axes[0].scatter(x, y, s=3, color='blue', alpha=0.5, label='', edgecolors='black')

            if k == 0:
                for i in range(len(self.x3)):
                    self.axes[0].annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]), fontsize=6, xytext=(16, 16),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z3:
            Xline3 = np.linspace(min(self.x3), max(max(self.x3_Plot_Only), max(self.x3)), 30)
            p3 = np.poly1d(i)
            Yline3 = p3(Xline3)

            self.axes[0].plot(Xline3, Yline3, 'b-',alpha=0.3)

            self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.RockCe))[0])
            self.DCe3test.append(np.power(np.e, p3(self.xCe3))[0])

        for k in range(len(self.yCe3)):

            x, y = self.xCe3, self.yCe3[k]

            self.axes[0].scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes[0].annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), fontsize=6, xytext=(16, 16),
                                    textcoords='offset points',
                                    ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=0.3),
                                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y3_Plot_Only)):

            for i in range(len(self.x3_Plot_Only)):
                x, y = self.x3_Plot_Only[i], self.y3_Plot_Only[k][i]
                self.axes[0].scatter(x, y, label='', s=3, color='blue', alpha=0.3)

            if k == 0:
                for i in range(len(self.x3_Plot_Only)):
                    self.axes[0].annotate(self.Elements3_Plot_Only[i], xy=(self.x3_Plot_Only[i], self.y3_Plot_Only[0][i]),
                                        fontsize=6,
                                        xytext=(-16*np.sqrt(2), 0),
                                        textcoords='offset points', ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.2', fc='green', alpha=0.2),
                                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y3)):

            tmpz3 = np.polyfit(self.x3, self.y3[k], 1)
            self.z3.append(tmpz3)

            for i in range(len(self.x3)):
                x, y = self.x3[i], self.y3[k][i]

                self.axes[0].scatter(x, y, label='', s=3, color='blue', alpha=0.3)

            if k == 0:
                for i in range(len(self.x3)):
                    self.axes[0].annotate(self.Elements3[i], xy=(self.x3[i], self.y3[0][i]), fontsize=6, xytext=(16, 16),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                                          # from geopytool.ZirconCe import ZirconCe
                                          arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z3:
            Xline3 = np.linspace(min(self.x3), max(max(self.x3_Plot_Only), max(self.x3)), 30)
            p3 = np.poly1d(i)
            Yline3 = p3(Xline3)
            self.axes[0].plot(Xline3, Yline3, 'b-',alpha=0.3)

            self.Ce3test.append(np.power(np.e, p3(self.xCe3) + np.log(self.RockCe))[0])
            self.DCe3test.append(np.power(np.e, p3(self.xCe3))[0])

        for k in range(len(self.yCe3)):

            x, y = self.xCe3, self.yCe3[k]
            self.axes[0].scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes[0].annotate('Ce3', xy=(self.xCe3[k], max(self.yCe3)), fontsize=6, xytext=(16, 16),
                                    textcoords='offset points',
                                    ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=0.3),
                                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for k in range(len(self.y4)):

            tmpz4 = np.polyfit(self.x4, self.y4[k], 1)
            self.z4.append(tmpz4)

            for i in range(len(self.x4)):
                x, y = self.x4[i], self.y4[k][i]
                self.axes[1].scatter(x, y, label='', s=3, color='r', alpha=0.5)

            if k == 0:
                for i in range(len(self.x4)):
                    self.axes[1].annotate(self.Elements4[i], xy=(self.x4[i], self.y4[0][i]), fontsize=6, xytext=(16, 16),
                                        textcoords='offset points',
                                        ha='right', va='bottom',
                                        bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                                        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        for i in self.z4:
            Xline4 = np.linspace(min(self.x4), max(self.x4), 30)
            p4 = np.poly1d(i)
            Yline4 = p4(Xline4)
            self.axes[1].plot(Xline4, Yline4, 'r-',alpha=0.3)

            self.Ce4test.append(np.power(np.e, p4(self.xCe4) + np.log(self.RockCe))[0])
            self.DCe4test.append(np.power(np.e, p4(self.xCe4))[0])

        for k in range(len(self.yCe4)):

            x, y = self.xCe4, self.yCe4[k]
            self.axes[1].scatter(x, y, label='', s=5, color='k', alpha=0.5)

            if k == 0:
                self.axes[1].annotate('Ce4', xy=(self.xCe4[k], max(self.yCe4)), fontsize=6, xytext=(16, 16),
                                    textcoords='offset points',
                                    ha='right',
                                    va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='red', alpha=0.3),
                                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        DataToWrite = [
            ['Zircon Sample Label', 'Zircon Ce4_3 Ratio', 'Melt Ce4_3 Ratio', 'DCe4', 'DCe3', 'DCe Zircon/Melt'], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], 'Label']
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])



        xlimleft3 = 0
        xlimleft4 = -0.005

        # print('\n the value is ', min(min(self.y3)))

        ylimleft3 = min(min(min(self.y3)), min(min(self.y3_Plot_Only)))

        ylimleft4 = min(min(min(self.y4)), min(min(self.yCe4), min(self.yCe3)))

        xlimright3 = 0.06
        xlimright4 = 0.03

        ylimright3 = max(max(self.y3))
        ylimright4 = max(max(self.y4))


        self.canvas.draw()

        self.DataToWrite = [
            ['Zircon Sample Label', 'Zircon Ce4_3 Ratio', 'Melt Ce4_3 Ratio', 'DCe4', 'DCe3', 'DCe Zircon/Melt'], ]

        for i in range(len(self.ZirconCe)):
            TMP = self.raw.at[self.Zircon[i], 'Label']
            ZirconTmp = (self.RockCe - self.ZirconCe[i] / self.DCe3test[i]) / (
                self.ZirconCe[i] / self.DCe4test[i] - self.RockCe)
            MeltTmp = (self.ZirconCe[i] - self.Ce3test[i]) / self.Ce3test[i] * self.DCe3test[i] / self.DCe4test[i]
            self.Ce4_3_Ratio.append(ZirconTmp)
            self.DataToWrite.append(
                [TMP, ZirconTmp, MeltTmp, self.DCe4test[i], self.DCe3test[i], self.ZirconCe[i] / self.RockCe])

        self.newdf = pd.DataFrame(self.DataToWrite)
        # print('\n')
        # print(self.newdf)


