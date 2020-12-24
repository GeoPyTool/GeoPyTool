from ImportDependence import *
from CustomClass import *



class ZirconTiTemp(AppForm):
    reference = 'Ferry J M, Watson E B. New thermodynamic models and revised calibrations for the Ti-in-zircon and Zr-[J]. Contributions to Mineralogy & Petrology, 2007, 154(4):429-437.'
    Calced = ['Temperature']

    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Zircon Ti Temperature Calculator')

        self._df = df
        self.raw = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):


        self.resize(800, 600)
        self.main_frame = QWidget()
        self.dpi = 128

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, ]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def ZirconTiTemp(self):

        MaxTemps = []
        MinTemps = []
        MidTemps = []

        for i in range(len(self.raw)):
            Ti = self.raw.at[i, 'Ti']

            try:
                ASiO2 = self.raw.at[i, 'ASiO2']
            except(KeyError):
                ASiO2 = 1

            try:
                ATiO2 = self.raw.at[i, 'ATiO2']
            except(KeyError):
                ATiO2 = 1

            TiTemp1 = (4800 + 86) / ((5.711 + 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp2 = (4800 - 86) / ((5.711 + 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp3 = (4800 + 86) / ((5.711 - 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTemp4 = (4800 - 86) / ((5.711 - 0.072) - np.log10(Ti) - np.log10(ASiO2) + np.log10(ATiO2)) - 273.15

            TiTempBig, TiTempSmall = max([TiTemp1, TiTemp2, TiTemp3, TiTemp4]), min(
                ([TiTemp1, TiTemp2, TiTemp3, TiTemp4]))

            MaxTemps.append(TiTempBig)
            MinTemps.append(TiTempSmall)
            MidTemps.append((TiTempSmall + TiTempBig) / 2)

        tmpdata = {'Temp Max': MaxTemps, 'Temp Min': MinTemps, 'Temp Mid': MidTemps, }

        tmpdftoadd = pd.DataFrame(tmpdata)

        self.newdf = pd.concat([tmpdftoadd, self.raw], axis=1)
        self.model = PandasModel(self.newdf)
        self.tableView.setModel(self.model)

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


class RutileZrTemp(AppForm):
    reference = 'Ferry J M, Watson E B. New thermodynamic models and revised calibrations for the Ti-in-zircon and Zr-[J]. Contributions to Mineralogy & Petrology, 2007, 154(4):429-437.'
    Calced = ['Temperature']

    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Rutile Zr Temperature Calculator')

        self._df = df
        self.raw = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved')

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.resize(800, 600)
        self.main_frame = QWidget()
        self.dpi = 128

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, ]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def RutileZrTemp(self):

        MaxTemps = []
        MinTemps = []
        MidTemps = []

        for i in range(len(self.raw)):
            Zr = self.raw.at[i, 'Zr']

            try:
                ASiO2 = self.raw.at[i, 'ASiO2']
            except(KeyError):
                ASiO2 = 1

            ZrTemp1 = (4530 + 111) / ((7.42 + 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp2 = (4530 - 111) / ((7.42 + 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp3 = (4530 + 111) / ((7.42 - 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTemp4 = (4530 - 111) / ((7.42 - 0.105) - np.log10(Zr) - np.log10(ASiO2)) - 273.15

            ZrTempBig, ZrTempSmall = max([ZrTemp1, ZrTemp2, ZrTemp3, ZrTemp4]), min(
                ([ZrTemp1, ZrTemp2, ZrTemp3, ZrTemp4]))

            MaxTemps.append(ZrTempBig)
            MinTemps.append(ZrTempSmall)
            MidTemps.append((ZrTempSmall + ZrTempBig) / 2)

        tmpdata = {'Temp Max': MaxTemps, 'Temp Min': MinTemps, 'Temp Mid': MidTemps, }

        tmpdftoadd = pd.DataFrame(tmpdata)

        self.newdf = pd.concat([tmpdftoadd, self.raw], axis=1)
        self.model = PandasModel(self.newdf)
        self.tableView.setModel(self.model)

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

