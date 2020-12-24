from ImportDependence import *
from CustomClass import *
from QAPF import *

class TabelViewer(AppForm):
    addon = 'Name Author DataType Label Marker Color Size Alpha Style Width TOTAL total LOI loi'

    Minerals = ['Quartz',
                'Zircon',
                'K2SiO3',
                'Anorthite',
                'Na2SiO3',
                'Acmite',
                'Diopside',
                'Sphene',
                'Hypersthene',
                'Albite',
                'Orthoclase',
                'Wollastonite',
                'Olivine',
                'Perovskite',
                'Nepheline',
                'Leucite',
                'Larnite',
                'Kalsilite',
                'Apatite',
                'Halite',
                'Fluorite',
                'Anhydrite',
                'Thenardite',
                'Pyrite',
                'Magnesiochromite',
                'Chromite',
                'Ilmenite',
                'Calcite',
                'Na2CO3',
                'Corundum',
                'Rutile',
                'Magnetite',
                'Hematite',
                'Q',
                'A',
                'P',
                'F', ]

    Calced = ['Fe3+/(Total Fe) in rock',
              'Mg/(Mg+Total Fe) in rock',
              'Mg/(Mg+Fe2+) in rock',
              'Mg/(Mg+Fe2+) in silicates',
              'Ca/(Ca+Na) in rock',
              'Plagioclase An content',
              'Differentiation Index']
    DataWeight = {}
    DataVolume = {}
    DataBase = {}
    DataCalced = {}
    raw = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame(),title='Statistical Result'):
        QMainWindow.__init__(self, parent)
        self.setAcceptDrops(True)
        self.setWindowTitle(title)
        self.df = df
        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):

        self.resize(800, 600)
        self.main_frame = QWidget()

        self.save_button = QPushButton('&Save Result')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)


        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)
        self.vbox.addWidget(self.save_button)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)




    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            print(f)

    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出


        df = self.df
        if 'Label' in df.columns.values:
            df.set_index('Label', inplace=True)

        #self.model._df.reset_index(drop=True)


        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                df.to_excel(DataFileOutput, encoding='utf-8')
