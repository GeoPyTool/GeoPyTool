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
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('Cluster Figure')

        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveDataFile)

        # self.save_button.clicked.connect(self.saveImgFile)


        self.draw_button = QPushButton('&Show')
        self.draw_button.clicked.connect(self.Show)

        self.legend_cb = QCheckBox('&Horizontal')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Cluster)  # int

        self.slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.Cluster)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

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

        if (self.legend_cb.isChecked()):
            self.legend_cb.setText('&Horizontal')
        else:
            self.legend_cb.setText('&Vertical')

        self.WholeData = []

        self.axes.clear()

        dataframe = self._df

        ItemsAvalibale = self._df.columns.values.tolist()

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Label', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        self._df = dataframe

        self.model = PandasModel(self._df)
        self.tableView.setModel(self.model)

        PointLabels = []


        # self.canvas.draw()

    def Show(self):
        dataframe = self._df
        corr = 1 - dataframe.corr()

        try:
            corr_condensed = hc.distance.squareform(corr)  # convert to condensed

            z = hc.linkage(corr_condensed, method='average')

            dendrogram = hc.dendrogram(abs(z), labels=corr.columns)

            plt.title('Cluster Diagram')
            plt.show()

        except(ValueError):
            reply = QMessageBox.warning(self, 'Value Error',
                                        'Check Your Data and make sure it contains only numerical values.')
            pass
