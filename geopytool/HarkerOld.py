from ImportDependence import *
from CustomClass import *

class HarkerOld(AppForm):
    Lines = []
    Tags = []
    description = 'Classical Harker diagram'
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

    itemstocheck = ['Al2O3', 'MgO', 'FeO', 'Fe2O3','CaO', 'Na2O', 'K2O', 'TiO2', 'P2O5', 'SiO2']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Classical Harker diagram')

        self.FileName_Hint='Harker'

        self.items = []

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Classical Harker diagram')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()
        self.create_status_bar()


    def Check(self):

        row = self._df.index.tolist()
        col = self._df.columns.tolist()
        itemstocheck = self.itemstocheck
        checklist = list((set(itemstocheck).union(set(col))) ^ (set(itemstocheck) ^ set(col)))
        if len(checklist) >= (len(itemstocheck)-1) and ('FeO' in checklist or 'Fe2O3' in checklist):
            self.OutPutCheck = True
        else:
            self.OutPutCheck = False
        return(self.OutPutCheck)

    def create_main_frame(self):
        self.resize(800, 1000)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig ,self.axes= plt.subplots(4, 2,figsize=(15, 20),dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.2, wspace=0.4,left=0.1, bottom=0.2, right=0.7, top=0.95)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        
        self.save_img_button = QPushButton('&Save IMG')
        self.save_img_button.clicked.connect(self.saveImgFile)

        self.seter_left_label = QLabel('Left')
        self.seter_left = QLineEdit(self)
        self.seter_left.textChanged[str].connect(self.HarkerOld)
        self.seter_right_label = QLabel('Right')
        self.seter_right = QLineEdit(self)
        self.seter_right.textChanged[str].connect(self.HarkerOld)


        #self.result_button = QPushButton('&Result')
        #self.result_button.clicked.connect(self.HarkerOld)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.HarkerOld)  # int



        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.seter_left_label ,self.seter_left,self.seter_right_label ,self.seter_right, self.legend_cb,self.save_img_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)


        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference+self.description)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        w=self.width()
        h=self.height()

        self.seter_left_label.setFixedWidth(w / 20)
        self.seter_left.setFixedWidth(w / 20)
        self.seter_right_label.setFixedWidth(w / 20)
        self.seter_right.setFixedWidth(w / 20)

    def HarkerOld(self):

        self.WholeData = []

        #raw = self._df



        raw = self.CleanDataFile(self._df)


        itemstoshow = [r'$Al_2O_3$', r'$MgO$', r'$Fe2O3_{Total}$', r'$CaO$', r'$Na_2O$', r'$K_2O$', r'$TiO_2$', r'$P_2O_5$', r'$SiO_2$', ]

        self.axes[0, 0].clear()
        #self.axes[0, 0].set_xlim(45, 75)
        self.axes[0, 0].set_ylabel(itemstoshow[0])
        self.axes[0,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[0, 0].set_xticklabels('')

        self.axes[0, 1].clear()
        #self.axes[0, 1].set_xlim(45, 75)
        self.axes[0, 1].set_ylabel(itemstoshow[1])
        self.axes[0,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[0, 1].set_xticklabels('')

        self.axes[1,0].clear()
        #self.axes[1,0].set_xlim(45, 75)
        self.axes[1,0].set_ylabel(itemstoshow[2])
        self.axes[1,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[1, 0].set_xticklabels('')


        self.axes[1,1].clear()
        #self.axes[1,1].set_xlim(45, 75)
        self.axes[1,1].set_ylabel(itemstoshow[3])
        self.axes[1,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[1, 1].set_xticklabels('')

        self.axes[2,0].clear()
        #self.axes[2,0].set_xlim(45, 75)
        self.axes[2,0].set_ylabel(itemstoshow[4])
        self.axes[2,0].set_xticks([45,50,55,60,65,70,75])
        self.axes[2, 0].set_xticklabels('')

        self.axes[2,1].clear()
        #self.axes[2,1].set_xlim(45, 75)
        self.axes[2,1].set_ylabel(itemstoshow[5])
        self.axes[2,1].set_xticks([45,50,55,60,65,70,75])
        self.axes[2, 1].set_xticklabels('')

        self.axes[3,0].clear()
        #self.axes[3,0].set_xlim(45, 75)
        self.axes[3,0].set_ylabel(itemstoshow[6])
        self.axes[3, 0].set_xticks([45,50,55,60,65,70,75])

        self.axes[3, 0].set_xticklabels([45,50,55,60,65,70,75])

        self.axes[3,0].set_xlabel(itemstoshow[8])



        self.axes[3,1].clear()
        #self.axes[3,1].set_xlim(45, 75)
        self.axes[3,1].set_ylabel(itemstoshow[7])
        self.axes[3, 1].set_xticks([45,50,55,60,65,70,75])

        self.axes[3, 1].set_xticklabels([45,50,55,60,65,70,75])

        self.axes[3,1].set_xlabel(itemstoshow[8])



        try:
            left = float(self.seter_left.text())
            # if( type(left) == int or type(left)== float or type(left)== np.float ):pass
            self.axes[0, 1].set_xlim(left=left)
            self.axes[0, 0].set_xlim(left=left)
            self.axes[1, 0].set_xlim(left=left)
            self.axes[1, 1].set_xlim(left=left)
            self.axes[2, 0].set_xlim(left=left)
            self.axes[2, 1].set_xlim(left=left)
            self.axes[3, 0].set_xlim(left=left)
            self.axes[3, 1].set_xlim(left=left)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))



        try:
            right = float(self.seter_right.text())
            self.axes[0, 1].set_xlim(right=right)
            self.axes[0, 0].set_xlim(right=right)
            self.axes[1, 0].set_xlim(right=right)
            self.axes[1, 1].set_xlim(right=right)
            self.axes[2, 0].set_xlim(right=right)
            self.axes[2, 1].set_xlim(right=right)
            self.axes[3, 0].set_xlim(right=right)
            self.axes[3, 1].set_xlim(right=right)
            pass
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))

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


            Al2O3, MgO, FeO, Fe2O3, CaO, Na2O, K2O, TiO2, P2O5, SiO2 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

            Al2O3 = raw.at[i,'Al2O3']
            MgO = raw.at[i, 'MgO']
            CaO = raw.at[i,'CaO']
            Na2O = raw.at[i, 'Na2O']
            K2O = raw.at[i, 'K2O']
            TiO2 = raw.at[i, 'TiO2']
            P2O5 = raw.at[i, 'P2O5']
            SiO2 = raw.at[i, 'SiO2']

            if ('FeO' in raw.columns.tolist()):
                FeO=raw.at[i, 'FeO']

            if ('Fe2O3' in raw.columns.tolist()):
                Fe2O3=raw.at[i, 'Fe2O3']

            FeTotal= FeO/72*80+Fe2O3

            if ('TFeO' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFeO']

            if ('TFe2O3' in raw.columns.tolist()):
                FeTotal=raw.at[i, 'TFe2O3']



            self.axes[0, 0].scatter(SiO2, Al2O3, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[0, 1].scatter(SiO2, MgO, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[1, 0].scatter(SiO2, FeTotal, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[1, 1].scatter(SiO2, CaO, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[2, 0].scatter(SiO2, Na2O, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[2, 1].scatter(SiO2, K2O, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[3, 0].scatter(SiO2, TiO2, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

            self.axes[3, 1].scatter(SiO2, P2O5, marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)





        if (self.legend_cb.isChecked()):
            self.axes[0, 1].legend(bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0, prop=fontprop)







        self.canvas.draw()


        self.OutPutTitle='Classical Harker diagram'

        self.OutPutFig=self.fig
