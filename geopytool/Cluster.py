from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class Cluster(AppForm):
    Lines = []
    Tags = []
    description = 'Cluster diagram'
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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Cluster Data')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Cluster')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('Cluster Figure')

        self.fig = plt.figure(figsize=(8, 8))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.6, top=0.9)

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

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button]:
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

    def Cluster(self):

        self.WholeData = []





        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)






        dataframe2 = dataframe.T

        TmpDataFrame = dataframe
        TmpDataMatrix = TmpDataFrame.values

        #DistanceMatrix = euclidean_distances(TmpDataMatrix, TmpDataMatrix)
        #D=DistanceMatrix

        #self.model = PandasModel(self._df)
        #self.tableView.setModel(self.model)

        ax1 = self.fig.add_axes([0.3,0.75,0.5,0.1])


        corr1 = 1 - dataframe.corr()
        corr_condensed1 = hc.distance.squareform(corr1)  # convert to condensed
        z1 = hc.linkage(corr_condensed1, method='average')
        Z1 = hc.dendrogram(abs(z1),labels=corr1.columns)

        ax1.set_xticks([])
        ax1.set_yticks([])

        ax2 = self.fig.add_axes([0.09,0.1,0.15,0.6])

        # Compute and plot second dendrogram.

        corr2 = 1- dataframe2.corr()
        corr_condensed2 = hc.distance.squareform(corr2)  # convert to condensed
        z2 = hc.linkage(corr_condensed2, method='average')
        Z2 = hc.dendrogram(abs(z2),labels=corr2.columns,orientation='left')

        ax2.set_xticks([])
        ax2.set_yticks([])


        #Plot distance matrix.
        axmatrix = self.fig.add_axes([0.3, 0.1, 0.5, 0.6])
        idx1 = Z1['leaves']
        idx2 = Z2['leaves']

        done = np.ones(dataframe.shape)
        a = np.dot(done, corr1)

        b = np.dot(a.T, corr2)

        D = b.T

        D = D[idx2, :]
        D = D[:, idx1]
        im = axmatrix.matshow(D, aspect='auto', origin='lower', cmap='Greys')


        XLabelList = [corr1.columns[i] for i in idx1]
        YLabelList = [corr2.columns[i] for i in idx2]

        XstickList=[i for i in range(len(XLabelList))]
        YstickList=[i for i in range(len(YLabelList))]

        axmatrix.set_xticks(XstickList)
        axmatrix.set_xticklabels( XLabelList, minor=False)
        axmatrix.xaxis.set_label_position('top')
        axmatrix.xaxis.tick_top()

        axmatrix.set_yticks(YstickList)
        axmatrix.set_yticklabels( YLabelList, minor=False)
        axmatrix.yaxis.set_label_position('left')
        axmatrix.yaxis.tick_left()


        plt.xticks(rotation=-90, fontsize=6)
        plt.yticks(fontsize=6)

        axcolor1 = self.fig.add_axes([0.9, 0.1, 0.02, 0.6])

        # Plot colorbar.

        plt.colorbar(im, cax=axcolor1)

        self.canvas.draw()

    def Show(self):
        dataframe = self._df
        corr = 1 - dataframe.corr()

        try:
            corr_condensed = hc.distance.squareform(corr)  # convert to condensed

            z = hc.linkage(corr_condensed, method='average')

            dendrogram = hc.dendrogram(abs(z), labels=corr.columns)

            #self.axes.title('Cluster Diagram')


        except(ValueError):
            reply = QMessageBox.warning(self, 'Value Error',
                                        'Check Your Data and make sure it contains only numerical values.')
            pass
