from ImportDependence import *
from CustomClass import *


class MyICA(AppForm):
    Lines = []
    Tags = []
    description = 'ICA'
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

    corr1 = pd.DataFrame()
    corr2 = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('ICA Data')

        self.items = []
        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to ICA')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()


    def showResultUp(self):

        self.tablepopUp = TableViewer(df=self.corr1, title='Correlation Matrix of Columns (Top Matrix)')
        self.tablepopUp.show()

    def showResultLeft(self):
        self.tablepopLeft = TableViewer(df=self.corr2, title='Correlation Matrix of Rows (Left Matrix)')
        self.tablepopLeft.show()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('ICA Figure')

        self.fig = plt.figure(figsize=(12, 12))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        #self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas

        #self.tableView = CustomQTableView(self.main_frame)
        #self.tableView.setObjectName('tableView')
        #self.tableView.setSortingEnabled(True)

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')

        # self.save_button.clicked.connect(self.saveDataFile)

        self.save_button.clicked.connect(self.saveImgFile)

        self.stat_button = QPushButton('&Stat')
        self.stat_button.clicked.connect(self.Stat)

        self.show_data_buttonUp = QPushButton('&Show Correlation Matrix of Columns (Top Matrix)')
        self.show_data_buttonUp.clicked.connect(self.showResultUp)
        self.show_data_buttonLeft = QPushButton('&Show Correlation Matrix of Rows (Left Matrix)')
        self.show_data_buttonLeft.clicked.connect(self.showResultLeft)


        self.ShowValue_cb = QCheckBox('&Value Off')
        self.ShowValue_cb.setChecked(False)
        self.ShowValue_cb.stateChanged.connect(self.ICA)  # int

        self.ShowCorr_cb = QCheckBox('&Show Correlation Matrix on Plot')
        self.ShowCorr_cb.setChecked(False)
        self.ShowCorr_cb.stateChanged.connect(self.ICA)  # int


        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button,self.stat_button, self.ShowCorr_cb,self.show_data_buttonLeft,self.show_data_buttonUp]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        #self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Read(self, inpoints):
        points = []
        for i in inpoints:
            points.append(i.split())

        result = []
        for i in points:
            for l in range(len(i)):
                a = float((i[l].split(','))[0])
                a = a * self.x_scale

                b = float((i[l].split(','))[1])
                b = (self.height_load - b) * self.y_scale

                result.append((a, b))
        return (result)

    def ICA(self):

        self.fig.clear()
        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df

        dataframe =  dataframe.dropna(axis=1,how='all')



        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)



        dataframe2 = dataframe.T

        if self.ShowCorr_cb.isChecked():

            axup = self.fig.add_axes([0.53, 0.88, 0.38, 0.1])

        else:

            axup = self.fig.add_axes([0.3, 0.75, 0.5, 0.1])


        corr1 = 1 - dataframe.corr()


        able =True

        try:
            corr_condensed1 = hc.distance.squareform(corr1)  # convert to condensed
        except:
            able =False
            pass


        if able == False:
            reply = QMessageBox.information(self,'Warning','Your Data Failed to ICA.\n Please remove Non Valued items and Blanks!')


        else:
            z1 = hc.linkage(corr_condensed1, method='average')
            Z1 = hc.dendrogram(abs(z1),labels=corr1.columns)

            axup.set_xticks([])
            axup.set_yticks([])

            if self.ShowCorr_cb.isChecked():
                axmatrixup = self.fig.add_axes([0.53, 0.49, 0.38, 0.38])

                imup = axmatrixup.matshow(corr1, aspect='auto', origin='lower', cmap='GnBu')

                axmatrixup.set_xticks([])
                axmatrixup.set_xticklabels([], minor=False,prop=fontprop)
                axmatrixup.xaxis.set_label_position('bottom')
                axmatrixup.xaxis.tick_bottom()

                axmatrixup.set_yticks([])
                axmatrixup.set_yticklabels([], minor=False,prop=fontprop)
                axmatrixup.yaxis.set_label_position('right')
                axmatrixup.yaxis.tick_right()

                axleft = self.fig.add_axes([0.0,0.1,0.13,0.38])

            else:

                axleft = self.fig.add_axes([0.09, 0.1, 0.15, 0.6])


            # Compute and plot second dendrogram.

            corr2 = 1- dataframe2.corr()
            corr_condensed2 = hc.distance.squareform(corr2)  # convert to condensed
            z2 = hc.linkage(corr_condensed2, method='average')
            Z2 = hc.dendrogram(abs(z2),labels=corr2.columns,orientation='left')

            axleft.set_xticks([])
            axleft.set_yticks([])

            if self.ShowCorr_cb.isChecked():
                axmatrixleft = self.fig.add_axes([0.14, 0.1, 0.38, 0.38])
                imleft = axmatrixleft.matshow(corr2, aspect='auto', origin='lower', cmap='GnBu')


                axmatrixleft.set_xticks([])
                axmatrixleft.set_xticklabels([], minor=False)
                axmatrixleft.xaxis.set_label_position('bottom')
                axmatrixleft.xaxis.tick_bottom()

                axmatrixleft.set_yticks([])
                axmatrixleft.set_yticklabels([], minor=False)
                axmatrixleft.yaxis.set_label_position('right')
                axmatrixleft.yaxis.tick_right()

                #Plot distance matrix.
                axmatrix = self.fig.add_axes([0.53, 0.1, 0.38, 0.38])

            else:
                axmatrix = self.fig.add_axes([0.3, 0.1, 0.5, 0.6])

            idx1 = Z1['leaves']
            idx2 = Z2['leaves']

            done = np.ones(dataframe.shape)
            a = np.dot(done, corr1)

            b = np.dot(a.T, corr2)

            D = b.T

            D = D[idx2, :]
            D = D[:, idx1]
            im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap='Blues')


            XLabelList = [corr1.columns[i] for i in idx1]
            YLabelList = [corr2.columns[i] for i in idx2]

            XstickList=[i for i in range(len(XLabelList))]
            YstickList=[i for i in range(len(YLabelList))]

            axmatrix.set_xticks(XstickList)
            axmatrix.set_xticklabels( XLabelList, minor=False)



            axmatrix.set_yticks(YstickList)
            axmatrix.set_yticklabels( YLabelList, minor=False)



            if self.ShowCorr_cb.isChecked():
                pass
                axmatrix.xaxis.set_label_position('bottom')
                axmatrix.xaxis.tick_bottom()
                axmatrix.yaxis.set_label_position('right')
                axmatrix.yaxis.tick_right()
            else:
                axmatrix.xaxis.set_label_position('top')
                axmatrix.xaxis.tick_top()
                axmatrix.yaxis.set_label_position('left')
                axmatrix.yaxis.tick_left()


            plt.xticks(rotation=-90, fontsize=6)
            plt.yticks(fontsize=6)

            #axcolor1 = self.fig.add_axes([0.3, 0.54, 0.02, 0.4])

            # Plot colorbar.

            #plt.colorbar(im, cax=axcolor1)




            '''
            if self.ShowValue_cb.isChecked():
                self.ShowValue_cb.setText('&Value On')
                for (j, i), label in np.ndenumerate(1-corr1):
                    axmatrixup.text(i, j, "%.2f" % label, ha='center', va='center')
                for (j, i), label in np.ndenumerate(1-corr2):
                    axmatrixleft.text(i, j, "%.2f" % label, ha='center', va='center')
                for (j, i), label in np.ndenumerate(D):
                    axmatrix.text(i, j, "%.2f" % label, ha='center', va='center')

            else:
                self.ShowValue_cb.setText('&Value Off')
                
            if self.ShowCorr_cb.isChecked():
                self.ShowCorr_cb.setText('&Hide Correlation Matrix')
            else:
                self.ShowCorr_cb.setText('&Show Correlation Matrix')
            
            '''


            self.corr1=1-corr1
            self.corr2=1-corr2

            self.canvas.draw()
            self.show()



    def Stat(self):

        df=self._df


        m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']
        for i in m:
            if i in df.columns.values:
                df = df.drop(i, 1)
        #df.set_index('Label', inplace=True)

        items = df.columns.values
        index = df.index.values

        StatResultDict = {}

        for i in items:
            StatResultDict[i] = self.stateval(df[i])

        StdSortedList = sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std'])

        StdSortedList.reverse()

        '''
        for k in sorted(StatResultDict.keys(), key=lambda x: StatResultDict[x]['std']):
            print("%s=%s" % (k, StatResultDict[k]))
        '''



        StatResultDf = pd.DataFrame.from_dict(StatResultDict, orient='index')
        StatResultDf['Items']=StatResultDf.index.tolist()

        self.tablepop = TableViewer(df=StatResultDf,title='Statistical Result')
        self.tablepop.show()

        self.Intro = StatResultDf
        return(StatResultDf)
