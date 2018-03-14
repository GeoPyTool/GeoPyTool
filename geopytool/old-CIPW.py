from geopytool.ImportDependence import *
from geopytool.CustomClass import *
from geopytool.QAPF import *

class CIPW(AppForm):
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

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('CIPW Norm Result')

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



        self.qapf_button = QPushButton('&QAPF')
        self.qapf_button.clicked.connect(self.QAPF)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)




        #
        # Layout with box sizers
        #

        self.hbox = QHBoxLayout()

        for w in [self.qapf_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)
        self.vbox.addWidget(self.save_button)

        self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def Calc(self):

        self.DataBase.update({'Quartz': [60.0843, 2.65]})
        self.DataBase.update({'Zircon': [183.3031, 4.56]})
        self.DataBase.update({'K2SiO3': [154.2803, 2.5]})
        self.DataBase.update({'Anorthite': [278.2093, 2.76]})
        self.DataBase.update({'Na2SiO3': [122.0632, 2.4]})
        self.DataBase.update({'Acmite': [462.0083, 3.6]})
        self.DataBase.update({'Diopside': [229.0691997, 3.354922069]})
        self.DataBase.update({'Sphene': [196.0625, 3.5]})
        self.DataBase.update({'Hypersthene': [112.9054997, 3.507622212]})
        self.DataBase.update({'Albite': [524.446, 2.62]})
        self.DataBase.update({'Orthoclase': [556.6631, 2.56]})
        self.DataBase.update({'Wollastonite': [116.1637, 2.86]})
        self.DataBase.update({'Olivine': [165.7266995, 3.68429065]})
        self.DataBase.update({'Perovskite': [135.9782, 4]})
        self.DataBase.update({'Nepheline': [284.1088, 2.56]})
        self.DataBase.update({'Leucite': [436.4945, 2.49]})
        self.DataBase.update({'Larnite': [172.2431, 3.27]})
        self.DataBase.update({'Kalsilite': [316.3259, 2.6]})
        self.DataBase.update({'Apatite': [493.3138, 3.2]})
        self.DataBase.update({'Halite': [66.44245, 2.17]})
        self.DataBase.update({'Fluorite': [94.0762, 3.18]})
        self.DataBase.update({'Anhydrite': [136.1376, 2.96]})
        self.DataBase.update({'Thenardite': [142.0371, 2.68]})
        self.DataBase.update({'Pyrite': [135.9664, 4.99]})
        self.DataBase.update({'Magnesiochromite': [192.2946, 4.43]})
        self.DataBase.update({'Chromite': [223.8366, 5.09]})
        self.DataBase.update({'Ilmenite': [151.7452, 4.75]})
        self.DataBase.update({'Calcite': [100.0892, 2.71]})
        self.DataBase.update({'Na2CO3': [105.9887, 2.53]})
        self.DataBase.update({'Corundum': [101.9613, 3.98]})
        self.DataBase.update({'Rutile': [79.8988, 4.2]})
        self.DataBase.update({'Magnetite': [231.5386, 5.2]})
        self.DataBase.update({'Hematite': [159.6922, 5.25]})
        self.b = self.raw.columns
        self.WeightCorrectionFactor = []
        self.BaseMass = {}
        self.Elements = ['SiO2',
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
        self.DataMole = []
        self.DataCalculating = {}
        self.DataResult = {}

        self.ElementsMass = [('SiO2', 60.083),
                             ('TiO2', 79.865),
                             ('Al2O3', 101.960077),
                             ('Fe2O3', 159.687),
                             ('FeO', 71.844),
                             ('MnO', 70.937044),
                             ('MgO', 40.304),
                             ('CaO', 56.077000000000005),
                             ('Na2O', 61.978538560000004),
                             ('K2O', 94.1956),
                             ('P2O5', 141.942523996),
                             ('CO2', 44.009),
                             ('SO3', 80.057),
                             ('S', 32.06),
                             ('F', 18.998403163),
                             ('Cl', 35.45),
                             ('Sr', 87.62),
                             ('Ba', 137.327),
                             ('Ni', 58.6934),
                             ('Cr', 51.9961),
                             ('Zr', 91.224)]

        self.BaseMass = {'SiO2': 60.083,
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

        for i in range(len(self.raw)):
            TmpWhole = 0
            TmpMole = {}

            for j in self.Elements:
                '''
                Get the Whole Mole of the dataset
                '''

                try:
                    T_TMP = self.raw.at[i, j]
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

                V = TMP

                try:
                    TmpWhole += float(V)
                except ValueError:
                    pass

            self.WeightCorrectionFactor.append(100 / TmpWhole)

            for j in self.Elements:
                '''
                Get the Mole percentage of each element
                '''

                try:
                    T_TMP = self.raw.at[i, j]
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
                    M = TMP / self.BaseMass[j] * self.WeightCorrectionFactor[i]
                except TypeError:
                    pass

                # M= TMP/NewMass(j) * WeightCorrectionFactor[i]

                TmpMole.update({j: M})
            self.DataMole.append(TmpMole)

        self.DataCalculating = {k: [] for k in self.Elements}

        for i in range(len(self.DataMole)):
            k = self.raw.at[i, 'Label']
            self.DataResult.update({k: {}})
            self.DataWeight.update({k: {}})
            self.DataVolume.update({k: {}})
            self.DataCalced.update({k: {}})

            a = self.DataMole[i]
            for j in list(a):
                self.DataCalculating[j].append(a[j])

            Fe3 = self.DataCalculating['Fe2O3'][i]
            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]
            Ca = self.DataCalculating['CaO'][i]
            Na = self.DataCalculating['Na2O'][i]

            try:
                self.DataCalced[k].update({'Fe3+/(Total Fe) in rock': 100 * Fe3 * 2 / (Fe3 * 2 + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Fe3+/(Total Fe) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Mg/(Mg+Total Fe) in rock': 100 * Mg / (Mg + Fe3 * 2 + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Mg/(Mg+Total Fe) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in rock': 100 * Mg / (Mg + Fe2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in rock': 0})
                pass

            try:
                self.DataCalced[k].update({'Ca/(Ca+Na) in rock': 100 * Ca / (Ca + Na * 2)})
            except(ZeroDivisionError):
                self.DataCalced[k].update({'Ca/(Ca+Na) in rock': 0})
                pass

            self.DataCalculating['CaO'][i] += self.DataCalculating['Sr'][i]
            self.DataCalculating['Sr'][i] = 0

            self.DataCalculating['K2O'][i] += 2 * self.DataCalculating['Ba'][i]
            self.DataCalculating['Ba'][i] = 0

            try:
                if self.DataCalculating['CaO'][i] >= 10 / 3 * self.DataCalculating['P2O5'][i]:
                    self.DataCalculating['CaO'][i] -= 10 / 3 * self.DataCalculating['P2O5'][i]
                else:
                    self.DataCalculating['CaO'][i] = 0
            except(ZeroDivisionError):
                pass

            self.DataCalculating['P2O5'][i] = self.DataCalculating['P2O5'][i] / 1.5

            Apatite = self.DataCalculating['P2O5'][i]

            # IF(S19>=T15,S19-T15,0)

            if self.DataCalculating['F'][i] >= self.DataCalculating['P2O5'][i]:
                self.DataCalculating['F'][i] -= self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['F'][i] = 0

            if self.DataCalculating['F'][i] >= self.DataCalculating['P2O5'][i]:
                self.DataCalculating['F'][i] -= self.DataCalculating['P2O5'][i]
            else:
                self.DataCalculating['F'][i] = 0

            if self.DataCalculating['Na2O'][i] >= self.DataCalculating['Cl'][i]:
                self.DataCalculating['Na2O'][i] -= self.DataCalculating['Cl'][i]
            else:
                self.DataCalculating['Na2O'][i] = 0

            Halite = self.DataCalculating['Cl'][i]

            # IF(U12>=(U19/2),U12-(U19/2),0)
            if self.DataCalculating['CaO'][i] >= 0.5 * self.DataCalculating['F'][i]:
                self.DataCalculating['CaO'][i] -= 0.5 * self.DataCalculating['F'][i]
            else:
                self.DataCalculating['CaO'][i] = 0

            self.DataCalculating['F'][i] *= 0.5

            Fluorite = self.DataCalculating['F'][i]

            # =IF(V17>0,IF(V13>=V17,'Thenardite',IF(V13>0,'Both','Anhydrite')),'None')
            AorT = 0
            if self.DataCalculating['SO3'][i] <= 0:
                AorT = 'None'
            else:
                if self.DataCalculating['Na2O'][i] >= self.DataCalculating['SO3'][i]:
                    AorT = 'Thenardite'
                else:
                    if self.DataCalculating['Na2O'][i] > 0:
                        AorT = 'Both'
                    else:
                        AorT = 'Anhydrite'

            # =IF(W26='Anhydrite',V17,IF(W26='Both',V12,0))
            # =IF(W26='Thenardite',V17,IF(W26='Both',V17-W17,0))

            if AorT == 'Anhydrite':
                self.DataCalculating['Sr'][i] = 0
            elif AorT == 'Thenardite':
                self.DataCalculating['Sr'][i] = self.DataCalculating['SO3'][i]
                self.DataCalculating['SO3'][i] = 0
            elif AorT == 'Both':
                self.DataCalculating['Sr'][i] = self.DataCalculating['SO3'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['SO3'][i] = self.DataCalculating['CaO'][i]
            else:
                self.DataCalculating['SO3'][i] = 0
                self.DataCalculating['Sr'][i] = 0

            self.DataCalculating['CaO'][i] -= self.DataCalculating['SO3'][i]

            self.DataCalculating['Na2O'][i] -= self.DataCalculating['Sr'][i]

            Anhydrite = self.DataCalculating['SO3'][i]
            Thenardite = self.DataCalculating['Sr'][i]

            Pyrite = 0.5 * self.DataCalculating['S'][i]

            # =IF(W9>=(W18*0.5),W9-(W18*0.5),0)

            if self.DataCalculating['FeO'][i] >= self.DataCalculating['S'][i] * 0.5:
                self.DataCalculating['FeO'][i] -= self.DataCalculating['S'][i] * 0.5
            else:
                self.DataCalculating['FeO'][i] = 0

            # =IF(X24>0,IF(X9>=X24,'Chromite',IF(X9>0,'Both','Magnesiochromite')),'None')

            if self.DataCalculating['Cr'][i] > 0:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['Cr'][i]:
                    CorM = 'Chromite'
                elif self.DataCalculating['FeO'][i] > 0:
                    CorM = 'Both'
                else:
                    CorM = 'Magnesiochromite'
            else:
                CorM = 'None'

            # =IF(Y26='Chromite',X24,IF(Y26='Both',X9,0))
            # =IF(Y26='Magnesiochromite',X24,IF(Y26='Both',X24-Y24,0))

            if CorM == 'Chromite':
                self.DataCalculating['Cr'][i] = self.DataCalculating['Cr'][i]
                self.DataCalculating['Ni'][i] = 0

            elif CorM == 'Magnesiochromite':
                self.DataCalculating['Ni'][i] = self.DataCalculating['Cr'][i]
                self.DataCalculating['Cr'][i] = 0

            elif CorM == 'Both':
                self.DataCalculating['Ni'][i] = self.DataCalculating['Cr'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['Cr'][i] = self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['Cr'][i] = 0
                self.DataCalculating['Ni'][i] = 0

            self.DataCalculating['MgO'][i] -= self.DataCalculating['Ni'][i]

            Magnesiochromite = self.DataCalculating['Ni'][i]
            Chromite = self.DataCalculating['Cr'][i]

            # =IF(X9>=Y24,X9-Y24,0)

            if self.DataCalculating['FeO'][i] >= self.DataCalculating['Cr'][i]:
                self.DataCalculating['FeO'][i] -= self.DataCalculating['Cr'][i]
            else:
                self.DataCalculating['FeO'][i] = 0

            # =IF(Y6>0,IF(Y9>=Y6,'Ilmenite',IF(Y9>0,'Both','Sphene')),'None')

            if self.DataCalculating['TiO2'][i] < 0:
                IorS = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['TiO2'][i]:
                    IorS = 'Ilmenite'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        IorS = 'Both'
                    else:
                        IorS = 'Sphene'

            # =IF(Z26='Ilmenite',Y6,IF(Z26='Both',Y9,0))
            # =IF(Z26='Sphene',Y6,IF(Z26='Both',Y6-Z6,0))

            if IorS == 'Ilmenite':
                self.DataCalculating['TiO2'][i] = self.DataCalculating['TiO2'][i]
                self.DataCalculating['MnO'][i] = 0

            elif IorS == 'Sphene':
                self.DataCalculating['MnO'][i] = self.DataCalculating['TiO2'][i]
                self.DataCalculating['TiO2'][i] = 0

            elif IorS == 'Both':

                self.DataCalculating['MnO'][i] = self.DataCalculating['TiO2'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['TiO2'][i] = self.DataCalculating['FeO'][i]

            else:
                self.DataCalculating['TiO2'][i] = 0
                self.DataCalculating['MnO'][i] = 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['TiO2'][i]

            Ilmenite = self.DataCalculating['TiO2'][i]

            # =IF(Z16>0,IF(Z12>=Z16,'Calcite',IF(Z12>0,'Both','Na2CO3')),'None')


            if self.DataCalculating['CO2'][i] <= 0:
                CorN = 'None'
            else:
                if self.DataCalculating['CaO'][i] >= self.DataCalculating['CO2'][i]:
                    CorN = 'Calcite'
                else:
                    if self.DataCalculating['CaO'][i] > 0:
                        CorN = 'Both'
                    else:
                        CorN = 'Na2CO3'

            # =IF(AA26='Calcite',Z16,IF(AA26='Both',Z12,0))


            # =IF(AA26='Na2CO3',Z16,IF(AA26='Both',Z16-AA16,0))

            if CorN == 'None':
                self.DataCalculating['CO2'][i] = 0
                self.DataCalculating['SO3'][i] = 0

            elif CorN == 'Calcite':
                self.DataCalculating['CO2'][i] = self.DataCalculating['CO2'][i]
                self.DataCalculating['SO3'][i] = 0

            elif CorN == 'Na2CO3':
                self.DataCalculating['SO3'][i] = self.DataCalculating['SO3'][i]
                self.DataCalculating['CO2'][i] = 0

            elif CorN == 'Both':
                self.DataCalculating['SO3'][i] = self.DataCalculating['CO2'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['CO2'][i] = self.DataCalculating['CaO'][i]

            self.DataCalculating['CaO'][i] -= self.DataCalculating['CO2'][i]

            Calcite = self.DataCalculating['CO2'][i]

            Na2CO3 = self.DataCalculating['SO3'][i]

            # =IF(AA17>Z13,0,Z13-AA17)
            if self.DataCalculating['SO3'][i] > self.DataCalculating['Na2O'][i]:
                self.DataCalculating['Na2O'][i] = 0
            else:
                self.DataCalculating['Na2O'][i] -= self.DataCalculating['SO3'][i]

            self.DataCalculating['SiO2'][i] -= self.DataCalculating['Zr'][i]
            Zircon = self.DataCalculating['Zr'][i]

            # =IF(AB14>0,IF(AB7>=AB14,'Orthoclase',IF(AB7>0,'Both','K2SiO3')),'None')

            if self.DataCalculating['K2O'][i] <= 0:
                OorK = 'None'
            else:
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['K2O'][i]:
                    OorK = 'Orthoclase'
                else:
                    if self.DataCalculating['Al2O3'][i] > 0:
                        OorK = 'Both'
                    else:
                        OorK = 'K2SiO3'

            # =IF(AC26='Orthoclase',AB14,IF(AC26='Both',AB7,0))
            # =IF(AC26='K2SiO3',AB14,IF(AC26='Both',AB14-AB7,0))

            if OorK == 'None':
                self.DataCalculating['K2O'][i] = 0
                self.DataCalculating['P2O5'][i] = 0


            elif OorK == 'Orthoclase':
                self.DataCalculating['K2O'][i] = self.DataCalculating['K2O'][i]
                self.DataCalculating['P2O5'][i] = 0


            elif OorK == 'K2SiO3':
                self.DataCalculating['P2O5'][i] = self.DataCalculating['K2O'][i]
                self.DataCalculating['K2O'][i] = 0



            elif OorK == 'Both':

                self.DataCalculating['P2O5'][i] = self.DataCalculating['K2O'][i] - self.DataCalculating['Al2O3'][i]
                self.DataCalculating['K2O'][i] = self.DataCalculating['Al2O3'][i]

            self.DataCalculating['Al2O3'][i] -= self.DataCalculating['K2O'][i]

            # =IF(AC13>0,IF(AC7>=AC13,'Albite',IF(AC7>0,'Both','Na2SiO3')),'None')

            if self.DataCalculating['Na2O'][i] <= 0:
                AorN = 'None'
            else:
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['Na2O'][i]:
                    AorN = 'Albite'
                else:
                    if self.DataCalculating['Al2O3'][i] > 0:
                        AorN = 'Both'
                    else:
                        AorN = 'Na2SiO3'

            # =IF(AND(AC7>=AC13,AC7>0),AC7-AC13,0)

            if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['Na2O'][i] and self.DataCalculating['Al2O3'][
                i] > 0:
                self.DataCalculating['Al2O3'][i] -= self.DataCalculating['Na2O'][i]
            else:
                self.DataCalculating['Al2O3'][i] = 0

            # =IF(AD26='Albite',AC13,IF(AD26='Both',AC7,0))
            # =IF(AD26='Na2SiO3',AC13,IF(AD26='Both',AC13-AD13,0))


            if AorN == 'Albite':
                self.DataCalculating['Cl'][i] = 0

            elif AorN == 'Both':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Na2O'][i] - self.DataCalculating['Al2O3'][i]
                self.DataCalculating['Na2O'][i] = self.DataCalculating['Al2O3'][i]

            elif AorN == 'Na2SiO3':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Na2O'][i]
                self.DataCalculating['Na2O'][i] = 0

            elif AorN == 'None':
                self.DataCalculating['Na2O'][i] = 0
                self.DataCalculating['Cl'][i] = 0

            # =IF(AD7>0,IF(AD12>0,'Anorthite','None'),'None')

            '''
            Seem like should be =IF(AD7>0,IF(AD12>AD7,'Anorthite','Corundum'),'None')

            If Al2O3 is left after alloting orthoclase and albite, then:
            Anorthite = Al2O3, CaO = CaO - Al2O3, SiO2 = SiO2 - 2 Al2O3, Al2O3 = 0
            If Al2O3 exceeds CaO in the preceding calculation, then:
            Anorthite = CaO, Al2O3 = Al2O3 - CaO, SiO2 = SiO2 - 2 CaO
            Corundum = Al2O3, CaO =0, Al2O3 = 0


                if self.DataCalculating['Al2O3'][i]<=0:
                    AorC='None'
                else:
                    if self.DataCalculating['CaO'][i]>self.DataCalculating['Al2O3'][i]:
                        AorC= 'Anorthite'
                    else:
                        Aorc='Corundum'

            '''

            if self.DataCalculating['Al2O3'][i] <= 0:
                AorC = 'None'
            else:
                if self.DataCalculating['CaO'][i] > 0:
                    AorC = 'Anorthite'
                else:
                    Aorc = 'None'

            # =IF(AE26='Anorthite',IF(AD12>AD7,0,AD7-AD12),AD7)

            # =IF(AE26='Anorthite',IF(AD7>AD12,0,AD12-AD7),AD12)

            # =IF(AE26='Anorthite',IF(AD7>AD12,AD12,AD7),0)

            if AorC == 'Anorthite':
                if self.DataCalculating['Al2O3'][i] >= self.DataCalculating['CaO'][i]:
                    self.DataCalculating['Sr'][i] = self.DataCalculating['CaO'][i]
                    self.DataCalculating['Al2O3'][i] -= self.DataCalculating['CaO'][i]
                    self.DataCalculating['CaO'][i] = 0

                else:
                    self.DataCalculating['Sr'][i] = self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['CaO'][i] -= self.DataCalculating['Al2O3'][i]
                    self.DataCalculating['Al2O3'][i] = 0

            else:
                self.DataCalculating['Sr'][i] = 0

            Corundum = self.DataCalculating['Al2O3'][i]
            Anorthite = self.DataCalculating['Sr'][i]

            # =IF(AE10>0,IF(AE12>=AE10,'Sphene',IF(AE12>0,'Both','Rutile')),'None')

            if self.DataCalculating['MnO'][i] <= 0:
                SorR = 'None'
            else:
                if self.DataCalculating['CaO'][i] >= self.DataCalculating['MnO'][i]:
                    SorR = 'Sphene'
                elif self.DataCalculating['CaO'][i] > 0:
                    SorR = 'Both'
                else:
                    SorR = 'Rutile'

            # =IF(AF26='Sphene',AE10,IF(AF26='Both',AE12,0))

            # =IF(AF26='Rutile',AE10,IF(AF26='Both',AE10-AE12,0))

            if SorR == 'Sphene':
                self.DataCalculating['MnO'][i] = self.DataCalculating['MnO'][i]
                self.DataCalculating['S'][i] = 0

            elif SorR == 'Rutile':
                self.DataCalculating['S'][i] = self.DataCalculating['MnO'][i]
                self.DataCalculating['MnO'][i] = 0


            elif SorR == 'Both':
                self.DataCalculating['S'][i] = self.DataCalculating['MnO'][i] - self.DataCalculating['CaO'][i]
                self.DataCalculating['MnO'][i] = self.DataCalculating['CaO'][i]

            elif SorR == 'None':
                self.DataCalculating['MnO'][i] = 0
                self.DataCalculating['S'][i] = 0

            self.DataCalculating['CaO'][i] -= self.DataCalculating['MnO'][i]

            Rutile = self.DataCalculating['S'][i]

            # =IF(AND(AF20>0),IF(AF8>=AF20,'Acmite',IF(AF8>0,'Both','Na2SiO3')),'None')

            if self.DataCalculating['Cl'][i] <= 0:
                ACorN = 'None'
            else:
                if self.DataCalculating['Fe2O3'][i] >= self.DataCalculating['Cl'][i]:
                    ACorN = 'Acmite'
                else:
                    if self.DataCalculating['Fe2O3'][i] > 0:
                        ACorN = 'Both'
                    else:
                        ACorN = 'Na2SiO3'

            # =IF(AG26='Acmite',AF20,IF(AG26='Both',AF8,0))


            # =IF(AG26='Na2SiO3',AF20,IF(AG26='Both',AF20-AG19,0))

            if ACorN == 'Acmite':
                self.DataCalculating['F'][i] = self.DataCalculating['Cl'][i]
                self.DataCalculating['Cl'][i] = 0

            elif ACorN == 'Na2SiO3':
                self.DataCalculating['Cl'][i] = self.DataCalculating['Cl'][i]
                self.DataCalculating['F'][i] = 0

            elif ACorN == 'Both':
                self.DataCalculating['F'][i] = self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Cl'][i] = self.DataCalculating['Cl'][i] - self.DataCalculating['F'][i]

            elif ACorN == 'None':
                self.DataCalculating['F'][i] = 0
                self.DataCalculating['Cl'][i] = 0

            self.DataCalculating['Fe2O3'][i] -= self.DataCalculating['F'][i]

            Acmite = self.DataCalculating['F'][i]

            # =IF(AG8>0,IF(AG9>=AG8,'Magnetite',IF(AG9>0,'Both','Hematite')),'None')


            if self.DataCalculating['Fe2O3'][i] <= 0:
                MorH = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['Fe2O3'][i]:
                    MorH = 'Magnetite'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        MorH = 'Both'
                    else:
                        MorH = 'Hematite'

            # =IF(AH26='Magnetite',AG8,IF(AH26='Both',AG9,0))
            # =IF(AH26='Hematite',AG8,IF(AH26='Both',AG8-AG9,0))



            if MorH == 'Magnetite':
                self.DataCalculating['Fe2O3'][i] = self.DataCalculating['Fe2O3'][i]
                self.DataCalculating['Ba'][i] = 0

            elif MorH == 'Hematite':
                self.DataCalculating['Fe2O3'][i] = 0
                self.DataCalculating['Ba'][i] = self.DataCalculating['FeO'][i]


            elif MorH == 'Both':
                self.DataCalculating['Fe2O3'][i] = self.DataCalculating['FeO'][i]
                self.DataCalculating['Ba'][i] = self.DataCalculating['Fe2O3'][i] - self.DataCalculating['FeO'][i]


            elif MorH == 'None':
                self.DataCalculating['Fe2O3'][i] = 0
                self.DataCalculating['Ba'][i] == 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['Fe2O3'][i]

            Magnetite = self.DataCalculating['Fe2O3'][i]
            Hematite = self.DataCalculating['Ba'][i]

            # =IF(AH11>0,AH11/(AH11+AH9),0)

            Fe2 = self.DataCalculating['FeO'][i]
            Mg = self.DataCalculating['MgO'][i]

            if Mg > 0:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 100 * Mg / (Mg + Fe2)})
            else:
                self.DataCalced[k].update({'Mg/(Mg+Fe2+) in silicates': 0})

            self.DataCalculating['FeO'][i] += self.DataCalculating['MgO'][i]

            self.DataCalculating['MgO'][i] = 0

            # =IF(AI12>0,IF(AI9>=AI12,'Diopside',IF(AI9>0,'Both','Wollastonite')),'None')


            if self.DataCalculating['CaO'][i] <= 0:
                DorW = 'None'
            else:
                if self.DataCalculating['FeO'][i] >= self.DataCalculating['CaO'][i]:
                    DorW = 'Diopside'
                else:
                    if self.DataCalculating['FeO'][i] > 0:
                        DorW = 'Both'
                    else:
                        DorW = 'Wollastonite'

            # =IF(AJ26='Diopside',AI12,IF(AJ26='Both',AI9,0))

            # =IF(AJ26='Wollastonite',AI12,IF(AJ26='Both',AI12-AI9,0))



            if DorW == 'Diopside':
                self.DataCalculating['CaO'][i] = self.DataCalculating['CaO'][i]
                self.DataCalculating['S'][i] = 0

            elif DorW == 'Wollastonite':
                self.DataCalculating['S'][i] = self.DataCalculating['CaO'][i]
                self.DataCalculating['CaO'][i] = 0

            elif DorW == 'Both':
                self.DataCalculating['S'][i] = self.DataCalculating['CaO'][i] - self.DataCalculating['FeO'][i]
                self.DataCalculating['CaO'][i] = self.DataCalculating['FeO'][i]

            elif DorW == 'None':
                self.DataCalculating['CaO'][i] = 0
                self.DataCalculating['S'][i] = 0

            self.DataCalculating['FeO'][i] -= self.DataCalculating['CaO'][i]

            Diopside = self.DataCalculating['CaO'][i]

            Quartz = self.DataCalculating['SiO2'][i]

            Zircon = self.DataCalculating['Zr'][i]
            K2SiO3 = self.DataCalculating['P2O5'][i]

            Na2SiO3 = self.DataCalculating['Cl'][i]

            Sphene = self.DataCalculating['MnO'][i]

            Hypersthene = self.DataCalculating['FeO'][i]

            Albite = self.DataCalculating['Na2O'][i]

            Orthoclase = self.DataCalculating['K2O'][i]

            Wollastonite = self.DataCalculating['S'][i]

            # =AJ5-(AL6)-(AL7)-(AL8*2)-(AL12)-(AL9)-(AL10*4)-(AL11*2)-(AL13)-(AL14*6)-(AL15*6)-(AL16)

            Quartz -= (Zircon +
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

            if Quartz > 0:
                Quartz = Quartz
            else:
                Quartz = 0

            # =IF(AL13>0,IF(AL5>=0,'Hypersthene',IF(AL13+(2*AL5)>0,'Both','Olivine')),'None')

            if Hypersthene <= 0:
                HorO = 'None'
            else:
                if Quartz >= 0:
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
            Quartz += Old_Hypersthene - (Hypersthene + Olivine)

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
                self.DataCalced[k].update({'Plagioclase An content': 0})
            else:
                self.DataCalced[k].update({'Plagioclase An content': 100 * Anorthite / (Anorthite + 2 * Albite)})

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



            WholeVolume=0

            for i in self.Minerals:# Calculate the Weight Pecentage of Minerals
                exec('self.DataResult[k].update({\'' + i + '\':' + i + '}) ')

                if i == 'Q':
                    m = 'Quartz'
                    tmpcmdW='self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]}) '
                    exec(tmpcmdW)

                elif i == 'A':
                    m = 'Orthoclase'
                    tmpcmdW='self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + m + '\'][0]}) '
                    exec(tmpcmdW)

                elif i == 'P':
                    a = 'Anorthite'
                    b = 'Albite'
                    tmpcmdW='self.DataWeight[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]+' + b + '*self.DataBase[\'' + b + '\'][0]}) '
                    #print(tmpcmdW, '\n')
                    exec(tmpcmdW)

                elif i == 'F':
                    a = 'Nepheline'
                    b = 'Leucite'
                    c = 'Kalsilite'

                    exec(
                        'self.DataWeight[k].update({\'' + i + '\':' + a + '*self.DataBase[\'' + a + '\'][0]+' + b + '*self.DataBase[\'' + b + '\'][0]+' + c + '*self.DataBase[\'' + c + '\'][0]}) ')

                if i not in ['Q', 'A', 'P', 'F', ]:
                    exec('self.DataWeight[k].update({\'' + i + '\':' + i + '*self.DataBase[\'' + i + '\'][0]}) ')

            for i in self.Minerals:# Calculate the Whole Volume of Minerals

                self.tmpVolume = 0
                tmpcmdAccV='self.tmpVolume  =  '+ i + '*self.DataBase[\'' + i + '\'][0]/self.DataBase[\'' + i + '\'][1]'
                if i not in ['Q', 'A', 'P', 'F', ]:
                    exec(tmpcmdAccV)
                    if self.tmpVolume != 0:
                        pass
                        #print(tmpcmdAccV, '\t', self.tmpVolume)

                WholeVolume= WholeVolume+ self.tmpVolume

                #print(WholeVolume)

            for i in self.Minerals:# Calculate the Volume Pecentage of Minerals

                if i == 'Q':
                    m = 'Quartz'
                    tmpcmdV='self.DataVolume[k].update({\'' + i + '\':' + i + '*100* self.DataBase[\'' + m + '\'][0]/(self.DataBase[\'' + m + '\'][1]*WholeVolume)}) '
                    exec(tmpcmdV)

                elif i == 'A':
                    m = 'Orthoclase'
                    tmpcmdV='self.DataVolume[k].update({\'' + i + '\':' + i + '*100* self.DataBase[\'' + m + '\'][0]/(self.DataBase[\'' + m + '\'][1]*WholeVolume)}) '
                    exec(tmpcmdV)

                elif i == 'P':
                    a = 'Anorthite'
                    b = 'Albite'
                    tmpcmdV = (
                            'self.DataVolume[k].update({\'' + i + '\':100/WholeVolume*(' + a + '*self.DataBase[\'' + a + '\'][0]/self.DataBase[\'' + a + '\'][1]+' + b + '*self.DataBase[\'' + b + '\'][0]/self.DataBase[\'' + b + '\'][1])}) ')
                    #print(tmpcmdV,'\n')
                    exec(tmpcmdV)

                elif i == 'F':
                    a = 'Nepheline'
                    b = 'Leucite'
                    c = 'Kalsilite'

                    tmpcmdV= (
                        'self.DataVolume[k].update({\'' + i + '\':100/WholeVolume*(' + a + '*self.DataBase[\'' + a + '\'][0]/self.DataBase[\'' + a + '\'][1]+' + b + '*self.DataBase[\'' + b + '\'][0]/self.DataBase[\'' + b + '\'][1]+' + c + '*self.DataBase[\'' + c + '\'][0]/self.DataBase[\'' + c + '\'][1])}) ')
                    #print(tmpcmdV,'\n')
                    exec(tmpcmdV)



                if i not in ['Q', 'A', 'P', 'F', ]:
                    exec(
                        'self.DataVolume[k].update({\'' + i + '\':' + i + '* 100 *self.DataBase[\'' + i + '\'][0]/(self.DataBase[\'' + i + '\'][1]*WholeVolume)}) ')

            self.DI = 0
            # for i in ['Quartz', 'Anorthite', 'Albite', 'Orthoclase', 'Nepheline', 'Leucite', 'Kalsilite']:
            # exec('self.DI+=' + i + '*self.DataBase[\'' + i + '\'][0]')

            exec('self.DI= Quartz +  Anorthite +  Albite +  Orthoclase +  Nepheline +  Leucite +  Kalsilite ')
            DI = Quartz + Anorthite + Albite + Orthoclase + Nepheline + Leucite + Kalsilite

            # print('\n\n DI is\n',DI,'\n\n')
            self.DataCalced[k].update({'Differentiation Index': DI})


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


    def CIPW(self):

        self.Calc()
        a = []
        a.append(self.WriteData(target='DataResult'))
        a.append(self.WriteData(target='DataWeight'))
        a.append(self.WriteData(target='DataVolume'))
        a.append(self.WriteCalced(target='DataCalced'))




        tmp = a[0]
        labels = tmp[0]
        newtmp = []
        for s in range(len(tmp)):
            if s != 0:
                newtmp.append(tmp[s])



        self.newdf=self.ReduceSize(pd.DataFrame.from_records(newtmp, columns=labels))
        self.newdf.rename(columns= lambda x: x if x in ['Label'] else x[0:]+' (Mole)', inplace=True)


        tmp1 = a[1]
        labels1 = tmp1[0]
        newtmp1 = []
        for s in range(len(tmp1)):
            if s != 0:
                newtmp1.append(tmp1[s])

        self.newdf1 = self.ReduceSize(pd.DataFrame.from_records(newtmp1, columns=labels1))
        self.newdf1.rename(columns= lambda x: x if x in ['Label'] else x[0:]+' (Mass)', inplace=True)





        tmp2 = a[2]
        labels2 = tmp2[0]
        newtmp2 = []
        for s in range(len(tmp2)):
            if s != 0:
                newtmp2.append(tmp2[s])
        self.useddf = pd.DataFrame.from_records(newtmp2, columns=labels2)
        self.newdf2 = self.ReduceSize(self.useddf)

        self.newdf2.rename(columns= lambda x: x if x in ['Label','Q','A','P','F'] else x[0:]+' (Volume)', inplace=True)



        tmp3 = a[3]
        labels3 = tmp3[0]
        newtmp3 = []
        for s in range(len(tmp3)):
            if s != 0:
                newtmp3.append(tmp3[s])

        self.newdf3 = self.ReduceSize(pd.DataFrame.from_records(newtmp3, columns=labels3))

        self.newdf = self.DropUseless(self.newdf)

        self.newdf1 = self.DropUseless(self.newdf1)


        self.WholeResult = pd.concat([self.newdf,self.newdf1,self.newdf2,self.newdf3], axis=1)

        self.WholeResult = self.WholeResult.T.groupby(level=0).first().T

        self.model = PandasModel(self.WholeResult)
        self.tableView.setModel(self.model)

        self.newdf = self.newdf.set_index('Label')
        self.newdf1 = self.newdf1.set_index('Label')
        self.newdf2 = self.newdf2.set_index('Label')
        self.newdf3 = self.newdf3.set_index('Label')

        self.OutPutData = self.WholeResult


        


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
                self.newdf.to_csv(DataFileOutput + '-cipw-mole.csv', sep=',', encoding='utf-8')
                self.newdf1.to_csv(DataFileOutput + '-cipw-mass.csv', sep=',', encoding='utf-8')
                self.newdf2.to_csv(DataFileOutput + '-cipw-volume.csv', sep=',', encoding='utf-8')
                self.newdf3.to_csv(DataFileOutput + '-cipw-index.csv', sep=',', encoding='utf-8')
                

            elif ('xlsx' in DataFileOutput):

                DataFileOutput = DataFileOutput[0:-5]

                #self.newdf.to_excel(DataFileOutput, encoding='utf-8')

                self.newdf.to_excel(DataFileOutput + '-cipw-mole.xlsx',  encoding='utf-8')
                self.newdf1.to_excel(DataFileOutput + '-cipw-mass.xlsx',  encoding='utf-8')
                self.newdf2.to_excel(DataFileOutput + '-cipw-volume.xlsx',  encoding='utf-8')
                self.newdf3.to_excel(DataFileOutput + '-cipw-index.xlsx', encoding='utf-8')