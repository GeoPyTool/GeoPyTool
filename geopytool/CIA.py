from ImportDependence import *
from CustomClass import *


class CIA(AppForm):
    useddf=pd.DataFrame()
    Lines = []
    Tags = []
    description = 'Chemical Index of Alteration'
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


    reference = '''
        CIA = [Al2O3/(Al2O3+CaO*+Na2O+K2O]×100    
        ICV = (Fe2O3+K2O+Na2O+CaO*+MgO+MnO+TiO2)/Al2O3 (Cox,1995)    
        PIA = {(Al2O3-K2O)/[(Al2O3-K2O)+CaO*+Na2O]}×100
        CIW = [Al2O3/(Al2O3+CaO*+Na2O)]×100
        CIW' = [Al2O3/(Al2O3+Na2O)]×100
                   
        where CaO* is the amount of CaO incorporated in the silicate fraction of the rock.
        CaO* = CaO - (10/3 * P2O5)        
        if CaO* < Na2O:
            CaO* = CaO*
        else:
            CaO* = Na2O
         
        
        
        References:
        Nesbitt-CIA-1982
        Harnois-CIW-1988
        Mclennan-CIA-1993
        Cox R-ICV-1995
        Fedo-PIA-1995
        Cullers-CIW'-2000
        Song B W-2013
        
        Cox R, Lowe D R, Cullers R L. The influence of sediment recycling and basement composition on evolution of mudrock chemistry in the southwestern United States[J]. Geochimica Et Cosmochimica Acta, 1995, 59(14):2919-2940.
        Harnois, L., 1988, The CIW index: A new chemical index of weathering: Sedimentary Geology, v. 55, p. 319–322. doi:10.1016/0037-0738(88)90137-6
        Nesbitt, H.W., and Young, G.M., 1982, Early Proterozoic climates and plate motions inferred from major element chemistry of lutites: Nature, v. 299, p. 715–717. doi:10.1038/299715a0
        '''


    BaseMass  = {'SiO2': 60.083,
                 'TiO2': 79.865,
                 'Al2O3': 101.960077,
                 'TFe2O3': 159.687,
                 'Fe2O3': 159.687,
                 'TFeO': 71.844,
                 'FeO': 71.844,
                 'MnO': 70.937044,
                 'MgO': 40.304,
                 'CaO': 56.077000000000005,
                 'Na2O': 61.978538560000004,
                 'K2O': 94.1956,
                 'P2O5': 141.942523996,
                 'CO2': 44.009,
                 'SO3': 80.057,
                 'FeO': 71.844,
                 'Fe3O4': 231.531,
                 'BaO': 153.326,
                 'SrO': 103.619,
                 'Cr2O3': 151.98919999999998,
                 }

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Chemical Index of Alteration & Index of Compositional Variability')

        self.items = []

        self._df = df
        self._df.reindex()

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to CIA')

        self.raw = df



        self.raw = self.CleanDataFile(df)



        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):
        self.resize(800,600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('Chemical Index of Alteration & Index of Compositional Variability')

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)


        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)
        # Other GUI controls
        self.save_button = QPushButton('&Save')

        self.save_button.clicked.connect(self.saveDataFile)
        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)
        #self.vbox.addWidget(self.tableView)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.textbox)
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

    def CIA(self):

        self.WholeData = []
        dataframe=pd.DataFrame()

        dataframe = self._df

        #dataframe.set_index('Label')




        ItemsAvalibale = dataframe.columns.values.tolist()
        Indexes = dataframe.index.values.tolist()


        #ItemsToCheck = ['Label','SiO2','Al2O3','Fe2O3','MgO','CaO','Na2O','K2O','P2O5','MnO','TiO2']
        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']


        for i in ItemsAvalibale:
            if 'O' not in i and i !='Label':
                dataframe = dataframe.drop(i, 1)



        WholeItemsAvalibale = dataframe.columns.values.tolist()

        ItemsAvalibale = dataframe.columns.values.tolist()
        Indexes = dataframe.index.values.tolist()

        if 'Whole' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('Whole')

        if 'CIA' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('CIA')

        if 'ICV' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('ICV')

        if 'PIA' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('PIA')

        if 'CIW' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('CIW')
        if 'CIW\'' not in WholeItemsAvalibale:
            WholeItemsAvalibale.append('CIW\'')





        print('index',Indexes,'\ncolums',WholeItemsAvalibale)



        WholeMole=[]
        WholeList=[]

        dataframe =  dataframe.dropna(axis=1,how='all')

        print(dataframe)


        for j in Indexes:
            tmpList=[]
            tmpMoleSum=0
            tmpcia=0
            tmpAl2O3=0
            tmpCaO=0
            tmpNa2O=0
            tmpK2O=0
            tmpP2O5=0
            tmpFe2O3=0
            tmpMgO=0
            tmpMnO=0
            tmpTiO2=0


            #ICV =(Fe2O3+K2O+Na2O+CaO*+MgO+MnO+TiO2)/Al2O3 (Cox,1995)


            for i in ItemsAvalibale:

                if i in self.BaseMass:

                    m=dataframe.at[j,i]
                    n=self.BaseMass[i]

                    #print('\nm & n is \t',m,n)
                    tmpmole= m/n

                    #print(tmpmole)
                    tmpMoleSum = tmpMoleSum + tmpmole
                    #tmpList.append(dataframe.at[i,j])


            #print('\n total mole is',tmpMoleSum)


            for i in ItemsAvalibale:
                if i in self.BaseMass:
                    tmpdata= 100*(dataframe.at[j,i]/self.BaseMass[i])/tmpMoleSum
                    tmpList.append(tmpdata)

                    #print(i, tmpdata)


                    if i =='Al2O3':
                        tmpAl2O3=tmpdata

                    elif i =='CaO':
                        tmpCaO=tmpdata

                    elif i =='Na2O':
                        tmpNa2O = tmpdata
                    elif i =='K2O':
                        tmpK2O=tmpdata

                    elif i =='P2O5':
                        tmpP2O5=tmpdata

                    elif i =='Fe2O3':
                        tmpFe2O3=tmpdata

                    elif i == 'MgO':
                        tmpMgO = tmpdata
                    elif i == 'MnO':
                        tmpMnO = tmpdata
                    elif i == 'TiO2':
                        tmpTiO2 = tmpdata








                elif i == 'Label' :
                    tmpdata = dataframe.at[j,i]
                    tmpList.append(tmpdata)
                elif i in WholeItemsAvalibale:
                    del WholeItemsAvalibale[WholeItemsAvalibale.index(i)]


            tmpList.append(tmpMoleSum)




            usedCaO=0

            middleCaO= tmpCaO-(10/3.0*tmpP2O5)

            if middleCaO< tmpNa2O:
                usedCaO=middleCaO
            else:
                usedCaO=tmpNa2O

            #print(tmpAl2O3, usedCaO, tmpK2O, tmpNa2O)



            CIA=tmpAl2O3/(tmpAl2O3+usedCaO+tmpNa2O+tmpK2O)*100
            tmpList.append(CIA)

            ICV =(tmpFe2O3+tmpK2O+tmpNa2O+usedCaO+tmpMgO+tmpMnO+tmpTiO2)/tmpAl2O3 #(Cox,1995)
            tmpList.append(ICV)

            PIA = ((tmpAl2O3-tmpK2O)/(tmpAl2O3-tmpK2O+usedCaO+tmpNa2O))*100
            tmpList.append(PIA)

            CIW = (tmpAl2O3/(tmpAl2O3+usedCaO+tmpNa2O))*100
            tmpList.append(CIW)

            CIW2 = (tmpAl2O3/(tmpAl2O3+tmpNa2O))*100
            tmpList.append(CIW2)


            '''
            CIA = [Al2O3/(Al2O3+CaO*+Na2O+K2O]×100    
            ICV = (Fe2O3+K2O+Na2O+CaO*+MgO+MnO+TiO2)/Al2O3 (Cox,1995)    
            PIA = {(Al2O3-K2O)/[(Al2O3-K2O)+CaO*+Na2O]}×100
            CIW = [Al2O3/(Al2O3+CaO*+Na2O)]×100
            CIW' = [Al2O3/(Al2O3+Na2O)]×100   
            '''

            #print(len(tmpList))
            WholeList.append(tmpList)
            pass




        print(len(WholeList))
        print(len(WholeItemsAvalibale))

        df = pd.DataFrame(WholeList,columns=WholeItemsAvalibale)
        self.useddf = df

        self.tableView.setModel(PandasModel(self.useddf))



        self.show()

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.useddf.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.useddf.to_excel(DataFileOutput, encoding='utf-8')