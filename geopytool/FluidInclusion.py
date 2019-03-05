from geopytool.ImportDependence import *
from geopytool.CustomClass import *
#from geopytool.TableViewer import TableViewer


class FluidInclusion(AppForm):
    _df = pd.DataFrame()
    _changed = False

    xlabel = r'Homogenization Temperature'
    ylabel = r'Frequency'

    reference = 'Wang Zhenyi Research on Fluid Inclusions of the Gejiu Tin-Copper Polymetallic Deposit 王振义. 个旧锡铜多金属矿床流体包裹体特征研究[D].'


    whole_labels = []
    all_labels = []
    all_colors = []
    all_markers = []
    all_alpha = []
    all_data_list = []


    def __init__(self, parent=None, df=pd.DataFrame(),filename= '/'):
        QWidget.__init__(self, parent)

        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')
        self.FileName_Hint = ''
        self._df = df
        self.filename= filename

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')

        self.create_main_frame()
        self.create_status_bar()



    def create_main_frame(self):
        self.resize(1000, 800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((18.0, 12.0), dpi=self.dpi)
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.2, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('off')
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls


        self.save_button = QPushButton('&Save Img')
        self.save_button.clicked.connect(self.saveImgFile)

        self.stat_button = QPushButton('&Calculation')
        self.stat_button.clicked.connect(self.Explain)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.FluidInclusion)  # int


        self.density_cb = QCheckBox('&Density')
        self.density_cb.setChecked(True)
        self.density_cb.stateChanged.connect(self.FluidInclusion)  # int

        self.stack_cb = QCheckBox('&Stack')
        self.stack_cb.setChecked(True)
        self.stack_cb.stateChanged.connect(self.FluidInclusion)  # int


        self.combine_cb = QCheckBox('&Combine')
        self.combine_cb.setChecked(False)
        self.combine_cb.stateChanged.connect(self.FluidInclusion)  # int


        self.overlap_cb = QCheckBox('&Overlap')
        self.overlap_cb.setChecked(False)
        self.overlap_cb.stateChanged.connect(self.FluidInclusion)  # int


        self.hbox = QHBoxLayout()

        for w in [self.save_button,self.stat_button, self.legend_cb,self.density_cb,self.stack_cb,self.overlap_cb,self.combine_cb]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)

        self.vbox.addWidget(self.textbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)


    def FluidInclusion(self):
        self.setWindowTitle('Fluid Inclusion ')
        self.axes.clear()
        #self.axes.axis('off')
        self.axes.set_xlabel(self.xlabel)
        self.axes.set_ylabel(self.ylabel)
        ##self.axes.spines['top'].set_color('none')

        title = 'Fluid Inclusion '
        self.setWindowTitle(title)
        self.textbox.setText(self.reference)


        self.all_labels=[]
        self.all_colors=[]
        self.all_markers=[]
        self.all_alpha=[]
        self.all_data_list=[]


        if (self.combine_cb.isChecked()):

            self.all_data_list = self._df.Th


            if (self.density_cb.isChecked()):
                self.axes.hist(self.all_data_list,density=True, facecolor= 'grey', alpha= 0.6,
                           label=self.getFileName([self.filename]), edgecolor='k')
            else:
                self.axes.hist(self.all_data_list, density=False, facecolor= 'grey', alpha= 0.6,
                           label=self.getFileName([self.filename]), edgecolor='k')


        else:

            for i in range(len(self._df)):
                target = self._df.at[i, 'Label']
                color = self._df.at[i, 'Color']
                marker = self._df.at[i, 'Marker']
                alpha = self._df.at[i, 'Alpha']

                if target not in self.all_labels:
                    self.all_labels.append(target)
                    self.all_colors.append(color)
                    self.all_markers.append(marker)
                    self.all_alpha.append(alpha)

            self.whole_labels = self.all_labels

            for j in self.all_labels:
                tmp_data_list = []
                for i in range(len(self._df)):
                    target = self._df.at[i, 'Label']
                    if target == j:
                        tmp_data_list.append(self._df.at[i, 'Th'])

                self.all_data_list.append(tmp_data_list)

            if (self.stack_cb.isChecked()):
                pass

                if (self.density_cb.isChecked()):

                    self.axes.set_ylabel(self.ylabel+' Density')

                    N, bins, patches = self.axes.hist(self.all_data_list, density=True, stacked=True,edgecolor='k',alpha= 0.6)
                else:
                    N, bins, patches = self.axes.hist(self.all_data_list, density=False, stacked=True,edgecolor='k',alpha= 0.6)


                    #patches[i].set_facecolor('red')
                width = (bins[1] - bins[0]) * 0.4

                tmp_label_check=[]
                for k in range(len(patches)):
                    for p in patches[k]:
                        p.set_facecolor(self.all_colors[k])
                        p.set_alpha(self.all_alpha[k])

                        if self.all_labels[k] not in tmp_label_check:
                            tmp_label_check.append(self.all_labels[k])
                            p.set_label(self.all_labels[k])


            else:

                if (self.overlap_cb.isChecked()):
                    for k in range(len(self.all_labels)):

                        if (self.density_cb.isChecked()):

                            self.axes.set_ylabel(self.ylabel+' Density')

                            self.axes.hist(self.all_data_list[k], density=True, facecolor= self.all_colors[k], alpha= self.all_alpha[k],label=self.all_labels[k],edgecolor ='k')
                        else:
                            self.axes.hist(self.all_data_list[k], density=False, facecolor= self.all_colors[k], alpha= self.all_alpha[k],label=self.all_labels[k],edgecolor ='k')

                else:
                    if (self.density_cb.isChecked()):

                        self.axes.set_ylabel(self.ylabel+' Density')

                        N, bins, patches = self.axes.hist(self.all_data_list, density=True, stacked=False,edgecolor='k',alpha= 0.6)
                    else:
                        N, bins, patches = self.axes.hist(self.all_data_list, density=False, stacked=False,edgecolor='k',alpha= 0.6)


                        #patches[i].set_facecolor('red')

                    tmp_label_check=[]
                    for k in range(len(patches)):
                        for p in patches[k]:
                            p.set_facecolor(self.all_colors[k])
                            p.set_alpha(self.all_alpha[k])

                            if self.all_labels[k] not in tmp_label_check:
                                tmp_label_check.append(self.all_labels[k])
                                p.set_label(self.all_labels[k])



        if (self.legend_cb.isChecked()):
            self.axes.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0, prop=fontprop)

        self.canvas.draw()


    def Explain(self):

        #self.OutPutData = self.OutPutData.set_index('Label')

        self.OutPutData = pd.DataFrame()

        low_salt_list=[]
        high_salt_list=[]
        salt_list = []
        Th_list=[]
        Tm_list=[]



        salt_used_in_calc = []

        if 'Salinity(Wt%)'in self._df.columns.values.tolist():
            salt_used_in_calc= self._df['Salinity(Wt%)']
            self.OutPutData=self._df

            for i in range(len(self._df)):
                tmp = self._df.at[i, 'Tm']
                if abs(tmp) > 0:
                    Tm_list.append(tmp)
                    print(tmp)
                else:
                    Tm_list.append(np.NaN)
                tmp_th = self._df.at[i, 'Th']
                if abs(tmp_th) > 0:
                    Th_list.append(tmp_th)
                else:
                    Th_list.append(np.NaN)


        elif 'Salinity'in self._df.columns.values.tolist():
            salt_used_in_calc= self._df['Salinity']
            self.OutPutData=self._df
            for i in range(len(self._df)):
                tmp = self._df.at[i, 'Tm']
                if abs(tmp) > 0:
                    Tm_list.append(tmp)
                    print(tmp)
                else:
                    Tm_list.append(np.NaN)
                tmp_th = self._df.at[i, 'Th']
                if abs(tmp_th) > 0:
                    Th_list.append(tmp_th)
                else:
                    Th_list.append(np.NaN)
        else:
            for i in range(len(self._df)):
                tmp = self._df.at[i, 'Tm']
                if abs(tmp) > 0:
                    Tm_list.append(tmp)
                    print(tmp)
                    low_s = self.LowSalt(tmp)
                    high_s = self.HighSalt(tmp)
                    s = 0
                    if low_s <= 26.3:
                        s = low_s
                    else:
                        s = high_s

                    low_salt_list.append(round(low_s + 0.001, 2))
                    high_salt_list.append(round(high_s + 0.001, 2))
                    salt_list.append(round(s + 0.001, 2))
                else:
                    Tm_list.append(np.NaN)
                    low_salt_list.append(np.NaN)
                    high_salt_list.append(np.NaN)
                    salt_list.append(np.NaN)
                tmp_th = self._df.at[i, 'Th']
                if abs(tmp_th) > 0:
                    Th_list.append(tmp_th)
                else:
                    Th_list.append(np.NaN)

            SaltDict = {'Salinity(Wt%)': salt_list, 'LowSalinity(Wt%)': low_salt_list,
                        'HighSalinity(Wt%)': high_salt_list}
            SaltData = pd.DataFrame(SaltDict)

            self.OutPutData = pd.concat([self._df, SaltData], axis=1)
            salt_used_in_calc = salt_list

        density_list=[]
        p_ore_list=[]
        p_salt_list=[]
        depth_fluid_list=[]
        depth_host_list=[]
        for i in range(min(len(salt_used_in_calc),len(Th_list),len(Tm_list))):
            d_tmp=np.NaN
            po_tmp=np.NaN
            ps_tmp=np.NaN
            depth_fluid_tmp =np.NaN
            depth_host_rmp =np.NaN
            if abs(salt_used_in_calc[i]) >= 0 and abs(Th_list[i]) >= 0 and abs(Tm_list[i]) >= 0:
                d_tmp = self.DensitySalt(salt_used_in_calc[i],Th_list[i])
                po_tmp= self.PressureOre(salt_used_in_calc[i],Th_list[i])
                ps_tmp= self.PressureSalt(salt_used_in_calc[i],Th_list[i])

                depth_fluid_tmp =self.DepthFluid(po_tmp/10.0)
                depth_host_rmp =self.DepthHostRock(po_tmp/10.0)

            density_list.append(d_tmp)
            p_ore_list.append(po_tmp/10.0)
            p_salt_list.append(ps_tmp*np.power(10,2))

            depth_fluid_list.append(depth_fluid_tmp)
            depth_host_list.append(depth_host_rmp)


        CalcDict={'Liquid Density g/cm^3)':density_list,'Ore-forming Pressure(M Pa)':p_ore_list, 'Liquid Pressure(K Pa)':p_salt_list,'Depth by Fluid Pressure(km)':depth_fluid_list,'Depth of Host(km)':depth_host_list }
        CalcData = pd.DataFrame(CalcDict)

        self.OutPutData = pd.concat([self.OutPutData,CalcData], axis=1).set_index('Label')
        self.tablepop = TableViewer(df=self.OutPutData,title='Fluid Inclusion Calculation Result')
        self.tablepop.show()


    def LowSalt(self,Tm=0):
        # 低盐度流体(W(NaCl)< 23.3%,未见子矿物)的盐度计算公式, (Hall,1988)
        result= 0.00+1.78*abs(Tm)-0.0442*abs(Tm)*abs(Tm)+ 0.000557*abs(Tm)*abs(Tm)*abs(Tm)
        return(result)

    def HighSalt(self,Tm=0):
        # 高盐度流体(W(NaCl)> 26.3%,含有子矿物)的盐度计算公式, (Hall,1988;Sterner,1988)
        t = abs(Tm/1000.0)
        result = 26.242+ 0.4928*t+1.42*t*t-0.223*t*t*t +0.4129*t*t*t*t+0.006395*t*t*t*t*t-0.001967*t*t*t*t*t*t +0.0001112*t*t*t*t*t*t*t
        return (result)

    def CO2TripleSalt(self,Tmcla=0):
        # CO2三相流体包裹体的盐度计算公式 (Roedder,1984)
        result=0
        if -9/6<= Tmcla <=10.0:
            result = 15.52022-1.02342*Tmcla -0.05286*Tmcla*Tmcla
        return (result)

    def DensitySalt(self,W_NaCl,Th):
        # 不同浓度NaCl-H2O溶液密度公式(刘斌,1999,2001)
        w=W_NaCl
        t=Th
        A0 = 0.993531
        A1 = 8.72147 * (10**(-3))
        A2 = -2.43975 * (10**( -5))

        B0 = 7.11652 * (10**( -5))
        B1 = -5.2208 * (10**( -5))
        B2 = 1.26656 * (10**( -6))

        C0 = -3.4997 * (10**( -6))
        C1 = 2.12124 * (10**( -7))
        C2 = -4.52318 * (10**( -9))

        if 1<=w<30:
            # 1%~<30%时
            A0 = 0.993531
            A1 = 8.72147 * (10**( -3))
            A2 = -2.43975 * (10**( -5))

            B0 = 7.11652 * (10**( -5))
            B1 = -5.2208 * (10**( -5))
            B2 = 1.26656 * (10**( -6))

            C0 = -3.4997 * (10**( -6))
            C1 = 2.12124 * (10**( -7))
            C2 = -4.52318 * (10**( -9))

        elif 30<=w<60:

            # 30%~<60%时
            A0 = 1.376294
            A1 = 0.0106328
            A2 = -2.449428 * (10**( -4))

            B0 = -2.752237 * (10**( -3))
            B1 = 1.324187 * (10**( -5))
            B2 = 6.503339 * (10**( -7))

            C0 = 1.703392 * (10**( -6))
            C1 = -1.49158 * (10**( -8))
            C2 = -4.020795 * (10**( -10))

        elif 60<= w:
            # >60%时
            A0 = 21.31876
            A1 = -0.5715091
            A2 = 4.146964 * (10**( -3))

            B0 = -4.971499 * (10**( -2))
            B1 = 1.395219 * (10**( -3))
            B2 = -9.919401 * (10**( -6))

            C0 = 2.926059 * (10**( -5))
            C1 = -8.316942 * (10**( -7))
            C2 = 5.922209 * (10**( -9))


        A = A0 + A1 * w + A2 * w * w
        B = B0 + B1 * w + B2 * w * w
        C = C0 + C1 * w + C2 * w * w

        result = A + B * t + C * t * t
        return (result)

    def PressureOre(self,W_NaCl,Th):
        # 成矿压力经验公式, 邵洁涟, 1986
        result = 0
        w=W_NaCl
        Th=Th
        result = (219 + 2620 * w) * Th / (374 + 920 * w)
        # result 即压力, 单位是10^5 Pa
        return (result)

    def PressureSalt(self,W_NaCl,Th):
        # NaCl-H2O 溶液包裹体均一压力公式(Bain, 1964; Haas, 1976) 单位是bar, 即 10^5 Pa
        result = 0
        w=W_NaCl
        T=Th

        # 这里要先将NaCl的质量分数转换成摩尔浓度
        m=100*w/[58.4428 * (100-w)]

        e0 = 12.50849
        e1 = -4616.913
        e2 = 3.193455 * (10**( -4))
        e3 = 1.1965 * (10**( -11))
        e4 = -1.013137 * (10**( -2))
        e5 = -5.7148 * (10**( -3))
        em = np.log(10)
        A = 1 + 5.93582 * (10**( -6)) * m - 5.19386 * (10**( -5) )* m * m + 1.23156 * (10**( -5)) * m * m * m

        B = m * (1.1542 * (10**( -6)) + 1.4125 * (10**( -7) )* m - 1.92476 * (10**(-8)) * m * m - 1.70717 * (
            10**(-9)) * m * m * m + 1.0539 * (10**( -10)) * m * m * m * m)


        TH2O= np.power(np.e,np.log(T/(A+B*T)))

        z=TH2O+0.01

        Y= np.power(647.27-TH2O,1.25)

        delta = z*z -2.937* (10**(5))

        LnPg= e0+e1/z +e2*delta* (np.power(np.e, e3*em*delta*delta)- 1)/z+e4* np.power(10, e5*Y)

        result= np.power(np.e,LnPg)

        return (result)

    def PressureHighSalt(self,T):
        # NaCl-H2O 溶液包裹体有子晶的压力公式(Bischoff,1991) 温度范围在100-801℃
        # T 是NaCl子晶体最后消失的温度, 返回的P是压力, 单位是10^5 Pa
        t=T
        result=0
        result = 41.749 - 1.2125 * t + 0.0136213 * t * t - 7.52333 * (10**( -5)) * t * t * t + 2.19664 * (10**( -7)) * t * t * t * t - 2.82583 *(10**(-10)) * t * t * t * t * t + 1.27231 * (10**( -13)) * t * t * t * t * t * t

        return(result)


    def DepthFluid(self,Pressure_Ore_Forming=20):

        #断裂带流体压力与成矿深度之间的关系式（孙丰月，2000）
        #H 代表成矿深度（km），P 代表成矿压力（MPa）即 10^6 Pa。

        p=Pressure_Ore_Forming
        H=0

        if p <40:
            H=p/10.0
        elif 40<=p<220:
            H=(0.0868/(1/p+0.00388) +2)
        elif 220<=p<=370:
            H= 11+ (np.e**(p-221.95) )/79.075
        else: #p>370Mpa
            H=0.0331385*p+4.19898

        result = H

        return (result)

    def DepthHostRock(self,Pressure_Ore_Forming=20,rough=2.7,g=9.8):

        #静岩压力与深度的关系式 （孙丰月，2000）
        #P 为成矿压力（Mpa）即 10^6 Pa，rough 𝜌为上覆岩石的密度，取 2.7g/cm3,g 为重力加速度，取 9.8m/s2
        result = 0
        p=Pressure_Ore_Forming
        rough=rough
        g=g
        H=p/(rough*g)
        result=H
        return (result)
