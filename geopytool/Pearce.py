from ImportDependence import *
from CustomClass import *

class Pearce(AppForm):

    reference = 'Reference: Pearce, J. A., Harris, N. B. W., and Tindle, A. G., 1984, Trace Element Discrimination Diagrams for the Tectonic Interpretation of Granitic Rocks: Journal of Petrology, v. 25, no. 4, p. 956-983.'
    Lines = []
    Tags = []
    title = 'Pearce diagram (after Julian A. Pearce et al., 1984).'

    description = '\n syn-COLG: syn-collision granites\t VAG: volcanic arc granites\n WPG: within plate granites\t ORG: ocean ridge granites  \n '

    itemstocheck = [u'Y', u'Yb', u'Nb', u'Rb', u'Ta']

    text = [u'0.1', u'1', u'10', u'100', u'1000', u'10000', u'100000', u'1000000', u'10000000']

    Condation0 = {'BaseLines': [[(2, 80), (55, 300)],
                                [(55, 300), (400, 2000)],
                                [(55, 300), (51.5, 8)],
                                [(51.5, 8), (50, 1)],
                                [(51.5, 8), (2000, 400)], ],
                  'xLabel': r'Y+Nb (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(1, 3), (1, 1), (2.4, 2.4), (3, 1)],
                  }

    Condation1 = {'BaseLines': [[(0.5, 140), (6, 200)],
                                [(6, 200), (50, 2000)],
                                [(6, 200), (6, 8)],
                                [(6, 8), (6, 1)],
                                [(6, 8), (200, 400)], ],
                  'xLabel': r'Yb+Ta (PPM)',
                  'yLabel': r'Rb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 3), (0.5, 1), (1.5, 2.4), (2, 1)],
                  }

    Condation2 = {'BaseLines': [[(1, 2000), (50, 10)],
                                [(40, 1), (50, 10)],
                                [(50, 10), (1000, 100)],
                                [(25, 25), (1000, 400)], ],
                  'xLabel': r'Y (PPM)',
                  'yLabel': r'Nb (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(0.5, 1.5), (0.5, 2), (2, 2), (2.2, 0.5)],
                  }

    Condation3 = {'BaseLines': [[(0.55, 20), (3, 2)],
                                [(0.1, 0.35), (3, 2)],
                                [(3, 2), (5, 1)],
                                [(5, 0.05), (5, 1)],
                                [(5, 1), (100, 7)],
                                [(3, 2), (100, 20)], ],
                  'xLabel': r'Yb (PPM)',
                  'yLabel': r'Ta (PPM)',
                  'Labels': [u'syn-COLG', u'VAG', u'WPG', u'ORG'],
                  'Locations': [(-0.5, 0.1), (-0.5, -1), (0.7, 1), (1.5, 0)],
                  }

    condation = [Condation0, Condation1, Condation2, Condation3]

    LocationAreas0 = [ [[2, 80], [55, 300],[400,2000],[2,2000]],
                      [[400, 2000],[55, 300],[51.5,8],[2000,400],[2000,2000]],
                      [[2, 80], [55, 300], [51.5, 8], [50, 1],[2,1]],
                      [[50, 1],[51.5, 8],[2000,400],[2000,1]],
                      ]

    ItemNames0 =[u'syn-COLG', u'WPG', u'VAG', u'ORG']


    LocationAreas1 = [[[0.5, 140], [6, 200], [50, 2000],[0.5,2000]],
                      [[50, 2000],[6, 200], [6, 8],[200, 400],[200,2000]],
                      [[0.5, 140],[6, 200], [6,8],[6,1],[0.5,1]],
                      [[6, 1], [6, 8],[200, 400],[200,1]],
                      ]

    ItemNames1 =[u'syn-COLG', u'WPG', u'VAG', u'ORG']


    LocationAreas2 = [[[1, 2000], [25, 25],[1000, 400],[1000,2000]],
                      [[1000,400],[25, 25], [50, 10], [1000, 100]],
                      [[40, 1],[50,10], [1000, 100],[1000,1]],
                      ]

    ItemNames2 =[u'WPG', u'ORG', u'VAG_or_syn-COLG']


    LocationAreas3 = [[[0.55, 20], [3, 2],[0.1, 0.35],[0.1,20]],
                      [[0.55, 20], [3, 2], [100,20]],
                      [[0.1, 0.35], [3, 2],[5,1],[5,0.05],[0.1,0.05]],
                      [[100,20],[3, 2], [5, 1],[100,7]],
                      [[5, 0.05], [5, 1],[100,7],[100,0.05]],
                      ]

    ItemNames3 =[u'syn-COLG', u'WPG1', u'VAG',u'WPG2', u'ORG']

    AreasHeadClosed = []
    SelectDic0 = {}
    SelectDic1 = {}
    SelectDic2 = {}
    SelectDic3 = {}


    def __init__(self, parent=None, df=pd.DataFrame()):
        QWidget.__init__(self, parent)
        self.setWindowTitle(self.title)


        self.FileName_Hint = 'Pearce'
        self._df = df
        self._df_back = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')

        self.AllLabel = []

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        for i in range(len(self.LocationAreas0)):
            tmpi = self.LocationAreas0[i] + [self.LocationAreas0[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic0[self.ItemNames0[i]] = tmppath

        for i in range(len(self.LocationAreas1)):
            tmpi = self.LocationAreas1[i] + [self.LocationAreas1[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic1[self.ItemNames1[i]] = tmppath

        for i in range(len(self.LocationAreas2)):
            tmpi = self.LocationAreas2[i] + [self.LocationAreas2[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic2[self.ItemNames2[i]] = tmppath

        for i in range(len(self.LocationAreas3)):
            tmpi = self.LocationAreas3[i] + [self.LocationAreas3[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)
            self.SelectDic3[self.ItemNames3[i]] = tmppath


        self.create_main_frame()
        self.create_status_bar()


    def create_main_frame(self):

        self.resize(900, 900)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig ,self.axes= plt.subplots(2, 2,figsize=(16.0, 16.0),dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5,left=0.1, bottom=0.2, right=0.8, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)


        self.result_button = QPushButton('&Classification Result')
        self.result_button.clicked.connect(self.Explain)


        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Pearce)  # int


        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.Pearce)  # int


        self.show_data_index_cb = QCheckBox('&Show Data Index')
        self.show_data_index_cb.setChecked(False)
        self.show_data_index_cb.stateChanged.connect(self.Pearce)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.result_button,self.legend_cb,  self.detail_cb,self.show_data_index_cb]:
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


    def customDrawLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                 alpha=0.5):
        x = []
        y = []

        label = linelabel

        for i in l:
            x.append(i[0])
            y.append(i[1])

        return (x, y)

    def customDrawLogLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                    alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(math.log(i[0], 10))
            y.append(math.log(i[1], 10))

        return (x, y)


    def Pearce(self):

        self.WholeData = []

        #raw = self._df

        raw = self.CleanDataFile(self._df)


        self.axes[0, 0].clear()
        #self.axes[0, 0].axis('off')

        self.axes[0, 0].set_xlabel(self.condation[0]['xLabel'])
        self.axes[0, 0].set_ylabel(self.condation[0]['yLabel'])

        self.axes[0, 0].set_xlim(0.3, 3.2)
        self.axes[0, 0].set_xticks([ 1, 2, 3])
        self.axes[0, 0].set_xticklabels([ 10,  100, 1000])

        self.axes[0, 0].set_ylim(0, 3.2)
        self.axes[0, 0].set_yticks([0, 1, 2, 3])
        self.axes[0, 0].set_yticklabels([1, 10,  100, 1000])

        self.axes[0, 0].spines['right'].set_color('none')
        self.axes[0, 0].spines['top'].set_color('none')


        self.axes[0, 1].clear()
        #self.axes[0, 1].axis('off')

        self.axes[0, 1].set_xlabel(self.condation[1]['xLabel'])
        self.axes[0, 1].set_ylabel(self.condation[1]['yLabel'])

        self.axes[0, 1].set_xlim(-0.2, 2.5)
        self.axes[0, 1].set_xticks([0, 1, 2])
        self.axes[0, 1].set_xticklabels([1, 10, 100])

        self.axes[0, 1].set_ylim(0, 3.2)
        self.axes[0, 1].set_yticks([0, 1, 2, 3])
        self.axes[0, 1].set_yticklabels([1, 10, 100, 1000])

        self.axes[0, 1].spines['right'].set_color('none')
        self.axes[0, 1].spines['top'].set_color('none')




        self.axes[1,0].clear()
        #self.axes[1,0].axis('off')

        self.axes[1,0].set_xlabel(self.condation[2]['xLabel'])
        self.axes[1,0].set_ylabel(self.condation[2]['yLabel'])



        self.axes[1, 0].set_xlim(0, 3.2)
        self.axes[1, 0].set_xticks([0, 1, 2, 3])
        self.axes[1, 0].set_xticklabels([1, 10,  100, 1000])

        self.axes[1, 0].set_ylim(0, 3.2)
        self.axes[1, 0].set_yticks([0, 1, 2, 3])
        self.axes[1, 0].set_yticklabels([1, 10,  100, 1000])

        self.axes[1, 0].spines['right'].set_color('none')
        self.axes[1, 0].spines['top'].set_color('none')


        self.axes[1,1].clear()
        #self.axes[1,1].axis('off')

        self.axes[1,1].set_xlabel(self.condation[3]['xLabel'])
        self.axes[1,1].set_ylabel(self.condation[3]['yLabel'])



        self.axes[1, 1].set_xlim(-1, 2)
        self.axes[1, 1].set_xticks([-1, 0, 1, 2])
        self.axes[1, 1].set_xticklabels([0.1, 1, 10,  100])

        self.axes[1, 1].set_ylim(-1.2, 2)
        self.axes[1, 1].set_yticks([-1, 0, 1, 2])
        self.axes[1, 1].set_yticklabels([0.1, 1, 10,  100])

        self.axes[1, 1].spines['right'].set_color('none')
        self.axes[1, 1].spines['top'].set_color('none')




        self.OutPutData = pd.DataFrame()
        self.LabelList=[]
        self.IndexList=[]
        self.TypeList0=[]
        self.TypeList1=[]
        self.TypeList2=[]
        self.TypeList3=[]




        BaseLinesA = self.condation[0]['BaseLines']

        for i in BaseLinesA:
            #self.DrawLogLine(l=i)
            self.axes[0, 0].plot(self.customDrawLogLine(l=i)[0],self.customDrawLogLine(l=i)[1], color='black', linewidth=0.8, alpha=0.5)



        self.TagsA = []

        for i in range(len(self.condation[0]['Labels'])):
            self.TagsA.append(Tag(Label=self.condation[0]['Labels'][i], Location=self.condation[0]['Locations'][i]))


        BaseLinesB = self.condation[1]['BaseLines']

        for i in BaseLinesB:
            #self.DrawLogLine(l=i)
            self.axes[0, 1].plot(self.customDrawLogLine(l=i)[0],self.customDrawLogLine(l=i)[1], color='black', linewidth=0.8, alpha=0.5)



        self.TagsB = []

        for i in range(len(self.condation[1]['Labels'])):
            self.TagsB.append(Tag(Label=self.condation[1]['Labels'][i], Location=self.condation[1]['Locations'][i]))


        BaseLinesC = self.condation[2]['BaseLines']

        for i in BaseLinesC:
            #self.DrawLogLine(l=i)

            if (i==   [(25, 25), (1000, 400)]):
                self.axes[1, 0].plot(self.customDrawLogLine(l=i)[0], self.customDrawLogLine(l=i)[1],linestyle=':', color='grey',
                                     linewidth=0.8, alpha=0.3)

            else:
                self.axes[1, 0].plot(self.customDrawLogLine(l=i)[0],self.customDrawLogLine(l=i)[1], color='black', linewidth=0.8, alpha=0.5)



        self.TagsC = []

        for i in range(len(self.condation[2]['Labels'])):
            self.TagsC.append(Tag(Label=self.condation[2]['Labels'][i], Location=self.condation[2]['Locations'][i]))


        BaseLinesD = self.condation[3]['BaseLines']

        for i in BaseLinesD:
            #self.DrawLogLine(l=i)
            if (i==  [(3, 2), (100, 20)]):
                self.axes[1, 1].plot(self.customDrawLogLine(l=i)[0], self.customDrawLogLine(l=i)[1],linestyle=':', color='grey',
                                     linewidth=0.8, alpha=0.3)

            else:
                self.axes[1, 1].plot(self.customDrawLogLine(l=i)[0],self.customDrawLogLine(l=i)[1], color='black', linewidth=0.8, alpha=0.5)


        PointLabels = []

        self.TagsD = []

        for i in range(len(self.condation[3]['Labels'])):
            self.TagsD.append(Tag(Label=self.condation[3]['Labels'][i], Location=self.condation[3]['Locations'][i]))


        for i in range(len(raw)):
            # raw.at[i, 'DataType'] == 'User' or raw.at[i, 'DataType'] == 'user' or raw.at[i, 'DataType'] == 'USER'

            TmpLabel = ''

            #   self.WholeData.append(math.log(tmp, 10))

            self.LabelList.append(raw.at[i, 'Label'])

            if 'Index' in raw.columns.values:
                self.IndexList.append(raw.at[i, 'Index'])
            else:
                self.IndexList.append('No ' + str(i+1))



            if (raw.at[i, 'Label'] in PointLabels or raw.at[i, 'Label'] == ''):
                TmpLabel = ''
            else:
                PointLabels.append(raw.at[i, 'Label'])
                TmpLabel = raw.at[i, 'Label']



            xa, ya = 0, 0
            xb, yb = 0, 0
            xc, yc = 0, 0
            xd, yd = 0, 0

            Label = TmpLabel

            xa, ya = (raw.at[i, 'Y'] + raw.at[i, 'Nb']), raw.at[i, 'Rb']
            xb, yb = (raw.at[i, 'Yb'] + raw.at[i, 'Ta']), raw.at[i, 'Rb']
            xc, yc = raw.at[i, 'Y'], raw.at[i, 'Nb']
            xd, yd = raw.at[i, 'Yb'], raw.at[i, 'Ta']


            HitOnRegions=0
            for j in self.ItemNames0:
                if self.SelectDic0[j].contains_point([xa, ya]):
                    self.TypeList0.append(j)
                    HitOnRegions=1
                    break
            if HitOnRegions==0:
                self.TypeList0.append('on line or out')

            HitOnRegions = 0
            for j in self.ItemNames1:
                if self.SelectDic1[j].contains_point([xb, yb]):
                    self.TypeList1.append(j)
                    HitOnRegions=1
                    break
            if HitOnRegions==0:
                self.TypeList1.append('on line or out')

            HitOnRegions = 0
            for j in self.ItemNames2:
                if self.SelectDic2[j].contains_point([xc, yc]):
                    self.TypeList2.append(j)
                    HitOnRegions=1
                    break
            if HitOnRegions==0:
                self.TypeList2.append('on line or out')

            HitOnRegions = 0
            for j in self.ItemNames3:
                if self.SelectDic3[j].contains_point([xd, yd]):
                    self.TypeList3.append(j)
                    HitOnRegions=1
                    break
            if HitOnRegions==0:
                self.TypeList3.append('on line or out')




            try:
                self.axes[0, 0].scatter(math.log(xa, 10), math.log(ya, 10), marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

                if (self.show_data_index_cb.isChecked()):
                    if 'Index' in self._df.columns.values:
                        self.axes[0, 0].annotate(self._df.at[i, 'Index'],
                                                 xy=(math.log(xa, 10), math.log(ya, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes[0, 0].annotate('No' + str(i + 1),
                                                 xy=(math.log(xa, 10), math.log(ya, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
            except:
                pass

            try:
                self.axes[0, 1].scatter(math.log(xb, 10), math.log(yb, 10), marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

                if (self.show_data_index_cb.isChecked()):
                    if 'Index' in self._df.columns.values:
                        self.axes[0, 1].annotate(self._df.at[i, 'Index'],
                                                 xy=(math.log(xb, 10), math.log(yb, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes[0, 1].annotate('No' + str(i + 1),
                                                 xy=(math.log(xb, 10), math.log(yb, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
            except:
                pass

            try:
                self.axes[1, 0].scatter(math.log(xc, 10), math.log(yc, 10), marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

                if (self.show_data_index_cb.isChecked()):
                    if 'Index' in self._df.columns.values:
                        self.axes[1, 0].annotate(self._df.at[i, 'Index'],
                                                 xy=(math.log(xc, 10), math.log(yc, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes[1, 0].annotate('No' + str(i + 1),
                                                 xy=(math.log(xc, 10), math.log(yc, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
            except:
                pass

            try:
                self.axes[1, 1].scatter(math.log(xd, 10), math.log(yd, 10), marker=raw.at[i, 'Marker'],
                                    s=raw.at[i, 'Size'], color=raw.at[i, 'Color'], alpha=raw.at[i, 'Alpha'],
                                    label=TmpLabel)

                if (self.show_data_index_cb.isChecked()):
                    if 'Index' in self._df.columns.values:
                        self.axes[1, 1].annotate(self._df.at[i, 'Index'],
                                                 xy=(math.log(xd, 10), math.log(yd, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
                    else:
                        self.axes[1, 1].annotate('No' + str(i + 1),
                                                 xy=(math.log(xd, 10), math.log(yd, 10)),
                                                 color=self._df.at[i, 'Color'],
                                                 alpha=self._df.at[i, 'Alpha'])
            except:
                pass





        Tale = 0
        Head = 0

        if (len(self.WholeData) > 0):
            Tale = min(self.WholeData)
            Head = max(self.WholeData)

        Location = round(Tale - (Head - Tale) / 5)

        count = round((Head - Tale) / 5 * 7)


        if (self.legend_cb.isChecked()):
            self.axes[0, 1].legend(bbox_to_anchor=(1.05, 1),loc=2, borderaxespad=0, prop=fontprop)



        if (self.detail_cb.isChecked()):
            for i in self.TagsA:
                self.axes[0,0].annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

            for i in self.TagsB:
                self.axes[0,1].annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

            for i in self.TagsC:
                self.axes[1,0].annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)

            for i in self.TagsD:
                self.axes[1,1].annotate(i.Label, xy=i.Location, xycoords='data', xytext=(i.X_offset, i.Y_offset),
                                   textcoords='offset points',
                                   fontsize=8, color='grey', alpha=0.8)




        self.canvas.draw()

        self.OutPutTitle='Pearce'

        self.OutPutFig=self.fig

        print(len(self.LabelList), len(self.IndexList), len(self.TypeList0), len(self.TypeList1), len(self.TypeList2),
              len(self.TypeList3))

        self.OutPutData = pd.DataFrame({'Label': self.LabelList,
             'Index':self.IndexList,
             'TectonicTypeA': self.TypeList0,
             'TectonicTypeB': self.TypeList1,
             'TectonicTypeC': self.TypeList2,
             'TectonicTypeD': self.TypeList3,
             })



    def Explain(self):

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.tablepop = TableViewer(df=self.OutPutData,title='Pearce Result')
        self.tablepop.show()