from ImportDependence import *
from CustomClass import *


class MyThreeD_Vispy(AppForm):
    Lines = []
    Tags = []
    description = 'ThreeD'
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



    def __init__(self, parent=None, df=pd.DataFrame(),DataLocation='DataLocation'):
        QMainWindow.__init__(self, parent)

        self.DataLocation = DataLocation
        self.setWindowTitle('ThreeD Data Visualization Vispy')
        self._df = df




        self.items = []
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to ThreeD')

        self.raw = df
        self.rawitems = self.raw.columns.values.tolist()

        for i in self.rawitems:
            if i not in self.unuseful:
                self.items.append(i)
            else:
                pass

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.setWindowTitle('ThreeD Data Visualization Vispy')

        #self.fig = plt.figure(figsize=(12, 12))
        #self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)

        #self.axes = Axes3D(self.fig, elev=-150, azim=110)

        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)

        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls

        #self.canvas = vispy.app.Canvas()
        #self.fig = vispy.plot.Fig()

        self.Plot3D = vispy.scene.visuals.create_visual_node(vispy.visuals.LinePlotVisual)
        #self.Plot3D = vispy.scene.visuals.create_visual_node(vispy.visuals.SurfacePlotVisual)

        self.canvas = vispy.scene.SceneCanvas(keys='interactive', title='plot3d', show=True)

        # Add a ViewBox to let the user zoom/rotate
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = 'turntable'
        self.view.camera.fov = 45
        self.view.camera.distance = 6

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.ThreeD)  # int

        self.log_cb = QCheckBox('&Log')
        self.log_cb.setChecked(True)
        self.log_cb.stateChanged.connect(self.ThreeD)  # int

        self.save_img_button = QPushButton('&Save Image')
        self.save_img_button.clicked.connect(self.saveImgFile)

        self.vbox = QVBoxLayout()
        self.hbox =QHBoxLayout()

        #self.vbox.addWidget(self.mpl_toolbar)
        #self.vbox.addWidget(self.canvas.native)
        self.vbox.addWidget(self.canvas.native)
        #self.hbox.addWidget(self.log_cb)
        #self.hbox.addWidget(self.legend_cb)
        #self.hbox.addWidget(self.save_img_button)
        #self.vbox.addLayout(self.hbox)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)



    def ThreeD(self):

        #self.axes.clear()
        #self.create_main_frame()

        self.WholeData = []
        ItemsAvalibale = self._df.columns.values.tolist()


        if 'Label' in ItemsAvalibale:
            self._df = self._df.set_index('Label')

        dataframe = self._df

        dataframe =  dataframe.dropna(axis=1,how='all')



        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                dataframe = dataframe.drop(i, 1)

        dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
        dataframe = dataframe.dropna(axis='columns')


        self.result=dataframe

        self.originalresult=self.result


        self.result = pd.DataFrame(self.result.values.flatten())
        #print(self.originalresult.shape)

        a,b =self.originalresult.shape

        m=list(i for i in range(a))
        n=list(i for i in range(b))

        location_list= list(product(m,n))

        x=[]
        y=[]
        colors=[]

        for i in location_list:
            x.append(i[0])
            y.append(i[1])


        #print(np.log10(self.result.values))

        if (self.log_cb.isChecked()):
            zs = np.log10(self.result.values)
        else:
            zs = self.result.values

        pos=[]
        for i in range(len(location_list)):
            pos.append([location_list[i][1],location_list[i][0],zs[i]])

        self.Plot3D(pos, width= 0, color='red', edge_color='w', symbol='o', face_color=(0.2, 0.2, 1, 0.8),parent=self.view.scene)

        #self.Plot3D(pos,  color='red', edge_color='w', symbol='o', face_color=(0.2, 0.2, 1, 0.8),parent=self.view.scene)

        #self.Plot3D.set_data([x, y, zs, colors'red'])

        #self.fig[0, 0].plot(data=pos)


        #self.axes.scatter(xs =x  ,ys=y, zs= self.result, color= 'red', marker= 'o', label= self.DataLocation, alpha=0.6)
        #self.axes.scatter(xs =x  ,ys=y, zs= zs, color= 'red', marker= 'o', label= self.DataLocation, alpha=0.2)
        #if (self.legend_cb.isChecked()):
            #self.axes.legend(loc=2,prop=fontprop)
        #self.canvas.draw()

        self.show()

        #print(location_list)


    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            #self.canvas.print_figure(ImgFileOutput, dpi=300)
            img = self.canvas.render()

            # Use write_png to export your wonderful plot as png !
            vispy.io.write_png(ImgFileOutput, img)