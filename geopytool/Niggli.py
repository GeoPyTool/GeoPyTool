from geopytool.ImportDependence import *
from geopytool.CustomClass import *
from geopytool.QAPF import *

class Niggli(AppForm):
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
    DataBase = {'Quartz': [60.0843, 2.65],
                'Zircon': [183.3031, 4.56],
                'K2SiO3': [154.2803, 2.5],
                'Anorthite': [278.2093, 2.76],
                'Na2SiO3': [122.0632, 2.4],
                'Acmite': [462.0083, 3.6],
                'Diopside': [229.0691997, 3.354922069],
                'Sphene': [196.0625, 3.5],
                'Hypersthene': [112.9054997, 3.507622212],
                'Albite': [524.446, 2.62],
                'Orthoclase': [556.6631, 2.56],
                'Wollastonite': [116.1637, 2.86],
                'Olivine': [165.7266995, 3.68429065],
                'Perovskite': [135.9782, 4],
                'Nepheline': [284.1088, 2.56],
                'Leucite': [436.4945, 2.49],
                'Larnite': [172.2431, 3.27],
                'Kalsilite': [316.3259, 2.6],
                'Apatite': [493.3138, 3.2],
                'Halite': [66.44245, 2.17],
                'Fluorite': [94.0762, 3.18],
                'Anhydrite': [136.1376, 2.96],
                'Thenardite': [142.0371, 2.68],
                'Pyrite': [135.9664, 4.99],
                'Magnesiochromite': [192.2946, 4.43],
                'Chromite': [223.8366, 5.09],
                'Ilmenite': [151.7452, 4.75],
                'Calcite': [100.0892, 2.71],
                'Na2CO3': [105.9887, 2.53],
                'Corundum': [101.9613, 3.98],
                'Rutile': [79.8988, 4.2],
                'Magnetite': [231.5386, 5.2],
                'Hematite': [159.6922, 5.25]}
    BaseMass  = {'SiO2': 60.083,
                 'TiO2': 79.865,
                 'Al2O3': 101.960077,
                 'Fe2O3': 159.687,
                 'FeO': 71.844,
                 'MnO': 70.937044,
                 'MgO': 40.304,
                 'CaO': 56.077000000000005,
                 'Na2O': 61.978538560000004,
                 'K2O': 94.1956,
                 'P2O5': 141.942523996,
                 'CO2': 44.009,
                 'SO3': 80.057,
                 'S': 32.06,
                 'F': 18.998403163,
                 'Cl': 35.45,
                 'Sr': 87.62,
                 'Ba': 137.327,
                 'Ni': 58.6934,
                 'Cr': 51.9961,
                 'Zr': 91.224}

    CationNumber  = {'SiO2': 1,
                 'TiO2': 1,
                 'Al2O3': 2,
                 'Fe2O3': 2,
                 'FeO': 1,
                 'MnO': 1,
                 'MgO': 1,
                 'CaO': 1,
                 'Na2O': 2,
                 'K2O': 2,
                 'P2O5': 2,
                 'CO2': 1,
                 'SO3': 1,
                 'S': 0,
                 'F': 0,
                 'Cl': 0,
                 'Sr': 1,
                 'Ba': 1,
                 'Ni': 1,
                 'Cr': 1,
                 'Zr': 1}

    Elements  = ['SiO2',
                 'TiO2',
                 'Al2O3',
                 'Fe2O3',
                 'FeO',
                 'MnO',
                 'MgO',
                 'CaO',
                 'Na2O',
                 'K2O',
                 'P2O5',
                 'CO2',
                 'SO3',
                 'S',
                 'F',
                 'Cl',
                 'Sr',
                 'Ba',
                 'Ni',
                 'Cr',
                 'Zr']
    DataWeight = {}
    DataVolume = {}
    DataCalced = {}


    ResultMole  =[]
    ResultWeight=[]
    ResultVolume=[]
    ResultCalced=[]

    FinalResultMole = pd.DataFrame()
    FinalResultWeight = pd.DataFrame()
    FinalResultVolume = pd.DataFrame()
    FinalResultCalced = pd.DataFrame()

    raw = pd.DataFrame()

    DictList=[]

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Niggli Norm Result')


        self.FileName_Hint='Niggli'
        self._df = df
        #self.raw = df

        self.raw = self.CleanDataFile(self._df)


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



        self.qapf_button = QPushButton('&QAPF')
        self.qapf_button.clicked.connect(self.QAPF)


        '''
        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        '''


        self.tableViewMole = CustomQTableView(self.main_frame)
        self.tableViewMole.setObjectName('tableViewMole')
        self.tableViewMole.setSortingEnabled(True)

        self.tableViewWeight = CustomQTableView(self.main_frame)
        self.tableViewWeight.setObjectName('tableViewWeight')
        self.tableViewWeight.setSortingEnabled(True)

        self.tableViewVolume = CustomQTableView(self.main_frame)
        self.tableViewVolume.setObjectName('tableViewVolume')
        self.tableViewVolume.setSortingEnabled(True)

        self.tableViewCalced = CustomQTableView(self.main_frame)
        self.tableViewCalced.setObjectName('tableViewCalced')
        self.tableViewCalced.setSortingEnabled(True)
        #
        # Layout with box sizers
        #

        self.hbox = QHBoxLayout()

        for w in [self.qapf_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableViewMole)
        self.vbox.addWidget(self.tableViewWeight)
        self.vbox.addWidget(self.tableViewVolume)
        self.vbox.addWidget(self.tableViewCalced)
        self.vbox.addWidget(self.save_button)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


    def Niggli(self):
        self.ResultMole=[]
        self.ResultWeight=[]
        self.ResultVolume=[]
        self.ResultCalced=[]
        self.DictList=[]

        for i in range(len(self.raw)):
            tmpDict={}
            for j in self.raw.columns:
                tmpDict.update({j:self.raw.at[i,j]})

            TmpResult = self.singleCalc(m=tmpDict)
            TmpResultMole   = pd.DataFrame(TmpResult[0],index=[i])
            TmpResultWeight = pd.DataFrame(TmpResult[1],index=[i])
            TmpResultVolume = pd.DataFrame(TmpResult[2],index=[i])
            TmpResultCalced = pd.DataFrame(TmpResult[3],index=[i])


            self.ResultMole.append(TmpResultMole)
            self.ResultWeight.append(TmpResultWeight)
            self.ResultVolume.append(TmpResultVolume)
            self.ResultCalced.append(TmpResultCalced)

            self.DictList.append(tmpDict)

        self.useddf = pd.concat(self.ResultVolume)
        self.FinalResultMole = self.ReduceSize(pd.concat(self.ResultMole).set_index('Label'))
        self.FinalResultWeight = self.ReduceSize(pd.concat(self.ResultWeight).set_index('Label'))
        self.FinalResultVolume = self.ReduceSize(pd.concat(self.ResultVolume).set_index('Label'))
        self.FinalResultCalced = self.ReduceSize(pd.concat(self.ResultCalced).set_index('Label'))

        self.FinalResultMole = self.FinalResultMole.fillna(0)
        self.FinalResultWeight = self.FinalResultWeight.fillna(0)
        self.FinalResultVolume = self.FinalResultVolume.fillna(0)
        self.FinalResultCalced = self.FinalResultCalced.fillna(0)

        self.FinalResultMole = self.FinalResultMole.loc[:, (self.FinalResultMole != 0).any(axis=0)]
        self.FinalResultWeight = self.FinalResultWeight.loc[:, (self.FinalResultWeight != 0).any(axis=0)]
        self.FinalResultVolume = self.FinalResultVolume.loc[:, (self.FinalResultVolume != 0).any(axis=0)]
        self.FinalResultCalced = self.FinalResultCalced.loc[:, (self.FinalResultCalced != 0).any(axis=0)]




        self.newdf = self.FinalResultMole
        self.newdf1 = self.FinalResultWeight
        self.newdf2 = self.FinalResultVolume
        self.newdf3 = self.FinalResultCalced



        print(self.FinalResultVolume)

        #self.WholeResult = self.WholeResult.T.groupby(level=0).first().T

        #self.model = PandasModel(self.WholeResult)

        #self.model = PandasModel(self.FinalResultVolume)

        #self.model = PandasModel(self.useddf)
        self.modelMole = PandasModel(self.FinalResultMole)

        self.modelWeight= PandasModel(self.FinalResultWeight)

        self.modelVolume = PandasModel(self.FinalResultVolume)

        self.modelCalced = PandasModel(self.FinalResultCalced)


        #self.tableView.setModel(self.model)

        self.tableViewMole.setModel(self.modelMole)
        self.tableViewWeight.setModel(self.modelWeight)
        self.tableViewVolume.setModel(self.modelVolume)
        self.tableViewCalced.setModel(self.modelCalced)
        self.WholeResult = pd.concat([self.FinalResultMole,self.FinalResultWeight,self.FinalResultVolume,self.FinalResultCalced], axis=1,sort=False )
        self.OutPutData = self.WholeResult




    def singleCalc(self,
                   m={'Al2O3': 13.01, 'Alpha': 0.6, 'Ba': 188.0, 'Be': 0.85, 'CaO': 8.35, 'Ce': 28.2, 'Co': 45.2,
                      'Cr': 117.0, 'Cs': 0.83, 'Cu': 53.5, 'Dy': 5.58, 'Er': 2.96, 'Eu': 1.79, 'Fe2O3': 14.47,
                      'FeO': 5.51, 'Ga': 19.4, 'Gd': 5.24, 'Hf': 3.38, 'Ho': 1.1, 'K2O': 0.72, 'LOI': 5.05,
                      'La': 11.4, 'Label': 'ZhangSH2016', 'Li': 15.0, 'Lu': 0.39, 'Mg#': 41.9, 'MgO': 5.26,
                      'MnO': 0.21, 'Na2O': 1.88, 'Nb': 12.6, 'Nd': 18.4, 'Ni': 69.4, 'P2O5': 0.23, 'Pb': 3.17,
                      'Pr': 3.95, 'Rb': 18.4, 'Sc': 37.4, 'SiO2': 48.17, 'Size': 10, 'Sm': 5.08, 'Sr': 357,
                      'Ta': 0.77, 'Tb': 0.88, 'Th': 1.85, 'TiO2': 2.56, 'Tl': 0.06, 'Tm': 0.44, 'Total': 99.91,
                      'U': 0.41, 'V': 368.0, 'Y': 29.7, 'Yb': 2.68, 'Zn': 100.0, 'Zr': 130.0, }):

        DataResult={}
        DataWeight={}
        DataVolume={}
        DataCalced={}


        DataResult.update({'Label': m['Label']+' Mole%'})
        DataWeight.update({'Label': m['Label']+' Weight%'})
        DataVolume.update({'Label': m['Label']+' Volue%'})
        DataCalced.update({'Label': m['Label']})
        DataResult.update({'Width': m['Width']})
        DataWeight.update({'Width': m['Width']})
        DataVolume.update({'Width': m['Width']})
        DataCalced.update({'Width': m['Width']})
        DataResult.update({'Style': m['Style']})
        DataWeight.update({'Style': m['Style']})
        DataVolume.update({'Style': m['Style']})
        DataCalced.update({'Style': m['Style']})
        DataResult.update({'Alpha': m['Alpha']})
        DataWeight.update({'Alpha': m['Alpha']})
        DataVolume.update({'Alpha': m['Alpha']})
        DataCalced.update({'Alpha': m['Alpha']})
        DataResult.update({'Size': m['Size']})
        DataWeight.update({'Size': m['Size']})
        DataVolume.update({'Size': m['Size']})
        DataCalced.update({'Size': m['Size']})
        DataResult.update({'Color': m['Color']})
        DataWeight.update({'Color': m['Color']})
        DataVolume.update({'Color': m['Color']})
        DataCalced.update({'Color': m['Color']})
        DataResult.update({'Marker': m['Marker']})
        DataWeight.update({'Marker': m['Marker']})
        DataVolume.update({'Marker': m['Marker']})
        DataCalced.update({'Marker': m['Marker']})


        WholeCation = 0
        EachCation = {}

        for j in self.Elements:
            '''
            Get the Whole Cation  of the dataset
            '''

            try:
                T_TMP = m[j]
            except(KeyError):
                T_TMP = 0

            if j == 'Sr':
                TMP = T_TMP / (87.62 / 103.619 * 10000)
            elif j == 'Ba':
                TMP = T_TMP / (137.327 / 153.326 * 10000)
            elif j == 'Ni':
                TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)
            elif j == 'Cr':
                TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)
            elif j == 'Zr':
                # Zr Multi 2 here
                TMP = T_TMP / ((2 * 91.224) / 123.22200000000001 * 10000)
            else:
                TMP = T_TMP

            V = TMP * self.CationNumber[j] / self.BaseMass[j]
            try:
                WholeCation += float(V)
            except ValueError:
                pass

        print(WholeCation)


        for j in self.Elements:
            '''
            Get the Cation percentage of each element
            '''
            try:
                T_TMP = m[j]
            except(KeyError):
                T_TMP = 0

            if j == 'Sr':
                TMP = T_TMP / (87.62 / 103.619 * 10000)

            elif j == 'Ba':
                TMP = T_TMP / (137.327 / 153.326 * 10000)

            elif j == 'Ni':
                TMP = T_TMP / (58.6934 / 74.69239999999999 * 10000)

            elif j == 'Cr':
                TMP = T_TMP / ((2 * 51.9961) / 151.98919999999998 * 10000)

            elif j == 'Zr':
                # Zr not Multiple by 2 Here
                TMP = T_TMP / ((91.224) / 123.22200000000001 * 10000)

            else:
                TMP = T_TMP

            try:
                #C = TMP * self.CationNumber[j] / self.BaseMass[j] /WholeCation
                C = TMP  / self.BaseMass[j] /WholeCation
                print(C*100)
            except TypeError:
                pass

            EachCation.update({j: C})


        DataCalculating = EachCation

        Fe3 = DataCalculating['Fe2O3']
        Fe2 = DataCalculating['FeO']
        Mg = DataCalculating['MgO']
        Ca = DataCalculating['CaO']
        Na = DataCalculating['Na2O']

        try:
            DataCalced.update({'Fe3+/(Total Fe) in rock (Mole)': 100 * Fe3 * 2 / (Fe3 * 2 + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Fe3+/(Total Fe) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Mg/(Mg+Total Fe) in rock (Mole)': 100 * Mg / (Mg + Fe3 * 2 + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Mg/(Mg+Total Fe) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Mg/(Mg+Fe2+) in rock (Mole)': 100 * Mg / (Mg + Fe2)})
        except(ZeroDivisionError):
            DataCalced.update({'Mg/(Mg+Fe2+) in rock (Mole)': 0})
            pass

        try:
            DataCalced.update({'Ca/(Ca+Na) in rock (Mole)': 100 * Ca / (Ca + Na * 2)})
        except(ZeroDivisionError):
            DataCalced.update({'Ca/(Ca+Na) in rock (Mole)': 0})
            pass

        DataCalculating['CaO'] += DataCalculating['Sr']
        DataCalculating['Sr'] = 0

        DataCalculating['K2O'] += 2 * DataCalculating['Ba']
        DataCalculating['Ba'] = 0

        try:
            if DataCalculating['CaO'] >= 10 / 3 * DataCalculating['P2O5']:
                DataCalculating['CaO'] -= 10 / 3 * DataCalculating['P2O5']
            else:
                DataCalculating['CaO'] = 0
        except(ZeroDivisionError):
            pass

        DataCalculating['P2O5'] = DataCalculating['P2O5'] / 1.5

        Apatite = DataCalculating['P2O5']

        # IF(S19>=T15,S19-T15,0)

        if DataCalculating['F'] >= DataCalculating['P2O5']:
            DataCalculating['F'] -= DataCalculating['P2O5']
        else:
            DataCalculating['F'] = 0

        if DataCalculating['F'] >= DataCalculating['P2O5']:
            DataCalculating['F'] -= DataCalculating['P2O5']
        else:
            DataCalculating['F'] = 0

        if DataCalculating['Na2O'] >= DataCalculating['Cl']:
            DataCalculating['Na2O'] -= DataCalculating['Cl']
        else:
            DataCalculating['Na2O'] = 0

        Halite = DataCalculating['Cl']

        # IF(U12>=(U19/2),U12-(U19/2),0)
        if DataCalculating['CaO'] >= 0.5 * DataCalculating['F']:
            DataCalculating['CaO'] -= 0.5 * DataCalculating['F']
        else:
            DataCalculating['CaO'] = 0

        DataCalculating['F'] *= 0.5

        Fluorite = DataCalculating['F']

        # =IF(V17>0,IF(V13>=V17,'Thenardite',IF(V13>0,'Both','Anhydrite')),'None')
        AorT = 0
        if DataCalculating['SO3'] <= 0:
            AorT = 'None'
        else:
            if DataCalculating['Na2O'] >= DataCalculating['SO3']:
                AorT = 'Thenardite'
            else:
                if DataCalculating['Na2O'] > 0:
                    AorT = 'Both'
                else:
                    AorT = 'Anhydrite'

        # =IF(W26='Anhydrite',V17,IF(W26='Both',V12,0))
        # =IF(W26='Thenardite',V17,IF(W26='Both',V17-W17,0))

        if AorT == 'Anhydrite':
            DataCalculating['Sr'] = 0
        elif AorT == 'Thenardite':
            DataCalculating['Sr'] = DataCalculating['SO3']
            DataCalculating['SO3'] = 0
        elif AorT == 'Both':
            DataCalculating['Sr'] = DataCalculating['SO3'] - DataCalculating['CaO']
            DataCalculating['SO3'] = DataCalculating['CaO']
        else:
            DataCalculating['SO3'] = 0
            DataCalculating['Sr'] = 0

        DataCalculating['CaO'] -= DataCalculating['SO3']

        DataCalculating['Na2O'] -= DataCalculating['Sr']

        Anhydrite = DataCalculating['SO3']
        Thenardite = DataCalculating['Sr']

        Pyrite = 0.5 * DataCalculating['S']

        # =IF(W9>=(W18*0.5),W9-(W18*0.5),0)

        if DataCalculating['FeO'] >= DataCalculating['S'] * 0.5:
            DataCalculating['FeO'] -= DataCalculating['S'] * 0.5
        else:
            DataCalculating['FeO'] = 0

        # =IF(X24>0,IF(X9>=X24,'Chromite',IF(X9>0,'Both','Magnesiochromite')),'None')

        if DataCalculating['Cr'] > 0:
            if DataCalculating['FeO'] >= DataCalculating['Cr']:
                CorM = 'Chromite'
            elif DataCalculating['FeO'] > 0:
                CorM = 'Both'
            else:
                CorM = 'Magnesiochromite'
        else:
            CorM = 'None'

        # =IF(Y26='Chromite',X24,IF(Y26='Both',X9,0))
        # =IF(Y26='Magnesiochromite',X24,IF(Y26='Both',X24-Y24,0))

        if CorM == 'Chromite':
            DataCalculating['Cr'] = DataCalculating['Cr']
            DataCalculating['Ni'] = 0

        elif CorM == 'Magnesiochromite':
            DataCalculating['Ni'] = DataCalculating['Cr']
            DataCalculating['Cr'] = 0

        elif CorM == 'Both':
            DataCalculating['Ni'] = DataCalculating['Cr'] - DataCalculating['FeO']
            DataCalculating['Cr'] = DataCalculating['FeO']

        else:
            DataCalculating['Cr'] = 0
            DataCalculating['Ni'] = 0

        DataCalculating['MgO'] -= DataCalculating['Ni']

        Magnesiochromite = DataCalculating['Ni']
        Chromite = DataCalculating['Cr']

        # =IF(X9>=Y24,X9-Y24,0)

        if DataCalculating['FeO'] >= DataCalculating['Cr']:
            DataCalculating['FeO'] -= DataCalculating['Cr']
        else:
            DataCalculating['FeO'] = 0

        # =IF(Y6>0,IF(Y9>=Y6,'Ilmenite',IF(Y9>0,'Both','Sphene')),'None')

        if DataCalculating['TiO2'] < 0:
            IorS = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['TiO2']:
                IorS = 'Ilmenite'
            else:
                if DataCalculating['FeO'] > 0:
                    IorS = 'Both'
                else:
                    IorS = 'Sphene'

        # =IF(Z26='Ilmenite',Y6,IF(Z26='Both',Y9,0))
        # =IF(Z26='Sphene',Y6,IF(Z26='Both',Y6-Z6,0))

        if IorS == 'Ilmenite':
            DataCalculating['TiO2'] = DataCalculating['TiO2']
            DataCalculating['MnO'] = 0

        elif IorS == 'Sphene':
            DataCalculating['MnO'] = DataCalculating['TiO2']
            DataCalculating['TiO2'] = 0

        elif IorS == 'Both':

            DataCalculating['MnO'] = DataCalculating['TiO2'] - DataCalculating['FeO']
            DataCalculating['TiO2'] = DataCalculating['FeO']

        else:
            DataCalculating['TiO2'] = 0
            DataCalculating['MnO'] = 0

        DataCalculating['FeO'] -= DataCalculating['TiO2']

        Ilmenite = DataCalculating['TiO2']

        # =IF(Z16>0,IF(Z12>=Z16,'Calcite',IF(Z12>0,'Both','Na2CO3')),'None')

        if DataCalculating['CO2'] <= 0:
            CorN = 'None'
        else:
            if DataCalculating['CaO'] >= DataCalculating['CO2']:
                CorN = 'Calcite'
            else:
                if DataCalculating['CaO'] > 0:
                    CorN = 'Both'
                else:
                    CorN = 'Na2CO3'

        # =IF(AA26='Calcite',Z16,IF(AA26='Both',Z12,0))

        # =IF(AA26='Na2CO3',Z16,IF(AA26='Both',Z16-AA16,0))

        if CorN == 'None':
            DataCalculating['CO2'] = 0
            DataCalculating['SO3'] = 0

        elif CorN == 'Calcite':
            DataCalculating['CO2'] = DataCalculating['CO2']
            DataCalculating['SO3'] = 0

        elif CorN == 'Na2CO3':
            DataCalculating['SO3'] = DataCalculating['SO3']
            DataCalculating['CO2'] = 0

        elif CorN == 'Both':
            DataCalculating['SO3'] = DataCalculating['CO2'] - DataCalculating['CaO']
            DataCalculating['CO2'] = DataCalculating['CaO']

        DataCalculating['CaO'] -= DataCalculating['CO2']

        Calcite = DataCalculating['CO2']

        Na2CO3 = DataCalculating['SO3']

        # =IF(AA17>Z13,0,Z13-AA17)
        if DataCalculating['SO3'] > DataCalculating['Na2O']:
            DataCalculating['Na2O'] = 0
        else:
            DataCalculating['Na2O'] -= DataCalculating['SO3']

        DataCalculating['SiO2'] -= DataCalculating['Zr']
        Zircon = DataCalculating['Zr']

        # =IF(AB14>0,IF(AB7>=AB14,'Orthoclase',IF(AB7>0,'Both','K2SiO3')),'None')

        if DataCalculating['K2O'] <= 0:
            OorK = 'None'
        else:
            if DataCalculating['Al2O3'] >= DataCalculating['K2O']:
                OorK = 'Orthoclase'
            else:
                if DataCalculating['Al2O3'] > 0:
                    OorK = 'Both'
                else:
                    OorK = 'K2SiO3'

        # =IF(AC26='Orthoclase',AB14,IF(AC26='Both',AB7,0))
        # =IF(AC26='K2SiO3',AB14,IF(AC26='Both',AB14-AB7,0))

        if OorK == 'None':
            DataCalculating['K2O'] = 0
            DataCalculating['P2O5'] = 0


        elif OorK == 'Orthoclase':
            DataCalculating['K2O'] = DataCalculating['K2O']
            DataCalculating['P2O5'] = 0


        elif OorK == 'K2SiO3':
            DataCalculating['P2O5'] = DataCalculating['K2O']
            DataCalculating['K2O'] = 0



        elif OorK == 'Both':

            DataCalculating['P2O5'] = DataCalculating['K2O'] - DataCalculating['Al2O3']
            DataCalculating['K2O'] = DataCalculating['Al2O3']

        DataCalculating['Al2O3'] -= DataCalculating['K2O']

        # =IF(AC13>0,IF(AC7>=AC13,'Albite',IF(AC7>0,'Both','Na2SiO3')),'None')

        if DataCalculating['Na2O'] <= 0:
            AorN = 'None'
        else:
            if DataCalculating['Al2O3'] >= DataCalculating['Na2O']:
                AorN = 'Albite'
            else:
                if DataCalculating['Al2O3'] > 0:
                    AorN = 'Both'
                else:
                    AorN = 'Na2SiO3'

        # =IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)

        if DataCalculating['Al2O3'] >= DataCalculating['Na2O'] and DataCalculating['Al2O3'] > 0:
            DataCalculating['Al2O3'] -= DataCalculating['Na2O']
        else:
            DataCalculating['Al2O3'] = 0

        # =IF(AD26='Albite',AC13,IF(AD26='Both',AC7,0))
        # =IF(AD26='Na2SiO3',AC13,IF(AD26='Both',AC13-AD13,0))

        if AorN == 'Albite':
            DataCalculating['Cl'] = 0

        elif AorN == 'Both':
            DataCalculating['Cl'] = DataCalculating['Na2O'] - DataCalculating['Al2O3']
            DataCalculating['Na2O'] = DataCalculating['Al2O3']

        elif AorN == 'Na2SiO3':
            DataCalculating['Cl'] = DataCalculating['Na2O']
            DataCalculating['Na2O'] = 0

        elif AorN == 'None':
            DataCalculating['Na2O'] = 0
            DataCalculating['Cl'] = 0

        # =IF(AD7>0,IF(AD12>0,'Anorthite','None'),'None')

        '''
        Seem like should be =IF(AD7>0,IF(AD12>AD7,'Anorthite','Corundum'),'None')

        If Al2O3 is left after alloting orthoclase and albite, then:
        Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
        If Al2O3 exceeds CaO in the preceding calculation, then:
        Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
        Corundum = Al2O3, CaO =0, Al2O3 = 0


            if DataCalculating['Al2O3']<=0:
                AorC='None'
            else:
                if DataCalculating['CaO']>DataCalculating['Al2O3']:
                    AorC= 'Anorthite'
                else:
                    Aorc='Corundum'

        '''
        AorC = 'None'
        if DataCalculating['Al2O3'] <= 0:
            AorC = 'None'
        else:
            if DataCalculating['CaO'] > 0:
                AorC = 'Anorthite'
            else:
                Aorc = 'None'

        # =IF(AE26='Anorthite',IF(AD12>AD7,0,AD7-AD12),AD7)

        # =IF(AE26='Anorthite',IF(AD7>AD12,0,AD12-AD7),AD12)

        # =IF(AE26='Anorthite',IF(AD7>AD12,AD12,AD7),0)

        if AorC == 'Anorthite':
            if DataCalculating['Al2O3'] >= DataCalculating['CaO']:
                DataCalculating['Sr'] = DataCalculating['CaO']
                DataCalculating['Al2O3'] -= DataCalculating['CaO']
                DataCalculating['CaO'] = 0

            else:
                DataCalculating['Sr'] = DataCalculating['Al2O3']
                DataCalculating['CaO'] -= DataCalculating['Al2O3']
                DataCalculating['Al2O3'] = 0

        else:
            DataCalculating['Sr'] = 0

        Corundum = DataCalculating['Al2O3']
        Anorthite = DataCalculating['Sr']

        # =IF(AE10>0,IF(AE12>=AE10,'Sphene',IF(AE12>0,'Both','Rutile')),'None')

        if DataCalculating['MnO'] <= 0:
            SorR = 'None'
        else:
            if DataCalculating['CaO'] >= DataCalculating['MnO']:
                SorR = 'Sphene'
            elif DataCalculating['CaO'] > 0:
                SorR = 'Both'
            else:
                SorR = 'Rutile'

        # =IF(AF26='Sphene',AE10,IF(AF26='Both',AE12,0))

        # =IF(AF26='Rutile',AE10,IF(AF26='Both',AE10-AE12,0))

        if SorR == 'Sphene':
            DataCalculating['MnO'] = DataCalculating['MnO']
            DataCalculating['S'] = 0

        elif SorR == 'Rutile':
            DataCalculating['S'] = DataCalculating['MnO']
            DataCalculating['MnO'] = 0


        elif SorR == 'Both':
            DataCalculating['S'] = DataCalculating['MnO'] - DataCalculating['CaO']
            DataCalculating['MnO'] = DataCalculating['CaO']

        elif SorR == 'None':
            DataCalculating['MnO'] = 0
            DataCalculating['S'] = 0

        DataCalculating['CaO'] -= DataCalculating['MnO']

        Rutile = DataCalculating['S']

        # =IF(AND(AF20>0),IF(AF8>=AF20,'Acmite',IF(AF8>0,'Both','Na2SiO3')),'None')

        if DataCalculating['Cl'] <= 0:
            ACorN = 'None'
        else:
            if DataCalculating['Fe2O3'] >= DataCalculating['Cl']:
                ACorN = 'Acmite'
            else:
                if DataCalculating['Fe2O3'] > 0:
                    ACorN = 'Both'
                else:
                    ACorN = 'Na2SiO3'

        # =IF(AG26='Acmite',AF20,IF(AG26='Both',AF8,0))

        # =IF(AG26='Na2SiO3',AF20,IF(AG26='Both',AF20-AG19,0))

        if ACorN == 'Acmite':
            DataCalculating['F'] = DataCalculating['Cl']
            DataCalculating['Cl'] = 0

        elif ACorN == 'Na2SiO3':
            DataCalculating['Cl'] = DataCalculating['Cl']
            DataCalculating['F'] = 0

        elif ACorN == 'Both':
            DataCalculating['F'] = DataCalculating['Fe2O3']
            DataCalculating['Cl'] = DataCalculating['Cl'] - DataCalculating['F']

        elif ACorN == 'None':
            DataCalculating['F'] = 0
            DataCalculating['Cl'] = 0

        DataCalculating['Fe2O3'] -= DataCalculating['F']

        Acmite = DataCalculating['F']

        # =IF(AG8>0,IF(AG9>=AG8,'Magnetite',IF(AG9>0,'Both','Hematite')),'None')

        if DataCalculating['Fe2O3'] <= 0:
            MorH = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['Fe2O3']:
                MorH = 'Magnetite'
            else:
                if DataCalculating['FeO'] > 0:
                    MorH = 'Both'
                else:
                    MorH = 'Hematite'

        # =IF(AH26='Magnetite',AG8,IF(AH26='Both',AG9,0))
        # =IF(AH26='Hematite',AG8,IF(AH26='Both',AG8-AG9,0))

        if MorH == 'Magnetite':
            DataCalculating['Fe2O3'] = DataCalculating['Fe2O3']
            DataCalculating['Ba'] = 0

        elif MorH == 'Hematite':
            DataCalculating['Fe2O3'] = 0
            DataCalculating['Ba'] = DataCalculating['FeO']


        elif MorH == 'Both':
            DataCalculating['Fe2O3'] = DataCalculating['FeO']
            DataCalculating['Ba'] = DataCalculating['Fe2O3'] - DataCalculating['FeO']


        elif MorH == 'None':
            DataCalculating['Fe2O3'] = 0
            DataCalculating['Ba'] == 0

        DataCalculating['FeO'] -= DataCalculating['Fe2O3']

        Magnetite = DataCalculating['Fe2O3']
        Hematite = DataCalculating['Ba']

        # =IF(AH11>0,AH11/(AH11+AH9),0)

        Fe2 = DataCalculating['FeO']
        Mg = DataCalculating['MgO']

        if Mg > 0:
            DataCalced.update({'Mg/(Mg+Fe2+) in silicates': 100 * Mg / (Mg + Fe2)})
        else:
            DataCalced.update({'Mg/(Mg+Fe2+) in silicates': 0})

        DataCalculating['FeO'] += DataCalculating['MgO']

        DataCalculating['MgO'] = 0

        # =IF(AI12>0,IF(AI9>=AI12,'Diopside',IF(AI9>0,'Both','Wollastonite')),'None')

        if DataCalculating['CaO'] <= 0:
            DorW = 'None'
        else:
            if DataCalculating['FeO'] >= DataCalculating['CaO']:
                DorW = 'Diopside'
            else:
                if DataCalculating['FeO'] > 0:
                    DorW = 'Both'
                else:
                    DorW = 'Wollastonite'

        # =IF(AJ26='Diopside',AI12,IF(AJ26='Both',AI9,0))

        # =IF(AJ26='Wollastonite',AI12,IF(AJ26='Both',AI12-AI9,0))

        if DorW == 'Diopside':
            DataCalculating['CaO'] = DataCalculating['CaO']
            DataCalculating['S'] = 0

        elif DorW == 'Wollastonite':
            DataCalculating['S'] = DataCalculating['CaO']
            DataCalculating['CaO'] = 0

        elif DorW == 'Both':
            DataCalculating['S'] = DataCalculating['CaO'] - DataCalculating['FeO']
            DataCalculating['CaO'] = DataCalculating['FeO']

        elif DorW == 'None':
            DataCalculating['CaO'] = 0
            DataCalculating['S'] = 0

        DataCalculating['FeO'] -= DataCalculating['CaO']

        Diopside = DataCalculating['CaO']

        Quartz = DataCalculating['SiO2']

        Zircon = DataCalculating['Zr']
        K2SiO3 = DataCalculating['P2O5']

        Na2SiO3 = DataCalculating['Cl']

        Sphene = DataCalculating['MnO']

        Hypersthene = DataCalculating['FeO']

        Albite = DataCalculating['Na2O']

        Orthoclase = DataCalculating['K2O']

        Wollastonite = DataCalculating['S']

        # =AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)

        Quartz = Quartz -(Zircon +
                   K2SiO3 +
                   Anorthite * 2 +
                   Na2SiO3 +
                   Acmite * 4 +
                   Diopside * 2 +
                   Sphene +
                   Hypersthene +
                   Albite * 6 +
                   Orthoclase * 6 +
                   Wollastonite)

        # =IF(AL5>0,AL5,0)

        #if Quartz > 0:
        #    Quartz = Quartz
        #else:
        #    Quartz = 0

        # =IF(AL13>0,IF(AL5>=0,'Hypersthene',IF(AL13+(2*AL5)>0,'Both','Olivine')),'None')

        if Hypersthene <= 0:
            HorO = 'None'
        else:
            if Quartz > 0:
                HorO = 'Hypersthene'
            else:
                if Hypersthene + 2 * Quartz > 0:
                    HorO = 'Both'
                else:
                    HorO = 'Olivine'

        # =IF(AN26='Hypersthene',AL13,IF(AN26='Both',AL13+(2*AL5),0))
        # =IF(AN26='Olivine',AL13*0.5,IF(AN26='Both',ABS(AL5),0))
        Old_Hypersthene = Hypersthene
        if HorO == 'Hypersthene':
            Hypersthene = Hypersthene
            Olivine = 0

        elif HorO == 'Both':
            Hypersthene = Hypersthene + Quartz * 2
            Olivine = abs(Quartz)

        elif HorO == 'Olivine':
            Olivine = Hypersthene / 2
            Hypersthene = 0

        elif HorO == 'None':
            Hypersthene = 0
            Olivine = 0

        # =AL5+AL13-(AN13+AN17)
        Quartz =  Quartz + Old_Hypersthene - (Hypersthene + Olivine)

        # =IF(AL12>0,IF(AN5>=0,'Sphene',IF(AL12+AN5>0,'Both','Perovskite')),'None')

        if Sphene <= 0:
            SorP = 'None'
        else:
            if Quartz >= 0:
                SorP = 'Sphene'
            else:
                if Sphene + Quartz > 0:
                    SorP = 'Both'
                else:
                    SorP = 'Perovskite'

        # =IF(AO26='Sphene',AL12,IF(AO26='Both',AL12+AN5,0))
        # =IF(AO26='Perovskite',AL12,IF(AO26='Both',AL12-AO12,0))

        Old_Sphene = Sphene

        if SorP == 'Sphene':
            Sphene = Sphene
            Perovskite = 0

        elif SorP == 'Perovskite':
            Perovskite = Sphene
            Sphene = 0

        elif SorP == 'Both':
            Sphene += Quartz
            Perovskite = Old_Sphene - Sphene

        elif SorP == 'None':
            Sphene = 0
            Perovskite = 0

        Quartz += Old_Sphene - Sphene

        # =IF(AL14>0,IF(AO5>=0,'Albite',IF(AL14+(AO5/4)>0,'Both','Nepheline')),'None')

        if Albite <= 0:
            AlorNe = 'None'
        else:
            if Quartz >= 0:
                AlorNe = 'Albite'
            else:
                if Albite + (Quartz / 4) > 0:
                    AlorNe = 'Both'
                else:
                    AlorNe = 'Nepheline'

        # =AO5+(6*AL14)-(AP14*6)-(AP19*2)

        # =IF(AP26='Albite',AL14,IF(AP26='Both',AL14+(AO5/4),0))
        # =IF(AP26='Nepheline',AL14,IF(AP26='Both',AL14-AP14,0))

        Old_Albite = Albite

        if AlorNe == 'Albite':
            Albite = Albite
            Nepheline = 0

        elif AlorNe == 'Nepheline':
            Nepheline = Albite
            Albite = 0

        elif AlorNe == 'Both':
            Albite += Quartz / 4
            Nepheline = Old_Albite - Albite

        elif AlorNe == 'None':
            Nepheline = 0
            Albite = 0

        Quartz += (6 * Old_Albite) - (Albite * 6) - (Nepheline * 2)

        # =IF(AL8=0,0,AL8/(AL8+(AP14*2)))

        if Anorthite == 0:
            DataCalced.update({'Plagioclase An content': 0})
        else:
            DataCalced.update({'Plagioclase An content': 100 * Anorthite / (Anorthite + 2 * Albite)})

        # =IF(AL15>0,IF(AP5>=0,'Orthoclase',IF(AL15+(AP5/2)>0,'Both','Leucite')),'None')

        if Orthoclase <= 0:
            OorL = 'None'
        else:
            if Quartz >= 0:
                OorL = 'Orthoclase'
            else:
                if Orthoclase + Quartz / 2 > 0:
                    OorL = 'Both'
                else:
                    OorL = 'Leucite'

        # =IF(AQ26='Orthoclase',AL15,IF(AQ26='Both',AL15+(AP5/2),0))
        # =IF(AQ26='Leucite',AL15,IF(AQ26='Both',AL15-AQ15,0))

        Old_Orthoclase = Orthoclase

        if OorL == 'Orthoclase':
            Orthoclase = Orthoclase
            Leucite = 0

        elif OorL == 'Leucite':
            Leucite = Orthoclase
            Orthoclase = 0

        elif OorL == 'Both':
            Orthoclase += Quartz / 2
            Leucite = Old_Orthoclase - Orthoclase

        elif OorL == 'None':
            Orthoclase = 0
            Leucite = 0

        # =AP5+(AL15*6)-(AQ15*6)-(AQ20*4)

        Quartz += (Old_Orthoclase * 6) - (Orthoclase * 6) - (Leucite * 4)

        # =IF(AL16>0,IF(AQ5>=0,'Wollastonite',IF(AL16+(AQ5*2)>0,'Both','Larnite')),'None')
        if Wollastonite <= 0:
            WorB = 'None'
        else:
            if Quartz >= 0:
                WorB = 'Wollastonite'
            else:
                if Wollastonite + Quartz / 2 > 0:
                    WorB = 'Both'
                else:
                    WorB = 'Larnite'

        # =IF(AR26='Wollastonite',AL16,IF(AR26='Both',AL16+(2*AQ5),0))
        # =IF(AR26='Larnite',AL16/2,IF(AR26='Both',(AL16-AR16)/2,0))

        Old_Wollastonite = Wollastonite
        if WorB == 'Wollastonite':
            Wollastonite = Wollastonite
            Larnite = 0

        elif WorB == 'Larnite':
            Larnite = Wollastonite / 2
            Wollastonite = 0

        elif WorB == 'Both':
            Wollastonite += Quartz * 2
            Larnite = (Old_Wollastonite - Wollastonite) / 2

        elif WorB == 'None':
            Wollastonite = 0
            Larnite = 0

        # =AQ5+AL16-AR16-AR21
        Quartz += Old_Wollastonite - Wollastonite - Larnite

        # =IF(AL11>0,IF(AR5>=0,'Diopside',IF(AL11+AR5>0,'Both','LarniteOlivine')),'None')

        if Diopside <= 0:
            DorL = 'None'
        else:
            if Quartz >= 0:
                DorL = 'Diopside'
            else:
                if Diopside + Quartz > 0:
                    DorL = 'Both'
                else:
                    DorL = 'LarniteOlivine'

        # =IF(AS26='Diopside',AL11,IF(AS26='Both',AL11+AR5,0))
        # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AN17
        # =(IF(AS26='LarniteOlivine',AL11/2,IF(AS26='Both',(AL11-AS11)/2,0)))+AR21

        Old_Diopside = Diopside
        Old_Larnite = Larnite
        Old_Olivine = Olivine
        if DorL == 'Diopside':
            Diopside = Diopside



        elif DorL == 'LarniteOlivine':
            Larnite += Diopside / 2
            Olivine += Diopside / 2
            Diopside = 0

        elif DorL == 'Both':
            Diopside += Quartz
            Larnite += Old_Diopside - Diopside
            Olivine += Old_Diopside - Diopside



        elif DorL == 'None':
            Diopside = 0

        # =AR5+(AL11*2)+AN17+AR21-AS21-(AS11*2)-AS17
        Quartz += (Old_Diopside * 2) + Old_Olivine + Old_Larnite - Larnite - (Diopside * 2) - Olivine

        # =IF(AQ20>0,IF(AS5>=0,'Leucite',IF(AQ20+(AS5/2)>0,'Both','Kalsilite')),'None')

        if Leucite <= 0:
            LorK = 'None'
        else:
            if Quartz >= 0:
                LorK = 'Leucite'
            else:
                if Leucite + Quartz / 2 > 0:
                    LorK = 'Both'
                else:
                    LorK = 'Kalsilite'

        # =IF(AT26='Leucite',AQ20,IF(AT26='Both',AQ20+(AS5/2),0))
        # =IF(AT26='Kalsilite',AQ20,IF(AT26='Both',AQ20-AT20,0))

        Old_Leucite = Leucite

        if LorK == 'Leucite':
            Leucite = Leucite
            Kalsilite = 0

        elif LorK == 'Kalsilite':
            Kalsilite = Leucite
            Leucite = 0

        elif LorK == 'Both':
            Leucite += Quartz / 2
            Kalsilite = Old_Leucite - Leucite

        elif LorK == 'None':
            Leucite = 0
            Kalsilite = 0

        # =AS5+(AQ20*4)-(AT20*4)-(AT22*2)
        Quartz += Old_Leucite * 4 - Leucite * 4 - Kalsilite * 2

        Q = Quartz
        A = Orthoclase
        P = Anorthite + Albite
        F = Nepheline + Leucite + Kalsilite

        DataResult.update({'Quartz':  round(Quartz*100,4)})
        DataResult.update({'Zircon':  round(Zircon*100,4)})
        DataResult.update({'K2SiO3':  round(K2SiO3*100,4)})
        DataResult.update({'Anorthite':  round(Anorthite*100,4)})
        DataResult.update({'Na2SiO3':  round(Na2SiO3*100,4)})
        DataResult.update({'Acmite':  round(Acmite*100,4)})
        DataResult.update({'Diopside':  round(Diopside*100,4)})
        DataResult.update({'Sphene':  round(Sphene*100,4)})
        DataResult.update({'Hypersthene':  round(Hypersthene*100,4)})
        DataResult.update({'Albite':  round(Albite*100,4)})
        DataResult.update({'Orthoclase':  round(Orthoclase*100,4)})
        DataResult.update({'Wollastonite':  round(Wollastonite*100,4)})
        DataResult.update({'Olivine':  round(Olivine*100,4)})
        DataResult.update({'Perovskite':  round(Perovskite*100,4)})
        DataResult.update({'Nepheline':  round(Nepheline*100,4)})
        DataResult.update({'Leucite':  round(Leucite*100,4)})
        DataResult.update({'Larnite':  round(Larnite*100,4)})
        DataResult.update({'Kalsilite':  round(Kalsilite*100,4)})
        DataResult.update({'Apatite':  round(Apatite*100,4)})
        DataResult.update({'Halite':  round(Halite*100,4)})
        DataResult.update({'Fluorite':  round(Fluorite*100,4)})
        DataResult.update({'Anhydrite':  round(Anhydrite*100,4)})
        DataResult.update({'Thenardite':  round(Thenardite*100,4)})
        DataResult.update({'Pyrite':  round(Pyrite*100,4)})
        DataResult.update({'Magnesiochromite':  round(Magnesiochromite*100,4)})
        DataResult.update({'Chromite':  round(Chromite*100,4)})
        DataResult.update({'Ilmenite':  round(Ilmenite*100,4)})
        DataResult.update({'Calcite':  round(Calcite*100,4)})
        DataResult.update({'Na2CO3':  round(Na2CO3*100,4)})
        DataResult.update({'Corundum':  round(Corundum*100,4)})
        DataResult.update({'Rutile':  round(Rutile*100,4)})
        DataResult.update({'Magnetite':  round(Magnetite*100,4)})
        DataResult.update({'Hematite':  round(Hematite*100,4)})
        DataResult.update({'Q Mole':  round(Q*100,4)})
        DataResult.update({'A Mole':  round(A*100,4)})
        DataResult.update({'P Mole':  round(P*100,4)})
        DataResult.update({'F Mole':  round(F*100,4)})

        DataWeight.update({'Quartz':  round(Quartz * self.DataBase['Quartz'][0],4)})
        DataWeight.update({'Zircon':  round(Zircon * self.DataBase['Zircon'][0],4)})
        DataWeight.update({'K2SiO3':  round(K2SiO3 * self.DataBase['K2SiO3'][0],4)})
        DataWeight.update({'Anorthite':  round(Anorthite * self.DataBase['Anorthite'][0],4)})
        DataWeight.update({'Na2SiO3':  round(Na2SiO3 * self.DataBase['Na2SiO3'][0],4)})
        DataWeight.update({'Acmite':  round(Acmite * self.DataBase['Acmite'][0],4)})
        DataWeight.update({'Diopside':  round(Diopside * self.DataBase['Diopside'][0],4)})
        DataWeight.update({'Sphene':  round(Sphene * self.DataBase['Sphene'][0],4)})
        DataWeight.update({'Hypersthene':  round(Hypersthene * self.DataBase['Hypersthene'][0],4)})
        DataWeight.update({'Albite':  round(Albite * self.DataBase['Albite'][0],4)})
        DataWeight.update({'Orthoclase':  round(Orthoclase * self.DataBase['Orthoclase'][0],4)})
        DataWeight.update({'Wollastonite':  round(Wollastonite * self.DataBase['Wollastonite'][0],4)})
        DataWeight.update({'Olivine':  round(Olivine * self.DataBase['Olivine'][0],4)})
        DataWeight.update({'Perovskite':  round(Perovskite * self.DataBase['Perovskite'][0],4)})
        DataWeight.update({'Nepheline':  round(Nepheline * self.DataBase['Nepheline'][0],4)})
        DataWeight.update({'Leucite':  round(Leucite * self.DataBase['Leucite'][0],4)})
        DataWeight.update({'Larnite':  round(Larnite * self.DataBase['Larnite'][0],4)})
        DataWeight.update({'Kalsilite':  round(Kalsilite * self.DataBase['Kalsilite'][0],4)})
        DataWeight.update({'Apatite':  round(Apatite * self.DataBase['Apatite'][0],4)})
        DataWeight.update({'Halite':  round(Halite * self.DataBase['Halite'][0],4)})
        DataWeight.update({'Fluorite':  round(Fluorite * self.DataBase['Fluorite'][0],4)})
        DataWeight.update({'Anhydrite':  round(Anhydrite * self.DataBase['Anhydrite'][0],4)})
        DataWeight.update({'Thenardite':  round(Thenardite * self.DataBase['Thenardite'][0],4)})
        DataWeight.update({'Pyrite':  round(Pyrite * self.DataBase['Pyrite'][0],4)})
        DataWeight.update({'Magnesiochromite':  round(Magnesiochromite * self.DataBase['Magnesiochromite'][0],4)})
        DataWeight.update({'Chromite':  round(Chromite * self.DataBase['Chromite'][0],4)})
        DataWeight.update({'Ilmenite':  round(Ilmenite * self.DataBase['Ilmenite'][0],4)})
        DataWeight.update({'Calcite':  round(Calcite * self.DataBase['Calcite'][0],4)})
        DataWeight.update({'Na2CO3':  round(Na2CO3 * self.DataBase['Na2CO3'][0],4)})
        DataWeight.update({'Corundum':  round(Corundum * self.DataBase['Corundum'][0],4)})
        DataWeight.update({'Rutile':  round(Rutile * self.DataBase['Rutile'][0],4)})
        DataWeight.update({'Magnetite':  round(Magnetite * self.DataBase['Magnetite'][0],4)})
        DataWeight.update({'Hematite':  round(Hematite * self.DataBase['Hematite'][0],4)})
        DataWeight.update({'Q Weight':  round(Quartz * self.DataBase['Quartz'][0],4)})
        DataWeight.update({'A Weight':  round(Orthoclase * self.DataBase['Orthoclase'][0],4)})
        DataWeight.update({'P Weight':  round(Anorthite * self.DataBase['Anorthite'][0] + Albite * self.DataBase['Albite'][0],4)})
        DataWeight.update({'F Weight':  round(Nepheline * self.DataBase['Nepheline'][0] + Leucite * self.DataBase['Leucite'][0] + Kalsilite * self.DataBase['Kalsilite'][0],4)})


        WholeVolume = 0
        WholeMole = 0
        tmpVolume = []

        tmpVolume.append(Quartz * self.DataBase['Quartz'][0] / self.DataBase['Quartz'][1])
        tmpVolume.append(Zircon * self.DataBase['Zircon'][0] / self.DataBase['Zircon'][1])
        tmpVolume.append(K2SiO3 * self.DataBase['K2SiO3'][0] / self.DataBase['K2SiO3'][1])
        tmpVolume.append(Anorthite * self.DataBase['Anorthite'][0] / self.DataBase['Anorthite'][1])
        tmpVolume.append(Na2SiO3 * self.DataBase['Na2SiO3'][0] / self.DataBase['Na2SiO3'][1])
        tmpVolume.append(Acmite * self.DataBase['Acmite'][0] / self.DataBase['Acmite'][1])
        tmpVolume.append(Diopside * self.DataBase['Diopside'][0] / self.DataBase['Diopside'][1])
        tmpVolume.append(Sphene * self.DataBase['Sphene'][0] / self.DataBase['Sphene'][1])
        tmpVolume.append(Hypersthene * self.DataBase['Hypersthene'][0] / self.DataBase['Hypersthene'][1])
        tmpVolume.append(Albite * self.DataBase['Albite'][0] / self.DataBase['Albite'][1])
        tmpVolume.append(Orthoclase * self.DataBase['Orthoclase'][0] / self.DataBase['Orthoclase'][1])
        tmpVolume.append(Wollastonite * self.DataBase['Wollastonite'][0] / self.DataBase['Wollastonite'][1])
        tmpVolume.append(Olivine * self.DataBase['Olivine'][0] / self.DataBase['Olivine'][1])
        tmpVolume.append(Perovskite * self.DataBase['Perovskite'][0] / self.DataBase['Perovskite'][1])
        tmpVolume.append(Nepheline * self.DataBase['Nepheline'][0] / self.DataBase['Nepheline'][1])
        tmpVolume.append(Leucite * self.DataBase['Leucite'][0] / self.DataBase['Leucite'][1])
        tmpVolume.append(Larnite * self.DataBase['Larnite'][0] / self.DataBase['Larnite'][1])
        tmpVolume.append(Kalsilite * self.DataBase['Kalsilite'][0] / self.DataBase['Kalsilite'][1])
        tmpVolume.append(Apatite * self.DataBase['Apatite'][0] / self.DataBase['Apatite'][1])
        tmpVolume.append(Halite * self.DataBase['Halite'][0] / self.DataBase['Halite'][1])
        tmpVolume.append(Fluorite * self.DataBase['Fluorite'][0] / self.DataBase['Fluorite'][1])
        tmpVolume.append(Anhydrite * self.DataBase['Anhydrite'][0] / self.DataBase['Anhydrite'][1])
        tmpVolume.append(Thenardite * self.DataBase['Thenardite'][0] / self.DataBase['Thenardite'][1])
        tmpVolume.append(Pyrite * self.DataBase['Pyrite'][0] / self.DataBase['Pyrite'][1])
        tmpVolume.append(Magnesiochromite * self.DataBase['Magnesiochromite'][0] / self.DataBase['Magnesiochromite'][1])
        tmpVolume.append(Chromite * self.DataBase['Chromite'][0] / self.DataBase['Chromite'][1])
        tmpVolume.append(Ilmenite * self.DataBase['Ilmenite'][0] / self.DataBase['Ilmenite'][1])
        tmpVolume.append(Calcite * self.DataBase['Calcite'][0] / self.DataBase['Calcite'][1])
        tmpVolume.append(Na2CO3 * self.DataBase['Na2CO3'][0] / self.DataBase['Na2CO3'][1])
        tmpVolume.append(Corundum * self.DataBase['Corundum'][0] / self.DataBase['Corundum'][1])
        tmpVolume.append(Rutile * self.DataBase['Rutile'][0] / self.DataBase['Rutile'][1])
        tmpVolume.append(Magnetite * self.DataBase['Magnetite'][0] / self.DataBase['Magnetite'][1])
        tmpVolume.append(Hematite * self.DataBase['Hematite'][0] / self.DataBase['Hematite'][1])

        WholeVolume = sum(tmpVolume)

        DataVolume.update(
            {'Quartz':  round((Quartz * self.DataBase['Quartz'][0] / self.DataBase['Quartz'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Zircon':  round((Zircon * self.DataBase['Zircon'][0] / self.DataBase['Zircon'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'K2SiO3':  round((K2SiO3 * self.DataBase['K2SiO3'][0] / self.DataBase['K2SiO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Anorthite':  round((Anorthite * self.DataBase['Anorthite'][0] / self.DataBase['Anorthite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Na2SiO3':  round((Na2SiO3 * self.DataBase['Na2SiO3'][0] / self.DataBase['Na2SiO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Acmite':  round((Acmite * self.DataBase['Acmite'][0] / self.DataBase['Acmite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Diopside':  round((Diopside * self.DataBase['Diopside'][0] / self.DataBase['Diopside'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Sphene':  round((Sphene * self.DataBase['Sphene'][0] / self.DataBase['Sphene'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Hypersthene':  round((Hypersthene * self.DataBase['Hypersthene'][0] / self.DataBase['Hypersthene'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Albite':  round((Albite * self.DataBase['Albite'][0] / self.DataBase['Albite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Orthoclase':  round((Orthoclase * self.DataBase['Orthoclase'][0] / self.DataBase['Orthoclase'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Wollastonite':  round((Wollastonite * self.DataBase['Wollastonite'][0] /
                                            self.DataBase['Wollastonite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Olivine':  round((Olivine * self.DataBase['Olivine'][0] / self.DataBase['Olivine'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Perovskite':  round((Perovskite * self.DataBase['Perovskite'][0] / self.DataBase['Perovskite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Nepheline':  round((Nepheline * self.DataBase['Nepheline'][0] / self.DataBase['Nepheline'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Leucite':  round((Leucite * self.DataBase['Leucite'][0] / self.DataBase['Leucite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Larnite':  round((Larnite * self.DataBase['Larnite'][0] / self.DataBase['Larnite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Kalsilite':  round((Kalsilite * self.DataBase['Kalsilite'][0] / self.DataBase['Kalsilite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Apatite':  round((Apatite * self.DataBase['Apatite'][0] / self.DataBase['Apatite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Halite':  round((Halite * self.DataBase['Halite'][0] / self.DataBase['Halite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Fluorite':  round((Fluorite * self.DataBase['Fluorite'][0] / self.DataBase['Fluorite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Anhydrite':  round((Anhydrite * self.DataBase['Anhydrite'][0] / self.DataBase['Anhydrite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update({'Thenardite':  round((Thenardite * self.DataBase['Thenardite'][0] / self.DataBase['Thenardite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Pyrite':  round((Pyrite * self.DataBase['Pyrite'][0] / self.DataBase['Pyrite'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Magnesiochromite':  round((Magnesiochromite * self.DataBase['Magnesiochromite'][0] /
                                                self.DataBase['Magnesiochromite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Chromite':  round((Chromite * self.DataBase['Chromite'][0] / self.DataBase['Chromite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Ilmenite':  round((Ilmenite * self.DataBase['Ilmenite'][0] / self.DataBase['Ilmenite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Calcite':  round((Calcite * self.DataBase['Calcite'][0] / self.DataBase['Calcite'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Na2CO3':  round((Na2CO3 * self.DataBase['Na2CO3'][0] / self.DataBase['Na2CO3'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Corundum':  round((Corundum * self.DataBase['Corundum'][0] / self.DataBase['Corundum'][1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Rutile':  round((Rutile * self.DataBase['Rutile'][0] / self.DataBase['Rutile'][1]) / WholeVolume * 100,4)})
        DataVolume.update({'Magnetite':  round((Magnetite * self.DataBase['Magnetite'][0] / self.DataBase['Magnetite'][
            1]) / WholeVolume * 100,4)})
        DataVolume.update(
            {'Hematite':  round((Hematite * self.DataBase['Hematite'][0] / self.DataBase['Hematite'][1]) / WholeVolume * 100,4)})

        DataVolume.update({'Q':  round(DataVolume['Quartz'],4)})
        DataVolume.update({'A':  round(DataVolume['Orthoclase'],4)})

        DataVolume.update({'P':  round(DataVolume['Anorthite'] + DataVolume['Albite'],4)})
        DataVolume.update({'F':  round(DataVolume['Nepheline'] + DataVolume['Leucite'] + DataVolume['Kalsilite'],4)})

        DI = 0
        # for i in ['Quartz', 'Anorthite', 'Albite', 'Orthoclase', 'Nepheline', 'Leucite', 'Kalsilite']:
        # exec('DI+=' + i + '*self.DataBase[\'' + i + '\'][0]')

        DI = Quartz + Anorthite + Albite + Orthoclase + Nepheline + Leucite + Kalsilite


        DiWeight=0
        DiVolume=0

        DiWeight = DataWeight['Quartz']+DataWeight['Anorthite']+DataWeight['Albite']+DataWeight['Orthoclase']+DataWeight['Nepheline']+DataWeight['Leucite']+DataWeight['Kalsilite']
        DiVolume = DataVolume['Quartz']+DataVolume['Anorthite']+DataVolume['Albite']+DataVolume['Orthoclase']+DataVolume['Nepheline']+DataVolume['Leucite']+DataVolume['Kalsilite']

        # print('\n\n DI is\n',DI,'\n\n')
        DataCalced.update({'Differentiation Index Weight': DiWeight})

        DataCalced.update({'Differentiation Index Volume': DiVolume})

        return (DataResult, DataWeight, DataVolume, DataCalced)


    def WriteData(self, target='DataResult'):
        DataToWrite = []
        TMP_DataToWrite = ['Label']

        TMP_DataToWrite = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']

        for j in self.Minerals:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite = []
            k = self.raw.at[i, 'Label']
            TMP_DataToWrite = [self.raw.at[i, 'Label'], self.raw.at[i, 'Marker'], self.raw.at[i, 'Color'],
                               self.raw.at[i, 'Size'], self.raw.at[i, 'Alpha'], self.raw.at[i, 'Style'],
                               self.raw.at[i, 'Width']]
            for j in self.Minerals:
                command = 'TMP_DataToWrite.append((self.' + target + '[k][j]))'

                exec('#print((self.' + target + '[k][j]))')

                try:
                    exec(command)
                except(KeyError):
                    pass
            DataToWrite.append(TMP_DataToWrite)
        return (DataToWrite)

    def WriteCalced(self, target='DataCalced'):
        DataToWrite = []
        TMP_DataToWrite = ['Label']

        TMP_DataToWrite = ['Label', 'Marker', 'Color', 'Size', 'Alpha', 'Style', 'Width']
        for j in self.Calced:
            TMP_DataToWrite.append(str(j))
        DataToWrite.append(TMP_DataToWrite)
        for i in range(len(self.DataMole)):
            TMP_DataToWrite = []
            k = self.raw.at[i, 'Label']
            TMP_DataToWrite = [self.raw.at[i, 'Label'], self.raw.at[i, 'Marker'], self.raw.at[i, 'Color'],
                               self.raw.at[i, 'Size'], self.raw.at[i, 'Alpha'], self.raw.at[i, 'Style'],
                               self.raw.at[i, 'Width']]

            for j in self.Calced:
                command = 'TMP_DataToWrite.append((self.' + target + '[k][j]))'
                try:

                    exec('#print((self.' + target + '[k][j]))')

                    exec(command)
                except(KeyError):
                    pass

            DataToWrite.append(TMP_DataToWrite)

        # print('\n',DataToWrite,'\n')
        return (DataToWrite)

    def ReduceSize(self,df=pd.DataFrame):

        m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']

        for i in m:
            if i in df.columns.values:
                df = df.drop(i, 1)
        df = df.loc[:, (df != 0).any(axis=0)]
        return(df)


    def GetSym(self,df=pd.DataFrame):

        m = ['Label', 'Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']

        for i in df.columns.values:
            if i not in m:
                df = df.drop(i, 1)
        df = df.loc[:, (df != 0).any(axis=0)]
        return(df)




    def DropUseless(self,df= pd.DataFrame(),droplist = ['Q (Mole)', 'A (Mole)', 'P (Mole)', 'F (Mole)',
                    'Q (Mass)', 'A (Mass)', 'P (Mass)', 'F (Mass)']):

        for t in droplist:
            if t in df.columns.values:
                df = df.drop(t, 1)
        return(df)


    def QAPF(self):
        self.qapfpop = QAPF(df=self.useddf)
        try:
            self.qapfpop.QAPF()
        except(TypeError):
            pass
        self.qapfpop.show()

    def QAPFsilent(self):
        self.qapfpop = QAPF(df=self.useddf)
        try:
            self.qapfpop.QAPF()
        except(TypeError):
            pass

        self.OutPutFig = self.qapfpop.OutPutFig


    def saveResult(self):
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出






        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):

                DataFileOutput=DataFileOutput[0:-4]


                #self.newdf.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                self.newdf.to_csv(DataFileOutput + '-Niggli-mole.csv', sep=',', encoding='utf-8')
                self.newdf1.to_csv(DataFileOutput + '-Niggli-mass.csv', sep=',', encoding='utf-8')
                self.newdf2.to_csv(DataFileOutput + '-Niggli-volume.csv', sep=',', encoding='utf-8')
                self.newdf3.to_csv(DataFileOutput + '-Niggli-index.csv', sep=',', encoding='utf-8')
                

            elif ('xlsx' in DataFileOutput):

                DataFileOutput = DataFileOutput[0:-5]

                #self.newdf.to_excel(DataFileOutput, encoding='utf-8')

                self.newdf.to_excel(DataFileOutput + '-Niggli-mole.xlsx',  encoding='utf-8')
                self.newdf1.to_excel(DataFileOutput + '-Niggli-mass.xlsx',  encoding='utf-8')
                self.newdf2.to_excel(DataFileOutput + '-Niggli-volume.xlsx',  encoding='utf-8')
                self.newdf3.to_excel(DataFileOutput + '-Niggli-index.xlsx', encoding='utf-8')