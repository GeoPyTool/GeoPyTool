from geopytool.ImportDependence import *
from geopytool.CustomClass import *

class Bivariate(AppForm):
    Lines = []
    Tags = []
    description = 'Bivariate diagram'
    usefulelements = ['SiO2',
                      'TiO2',
                      'Al2O3',
                      'TFe2O3',
                      'Fe2O3',
                      'FeO',
                      'TFe',
                      'MnO',
                      'MgO',
                      'CaO',
                      'Na2O',
                      'K2O',
                      'P2O5',
                      'Loi',
                      'DI',
                      'Mg#',
                      'Li',
                      'Be',
                      'Sc',
                      'V',
                      'Cr',
                      'Co',
                      'Ni',
                      'Cu',
                      'Zn',
                      'Ga',
                      'Ge',
                      'Rb',
                      'Sr',
                      'Y',
                      'Zr',
                      'Nb',
                      'Cs',
                      'Ba',
                      'La',
                      'Ce',
                      'Pr',
                      'Nd',
                      'Sm',
                      'Eu',
                      'Gd',
                      'Tb',
                      'Dy',
                      'Ho',
                      'Er',
                      'Tm',
                      'Yb',
                      'Lu',
                      'III',
                      'Ta',
                      'Pb',
                      'Th',
                      'U']
    unuseful = ['Name',
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
        self.setWindowTitle('Bivariate diagram')

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Bivariate')

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
        self.resize(800, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # self.axes.hold(False)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Bivariate)  # int

        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, len(self.items) - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Bivariate)  # int

        self.x_element_label = QLabel('X')

        self.logx_cb = QCheckBox('&Log')
        self.logx_cb.setChecked(False)
        self.logx_cb.stateChanged.connect(self.Bivariate)  # int

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, len(self.items) - 1)
        self.y_element.setValue(0)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Bivariate)  # int

        self.y_element_label = QLabel('Y')

        self.logy_cb = QCheckBox('&Log')
        self.logy_cb.setChecked(False)
        self.logy_cb.stateChanged.connect(self.Bivariate)  # int

        #
        # Layout with box sizers

        #
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        for w in [self.save_button,
                  self.legend_cb]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logx_cb, self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)

        for w in [self.logy_cb, self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Bivariate(self):

        self.WholeData = []

        raw = self._df

        a = int(self.x_element.value())

        b = int(self.y_element.value())

        self.axes.clear()

        self.axes.set_xlabel(self.items[a])
        self.x_element_label.setText(self.items[a])

        self.axes.set_ylabel(self.items[b])
        self.y_element_label.setText(self.items[b])

        PointLabels = []

        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']

            x, y = 0, 0
            xuse, yuse = 0, 0

            x, y = raw.at[i, self.items[a]], raw.at[i, self.items[b]]

            try:
                xuse = x
                yuse = y

                if (self.logx_cb.isChecked()):
                    xuse = math.log(x, 10)

                    self.axes.set_xlabel('$log10$ ' + self.items[a])

                if (self.logy_cb.isChecked()):
                    yuse = math.log(y, 10)

                    self.axes.set_ylabel('$log10$ ' + self.items[b])

                self.axes.scatter(xuse, yuse, marker=raw.at[i, 'Marker'],
                                  s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                  label=TmpLabel, edgecolors='black')
            except(ValueError):
                pass


        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()

